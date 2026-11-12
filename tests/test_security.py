# -*- coding: utf-8 -*-
import unittest

from qharness.security import redact_secrets, CommandAllowlist, Policy


class TestSecurity(unittest.TestCase):
    def test_redact(self):
        out = redact_secrets("Authorization: Bearer abc.def")
        self.assertNotIn("abc.def", out)

    def test_allowlist(self):
        al = CommandAllowlist()
        self.assertTrue(al.is_allowed("ls -la"))
        self.assertFalse(al.is_allowed("rm -rf /"))

    def test_policy_deny_first(self):
        p = Policy().add_deny(lambda c: True)
        self.assertFalse(p.check({}))


if __name__ == "__main__":
    unittest.main()
