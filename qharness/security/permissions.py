# -*- coding: utf-8 -*-
"""权限模型：基于规则的拒绝/允许。"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DenyRule:
    """拒绝规则：命中即拒绝。"""

    predicate: callable  # (ctx) -> bool
    reason: str = "denied"

    def match(self, ctx) -> bool:
        return bool(self.predicate(ctx))


@dataclass
class AllowRule:
    """允许规则：命中即放行（默认拒绝时使用）。"""

    predicate: callable
    reason: str = "allowed"

    def match(self, ctx) -> bool:
        return bool(self.predicate(ctx))


class Policy:
    """权限策略：默认允许 + 拒绝规则优先（default_deny=True 则默认拒绝 + 允许规则放行）。"""

    def __init__(self, default_deny: bool = False):
        self.default_deny = default_deny
        self.deny_rules: list = []
        self.allow_rules: list = []

    def add_deny(self, predicate, reason="denied") -> "Policy":
        self.deny_rules.append(DenyRule(predicate, reason))
        return self

    def add_allow(self, predicate, reason="allowed") -> "Policy":
        self.allow_rules.append(AllowRule(predicate, reason))
        return self

    def check(self, ctx) -> bool:
        """返回是否允许。拒绝规则优先。"""
        for r in self.deny_rules:
            if r.match(ctx):
                return False
        if self.default_deny:
            for r in self.allow_rules:
                if r.match(ctx):
                    return True
            return False
        return True


class Permission:
    """权限门面：对「命令执行 / 文件访问」做统一鉴权。"""

    def __init__(self):
        self.command_policy = Policy(default_deny=False)
        self.file_policy = Policy(default_deny=False)

    def can_run_command(self, command: str) -> bool:
        return self.command_policy.check({"command": command})

    def can_access_file(self, path: str) -> bool:
        return self.file_policy.check({"path": path})
