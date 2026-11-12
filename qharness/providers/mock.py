# -*- coding: utf-8 -*-
"""确定性 mock 后端：离线跑通完整 Agent 循环，行为逐位可复现。

设计：mock 依据「已收到的工具结果数量」从确定性脚本里取下一个工具调用，
脚本执行完则返回确定性最终答案。这样：不接真实模型也能验证
「模型 -> 工具 -> 结果 -> 模型 ... -> 完成」的完整链路，且每次运行结果一致。
"""
from __future__ import annotations

import hashlib
from typing import Optional

from .base import Provider, ModelResponse, ToolCall

_SCRIPT = [
    ("list_files", {"path": ".", "recursive": False}),
    ("read_file", {"path": "README.md"}),
    ("write_file", {"path": "out/summary.md", "content": "# 任务总结\n\n已由 qharness 确定性生成。"}),
    ("run_bash", {"command": "echo done"}),
]


class MockProvider(Provider):
    name = "mock"

    def __init__(self, skill: float = 1.0, script: Optional[list] = None, seed: str = "qharness"):
        self.skill = skill
        self.script = script or _SCRIPT
        self.seed = seed

    def supports_tools(self) -> bool:
        return True

    def chat(self, messages: list, tools: Optional[list] = None, **kw) -> ModelResponse:
        # 统计已返回的工具结果条数
        n_results = sum(1 for m in messages if (m.get("role") if isinstance(m, dict) else getattr(m, "role", "")) == "tool")
        if n_results < len(self.script):
            name, args = self.script[n_results]
            call_id = hashlib.md5(f"{self.seed}:{n_results}".encode()).hexdigest()[:8]
            return ModelResponse(
                tool_calls=[ToolCall(id=call_id, name=name, arguments=dict(args))],
                finish_reason="tool_calls",
            )
        # 脚本执行完毕：返回确定性最终答案
        digest = hashlib.sha256(f"{self.seed}:{self.skill}".encode()).hexdigest()[:12]
        return ModelResponse(
            content=f"任务完成。已按确定性脚本执行 {len(self.script)} 步工具调用，最终产物已生成（run_id={digest}）。",
            finish_reason="stop",
        )

    def score(self) -> float:
        """能力评分：随 skill 单调、随脚本推进趋近 1。"""
        return self.skill


from .registry import register  # noqa: E402
register(MockProvider)
