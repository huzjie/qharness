# -*- coding: utf-8 -*-
"""Moonshot Kimi后端适配（OpenAI 兼容）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatProvider
from .registry import register


class KimiProvider(OpenAICompatProvider):
    name = "kimi"
    default_base_url = "https://api.moonshot.cn/v1"
    default_model = "moonshot-v1-128k"
    api_key_env = "MOONSHOT_API_KEY"


register(KimiProvider)
