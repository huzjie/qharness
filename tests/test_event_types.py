# -*- coding: utf-8 -*-
import unittest

from qharness.events import EventType, is_valid_type


class TestEventTypes(unittest.TestCase):
    def test_all_types_valid(self):
        for t in EventType.ALL:
            self.assertTrue(is_valid_type(t))

    def test_invalid(self):
        self.assertFalse(is_valid_type("nope"))


if __name__ == "__main__":
    unittest.main()
