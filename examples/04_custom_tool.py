# -*- coding: utf-8 -*-
"""注册一个自定义工具。"""
from qharness.tools.base import Tool, ToolResult
from qharness.tools.registry import register


class HelloTool(Tool):
    name = "hello"
    description = "打招呼"
    parameters = {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}

    def run(self, args, ctx):
        return ToolResult(True, output=f"你好，{args['name']}！")


register(HelloTool)

from qharness.hand import execute_tool
from qharness.tools.base import ToolContext
r = execute_tool("hello", {"name": "qharness"}, ToolContext())
print(r.output)
