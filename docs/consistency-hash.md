# Consistency Hash

# 一致性哈希分片

MD5 取模把 session 固定到分片。session 状态本地化，避免跨节点搬状态。

## 复用要点

加虚拟节点可缓解哈希不均；扩缩容时只迁移部分 session。
