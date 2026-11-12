# -*- coding: utf-8 -*-
"""命令白名单：内置安全命令集合。"""
from __future__ import annotations

import shlex

_SAFE = {
    "ls", "cat", "head", "tail", "pwd", "echo", "printf", "grep", "find",
    "wc", "sort", "uniq", "diff", "sed", "awk", "mkdir", "touch", "cp", "mv",
    "python", "python3", "pip", "git", "curl", "wget", "make", "pytest", "tree",
}

_DENY = {"rm", "rmdir", "del", "format", "shutdown", "reboot", "mkfs", "dd", "chmod", "chown", "sudo"}


class CommandAllowlist:
    def __init__(self, safe=_SAFE, deny=_DENY):
        self.safe = safe
        self.deny = deny

    def is_allowed(self, command: str) -> bool:
        try:
            argv = shlex.split(command)
        except Exception:
            argv = command.split()
        if not argv:
            return False
        base = argv[0].split("/")[-1].split("\\")[-1]
        if base in self.deny:
            return False
        return base in self.safe

    def reason(self, command: str) -> str:
        return "ok" if self.is_allowed(command) else "blocked"
