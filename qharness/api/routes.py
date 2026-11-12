# -*- coding: utf-8 -*-
"""控制面路由。"""
from __future__ import annotations

import uuid
from typing import Optional


def build_routes(loop, manager):
    """构造路由（与 FastAPI 解耦，便于无依赖场景下复用逻辑）。"""
    from .schemas import ChatRequest, ChatResponse

    def _chat(req: ChatRequest) -> dict:
        from ..session.model import Session, Message
        session_id = req.messages[0].get("meta", {}).get("session_id") if req.messages else None
        session = manager.get(session_id) if session_id else None
        if session is None:
            session = manager.create(session_id)
        user = ""
        for m in req.messages:
            if m.get("role") == "user":
                user = m.get("content", "")
        if not user:
            user = " ".join(str(m.get("content", "")) for m in req.messages if m.get("role") == "user")
        result = loop.run(session, user, tools=req.tools, temperature=req.temperature)
        return {
            "id": uuid.uuid4().hex,
            "object": "chat.completion",
            "choices": [{"index": 0, "message": {"role": "assistant", "content": result.answer},
                         "finish_reason": "stop"}],
            "usage": {"turns": result.turns, "tool_calls": result.tool_calls},
        }

    return {"chat": _chat}
