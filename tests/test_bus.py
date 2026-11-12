# -*- coding: utf-8 -*-
import unittest

from qharness.bus import MemoryBus, match_topic
from qharness.events import Event, EventType


class TestBus(unittest.TestCase):
    def test_pubsub(self):
        b = MemoryBus()
        got = []
        b.subscribe(EventType.USER_MESSAGE, lambda e: got.append(e))
        n = b.publish(Event(EventType.USER_MESSAGE, "s1", {"content": "x"}))
        self.assertEqual(n, 1)
        self.assertEqual(len(got), 1)

    def test_wildcard(self):
        self.assertTrue(match_topic("*", EventType.USER_MESSAGE))
        self.assertFalse(match_topic("tool_call", EventType.TOOL_RESULT))

    def test_unsubscribe(self):
        b = MemoryBus()
        got = []
        sub = b.subscribe(EventType.TOOL_CALL, lambda e: got.append(e))
        b.unsubscribe(sub)
        b.publish(Event(EventType.TOOL_CALL, "s1"))
        self.assertEqual(len(got), 0)


if __name__ == "__main__":
    unittest.main()
