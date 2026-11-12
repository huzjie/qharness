# -*- coding: utf-8 -*-
import unittest

from qharness.events import Event, EventType, EventFactory, encode_event, decode_event


class TestEvents(unittest.TestCase):
    def test_event_codec_roundtrip(self):
        f = EventFactory("t")
        ev = f.user_message("s1", "hi")
        ev2 = decode_event(encode_event(ev))
        self.assertEqual(ev2.type, EventType.USER_MESSAGE)
        self.assertEqual(ev2.session_id, "s1")
        self.assertEqual(ev2.payload["content"], "hi")

    def test_causation_chain(self):
        f = EventFactory("brain")
        parent = f.user_message("s1", "go")
        child = parent.child(EventType.TOOL_CALL, {"tool": "read_file"}, "brain")
        self.assertEqual(child.causation, parent.event_id)

    def test_fingerprint_stable(self):
        a = Event(EventType.USER_MESSAGE, "s1", {"x": 1})
        b = Event(EventType.USER_MESSAGE, "s1", {"x": 1})
        self.assertEqual(a.fingerprint(), b.fingerprint())


if __name__ == "__main__":
    unittest.main()
