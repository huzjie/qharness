# -*- coding: utf-8 -*-
"""接入层抽象：把外部请求转成 user_message 事件。"""
from __future__ import annotations

from abc import ABC, abstractmethod

from ..bus.base import Bus
from ..events.event import Event
from ..events.types import EventType


class IngressAdapter(ABC):
    """接入适配器：统一入口，业务只关心「把用户输入变事件」。"""

    def __init__(self, bus: Bus, source: str = "ingress"):
        self.bus = bus
        self.source = source

    def emit_user_message(self, session_id: str, content: str) -> Event:
        ev = Event(type=EventType.USER_MESSAGE, session_id=session_id,
                   payload={"content": content}, source=self.source)
        self.bus.publish(ev)
        return ev

    @abstractmethod
    def serve(self, *args, **kwargs):
        ...
