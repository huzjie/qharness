# -*- coding: utf-8 -*-
"""Provider 注册表与工厂。"""
from __future__ import annotations

from typing import Optional

from .base import Provider

_REGISTRY: dict = {}


_BUILTIN = ["mock", "qwen", "openai", "deepseek", "glm", "kimi", "ollama", "vllm", "sglang", "anthropic", "mistral"]


def register(provider_cls) -> None:
    _REGISTRY[provider_cls.name] = provider_cls


def _ensure_loaded() -> None:
    """惰性导入全部内置后端（触发各自 register）。"""
    import importlib
    for name in _BUILTIN:
        try:
            importlib.import_module(f"qharness.providers.{name}")
        except Exception:
            continue


def list_providers() -> list:
    _ensure_loaded()
    return sorted(_REGISTRY.keys())


def get_provider(name: str, **kw) -> Provider:
    """按名称构造 Provider。mock 为默认离线后端。"""
    if name not in _REGISTRY:
        import importlib
        try:
            importlib.import_module(f"qharness.providers.{name}")
        except ImportError:
            raise ValueError(f"未知 provider: {name}（可用：{list_providers()}）")
    if name not in _REGISTRY:
        raise ValueError(f"未知 provider: {name}（可用：{list_providers()}）")
    cls = _REGISTRY[name]
    if isinstance(cls, type):
        return cls(**kw)
    return cls
