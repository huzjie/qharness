# -*- coding: utf-8 -*-
"""基准：Agent 循环耗时。"""
import time
from qharness.brain import AgentLoop
from qharness.session import Session

loop = AgentLoop()
t0 = time.perf_counter()
for i in range(20):
    loop.run(Session.new(), f"任务 {i}")
dt = time.perf_counter() - t0
print(f"20 次循环共 {dt:.3f}s，平均 {dt/20*1000:.1f}ms/次")
