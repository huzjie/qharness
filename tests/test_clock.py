# -*- coding: utf-8 -*-
import unittest

from qharness.events import LamportClock


class TestClock(unittest.TestCase):
    def test_monotonic(self):
        c = LamportClock()
        a = c.tick()
        b = c.tick()
        self.assertGreater(b, a)

    def test_observe(self):
        c = LamportClock(0)
        c.observe(10)
        self.assertGreater(c.value, 10)


if __name__ == "__main__":
    unittest.main()
