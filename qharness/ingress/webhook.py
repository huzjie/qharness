# -*- coding: utf-8 -*-
"""Webhook 接入：接收外部回调（如 Git 平台事件）转成事件。"""
from __future__ import annotations

import json

from .adapter import IngressAdapter
from ..events.event import Event
from ..events.types import EventType


class WebhookIngress(IngressAdapter):
    """Webhook 接入：把外部回调 payload 转成 system 事件。"""

    def handle(self, payload: dict, session_id: str = "") -> Event:
        ev = Event(type=EventType.SYSTEM, session_id=session_id,
                   payload={"source": "webhook", "data": payload}, source=self.source)
        self.bus.publish(ev)
        return ev

    def serve(self, raw: str, session_id: str = ""):
        try:
            payload = json.loads(raw)
        except Exception:
            payload = {"raw": raw}
        return self.handle(payload, session_id)
