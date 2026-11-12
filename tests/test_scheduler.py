# -*- coding: utf-8 -*-
import unittest

from qharness.scheduler import SessionManager, PriorityQueue, FifoPolicy, FairPolicy


class TestScheduler(unittest.TestCase):
    def test_session_manager(self):
        m = SessionManager()
        s = m.create("s1")
        self.assertEqual(m.get("s1").id, "s1")
        m.close("s1")
        self.assertIsNone(m.get("s1"))

    def test_priority_queue(self):
        q = PriorityQueue()
        q.push("a", 10)
        q.push("b", 0)
        self.assertEqual(q.pop().session_id, "b")

    def test_fair_policy(self):
        p = FairPolicy()
        self.assertEqual(p.next_priority("s", {}), 0)
        self.assertEqual(p.next_priority("s", {}), 1)


if __name__ == "__main__":
    unittest.main()
