# -*- coding: utf-8 -*-
"""服务发现：静态列表 / 可扩展 gossip。"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Discovery(ABC):
    @abstractmethod
    def peers(self) -> list:
        ...


class StaticDiscovery(Discovery):
    """静态节点列表。"""

    def __init__(self, nodes: list):
        self.nodes = nodes

    def peers(self) -> list:
        return list(self.nodes)
