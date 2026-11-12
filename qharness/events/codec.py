# -*- coding: utf-8 -*-
"""事件编解码：Event <-> 可传输/可存储的字节/字典。零第三方依赖（JSON）。"""
from __future__ import annotations

import json
from typing import Any

from .event import Event


def encode_event(ev: Event) -> str:
    """把事件编码为 JSON 字符串。"""
    return json.dumps(ev.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def decode_event(raw: str) -> Event:
    """把 JSON 字符串解码回事件。"""
    d = json.loads(raw)
    return Event.from_dict(d)


def encode_events(events: list) -> str:
    return json.dumps([e.to_dict() for e in events], ensure_ascii=False, sort_keys=True)


def decode_events(raw: str) -> list:
    return [Event.from_dict(d) for d in json.loads(raw)]


def payload_to_json(payload: Any) -> str:
    """把任意 payload 序列化为 JSON（供日志/审计）。"""
    try:
        return json.dumps(payload, ensure_ascii=False, default=str)
    except Exception:
        return repr(payload)
