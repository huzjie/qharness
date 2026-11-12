# -*- coding: utf-8 -*-
"""会话分片：按 session_id 一致性哈希路由到节点。"""
from __future__ import annotations

import hashlib


def hash_shard(key: str, n_shards: int) -> int:
    """一致性哈希（MD5 取模），session 固定落到同一分片。"""
    h = int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)
    return h % n_shards


class ShardRouter:
    """把 session 路由到分片节点。"""

    def __init__(self, nodes: list):
        self.nodes = nodes

    @property
    def n(self) -> int:
        return len(self.nodes)

    def route(self, session_id: str):
        if not self.nodes:
            return None
        return self.nodes[hash_shard(session_id, self.n)]

    def rebalance(self, nodes: list) -> None:
        """重平衡：替换节点列表（一致性哈希 + 虚拟节点可再扩展）。"""
        self.nodes = nodes
