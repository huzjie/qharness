# -*- coding: utf-8 -*-
"""Python 客户端：通过 OpenAI 兼容 HTTP 调用 qharness 控制面。"""
from __future__ import annotations

import json
import urllib.request
from typing import Optional


class QHarnessClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000", token: Optional[str] = None,
                 model: str = "qharness", timeout: float = 120.0):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.model = model
        self.timeout = timeout

    def _headers(self) -> dict:
        h = {"Content-Type": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def chat(self, prompt: str, session_id: Optional[str] = None, strategy: str = "react") -> dict:
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt,
                          "meta": {"session_id": session_id} if session_id else {}}],
            "strategy": strategy,
        }
        req = urllib.request.Request(self.base_url + "/v1/chat/completions",
                                     data=json.dumps(payload).encode("utf-8"),
                                     headers=self._headers(), method="POST")
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            return json.loads(r.read().decode("utf-8"))

    def create_session(self, session_id: Optional[str] = None) -> str:
        payload = {"session_id": session_id or ""}
        req = urllib.request.Request(self.base_url + "/v1/sessions",
                                     data=json.dumps(payload).encode("utf-8"),
                                     headers=self._headers(), method="POST")
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))["session_id"]

    def health(self) -> dict:
        with urllib.request.urlopen(self.base_url + "/health", timeout=10) as r:
            return json.loads(r.read().decode("utf-8"))
