# -*- coding: utf-8 -*-
import unittest

from qharness.bus import MemoryBus
from qharness.events import Event, EventType
from qharness.hand import ToolExecutor


class TestHand(unittest.TestCase):
    def test_executor_publishes_result(self):
        bus = MemoryBus()
        results = []
        bus.subscribe(EventType.TOOL_RESULT, lambda e: results.append(e))
        ex = ToolExecutor(bus).start()
        bus.publish(Event(EventType.TOOL_CALL, "s1",
                          {"tool": "python_eval", "arguments": {"code": "1+1"}, "call_id": "c1"}))
        self.assertTrue(results)
        ex.stop()


if __name__ == "__main__":
    unittest.main()
