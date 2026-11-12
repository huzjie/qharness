# -*- coding: utf-8 -*-
"""沙箱抽象：隔离工具执行的副作用。"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Sandbox(ABC):
    """沙箱抽象：在受控环境中执行一个可调用对象。"""

    @abstractmethod
    def run(self, fn, *args, **kwargs) -> Any:
        ...


class ProcessSandbox(Sandbox):
    """进程沙箱：用子进程隔离（此处为示意，真实场景配合容器/seccomp）。"""

    def __init__(self, timeout_ms: int = 30000, workdir: str = "."):
        self.timeout_ms = timeout_ms
        self.workdir = workdir

    def run(self, fn, *args, **kwargs):
        # 简化：直接调用（真实沙箱在此替换为子进程/容器执行）
        import threading
        result = {}
        err = {}

        def _target():
            try:
                result["value"] = fn(*args, **kwargs)
            except Exception as e:  # noqa
                err["e"] = e

        t = threading.Thread(target=_target, daemon=True)
        t.start()
        t.join(self.timeout_ms / 1000.0)
        if t.is_alive():
            raise TimeoutError(f"沙箱执行超时（{self.timeout_ms}ms）")
        if "e" in err:
            raise err["e"]
        return result.get("value")
