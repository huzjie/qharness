# -*- coding: utf-8 -*-
import unittest

from qharness.providers import get_provider, list_providers


class TestProviders(unittest.TestCase):
    def test_mock_tool_then_answer(self):
        p = get_provider("mock")
        r1 = p.chat([])
        self.assertTrue(r1.has_tool_calls)
        r2 = p.chat([{"role": "tool", "content": "ok"}] * 4)
        self.assertFalse(r2.has_tool_calls)
        self.assertTrue(r2.content)

    def test_list_providers(self):
        self.assertIn("mock", list_providers())


if __name__ == "__main__":
    unittest.main()
