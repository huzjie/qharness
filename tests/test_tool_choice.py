# -*- coding: utf-8 -*-
import unittest

from qharness.brain.tool_choice import ToolChooser


class TestToolChoice(unittest.TestCase):
    def test_choose(self):
        c = ToolChooser()
        self.assertEqual(c.choose("读取文件", ["read_file", "write_file"]), "read_file")


if __name__ == "__main__":
    unittest.main()
