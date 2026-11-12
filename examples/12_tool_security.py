# -*- coding: utf-8 -*-
"""工具安全：危险命令被拒绝。"""
from qharness.hand import execute_tool
from qharness.tools.base import ToolContext

ctx = ToolContext(deny_commands=("rm", "rmdir", "format"))
r = execute_tool("run_bash", {"command": "rm -rf /"}, ctx)
print("success:", r.success)
print("error:", r.error)
