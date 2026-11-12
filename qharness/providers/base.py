# -*- coding: utf-8 -*-
"""Provider 抽象接口 + 统一响应结构。"""
from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict

    @staticmethod
    def from_dict(d: dict) -> "ToolCall":
        fn = d.get("function", d)
        args = fn.get("arguments", {})
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except Exception:
                args = {}
        return ToolCall(id=d.get("id", ""), name=fn.get("name", ""), arguments=args)


@dataclass
class ModelResponse:
    """统一模型响应：要么是文本，要么是工具调用（二者其一）。"""

    content: str = ""
    tool_calls: list = field(default_factory=list)
    raw: Any = None
    finish_reason: str = "stop"

    @property
    def has_tool_calls(self) -> bool:
        return bool(self.tool_calls)


class Provider(ABC):
    """LLM 后端抽象。"""

    name: str = "base"

    @abstractmethod
    def chat(self, messages: list, tools: Optional[list] = None, **kw) -> ModelResponse:
        """根据消息列表返回统一响应。tools 为 OpenAI 工具 schema 列表。"""

    def supports_tools(self) -> bool:
        return True


def to_openai_messages(messages) -> list:
    """把内部 Message 列表转成 OpenAI 兼容消息列表。"""
    out = []
    for m in messages:
        if hasattr(m, "to_dict"):
            out.append(m.to_dict())
        else:
            out.append(m)
    return out
