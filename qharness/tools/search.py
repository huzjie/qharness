# -*- coding: utf-8 -*-
"""语义搜索占位：接真实向量检索后端（如本地 sqlite-vec / 向量库）。"""
from __future__ import annotations

from .base import Tool, ToolContext, ToolResult
from .registry import register


class SearchTool(Tool):
    name = "search"
    description = "在代码库中语义搜索（占位：接真实嵌入后端）。"
    parameters = {"type": "object", "properties": {
        "query": {"type": "string"},
    }, "required": ["query"]}

    def run(self, args: dict, ctx: ToolContext) -> ToolResult:
        return ToolResult(True, output=f"[语义搜索占位] 查询：{args.get('query')}。接真实嵌入后端后返回相关片段。")


register(SearchTool)
