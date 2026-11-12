# -*- coding: utf-8 -*-
"""基准：事件总线吞吐。"""
import time
from qharness.bus import MemoryBus
from qharness.events import Event, EventType

bus = MemoryBus()
bus.subscribe(EventType.SYSTEM, lambda e: None)

n = 10000
t0 = time.perf_counter()
for i in range(n):
    bus.publish(Event(EventType.SYSTEM, "s", {"i": i}))
dt = time.perf_counter() - t0
print(f"{n} 事件耗时 {dt:.3f}s，吞吐 {n/dt:.0f} evt/s")
