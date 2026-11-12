# -*- coding: utf-8 -*-
import unittest

from qharness.observability import Metrics, Tracer, Auditor


class TestObservability(unittest.TestCase):
    def test_metrics(self):
        m = Metrics()
        m.incr("a")
        m.observe("lat", 1.0)
        snap = m.snapshot()
        self.assertEqual(snap["counters"]["a"], 1)
        self.assertEqual(snap["histograms"]["lat"]["avg"], 1.0)

    def test_tracer(self):
        t = Tracer()
        s = t.start("run")
        t.end(s)
        self.assertGreaterEqual(s.duration_ms, 0)

    def test_audit(self):
        a = Auditor()
        a.record("brain", "tool_call")
        self.assertEqual(a.count(), 1)


if __name__ == "__main__":
    unittest.main()
