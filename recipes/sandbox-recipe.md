# 配方：工具沙箱

**适用**：安全执行任意工具。

**配置**：
```yaml
hand:
  sandbox: process
  deny_commands: ["rm", "rmdir", "del", "format", "shutdown", "mkfs"]
  timeout_ms: 30000
```

**三层防护**：命令白名单 + 路径越界校验 + 超时。
