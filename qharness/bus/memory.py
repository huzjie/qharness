# -*- coding: utf-8 -*-
"""内存事件总线：进程内发布/订阅，零依赖、线程安全。"""
from __future__ import annotations

import threading
from collections import defaultdict
from typing import Callable, DefaultDict, List

from ..events.event import Event
from .base import Bus, Handler, Subscription
from .router import match_topic


class MemoryBus(Bus):
    """进程内内存总线。"""

    def __init__(self):
        self._lock = threading.RLock()
        self._subs: DefaultDict[str, List[Subscription]] = defaultdict(list)
        self._closed = False

    def subscribe(self, topic: str, handler: Handler) -> Subscription:
        sub = Subscription(topic, handler)
        with self._lock:
            self._subs[topic].append(sub)
        return sub

    def unsubscribe(self, sub: Subscription) -> None:
        with self._lock:
            sub.active = False
            if sub in self._subs.get(sub.topic, []):
                self._subs[sub.topic].remove(sub)

    def publish(self, event: Event) -> int:
        if self._closed:
            return 0
        fired = 0
        with self._lock:
            subs = list(self._subs.items())
        for topic, handlers in subs:
            if not match_topic(topic, event.type):
                continue
            for h in list(handlers):
                if h.active:
                    try:
                        h.handler(event)
                        fired += 1
                    except Exception:
                        # 单个处理器异常不阻断其它订阅者；由观测层记录
                        continue
        return fired

    def close(self) -> None:
        with self._lock:
            self._closed = True
            self._subs.clear()

    @property
    def subscriber_count(self) -> int:
        with self._lock:
            return sum(len(v) for v in self._subs.values())
