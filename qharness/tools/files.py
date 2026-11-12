# -*- coding: utf-8 -*-
"""文件工具：read_file / write_file / list_files / grep。"""
from __future__ import annotations

import os
import re
from pathlib import Path

from .base import Tool, ToolContext, ToolResult
from .registry import register


def _safe_join(workdir: str, path: str) -> Path:
    """把相对路径解析到 workdir 内，防止目录穿越。"""
    base = Path(workdir).resolve()
    p = (base / path).resolve()
    if not str(p).startswith(str(base)):
        raise ValueError(f"路径越界：{path}")
    return p


class ReadFileTool(Tool):
    name = "read_file"
    description = "读取指定文件内容（文本）。"
    parameters = {"type": "object", "properties": {
        "path": {"type": "string", "description": "文件路径"},
        "limit": {"type": "integer", "description": "最多读取行数，默认全部"},
    }, "required": ["path"]}

    def run(self, args: dict, ctx: ToolContext) -> ToolResult:
        try:
            p = _safe_join(ctx.workdir, args["path"])
            text = p.read_text(encoding="utf-8", errors="replace")
            if args.get("limit"):
                text = "\n".join(text.splitlines()[: args["limit"]])
            return ToolResult(True, output=text)
        except Exception as e:
            return ToolResult(False, error=str(e))


class WriteFileTool(Tool):
    name = "write_file"
    description = "写入文件内容（覆盖）。"
    parameters = {"type": "object", "properties": {
        "path": {"type": "string"},
        "content": {"type": "string"},
    }, "required": ["path", "content"]}

    def run(self, args: dict, ctx: ToolContext) -> ToolResult:
        try:
            p = _safe_join(ctx.workdir, args["path"])
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(args["content"], encoding="utf-8")
            return ToolResult(True, output=f"已写入 {p}（{len(args['content'])} 字节）")
        except Exception as e:
            return ToolResult(False, error=str(e))


class ListFilesTool(Tool):
    name = "list_files"
    description = "列出目录下的文件。"
    parameters = {"type": "object", "properties": {
        "path": {"type": "string", "description": "目录路径，默认 '.'"},
        "recursive": {"type": "boolean", "description": "是否递归"},
    }, "required": []}

    def run(self, args: dict, ctx: ToolContext) -> ToolResult:
        try:
            root = _safe_join(ctx.workdir, args.get("path", "."))
            recursive = bool(args.get("recursive", False))
            if recursive:
                items = sorted(str(p.relative_to(root)) for p in root.rglob("*"))
            else:
                items = sorted(p.name for p in root.iterdir())
            return ToolResult(True, output="\n".join(items))
        except Exception as e:
            return ToolResult(False, error=str(e))


class GrepTool(Tool):
    name = "grep"
    description = "在文件内容中正则搜索。"
    parameters = {"type": "object", "properties": {
        "pattern": {"type": "string"},
        "path": {"type": "string", "description": "目录或文件"},
        "ignore_case": {"type": "boolean"},
    }, "required": ["pattern"]}

    def run(self, args: dict, ctx: ToolContext) -> ToolResult:
        try:
            root = _safe_join(ctx.workdir, args.get("path", "."))
            pattern = re.compile(args["pattern"], re.I if args.get("ignore_case") else 0)
            hits = []
            files = [root] if root.is_file() else list(root.rglob("*"))
            for f in files:
                if not f.is_file():
                    continue
                try:
                    for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                        if pattern.search(line):
                            hits.append(f"{f.relative_to(root) if root.is_dir() else f.name}:{i}:{line.strip()}")
                except Exception:
                    continue
            return ToolResult(True, output="\n".join(hits[:200]) or "(无匹配)")
        except Exception as e:
            return ToolResult(False, error=str(e))


register(ReadFileTool)
register(WriteFileTool)
register(ListFilesTool)
register(GrepTool)
