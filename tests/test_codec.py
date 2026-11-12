# -*- coding: utf-8 -*-
import unittest

from qharness.events import Event, EventType, encode_event, decode_event


class TestCodec(unittest.TestCase):
    def test_roundtrip(self):
        e = Event(EventType.TOOL_CALL, "s", {"tool": "grep"})
        self.assertEqual(decode_event(encode_event(e)).payload["tool"], "grep")


if __name__ == "__main__":
    unittest.main()
