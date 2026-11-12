# -*- coding: utf-8 -*-
"""工具注册表。"""
from __future__ import annotations

from typing import Optional

from .base import Tool

_REGISTRY: dict = {}


def register(tool_cls) -> None:
    # 统一存实例（类则先实例化），保证 run() 以绑定方法调用
    if isinstance(tool_cls, type):
        _REGISTRY[tool_cls.name] = tool_cls()
    else:
        _REGISTRY[tool_cls.name] = tool_cls


def list_tools() -> list:
    return sorted(_REGISTRY.keys())


def get_tool(name: str) -> Optional[Tool]:
    return _REGISTRY.get(name)


def all_tool_schemas() -> list:
    return [t.schema() for _, t in sorted(_REGISTRY.items())]


def _load_builtin() -> None:
    """惰性加载全部内置工具（按需 import 各模块触发 register）。"""
    import importlib
    for mod in ("files", "search", "shell", "patch", "git", "web", "python", "note"):
        importlib.import_module(f"qharness.tools.{mod}")


def ensure_loaded() -> None:
    if not _REGISTRY:
        _load_builtin()
