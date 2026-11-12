# -*- coding: utf-8 -*-
"""背压：队列超过高水位时的丢弃策略，保护慢消费者不拖垮整条总线。"""
from __future__ import annotations

from collections import deque
from enum import Enum


class DropPolicy(Enum):
    """丢弃策略。"""

    NEWEST = "newest"   # 丢弃新事件
    OLDEST = "oldest"   # 丢弃最旧事件
    BLOCK = "block"     # 阻塞（等待消费）


class Backpressure:
    """带背压的有界队列。"""

    def __init__(self, capacity: int = 4096, policy: DropPolicy = DropPolicy.NEWEST):
        self.capacity = capacity
        self.policy = policy
        self._q = deque()
        self.dropped = 0

    def push(self, item) -> bool:
        """尝试入队；若被丢弃返回 False。"""
        if len(self._q) < self.capacity:
            self._q.append(item)
            return True
        if self.policy is DropPolicy.OLDEST:
            self._q.popleft()
            self._q.append(item)
            self.dropped += 1
            return False
        # NEWEST / BLOCK 语义：这里统一按丢弃新事件处理（BLOCK 由调用方实现）
        self.dropped += 1
        return False

    def pop(self):
        if self._q:
            return self._q.popleft()
        return None

    def __len__(self):
        return len(self._q)

    @property
    def usage(self) -> float:
        return len(self._q) / self.capacity if self.capacity else 0.0
