# -*- coding: utf-8 -*-
"""手脑分离：脑发 tool_call，手订阅并回发 tool_result。"""
from qharness.bus import MemoryBus
from qharness.events import Event, EventType, EventFactory
from qharness.hand.executor import execute_tool
from qharness.tools.base import ToolContext

bus = MemoryBus()
factory = EventFactory("brain")

def hand_handler(event):
    p = event.payload
    result = execute_tool(p["tool"], p.get("arguments", {}), ToolContext())
    bus.publish(Event(EventType.TOOL_RESULT, event.session_id,
                      {"call_id": p["call_id"], "result": result.to_dict()}, source="hand"))

bus.subscribe(EventType.TOOL_CALL, hand_handler)
bus.subscribe(EventType.TOOL_RESULT, lambda e: print("收到工具结果：", e.payload["result"]["output"]))

bus.publish(factory.tool_call("s1", "python_eval", {"code": "6*7"}, "c1"))
