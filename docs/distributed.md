# Distributed

# 分布式演进

- `ShardRouter`：按 session_id 做 MD5 一致性哈希，session 固定落到同一分片。
- `Cluster`：把节点按角色（brain/hand）分组。
- `Discovery`：静态列表，可扩展 gossip。

## 关键思路

「先单机跑通，再谈分布式」。因为事件模型不变，单机代码天然可分布——只是总线实现从内存换成网络。

