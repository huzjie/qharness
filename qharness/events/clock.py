# -*- coding: utf-8 -*-
"""逻辑时钟：Lamport 时钟用于分布式事件的偏序判定。"""
from __future__ import annotations

import time
from abc import ABC, abstractmethod


class Clock(ABC):
    """时钟抽象：给事件打时间戳 + 维护因果顺序。"""

    @abstractmethod
    def now(self) -> float:
        """当前时间戳。"""

    @abstractmethod
    def tick(self) -> int:
        """逻辑时钟前进一格并返回当前值。"""


class WallClock(Clock):
    """墙钟：返回 epoch 秒。"""

    def now(self) -> float:
        return time.time()

    def tick(self) -> int:
        return int(time.time() * 1000)


class LamportClock(Clock):
    """Lamport 逻辑时钟：本地递增，收到带更大计数的事件时对齐，用于判定"先于"关系。"""

    def __init__(self, start: int = 0):
        self._counter = start

    def now(self) -> float:
        return float(self._counter)

    def tick(self) -> int:
        self._counter += 1
        return self._counter

    def observe(self, other: int) -> None:
        """观察到外部事件的逻辑时间，本地对齐到 max(local, other)+1。"""
        self._counter = max(self._counter, other) + 1

    @property
    def value(self) -> int:
        return self._counter
