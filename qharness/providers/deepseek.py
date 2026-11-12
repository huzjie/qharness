# -*- coding: utf-8 -*-
"""DeepSeek后端适配（OpenAI 兼容）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatProvider
from .registry import register


class DeepSeekProvider(OpenAICompatProvider):
    name = "deepseek"
    default_base_url = "https://api.deepseek.com/v1"
    default_model = "deepseek-chat"
    api_key_env = "DEEPSEEK_API_KEY"


register(DeepSeekProvider)
