# -*- coding: utf-8 -*-
"""最小示例：发一个事件，走一遍总线。"""
from qharness.events import Event, EventType
from qharness.bus import MemoryBus

bus = MemoryBus()
seen = []
bus.subscribe(EventType.USER_MESSAGE, lambda e: seen.append(e))
bus.publish(Event(EventType.USER_MESSAGE, "s1", {"content": "你好"}))
print("收到事件数：", len(seen))
print("内容：", seen[0].payload["content"])
