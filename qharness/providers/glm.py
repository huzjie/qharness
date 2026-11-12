# -*- coding: utf-8 -*-
"""智谱 GLM后端适配（OpenAI 兼容）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatProvider
from .registry import register


class GLMProvider(OpenAICompatProvider):
    name = "glm"
    default_base_url = "https://open.bigmodel.cn/api/paas/v4"
    default_model = "glm-4-plus"
    api_key_env = "ZHIPUAI_API_KEY"


register(GLMProvider)
