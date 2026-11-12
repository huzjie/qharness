# -*- coding: utf-8 -*-
"""节点：一个可独立运行的 qharness 实例（脑/手可部署在不同节点）。"""
from __future__ import annotations

from dataclasses import dataclass, field

from ..bus.base import Bus


@dataclass
class Node:
    id: str
    role: str = "all"          # all | brain | hand
    bus: Bus = None
    meta: dict = field(default_factory=dict)

    @property
    def is_brain(self) -> bool:
        return self.role in ("all", "brain")

    @property
    def is_hand(self) -> bool:
        return self.role in ("all", "hand")
