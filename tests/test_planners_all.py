# -*- coding: utf-8 -*-
import unittest

from qharness.brain import get_planner


class TestPlannersAll(unittest.TestCase):
    def test_all_strategies(self):
        for name in ("react", "plan_execute", "reflect"):
            p = get_planner(name)
            self.assertTrue(p.system_prompt())


if __name__ == "__main__":
    unittest.main()
