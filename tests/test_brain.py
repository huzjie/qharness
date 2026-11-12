# -*- coding: utf-8 -*-
import unittest

from qharness.brain import AgentLoop, RunStatus
from qharness.session import Session


class TestBrain(unittest.TestCase):
    def test_loop_completes(self):
        loop = AgentLoop()
        res = loop.run(Session.new(), "hello")
        self.assertIn(res.status, (RunStatus.COMPLETED, RunStatus.MAX_TURNS))
        self.assertGreater(res.tool_calls, 0)

    def test_loop_mock(self):
        loop = AgentLoop()
        res = loop.run(Session.new(), "创建 TODO 应用")
        self.assertTrue(res.answer)


if __name__ == "__main__":
    unittest.main()
