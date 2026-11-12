# -*- coding: utf-8 -*-
"""OpenAI 兼容 HTTP 客户端（零第三方依赖，urllib 实现）。"""
from __future__ import annotations

import json
import urllib.request
from typing import Optional

from .base import Provider, ModelResponse, ToolCall


class OpenAICompatProvider(Provider):
    """OpenAI 兼容后端基类：子类只需配置 base_url / model / 认证头。"""

    name = "openai_compat"
    default_base_url = "https://api.openai.com/v1"
    default_model = "gpt-4o-mini"
    api_key_env = "OPENAI_API_KEY"
    auth_scheme = "Bearer"

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None,
                 model: Optional[str] = None, timeout: float = 60.0):
        import os
        self.api_key = api_key or os.environ.get(self.api_key_env, "")
        self.base_url = (base_url or self.default_base_url).rstrip("/")
        self.model = model or self.default_model
        self.timeout = timeout

    def _headers(self) -> dict:
        h = {"Content-Type": "application/json"}
        if self.api_key:
            h["Authorization"] = f"{self.auth_scheme} {self.api_key}"
        return h

    def chat(self, messages: list, tools: Optional[list] = None, **kw) -> ModelResponse:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": kw.get("temperature", 0.0),
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        req = urllib.request.Request(
            self.base_url + "/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers=self._headers(), method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            body = json.loads(r.read().decode("utf-8"))
        choice = body["choices"][0]
        msg = choice.get("message", {})
        tcs = [ToolCall.from_dict(t) for t in msg.get("tool_calls", [])]
        return ModelResponse(
            content=msg.get("content") or "",
            tool_calls=tcs,
            raw=body,
            finish_reason=choice.get("finish_reason", "stop"),
        )
