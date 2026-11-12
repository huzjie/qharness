# -*- coding: utf-8 -*-
"""集群：把多个节点组织起来，按角色分派脑/手。"""
from __future__ import annotations

from .node import Node
from .shard import ShardRouter


class Cluster:
    def __init__(self, nodes: list):
        self.nodes = nodes
        self.brain_nodes = [n for n in nodes if n.is_brain]
        self.hand_nodes = [n for n in nodes if n.is_hand]
        self.router = ShardRouter([n.id for n in nodes])

    def route_session(self, session_id: str) -> str:
        return self.router.route(session_id)

    def hand_for(self, session_id: str):
        """按会话一致性哈希选一个手节点。"""
        if not self.hand_nodes:
            return None
        from .shard import hash_shard
        return self.hand_nodes[hash_shard(session_id, len(self.hand_nodes))]

    def summary(self) -> dict:
        return {
            "total_nodes": len(self.nodes),
            "brain_nodes": len(self.brain_nodes),
            "hand_nodes": len(self.hand_nodes),
        }
