# -*- coding: utf-8 -*-
"""事件总线子系统：业务组件只依赖 Bus 接口，进程内/分布式可无缝切换。"""
from __future__ import annotations

from .base import Bus, Subscription
from .memory import MemoryBus
from .router import TopicRouter, match_topic
from .backpressure import Backpressure, DropPolicy
from .distributed import SocketBus, build_bus

__all__ = [
    "Bus", "Subscription", "MemoryBus", "TopicRouter", "match_topic",
    "Backpressure", "DropPolicy", "SocketBus", "build_bus",
]
