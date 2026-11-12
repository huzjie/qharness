# -*- coding: utf-8 -*-
"""工具并发池：限制并发、按需排队。"""
from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Iterable


class ToolPool:
    """有界并发工具执行池。"""

    def __init__(self, max_workers: int = 4):
        self._exec = ThreadPoolExecutor(max_workers=max_workers)

    def map(self, fn: Callable, tasks: Iterable):
        return self._exec.map(fn, tasks)

    def submit(self, fn: Callable, *args, **kwargs):
        return self._exec.submit(fn, *args, **kwargs)

    def run_all(self, fn: Callable, tasks: list, collect: bool = True):
        """执行所有任务，返回 (结果列表, 失败列表)。"""
        futures = [self._exec.submit(fn, *t) if isinstance(t, tuple) else self._exec.submit(fn, t) for t in tasks]
        results, errors = [], []
        for f in as_completed(futures):
            try:
                results.append(f.result())
            except Exception as e:  # noqa
                errors.append(e)
        return results, errors

    def shutdown(self):
        self._exec.shutdown(wait=True)
