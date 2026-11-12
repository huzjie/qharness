# Event Bus

# 事件总线

`Bus` 抽象只有三个方法：`subscribe` / `unsubscribe` / `publish`。

- `MemoryBus`：进程内，`defaultdict(list)` + 锁，零依赖。
- `SocketBus`：TCP socket，标准库实现，演示分布式。

## 可复用要点

订阅用 topic 通配（`*.tool` 匹配 `brain.tool`），发布返回「触发了多少个处理器」，便于观测。单个处理器抛异常不要阻断其它订阅者。

