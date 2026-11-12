# -*- coding: utf-8 -*-
"""ToolExecutor：订阅 tool_call 事件 -> 执行工具 -> 发布 tool_result/tool_error。

这是「手脑分离」的落地：脑只发 tool_call 事件，绝不直接调用工具；
手订阅事件、执行、回发结果。两者可部署在不同节点。
"""
from __future__ import annotations

import threading
from typing import Optional

from ..bus.base import Bus
from ..events.event import Event
from ..events.types import EventType
from ..tools.base import ToolContext, ToolResult
from ..tools.registry import ensure_loaded, get_tool
from .sandbox import ProcessSandbox


def execute_tool(name: str, arguments: dict, ctx: ToolContext) -> ToolResult:
    """同步执行单个工具（供 Agent 循环同步模式使用）。"""
    ensure_loaded()
    tool = get_tool(name)
    if tool is None:
        return ToolResult(False, error=f"未知工具：{name}")
    return tool.run(arguments or {}, ctx)


class ToolExecutor:
    """事件驱动的工具执行器。"""

    def __init__(self, bus: Bus, workdir: str = ".", allowlist: Optional[set] = None,
                 deny_commands: tuple = ("rm", "rmdir", "del", "format", "shutdown", "mkfs"),
                 timeout_ms: int = 30000):
        self.bus = bus
        self.workdir = workdir
        self.allowlist = allowlist
        self.deny_commands = deny_commands
        self.timeout_ms = timeout_ms
        self._sandbox = ProcessSandbox(timeout_ms, workdir)
        self._sub = None
        self.executed = 0

    def start(self):
        """订阅 tool_call 事件，开始监听。"""
        self._sub = self.bus.subscribe(EventType.TOOL_CALL, self._on_tool_call)
        return self

    def stop(self):
        if self._sub:
            self.bus.unsubscribe(self._sub)
            self._sub = None

    def _ctx(self, session_id: str) -> ToolContext:
        return ToolContext(workdir=self.workdir, session_id=session_id,
                           allowlist=self.allowlist, deny_commands=self.deny_commands,
                           timeout_ms=self.timeout_ms)

    def _on_tool_call(self, event: Event) -> None:
        p = event.payload
        call_id = p.get("call_id", event.event_id)
        tool = p.get("tool", "")
        args = p.get("arguments", {})
        result = self._sandbox.run(execute_tool, tool, args, self._ctx(event.session_id))
        self.executed += 1
        if result.success:
            out = self.bus.publish(Event(
                type=EventType.TOOL_RESULT, session_id=event.session_id,
                payload={"call_id": call_id, "result": result.to_dict(), "tool": tool},
                causation=event.event_id, source="hand",
            ))
        else:
            out = self.bus.publish(Event(
                type=EventType.TOOL_ERROR, session_id=event.session_id,
                payload={"call_id": call_id, "error": result.error, "tool": tool},
                causation=event.event_id, source="hand",
            ))
