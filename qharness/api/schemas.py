# -*- coding: utf-8 -*-
"""API 请求/响应模型（pydantic 可选依赖）。"""
from __future__ import annotations

try:
    from pydantic import BaseModel, Field
except ImportError:  # pragma: no cover
    class BaseModel:  # type: ignore
        def __init__(self, **kw):
            for k, v in kw.items():
                setattr(self, k, v)

    class Field:  # type: ignore
        def __init__(self, *a, **k):
            pass


class ChatMessage(BaseModel):
    role: str = "user"
    content: str = ""


class ChatRequest(BaseModel):
    model: str = "qharness"
    messages: list = []
    tools: list = []
    stream: bool = False
    temperature: float = 0.0
    max_turns: int = 40


class ChatResponse(BaseModel):
    id: str = ""
    object: str = "chat.completion"
    choices: list = []
    usage: dict = {}


class SessionCreate(BaseModel):
    session_id: str = ""


class RunRequest(BaseModel):
    session_id: str = ""
    prompt: str = ""
    strategy: str = "react"
