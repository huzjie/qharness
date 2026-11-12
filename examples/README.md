# 可运行示例

按编号递增，从最小的事件到完整 Agent 循环、分布式集群：

| 编号 | 示例 | 说明 |
|---|---|---|
| 01 | hello_event | 最小事件 + 总线 |
| 02 | tool_execute | 直接执行工具（手） |
| 03 | agent_loop | 完整 Agent 循环（mock） |
| 04 | custom_tool | 注册自定义工具 |
| 05 | memory_bus_pubsub | 手脑分离事件协作 |
| 06 | session_checkpoint | 会话检查点 |
| 07 | distributed_cluster | 分布式集群分派 |
| 08 | openai_compat | OpenAI 兼容客户端 |
| 09 | observability | 指标/追踪/审计 |
| 10 | security_redact | 密钥脱敏 |
| 11 | scheduler_queue | 优先级队列 |
| 12 | tool_security | 危险命令拦截 |

运行：`python examples/03_agent_loop.py`
