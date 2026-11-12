# -*- coding: utf-8 -*-
"""调度：优先级队列。"""
from qharness.scheduler import PriorityQueue

q = PriorityQueue()
q.push("s_low", priority=10)
q.push("s_high", priority=0)
q.push("s_mid", priority=5)
while len(q):
    t = q.pop()
    print(f"处理 {t.session_id}（优先级 {t.priority}）")
