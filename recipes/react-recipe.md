# 配方：ReAct 循环

**适用**：简单、单文件、判断性任务。

**配置**：
```yaml
brain:
  strategy: react
  max_turns: 40
  temperature: 0.0
```

**步骤**：user -> (思考 -> 工具调用 -> 观察) * n -> 结论
