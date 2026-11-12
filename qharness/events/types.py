# -*- coding: utf-8 -*-
"""事件类型枚举：统一事件模型里，一切交互都映射到这些类型。"""
from __future__ import annotations


class EventType:
    """事件类型常量。用字符串（而非 enum）以保持总线/序列化的零依赖与可扩展性。"""

    # ---- 会话生命周期 ----
    SESSION_CREATED = "session_created"
    SESSION_CLOSED = "session_closed"

    # ---- 运行生命周期 ----
    RUN_STARTED = "run_started"
    RUN_COMPLETED = "run_completed"
    RUN_FAILED = "run_failed"

    # ---- 对话 ----
    USER_MESSAGE = "user_message"
    ASSISTANT_MESSAGE = "assistant_message"

    # ---- 手脑协作 ----
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    TOOL_ERROR = "tool_error"

    # ---- 系统 ----
    SYSTEM = "system"
    HEARTBEAT = "heartbeat"
    METRIC = "metric"

    # 所有可路由的业务类型
    ALL = frozenset({
        SESSION_CREATED, SESSION_CLOSED,
        RUN_STARTED, RUN_COMPLETED, RUN_FAILED,
        USER_MESSAGE, ASSISTANT_MESSAGE,
        TOOL_CALL, TOOL_RESULT, TOOL_ERROR,
        SYSTEM, HEARTBEAT, METRIC,
    })


def is_valid_type(t: str) -> bool:
    return t in EventType.ALL
