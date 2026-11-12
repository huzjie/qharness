# -*- coding: utf-8 -*-
"""密钥脱敏。"""
from qharness.security import redact_secrets

text = "Authorization: Bearer abc.def.ghi  api_key=sk-1234567890  token=ghp_ABCDEFGHIJKLMNOPQRST"
print(redact_secrets(text))
