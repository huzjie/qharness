# -*- coding: utf-8 -*-
import unittest

from qharness.hand import execute_tool
from qharness.tools.base import ToolContext


class TestTools(unittest.TestCase):
    def test_python_eval(self):
        r = execute_tool("python_eval", {"code": "2**10"}, ToolContext())
        self.assertTrue(r.success)
        self.assertEqual(r.output.strip(), "1024")

    def test_list_files(self):
        r = execute_tool("list_files", {"path": "."}, ToolContext(workdir="."))
        self.assertTrue(r.success)

    def test_unknown_tool(self):
        r = execute_tool("nope", {}, ToolContext())
        self.assertFalse(r.success)

    def test_dangerous_command_blocked(self):
        ctx = ToolContext(deny_commands=("rm",))
        r = execute_tool("run_bash", {"command": "rm -rf /"}, ctx)
        self.assertFalse(r.success)


if __name__ == "__main__":
    unittest.main()
