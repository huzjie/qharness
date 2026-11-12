# -*- coding: utf-8 -*-
import unittest

from qharness.hand import execute_tool
from qharness.tools.base import ToolContext
from qharness.tools.registry import ensure_loaded, list_tools


class TestAllTools(unittest.TestCase):
    def test_every_tool_registered(self):
        ensure_loaded()
        self.assertGreaterEqual(len(list_tools()), 10)

    def test_tools_have_schema(self):
        ensure_loaded()
        from qharness.tools.registry import all_tool_schemas
        for s in all_tool_schemas():
            self.assertIn("function", s)
            self.assertTrue(s["function"]["name"])


if __name__ == "__main__":
    unittest.main()
