# -*- coding: utf-8 -*-
"""演示：分布式集群拓扑。"""
from qharness.dist import Node, Cluster

nodes = [Node(id="brain-1", role="brain"), Node(id="brain-2", role="brain")]
for i in range(1, 6):
    nodes.append(Node(id=f"hand-{i}", role="hand"))

cluster = Cluster(nodes)
print("集群拓扑：", cluster.summary())
print("会话路由示例：")
for sid in ["s-aaa", "s-bbb", "s-ccc"]:
    print(f"  {sid} -> {cluster.route_session(sid)}（手节点 {cluster.hand_for(sid).id}）")
