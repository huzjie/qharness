# -*- coding: utf-8 -*-
"""调度策略：决定事件/任务的处理顺序。"""
from __future__ import annotations

from abc import ABC, abstractmethod


class SchedulingPolicy(ABC):
    name = "policy"

    @abstractmethod
    def next_priority(self, session_id: str, meta: dict) -> int:
        """返回该任务应入队的优先级（越小越先）。"""


class FifoPolicy(SchedulingPolicy):
    name = "fifo"

    def next_priority(self, session_id: str, meta: dict) -> int:
        return 0


class PriorityPolicy(SchedulingPolicy):
    name = "priority"

    def next_priority(self, session_id: str, meta: dict) -> int:
        return int(meta.get("priority", 0))


class FairPolicy(SchedulingPolicy):
    """公平策略：按会话排队次数加权，避免饥饿。"""

    name = "fair"

    def __init__(self):
        self._counts: dict = {}

    def next_priority(self, session_id: str, meta: dict) -> int:
        n = self._counts.get(session_id, 0)
        self._counts[session_id] = n + 1
        return n
