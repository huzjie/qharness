# Event Model

# 统一事件模型

一切交互都是 `Event`：

```
Event(type, session_id, payload, event_id, timestamp, causation, source)
```

- `causation`：父事件 ID，串起因果链，用于分布式追踪。
- `source`：产生事件的组件（brain/hand/ingress），用于路由与审计。
- `payload`：业务载荷。

## 可复用思路

把系统里的「方法调用」改成「事件发布」，就能获得：可追踪、可重放、可解耦、可分布。代价是异步化带来的调试成本，需要 `causation` 链来抵消。

