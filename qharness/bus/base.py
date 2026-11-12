# -*- coding: utf-8 -*-
"""Bus 抽象接口：业务组件（brain/hand/ingress/...）只依赖这个接口。"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, List

from ..events.event import Event

Handler = Callable[[Event], None]


class Subscription:
    """订阅句柄：可用于退订。"""

    def __init__(self, topic: str, handler: Handler):
        self.topic = topic
        self.handler = handler
        self.active = True


class Bus(ABC):
    """事件总线抽象。

    关键设计：publish/subscribe 是唯一通信原语。进程内用 MemoryBus，
    多节点用 SocketBus，二者接口一致，业务代码零改动。
    """

    @abstractmethod
    def subscribe(self, topic: str, handler: Handler) -> Subscription:
        """订阅某个 topic（支持通配，见 TopicRouter.match_topic）。"""

    @abstractmethod
    def unsubscribe(self, sub: Subscription) -> None:
        """退订。"""

    @abstractmethod
    def publish(self, event: Event) -> int:
        """发布事件，返回实际触发的处理器数量。"""

    @abstractmethod
    def close(self) -> None:
        """关闭总线、释放资源。"""

    def publish_many(self, events: List[Event]) -> int:
        total = 0
        for e in events:
            total += self.publish(e)
        return total
