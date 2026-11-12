# -*- coding: utf-8 -*-
"""SGLang后端适配（OpenAI 兼容）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatProvider
from .registry import register


class SGLangProvider(OpenAICompatProvider):
    name = "sglang"
    default_base_url = "http://localhost:30000/v1"
    default_model = "Qwen/Qwen2.5-Coder-7B-Instruct"
    api_key_env = "SGLANG_API_KEY"


register(SGLangProvider)
