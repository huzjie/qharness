# Configuration

# 配置

见 `config.example.yaml`。所有配置可用环境变量 `QH_*` 覆盖。

| 分组 | 关键项 |
|---|---|
| events | clock / trace |
| bus | backend（memory/socket/redis） |
| session | max_turns / checkpoint |
| brain | strategy / context_window |
| hand | timeout_ms / allowlist |
| scheduler | max_sessions / priority |
| dist | mode / shard_key |

