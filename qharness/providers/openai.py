# -*- coding: utf-8 -*-
"""OpenAI后端适配（OpenAI 兼容）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatProvider
from .registry import register


class OpenAIProvider(OpenAICompatProvider):
    name = "openai"
    default_base_url = "https://api.openai.com/v1"
    default_model = "gpt-4o-mini"
    api_key_env = "OPENAI_API_KEY"


register(OpenAIProvider)
