# Security

# 安全

- 权限模型：拒绝规则优先，`default_deny` 时走允许规则放行。
- 密钥脱敏：正则抹掉 sk/token/secret/password/Bearer/ghp_。
- 命令白名单：内置安全命令集合 + 危险命令黑名单。

编码智能体会执行任意工具，安全是底线而非可选项。

