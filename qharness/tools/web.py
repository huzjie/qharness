# -*- coding: utf-8 -*-
"""Web 工具：抓取网页文本。"""
from __future__ import annotations

import urllib.request

from .base import Tool, ToolContext, ToolResult
from .registry import register


class WebFetchTool(Tool):
    name = "web_fetch"
    description = "抓取 URL 的文本内容（去标签）。"
    parameters = {"type": "object", "properties": {
        "url": {"type": "string"},
    }, "required": ["url"]}

    def run(self, args: dict, ctx: ToolContext) -> ToolResult:
        try:
            url = args["url"]
            req = urllib.request.Request(url, headers={"User-Agent": "qharness/0.1"})
            with urllib.request.urlopen(req, timeout=15) as r:
                html = r.read().decode("utf-8", "replace")
            # 极简去标签
            import re
            text = re.sub(r"<script.*?</script>", "", html, flags=re.S)
            text = re.sub(r"<style.*?</style>", "", text, flags=re.S)
            text = re.sub(r"<[^>]+>", " ", text)
            text = re.sub(r"\s+", " ", text).strip()
            return ToolResult(True, output=text[:4000])
        except Exception as e:
            return ToolResult(False, error=str(e))


register(WebFetchTool)
