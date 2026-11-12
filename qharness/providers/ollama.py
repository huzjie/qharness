# -*- coding: utf-8 -*-
"""Ollama 本地后端适配（OpenAI 兼容）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatProvider
from .registry import register


class OllamaProvider(OpenAICompatProvider):
    name = "ollama"
    default_base_url = "http://localhost:11434/v1"
    default_model = "qwen2.5-coder:7b"
    api_key_env = "OLLAMA_API_KEY"


register(OllamaProvider)
