# Tools

# 内置工具

14 个内置工具：`read_file / write_file / list_files / grep / search / run_bash / apply_patch / git_status / git_diff / git_log / web_fetch / python_eval / note`。

每个工具返回 `ToolResult(success, output, error, meta)`，并提供 OpenAI 兼容 schema。

## 安全三件套

1. `run_bash` 走命令白名单/黑名单。
2. `python_eval` 走受限全局命名空间（白名单内置函数）。
3. 文件工具做路径越界校验（`_safe_join` 防止 `../` 穿越）。

