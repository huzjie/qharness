# -*- coding: utf-8 -*-
"""检查点：长任务断点续跑。"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Checkpoint:
    session_id: str
    turn_count: int
    messages: list = field(default_factory=list)
    state: dict = field(default_factory=dict)
    pending_tool_calls: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "turn_count": self.turn_count,
            "messages": self.messages,
            "state": self.state,
            "pending_tool_calls": self.pending_tool_calls,
        }

    @staticmethod
    def from_dict(d: dict) -> "Checkpoint":
        return Checkpoint(
            session_id=d["session_id"], turn_count=d.get("turn_count", 0),
            messages=d.get("messages", []), state=d.get("state", {}),
            pending_tool_calls=d.get("pending_tool_calls", []),
        )


def save_checkpoint(cp: Checkpoint, path: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(cp.to_dict(), f, ensure_ascii=False)


def load_checkpoint(path: str) -> Optional[Checkpoint]:
    p = Path(path)
    if not p.exists():
        return None
    with open(p, encoding="utf-8") as f:
        return Checkpoint.from_dict(json.load(f))
