# -*- coding: utf-8 -*-
"""vLLM后端适配（OpenAI 兼容）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatProvider
from .registry import register


class VLLMProvider(OpenAICompatProvider):
    name = "vllm"
    default_base_url = "http://localhost:8000/v1"
    default_model = "Qwen/Qwen2.5-Coder-7B-Instruct"
    api_key_env = "VLLM_API_KEY"


register(VLLMProvider)
