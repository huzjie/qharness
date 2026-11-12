# Backpressure

# 背压

队列超水位时丢弃新/旧事件。保护慢消费者不拖垮总线。

## 复用要点

丢弃策略要显式（newest/oldest），并计数 dropped 供监控。
