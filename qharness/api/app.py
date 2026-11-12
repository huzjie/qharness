# -*- coding: utf-8 -*-
"""FastAPI 应用工厂：OpenAI 兼容 + 会话管理。"""
from __future__ import annotations

from typing import Optional


def create_app(loop=None, manager=None, auth_token: Optional[str] = None):
    """创建 FastAPI 应用（无 fastapi 时抛清晰错误）。"""
    try:
        from fastapi import FastAPI, Request
        from fastapi.responses import JSONResponse
    except ImportError as e:  # pragma: no cover
        raise ImportError("FastAPI 控制面需要安装：pip install -e '.[api]'") from e

    if loop is None:
        from ..brain.loop import AgentLoop
        loop = AgentLoop()
    if manager is None:
        from ..scheduler.manager import SessionManager
        manager = SessionManager()

    from .routes import build_routes
    routes = build_routes(loop, manager)

    app = FastAPI(title="qharness", version="0.1.0")

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "qharness"}

    @app.post("/v1/chat/completions")
    async def chat_completions(request: Request):
        body = await request.json()
        if auth_token:
            auth = request.headers.get("authorization", "")
            if auth != f"Bearer {auth_token}":
                return JSONResponse({"error": "unauthorized"}, status_code=401)
        return routes["chat"](body)

    @app.post("/v1/sessions")
    async def create_session(request: Request):
        body = await request.json()
        s = manager.create(body.get("session_id") or None)
        return {"session_id": s.id}

    @app.get("/v1/sessions")
    async def list_sessions():
        return {"sessions": manager.list_ids()}

    return app
