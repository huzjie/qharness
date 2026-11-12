# -*- coding: utf-8 -*-
"""run：用指定 provider 跑一个编码任务。"""
from __future__ import annotations

import os
import sys


def run_task(prompt: str, provider: str = "mock", model: str = None,
             workdir: str = ".", strategy: str = "react", max_turns: int = 40) -> int:
    from ..providers import get_provider
    from ..brain import AgentLoop
    from ..session import Session

    kw = {}
    if model:
        kw["model"] = model
    prov = get_provider(provider, **kw)
    loop = AgentLoop(provider=prov, workdir=workdir, strategy=strategy, max_turns=max_turns)
    session = Session.new()
    result = loop.run(session, prompt)
    print("=" * 60)
    print(f"任务：{prompt}")
    print(f"状态：{result.status.value}")
    print(f"轮数：{result.turns}  工具调用：{result.tool_calls}  耗时：{result.latency_ms:.1f}ms")
    print("-" * 60)
    print(result.answer)
    print("=" * 60)
    return 0 if result.status.value == "completed" else 1
