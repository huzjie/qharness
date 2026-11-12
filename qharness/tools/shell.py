# -*- coding: utf-8 -*-
"""Shell 工具：受限命令执行（白名单/黑名单 + 超时）。"""
from __future__ import annotations

import subprocess

from .base import Tool, ToolContext, ToolResult
from .registry import register


class RunBashTool(Tool):
    name = "run_bash"
    description = "执行 shell 命令（受白名单/黑名单与超时约束）。"
    parameters = {"type": "object", "properties": {
        "command": {"type": "string"},
    }, "required": ["command"]}

    def run(self, args: dict, ctx: ToolContext) -> ToolResult:
        command = args["command"]
        if not ctx.is_command_allowed(command):
            return ToolResult(False, error=f"命令被拒绝：{command}")
        try:
            proc = subprocess.run(
                command, shell=True, cwd=ctx.workdir,
                capture_output=True, text=True,
                timeout=ctx.timeout_ms / 1000.0,
            )
            out = proc.stdout + (proc.stderr if proc.returncode != 0 else "")
            return ToolResult(proc.returncode == 0, output=out.strip() or "(无输出)",
                              meta={"exit_code": proc.returncode})
        except subprocess.TimeoutExpired:
            return ToolResult(False, error="命令超时")
        except Exception as e:
            return ToolResult(False, error=str(e))


register(RunBashTool)
