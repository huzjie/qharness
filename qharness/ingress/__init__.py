# -*- coding: utf-8 -*-
"""接入层子系统：协议翻译 + 事件注入。"""
from __future__ import annotations

from .adapter import IngressAdapter
from .http import HttpIngress
from .ws import WebSocketIngress
from .webhook import WebhookIngress

__all__ = ["IngressAdapter", "HttpIngress", "WebSocketIngress", "WebhookIngress"]
