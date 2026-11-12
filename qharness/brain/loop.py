# -*- coding: utf-8 -*-
"""Agent 循环：脑的核心。模型 -> 工具调用 -> 结果 -> 模型 ... 直到完成。

手脑分离的关键：脑通过「发 tool_call 事件 + 收 tool_result 事件」与手协作，
同步模式下直接调用 executor 的同步执行方法；事件模式下走总线。
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from ..bus.base import Bus
from ..hand.executor import execute_tool
from ..providers.base import Provider
from ..providers.mock import MockProvider
from ..session.model import Message, Role, Session
from ..tools.base import ToolContext
from .planner import get_planner


class RunStatus(Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    MAX_TURNS = "max_turns"
    CANCELLED = "cancelled"


@dataclass
class RunResult:
    status: RunStatus
    answer: str = ""
    turns: int = 0
    tool_calls: int = 0
    messages: list = field(default_factory=list)
    error: str = ""
    latency_ms: float = 0.0


class AgentLoop:
    def __init__(self, provider: Optional[Provider] = None, bus: Optional[Bus] = None,
                 workdir: str = ".", strategy: str = "react", max_turns: int = 40,
                 tool_ctx: Optional[ToolContext] = None):
        self.provider = provider or MockProvider()
        self.bus = bus
        self.workdir = workdir
        self.strategy = strategy
        self.max_turns = max_turns
        self.planner = get_planner(strategy)
        self.tool_ctx = tool_ctx or ToolContext(workdir=workdir)

    def run(self, session: Session, user_input: str, **kw) -> RunResult:
        start = time.perf_counter()
        plan = self.planner.plan(user_input, [])
        messages = session.messages

        # 注入系统提示词（若尚无）
        if not messages or messages[0].role != Role.SYSTEM:
            messages.insert(0, Message(role=Role.SYSTEM, content=self.planner.system_prompt()))

        messages.append(Message(role=Role.USER, content=user_input))
        session.turn_count += 1

        tool_calls_made = 0
        for _ in range(self.max_turns):
            openai_msgs = self._to_openai(messages)
            resp = self.provider.chat(openai_msgs, tools=kw.get("tools"), temperature=kw.get("temperature", 0.0))

            if resp.has_tool_calls:
                for tc in resp.tool_calls:
                    tool_calls_made += 1
                    # 发事件（供观测/分布式），并同步执行
                    if self.bus:
                        from ..events.types import EventType
                        from ..events.event import Event
                        self.bus.publish(Event(
                            type=EventType.TOOL_CALL, session_id=session.id,
                            payload={"tool": tc.name, "arguments": tc.arguments, "call_id": tc.id},
                            source="brain",
                        ))
                    result = execute_tool(tc.name, tc.arguments, self.tool_ctx)
                    messages.append(Message(
                        role=Role.ASSISTANT, content="",
                        tool_calls=[{"id": tc.id, "type": "function",
                                     "function": {"name": tc.name, "arguments": tc.arguments}}],
                    ))
                    messages.append(Message(
                        role=Role.TOOL, content=result.output if result.success else result.error,
                        tool_call_id=tc.id, name=tc.name,
                    ))
                    if self.bus:
                        from ..events.types import EventType
                        from ..events.event import Event
                        self.bus.publish(Event(
                            type=EventType.TOOL_RESULT if result.success else EventType.TOOL_ERROR,
                            session_id=session.id,
                            payload={"call_id": tc.id, "result": result.to_dict()},
                            source="hand",
                        ))
                continue

            # 最终回答
            answer = resp.content or "(空回答)"
            messages.append(Message(role=Role.ASSISTANT, content=answer))
            return RunResult(status=RunStatus.COMPLETED, answer=answer,
                             turns=session.turn_count, tool_calls=tool_calls_made,
                             messages=list(messages), latency_ms=(time.perf_counter() - start) * 1000)

        return RunResult(status=RunStatus.MAX_TURNS, answer="达到最大轮数仍未完成",
                         turns=session.turn_count, tool_calls=tool_calls_made,
                         messages=list(messages), latency_ms=(time.perf_counter() - start) * 1000)

    @staticmethod
    def _to_openai(messages: list) -> list:
        return [m.to_dict() for m in messages]

    def new_session(self) -> Session:
        return Session(id=uuid.uuid4().hex[:16])
