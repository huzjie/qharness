# -*- coding: utf-8 -*-
"""用 mock 后端生成确定性 Agent 轨迹数据集（供训练/评测）。"""
import json
from qharness.brain import AgentLoop
from qharness.session import Session

tasks = [
    "创建 Flask 应用",
    "为代码写单测",
    "修复一个 Bug",
    "重构一个模块",
    "生成 API 文档",
]
loop = AgentLoop()
dataset = []
for t in tasks:
    s = Session.new()
    res = loop.run(s, t)
    dataset.append({"task": t, "status": res.status.value,
                    "tool_calls": res.tool_calls, "messages": [m.to_dict() for m in res.messages]})
with open("agent_trajectories.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)
print(f"生成 {len(dataset)} 条轨迹")
