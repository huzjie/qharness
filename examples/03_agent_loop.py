# -*- coding: utf-8 -*-
"""跑通完整 Agent 循环（mock 后端，离线）。"""
from qharness.brain import AgentLoop
from qharness.session import Session

loop = AgentLoop()
result = loop.run(Session.new(), "创建一个 TODO 应用")
print("状态：", result.status.value)
print("工具调用次数：", result.tool_calls)
print("答案：", result.answer)
