# -*- coding: utf-8 -*-
"""密钥脱敏：日志/审计前抹掉 API Key、Token、密码。"""
from __future__ import annotations

import re

_PATTERNS = [
    (re.compile(r"(sk|api[-_]?key|token|secret|password|passwd)\s*[=:]\s*[\w.-]+", re.I), "\\1=***"),
    (re.compile(r"(Bearer|Basic)\s+[\w.-]+", re.I), "\\1 ***"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AKIA***"),
    (re.compile(r"ghp_[0-9A-Za-z]{20,}"), "ghp_***"),
]


class Redactor:
    def __init__(self, patterns=None):
        self.patterns = patterns or _PATTERNS

    def redact(self, text: str) -> str:
        out = text
        for pat, repl in self.patterns:
            out = pat.sub(repl, out)
        return out


def redact_secrets(text: str) -> str:
    return Redactor().redact(text)
