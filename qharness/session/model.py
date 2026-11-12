# -*- coding: utf-8 -*-
"""会话模型：Message / Session。"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional


class Role:
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    SYSTEM = "system"


@dataclass
class Message:
    role: str
    content: str
    tool_calls: Optional[list] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None
    meta: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = {"role": self.role, "content": self.content}
        if self.tool_calls:
            d["tool_calls"] = self.tool_calls
        if self.tool_call_id:
            d["tool_call_id"] = self.tool_call_id
        if self.name:
            d["name"] = self.name
        return d


@dataclass
class Session:
    id: str
    messages: list = field(default_factory=list)
    state: dict = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    turn_count: int = 0

    @staticmethod
    def new(session_id: Optional[str] = None) -> "Session":
        return Session(id=session_id or uuid.uuid4().hex[:16])

    def append(self, msg: Message) -> None:
        self.messages.append(msg)
        self.updated_at = time.time()

    def history(self, max_messages: Optional[int] = None) -> list:
        """返回消息历史（可选截断到最近 N 条）。"""
        if max_messages is None:
            return self.messages
        return self.messages[-max_messages:]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "messages": [m.to_dict() for m in self.messages],
            "state": self.state,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "turn_count": self.turn_count,
        }

    @staticmethod
    def from_dict(d: dict) -> "Session":
        s = Session(id=d["id"], created_at=d.get("created_at", time.time()),
                    updated_at=d.get("updated_at", time.time()),
                    turn_count=d.get("turn_count", 0))
        s.state = dict(d.get("state", {}))
        for m in d.get("messages", []):
            s.messages.append(Message(
                role=m["role"], content=m.get("content", ""),
                tool_calls=m.get("tool_calls"), tool_call_id=m.get("tool_call_id"),
                name=m.get("name"),
            ))
        return s
