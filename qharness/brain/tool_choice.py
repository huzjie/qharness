# -*- coding: utf-8 -*-
"""工具选择：从候选工具里挑最合适的（路由打分）。"""
from __future__ import annotations

import re


class ToolChooser:
    """基于关键词的工具选择器（真实场景由模型决定，这里提供确定性启发式）。"""

    _KEYWORDS = {
        "read_file": ["读", "read", "查看文件", "看文件", "阅读"],
        "write_file": ["写", "write", "创建文件", "生成文件", "新建"],
        "list_files": ["列出", "list", "目录", "文件列表"],
        "grep": ["搜索", "grep", "查找", "检索"],
        "run_bash": ["执行", "运行", "命令", "bash", "shell", "测试", "安装"],
        "git_status": ["状态", "status"],
        "git_diff": ["差异", "diff"],
        "web_fetch": ["网页", "抓取", "url", "http"],
        "python_eval": ["计算", "求值", "eval"],
    }

    def choose(self, task: str, candidates: list) -> str:
        """返回最匹配的工具名（无匹配返回空字符串）。"""
        best, best_score = "", 0
        low = task.lower()
        for name in candidates:
            score = 0
            for kw in self._KEYWORDS.get(name, []):
                if kw.lower() in low:
                    score += 1
            if score > best_score:
                best, best_score = name, score
        return best
