# -*- coding: utf-8 -*-
"""分布式集群：脑/手节点分派。"""
from qharness.dist import Node, Cluster, hash_shard

nodes = [
    Node(id="brain-1", role="brain"),
    Node(id="brain-2", role="brain"),
    Node(id="hand-1", role="hand"),
    Node(id="hand-2", role="hand"),
    Node(id="hand-3", role="hand"),
]
cluster = Cluster(nodes)
print(cluster.summary())
for sid in ["a", "b", "c", "d"]:
    print(f"session {sid} -> 手节点 {cluster.hand_for(sid).id}")
