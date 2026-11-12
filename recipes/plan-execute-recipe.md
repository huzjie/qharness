# 配方：Plan-Execute

**适用**：多步骤工程任务（建项目、写多个模块）。

**配置**：
```yaml
brain:
  strategy: plan_execute
  max_plan_steps: 8
```

**步骤**：user -> 拆解 -> 逐步执行 + 复盘 -> 汇总
