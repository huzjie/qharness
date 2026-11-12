# -*- coding: utf-8 -*-
"""qharness —— 可嵌入的编码智能体运行时。

核心主张：一切交互都是事件，一切组件都通过事件总线通信，脑（推理）与手（执行）分离。
"""
from __future__ import annotations

__version__ = "0.1.0"
__all__ = ["__version__"]

from .events import Event, EventType, EventFactory, new_event_id, encode_event, decode_event  # noqa: E402,F401
