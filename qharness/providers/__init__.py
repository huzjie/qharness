# -*- coding: utf-8 -*-
"""LLM Provider 后端。默认 mock（离线零依赖），可接 qwen/openai/deepseek/glm/kimi/ollama/vllm/sglang/anthropic/mistral。"""
from __future__ import annotations

from .base import Provider, ModelResponse, ToolCall
from .registry import get_provider, register, list_providers

__all__ = ["Provider", "ModelResponse", "ToolCall", "get_provider", "register", "list_providers"]
