# Architecture

# 架构总览

qharness 的分层架构：

```
外部请求 -> ingress（接入层，协议翻译）
        -> scheduler（调度层，会话路由/优先级/背压）
        -> brain（推理编排，Agent 循环）
              <--tool_call / tool_result--> bus（事件总线）
        -> hand（工具执行，沙箱/超时/权限）
        -> executor（执行层，进程池/资源限制）
```

核心不变量：**组件只依赖事件，不依赖彼此**。brain 不 import hand，hand 不 import brain，二者通过 `tool_call`/`tool_result` 事件协作。

## 从单进程到多节点

| 演进 | 总线实现 | 改动 |
|---|---|---|
| 单进程多会话 | `MemoryBus` | 无 |
| 多节点 | `SocketBus` / Redis | 只换总线，业务代码零改动 |

这就是「统一事件模型」的价值：分布式是部署问题，不是代码问题。

