# 配方：分布式部署

**适用**：多节点扩展。

**配置**：
```yaml
dist:
  mode: cluster
  shard_key: session_id
  peers: ["node1:8000", "node2:8000"]
```

**拓扑**：脑节点（GPU）+ 手节点（CPU 沙箱），一致性哈希分片会话。
