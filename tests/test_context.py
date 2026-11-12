# -*- coding: utf-8 -*-
import unittest

from qharness.brain.context import ContextManager


class TestContext(unittest.TestCase):
    def test_fit_truncates(self):
        cm = ContextManager(max_messages=5)
        msgs = [{"role": "system"}, *[{"role": "user"} for _ in range(10)]]
        self.assertLessEqual(len(cm.fit(msgs)), 5)


if __name__ == "__main__":
    unittest.main()
