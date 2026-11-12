# -*- coding: utf-8 -*-
"""serve：启动 OpenAI 兼容控制面 + Web 控制台。"""
from __future__ import annotations


def serve(port: int = 8000, provider: str = "mock", model: str = None,
          workdir: str = ".", auth_token: str = None) -> int:
    from ..providers import get_provider
    from ..brain import AgentLoop
    from ..scheduler import SessionManager
    from ..api.app import create_app

    kw = {}
    if model:
        kw["model"] = model
    prov = get_provider(provider, **kw)
    loop = AgentLoop(provider=prov, workdir=workdir)
    manager = SessionManager()
    app = create_app(loop=loop, manager=manager, auth_token=auth_token)
    try:
        import uvicorn
    except ImportError:
        raise ImportError("启动控制面需要安装：pip install -e '.[api]'")
    print(f"qharness 控制面已启动：http://127.0.0.1:{port}  (provider={provider})")
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
    return 0
