# Sandbox

# 沙箱与资源限制

`ProcessSandbox` 用超时线程演示隔离；生产环境替换为容器/seccomp/cgroup。

## 分层防护

| 层 | 手段 |
|---|---|
| 命令 | 白名单/黑名单（拒绝 rm/format/shutdown） |
| 路径 | 目录越界校验 |
| 资源 | CPU/内存/超时限制 |
| 权限 | Policy（拒绝规则优先） |

