# -*- coding: utf-8 -*-
"""观测：指标 + 追踪 + 审计。"""
from qharness.observability import Metrics, Tracer, Auditor
from qharness.observability.metrics import Timer

m = Metrics()
with Timer(m, "task"):
    pass
m.incr("runs")
m.gauge("sessions", 3)
print(m.snapshot())

t = Tracer()
s = t.start("run", session="s1")
t.end(s)
print("span 时长(ms)：", s.duration_ms)

a = Auditor()
a.record("brain", "tool_call", session_id="s1", detail={"tool": "read_file"})
print("审计条数：", a.count())
