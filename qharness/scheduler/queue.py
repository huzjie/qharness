# -*- coding: utf-8 -*-
"""优先级队列：待调度任务的缓冲。"""
from __future__ import annotations

import heapq
import itertools
from dataclasses import dataclass, field


@dataclass(order=True)
class Task:
    priority: int
    seq: int
    session_id: str = field(compare=False)
    payload: dict = field(compare=False)

    @staticmethod
    def new(session_id: str, priority: int = 0, payload: dict = None, counter=None) -> "Task":
        return Task(priority=priority, seq=next(counter) if counter else 0,
                    session_id=session_id, payload=payload or {})


class PriorityQueue:
    """基于堆的优先级队列（数字越小优先级越高）。"""

    def __init__(self, capacity: int = 512):
        self.capacity = capacity
        self._heap = []
        self._counter = itertools.count()

    def push(self, session_id: str, priority: int = 0, payload: dict = None) -> bool:
        if len(self._heap) >= self.capacity:
            return False
        heapq.heappush(self._heap, Task.new(session_id, priority, payload, self._counter))
        return True

    def pop(self) -> Task | None:
        if not self._heap:
            return None
        return heapq.heappop(self._heap)

    def peek(self) -> Task | None:
        return self._heap[0] if self._heap else None

    def __len__(self):
        return len(self._heap)
