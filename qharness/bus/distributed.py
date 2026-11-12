# -*- coding: utf-8 -*-
"""分布式总线：同一套 Bus 接口，底层走 TCP socket（零第三方依赖）。

说明：真实生产可替换为 Redis pub/sub / Kafka / NATS，这里用标准库 socket
演示「事件模型不变、只换总线实现」这一核心思想。多节点场景下，
每个节点运行一个 SocketBus，节点间把事件转发到订阅的远端节点。
"""
from __future__ import annotations

import json
import socket
import socketserver
import threading
from typing import Callable, Optional

from ..events.codec import encode_event, decode_event
from ..events.event import Event
from .base import Bus, Handler, Subscription
from .memory import MemoryBus


class SocketBus(Bus):
    """基于 TCP socket 的分布式总线（含本地内存总线作为同节点分发）。"""

    def __init__(self, address: str = "127.0.0.1:0", peers: Optional[list] = None):
        host, _, port = address.rpartition(":")
        self.host = host or "127.0.0.1"
        self.port = int(port or 0)
        self.peers = peers or []
        self._local = MemoryBus()
        self._server: Optional[_BusServer] = None
        self._thread: Optional[threading.Thread] = None

    def start(self):
        self._server = _BusServer((self.host, self.port), self)
        self.port = self._server.server_address[1]
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        return self

    def subscribe(self, topic: str, handler: Handler) -> Subscription:
        return self._local.subscribe(topic, handler)

    def unsubscribe(self, sub: Subscription) -> None:
        self._local.unsubscribe(sub)

    def publish(self, event: Event) -> int:
        fired = self._local.publish(event)
        # 转发给所有远端 peer（尽力而为）
        for peer in self.peers:
            try:
                self._send(peer, event)
            except Exception:
                continue
        return fired

    def _receive(self, event: Event) -> None:
        self._local.publish(event)

    @staticmethod
    def _send(peer: str, event: Event) -> None:
        host, _, port = peer.rpartition(":")
        with socket.create_connection((host, int(port)), timeout=2) as s:
            s.sendall((encode_event(event) + "\n").encode("utf-8"))

    def close(self) -> None:
        if self._server:
            self._server.shutdown()
        self._local.close()


class _BusServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(self, addr, bus: SocketBus):
        super().__init__(addr, _BusHandler)
        self.bus = bus


class _BusHandler(socketserver.StreamRequestHandler):
    def handle(self):
        bus: SocketBus = self.server.bus
        for line in self.rfile:
            line = line.decode("utf-8").strip()
            if not line:
                continue
            try:
                bus._receive(decode_event(line))
            except Exception:
                continue


def build_bus(backend: str = "memory", address: Optional[str] = None, peers: Optional[list] = None) -> Bus:
    """按配置构造总线。"""
    if backend == "socket":
        return SocketBus(address or "127.0.0.1:0", peers or []).start()
    return MemoryBus()
