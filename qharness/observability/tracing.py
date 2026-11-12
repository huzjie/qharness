# -*- coding: utf-8 -*-
"""追踪：Span 树 + 事件因果链。"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field


@dataclass
class Span:
    name: str
    span_id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    parent_id: str = ""
    start: float = field(default_factory=time.time)
    end: float = 0.0
    tags: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    def finish(self):
        self.end = time.time()

    @property
    def duration_ms(self) -> float:
        return (self.end - self.start) * 1000 if self.end else 0.0


class Tracer:
    def __init__(self):
        self._stack: list = []
        self._spans: list = []

    def start(self, name: str, **tags) -> Span:
        parent = self._stack[-1].span_id if self._stack else ""
        s = Span(name=name, parent_id=parent, tags=tags)
        if self._stack:
            self._stack[-1].children.append(s)
        else:
            self._spans.append(s)
        self._stack.append(s)
        return s

    def end(self, span: Span) -> None:
        span.finish()
        if self._stack and self._stack[-1] is span:
            self._stack.pop()

    def roots(self) -> list:
        return self._spans

    def flatten(self) -> list:
        out = []

        def walk(s):
            out.append(s)
            for c in s.children:
                walk(c)
        for r in self._spans:
            walk(r)
        return out
