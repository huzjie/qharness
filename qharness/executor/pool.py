# -*- coding: utf-8 -*-
"""执行池：有界线程池 + 资源限制。"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable

from .limits import ResourceLimits


class ExecutorPool:
    def __init__(self, max_workers: int = 8, limits: ResourceLimits | None = None):
        self.max_workers = max_workers
        self.limits = limits or ResourceLimits()
        self._exec = ThreadPoolExecutor(max_workers=max_workers)

    def submit(self, fn: Callable, *args, **kwargs) -> Future:
        return self._exec.submit(fn, *args, **kwargs)

    def run_bounded(self, fn: Callable, *args, **kwargs):
        """在资源限制下运行（当前为占位校验，真实实现交给 cgroup/容器）。"""
        return fn(*args, **kwargs)

    def shutdown(self):
        self._exec.shutdown(wait=True)
