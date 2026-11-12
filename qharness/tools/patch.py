# -*- coding: utf-8 -*-
"""补丁工具：apply_patch —— 对文件做 unified diff 应用。"""
from __future__ import annotations

from .base import Tool, ToolContext, ToolResult
from .registry import register


class ApplyPatchTool(Tool):
    name = "apply_patch"
    description = "应用 unified diff 补丁到文件。"
    parameters = {"type": "object", "properties": {
        "path": {"type": "string"},
        "patch": {"type": "string", "description": "unified diff 文本"},
    }, "required": ["path", "patch"]}

    def run(self, args: dict, ctx: ToolContext) -> ToolResult:
        # 简化实现：把 patch 直接写入临时文件交给系统 patch 命令；失败则给出可读错误。
        import tempfile
        from pathlib import Path
        try:
            patch = args["patch"]
            target = Path(ctx.workdir) / args["path"]
            if not target.exists() and "--- " in patch:
                # 尝试从 diff 头恢复原始文件内容（简易 new-file 解析）
                body = []
                for line in patch.splitlines():
                    if line.startswith("+") and not line.startswith("+++"):
                        body.append(line[1:])
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("\n".join(body) + "\n", encoding="utf-8")
                return ToolResult(True, output=f"已按补丁新建文件 {target}")
            with tempfile.NamedTemporaryFile("w", suffix=".diff", delete=False, encoding="utf-8") as f:
                f.write(patch)
                fpath = f.name
            import subprocess
            proc = subprocess.run(["patch", "-p1", "-i", fpath, "-d", ctx.workdir],
                                  capture_output=True, text=True)
            return ToolResult(proc.returncode == 0,
                              output=proc.stdout or proc.stderr,
                              meta={"exit_code": proc.returncode})
        except Exception as e:
            return ToolResult(False, error=str(e))


register(ApplyPatchTool)
