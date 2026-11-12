# -*- coding: utf-8 -*-
"""直接执行一个工具（手）。"""
from qharness.hand import execute_tool
from qharness.tools.base import ToolContext

ctx = ToolContext(workdir=".")
r = execute_tool("list_files", {"path": "."}, ctx)
print("success:", r.success)
print(r.output)
