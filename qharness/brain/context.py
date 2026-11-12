# -*- coding: utf-8 -*-
"""上下文窗口管理：超长历史截断/压缩。"""
from __future__ import annotations


class ContextManager:
    """上下文管理器：控制喂给模型的消息数量，超限时压缩。"""

    def __init__(self, max_messages: int = 200, context_window: int = 8192, auto_compact: bool = True):
        self.max_messages = max_messages
        self.context_window = context_window
        self.auto_compact = auto_compact

    def fit(self, messages: list) -> list:
        """返回适合当前窗口的消息列表。"""
        if len(messages) <= self.max_messages:
            return messages
        # 保留首条 system + 最近 (max_messages - 1) 条
        head = [messages[0]] if messages and messages[0].get("role") == "system" else []
        return head + messages[-(self.max_messages - len(head)):]

    def compact(self, messages: list) -> list:
        """压缩：把中间的对话折叠为一条摘要。"""
        if len(messages) <= self.max_messages:
            return messages
        system = [m for m in messages if m.get("role") == "system"]
        rest = [m for m in messages if m.get("role") != "system"]
        keep_tail = rest[-self.max_messages // 2:]
        summary = {"role": "assistant",
                   "content": f"[上下文压缩] 已折叠此前 {len(rest) - len(keep_tail)} 条消息的关键信息。"}
        return system + [summary] + keep_tail
