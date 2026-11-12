# Observability

# 观测

- `Metrics`：计数器/直方图/摘要，零依赖。
- `Tracer`：Span 树 + 事件因果链。
- `Auditor`：审计日志（工具调用/命令执行），可追溯。

## 工程技巧

审计日志要经过密钥脱敏（`redact_secrets`）再落盘，避免 API Key 进日志。

