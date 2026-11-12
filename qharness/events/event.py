# -*- coding: utf-8 -*-
"""Event：统一事件模型的核心数据结构。

设计要点：
- 事件是不可变的值对象，只有 `event_id/type/session_id/payload/...` 字段；
- `causation` 记录"因哪个事件而产生"，串起因果链，用于分布式追踪（tracing）；
- `source` 标记产生该事件的组件（brain/hand/ingress/...），用于观测与路由审计。
"""
from __future__ import annotations

import hashlib
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional

from .types import EventType


def new_event_id() -> str:
    """确定性优先、碰撞极低的全局唯一事件 ID。"""
    return uuid.uuid4().hex[:16]


@dataclass(frozen=True)
class Event:
    """统一事件。"""

    type: str
    session_id: str
    payload: dict = field(default_factory=dict)
    event_id: str = field(default_factory=new_event_id)
    timestamp: float = field(default_factory=time.time)
    causation: Optional[str] = None      # 父事件 ID（因果链）
    source: str = "system"               # 产生该事件的组件名

    def with_payload(self, **kw) -> "Event":
        p = dict(self.payload)
        p.update(kw)
        return Event(
            type=self.type, session_id=self.session_id, payload=p,
            event_id=self.event_id, timestamp=self.timestamp,
            causation=self.causation, source=self.source,
        )

    def child(self, type_: str, payload: Optional[dict] = None, source: Optional[str] = None) -> "Event":
        """以当前事件为因（causation），生成一个子事件。"""
        return Event(
            type=type_, session_id=self.session_id,
            payload=payload or {}, causation=self.event_id,
            source=source or self.source,
        )

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "type": self.type,
            "session_id": self.session_id,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "causation": self.causation,
            "source": self.source,
        }

    @staticmethod
    def from_dict(d: dict) -> "Event":
        return Event(
            event_id=d.get("event_id", new_event_id()),
            type=d["type"],
            session_id=d.get("session_id", ""),
            payload=d.get("payload", {}) or {},
            timestamp=d.get("timestamp", time.time()),
            causation=d.get("causation"),
            source=d.get("source", "system"),
        )

    def fingerprint(self) -> str:
        """事件的确定性指纹（用于去重/幂等）。"""
        h = hashlib.sha256()
        h.update(self.type.encode("utf-8"))
        h.update(self.session_id.encode("utf-8"))
        h.update(repr(sorted(self.payload.items())).encode("utf-8"))
        return h.hexdigest()


class EventFactory:
    """便捷构造器：统一入口产生各类型事件，保证字段一致。"""

    def __init__(self, source: str = "system"):
        self.source = source

    def session_created(self, session_id: str, **kw) -> Event:
        return Event(EventType.SESSION_CREATED, session_id, kw, source=self.source)

    def user_message(self, session_id: str, content: str, **kw) -> Event:
        return Event(EventType.USER_MESSAGE, session_id, {"content": content, **kw}, source=self.source)

    def assistant_message(self, session_id: str, content: str, **kw) -> Event:
        return Event(EventType.ASSISTANT_MESSAGE, session_id, {"content": content, **kw}, source=self.source)

    def tool_call(self, session_id: str, tool: str, arguments: dict, call_id: str, **kw) -> Event:
        return Event(EventType.TOOL_CALL, session_id,
                     {"tool": tool, "arguments": arguments, "call_id": call_id, **kw},
                     source=self.source)

    def tool_result(self, session_id: str, call_id: str, result: Any, **kw) -> Event:
        return Event(EventType.TOOL_RESULT, session_id,
                     {"call_id": call_id, "result": result, **kw}, source=self.source)

    def tool_error(self, session_id: str, call_id: str, error: str, **kw) -> Event:
        return Event(EventType.TOOL_ERROR, session_id,
                     {"call_id": call_id, "error": error, **kw}, source=self.source)


