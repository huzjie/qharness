# -*- coding: utf-8 -*-
"""审计：记录关键操作（工具调用/命令执行），可追溯。"""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field


@dataclass
class AuditLog:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    ts: float = field(default_factory=time.time)
    actor: str = ""
    action: str = ""
    session_id: str = ""
    detail: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"id": self.id, "ts": self.ts, "actor": self.actor,
                "action": self.action, "session_id": self.session_id, "detail": self.detail}


class Auditor:
    def __init__(self):
        self._logs: list = []

    def record(self, actor: str, action: str, session_id: str = "", detail: dict = None) -> AuditLog:
        log = AuditLog(actor=actor, action=action, session_id=session_id, detail=detail or {})
        self._logs.append(log)
        return log

    def dump(self, path: str = None) -> str:
        data = json.dumps([l.to_dict() for l in self._logs], ensure_ascii=False, indent=2)
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(data)
        return data

    def count(self) -> int:
        return len(self._logs)
