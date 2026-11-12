# -*- coding: utf-8 -*-
"""WebSocket 接入：双向流式事件通道。"""
from __future__ import annotations

from .adapter import IngressAdapter


class WebSocketIngress(IngressAdapter):
    """WebSocket 接入适配器（骨架）。"""

    def serve(self, *args, **kwargs):
        return {"status": "ok", "ingress": "websocket"}
