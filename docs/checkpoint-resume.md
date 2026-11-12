# Checkpoint Resume

# 检查点断点续跑

长任务中断后，从检查点恢复。保存 turn_count/messages/state/pending_tool_calls。

## 复用要点

检查点要存「可重放」的状态而非「结果」，这样恢复后能继续推进。
