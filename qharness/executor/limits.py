# -*- coding: utf-8 -*-
"""资源限制：CPU/内存/超时约束。"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ResourceLimits:
    cpu_limit: float = 0.8
    mem_limit_mb: int = 2048
    timeout_ms: int = 30000
    max_open_files: int = 1024

    def as_dict(self) -> dict:
        return {"cpu_limit": self.cpu_limit, "mem_limit_mb": self.mem_limit_mb,
                "timeout_ms": self.timeout_ms, "max_open_files": self.max_open_files}

    def within(self, cpu_used: float, mem_used_mb: int) -> bool:
        return cpu_used <= self.cpu_limit and mem_used_mb <= self.mem_limit_mb
