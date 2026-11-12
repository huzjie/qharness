# -*- coding: utf-8 -*-
"""Anthropic Claude后端适配（OpenAI 兼容）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatProvider
from .registry import register


class AnthropicProvider(OpenAICompatProvider):
    name = "anthropic"
    default_base_url = "https://api.anthropic.com/v1"
    default_model = "claude-3-5-sonnet-latest"
    api_key_env = "ANTHROPIC_API_KEY"


register(AnthropicProvider)
