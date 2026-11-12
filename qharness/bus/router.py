# -*- coding: utf-8 -*-
"""Topic 路由：支持精确匹配与 '*' 通配匹配。"""
from __future__ import annotations


def match_topic(pattern: str, topic: str) -> bool:
    """判断 topic 是否匹配 pattern。pattern 中 '*' 匹配任意一段（不含 '.'）。"""
    if pattern == "*":
        return True
    p = pattern.split(".")
    t = topic.split(".")
    if len(p) != len(t):
        return False
    for a, b in zip(p, t):
        if a == "*" or a == b:
            continue
        return False
    return True


class TopicRouter:
    """把事件路由到若干订阅者的简单路由器。"""

    def __init__(self):
        self._routes: dict = {}

    def add(self, topic: str, target) -> None:
        self._routes[topic] = target

    def remove(self, topic: str) -> None:
        self._routes.pop(topic, None)

    def route(self, topic: str):
        """返回精确命中或通配命中的目标列表。"""
        hits = []
        for pattern, target in self._routes.items():
            if match_topic(pattern, topic):
                hits.append(target)
        return hits
