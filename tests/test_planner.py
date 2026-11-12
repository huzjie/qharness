# -*- coding: utf-8 -*-
import unittest

from qharness.brain import get_planner


class TestPlanner(unittest.TestCase):
    def test_get(self):
        self.assertEqual(get_planner("react").name, "react")

    def test_plan_execute_steps(self):
        p = get_planner("plan_execute").plan("A。B。C", [])
        self.assertEqual(len(p), 3)


if __name__ == "__main__":
    unittest.main()
