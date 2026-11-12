# -*- coding: utf-8 -*-
"""Tool 抽象接口 + 结果结构。"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ToolContext:
    """工具执行上下文：工作目录、会话、权限等。"""

    workdir: str = "."
    session_id: str = ""
    allowlist: Optional[set] = None
    deny_commands: tuple = ()
    timeout_ms: int = 30000

    def is_command_allowed(self, command: str) -> bool:
        """命令白名单/黑名单校验：拒绝危险命令。"""
        import shlex
        try:
            argv = shlex.split(command)
        except Exception:
            argv = command.split()
        if not argv:
            return False
        base = argv[0].split("/")[-1].split("\\")[-1]
        if self.deny_commands and base in self.deny_commands:
            return False
        if self.allowlist is not None:
            return base in self.allowlist
        return True


@dataclass
class ToolResult:
    success: bool
    output: str = ""
    error: str = ""
    meta: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"success": self.success, "output": self.output, "error": self.error, **self.meta}


class Tool(ABC):
    """工具抽象。"""

    name: str = "tool"
    description: str = ""
    parameters: dict = {"type": "object", "properties": {}}

    @abstractmethod
    def run(self, arguments: dict, ctx: ToolContext) -> ToolResult:
        ...

    def schema(self) -> dict:
        """返回 OpenAI 兼容的工具 schema。"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }
