# -*- coding: utf-8 -*-
"""通义千问 Qwen后端适配（OpenAI 兼容）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatProvider
from .registry import register


class QwenProvider(OpenAICompatProvider):
    name = "qwen"
    default_base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    default_model = "qwen-max"
    api_key_env = "DASHSCOPE_API_KEY"


register(QwenProvider)
