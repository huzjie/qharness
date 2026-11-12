# -*- coding: utf-8 -*-
"""Git 工具：status / diff / log / commit。"""
from __future__ import annotations

import subprocess

from .base import Tool, ToolContext, ToolResult
from .registry import register


def _git(args: list, ctx: ToolContext) -> ToolResult:
    try:
        proc = subprocess.run(["git", *args], cwd=ctx.workdir,
                              capture_output=True, text=True, timeout=ctx.timeout_ms / 1000.0)
        return ToolResult(proc.returncode == 0,
                          output=(proc.stdout or proc.stderr).strip() or "(无输出)",
                          meta={"exit_code": proc.returncode})
    except Exception as e:
        return ToolResult(False, error=str(e))


class GitStatusTool(Tool):
    name = "git_status"
    description = "查看 git 工作区状态。"
    parameters = {"type": "object", "properties": {}}

    def run(self, args, ctx: ToolContext) -> ToolResult:
        return _git(["status", "--short"], ctx)


class GitDiffTool(Tool):
    name = "git_diff"
    description = "查看 git diff。"
    parameters = {"type": "object", "properties": {}}

    def run(self, args, ctx: ToolContext) -> ToolResult:
        return _git(["diff"], ctx)


class GitLogTool(Tool):
    name = "git_log"
    description = "查看 git 提交历史。"
    parameters = {"type": "object", "properties": {"n": {"type": "integer"}}}

    def run(self, args, ctx: ToolContext) -> ToolResult:
        n = str(args.get("n", 10))
        return _git(["log", "--oneline", "-n", n], ctx)


register(GitStatusTool)
register(GitDiffTool)
register(GitLogTool)
