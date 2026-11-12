# -*- coding: utf-8 -*-
"""Mistral后端适配（OpenAI 兼容）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatProvider
from .registry import register


class MistralProvider(OpenAICompatProvider):
    name = "mistral"
    default_base_url = "https://api.mistral.ai/v1"
    default_model = "mistral-large-latest"
    api_key_env = "MISTRAL_API_KEY"


register(MistralProvider)
