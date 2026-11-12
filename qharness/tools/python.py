# -*- coding: utf-8 -*-
"""Python 求值工具：受限执行（白名单内置函数）。"""
from __future__ import annotations

from .base import Tool, ToolContext, ToolResult
from .registry import register

_SAFE_GLOBALS = {
    "__builtins__": {
        "abs": abs, "min": min, "max": max, "sum": sum, "len": len,
        "range": range, "enumerate": enumerate, "zip": zip, "list": list,
        "dict": dict, "set": set, "tuple": tuple, "str": str, "int": int,
        "float": float, "round": round, "sorted": sorted, "map": map, "filter": filter,
    },
    "math": None,
}


class PythonEvalTool(Tool):
    name = "python_eval"
    description = "执行受限 Python 表达式并返回结果。"
    parameters = {"type": "object", "properties": {
        "code": {"type": "string"},
    }, "required": ["code"]}

    def run(self, args: dict, ctx: ToolContext) -> ToolResult:
        try:
            import math
            g = dict(_SAFE_GLOBALS)
            g["math"] = math
            result = eval(args["code"], g, {})
            return ToolResult(True, output=str(result))
        except Exception as e:
            return ToolResult(False, error=str(e))


register(PythonEvalTool)
