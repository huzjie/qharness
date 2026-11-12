# -*- coding: utf-8 -*-
"""HTTP 接入：把 HTTP POST 请求转成事件（配合 api 控制面使用）。"""
from __future__ import annotations

from .adapter import IngressAdapter


class HttpIngress(IngressAdapter):
    """HTTP 接入适配器（骨架，具体路由在 api/routes.py）。"""

    def serve(self, *args, **kwargs):
        return {"status": "ok", "ingress": "http"}
