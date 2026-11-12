# -*- coding: utf-8 -*-
"""笔记/记忆工具：把关键结论写入会话状态（供后续轮次引用）。"""
from __future__ import annotations

from .base import Tool, ToolContext, ToolResult
from .registry import register


class NoteTool(Tool):
    name = "note"
    description = "记录一条结构化笔记到会话。"
    parameters = {"type": "object", "properties": {
        "key": {"type": "string"},
        "value": {"type": "string"},
    }, "required": ["key", "value"]}

    def run(self, args: dict, ctx: ToolContext) -> ToolResult:
        return ToolResult(True, output=f"已记录 {args['key']}={args['value']}",
                          meta={"key": args["key"], "value": args["value"]})


register(NoteTool)
