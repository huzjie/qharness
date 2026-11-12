# -*- coding: utf-8 -*-
"""指标：计数器 / 直方图 / 摘要（零依赖实现）。"""
from __future__ import annotations

import threading
import time
from collections import defaultdict


class Metrics:
    def __init__(self):
        self._lock = threading.RLock()
        self._counters = defaultdict(int)
        self._histograms = defaultdict(list)
        self._gauges = defaultdict(float)

    def incr(self, name: str, n: int = 1) -> None:
        with self._lock:
            self._counters[name] += n

    def observe(self, name: str, value: float) -> None:
        with self._lock:
            self._histograms[name].append(value)

    def gauge(self, name: str, value: float) -> None:
        with self._lock:
            self._gauges[name] = value

    def snapshot(self) -> dict:
        with self._lock:
            hist = {k: {"count": len(v), "sum": sum(v),
                        "avg": (sum(v) / len(v)) if v else 0.0}
                    for k, v in self._histograms.items()}
            return {"counters": dict(self._counters),
                    "histograms": hist, "gauges": dict(self._gauges)}


class Timer:
    """上下文计时器：自动把耗时记入 metrics。"""

    def __init__(self, metrics: Metrics, name: str):
        self.metrics = metrics
        self.name = name

    def __enter__(self):
        self._t = time.perf_counter()
        return self

    def __exit__(self, *a):
        self.metrics.observe(self.name + "_seconds", time.perf_counter() - self._t)
