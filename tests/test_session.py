# -*- coding: utf-8 -*-
import unittest

from qharness.session import Session, Message, Role


class TestSession(unittest.TestCase):
    def test_roundtrip(self):
        s = Session.new("s1")
        s.append(Message(Role.USER, "hi"))
        s2 = Session.from_dict(s.to_dict())
        self.assertEqual(s2.id, "s1")
        self.assertEqual(len(s2.messages), 1)

    def test_history_limit(self):
        s = Session.new("s1")
        for i in range(10):
            s.append(Message(Role.USER, f"m{i}"))
        self.assertEqual(len(s.history(3)), 3)


if __name__ == "__main__":
    unittest.main()
