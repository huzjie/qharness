# -*- coding: utf-8 -*-
"""doctor：逐项诊断各子系统是否就绪。"""
from __future__ import annotations


def run_doctor() -> int:
    checks = []

    def _check(name, fn):
        try:
            ok, detail = fn()
            checks.append((name, ok, detail))
        except Exception as e:  # noqa
            checks.append((name, False, f"异常: {e}"))

    _check("events", lambda: _check_events())
    _check("bus", lambda: _check_bus())
    _check("session", lambda: _check_session())
    _check("providers", lambda: _check_providers())
    _check("tools", lambda: _check_tools())
    _check("hand", lambda: _check_hand())
    _check("brain", lambda: _check_brain())
    _check("scheduler", lambda: _check_scheduler())
    _check("dist", lambda: _check_dist())

    all_ok = True
    print("qharness doctor 自检结果：")
    print("-" * 44)
    for name, ok, detail in checks:
        mark = "OK " if ok else "ERR"
        all_ok = all_ok and ok
        print(f"  [{mark}] {name:<10} {detail}")
    print("-" * 44)
    print(f"  汇总：{sum(1 for _, o, _ in checks if o)}/{len(checks)} 通过")
    return 0 if all_ok else 1


def _check_events():
    from ..events import Event, EventType, EventFactory, encode_event, decode_event
    f = EventFactory("doctor")
    ev = f.user_message("s1", "hello")
    ev2 = decode_event(encode_event(ev))
    return ev2.type == EventType.USER_MESSAGE and ev2.session_id == "s1", "事件编解码往返一致"


def _check_bus():
    from ..bus import MemoryBus
    from ..events import Event, EventType
    b = MemoryBus()
    got = []
    b.subscribe(EventType.USER_MESSAGE, lambda e: got.append(e))
    b.publish(Event(EventType.USER_MESSAGE, "s1", {"content": "x"}))
    return len(got) == 1, "内存总线发布/订阅正常"


def _check_session():
    from ..session import Session, Message, Role
    s = Session.new("s1")
    s.append(Message(Role.USER, "hi"))
    s2 = Session.from_dict(s.to_dict())
    return s2.id == "s1" and len(s2.messages) == 1, "会话序列化往返一致"


def _check_providers():
    from ..providers import get_provider, list_providers
    p = get_provider("mock")
    r = p.chat([])
    return p.name == "mock" and r.has_tool_calls, f"provider 可用（{len(list_providers())} 个后端）"


def _check_tools():
    from ..tools.registry import ensure_loaded, all_tool_schemas, list_tools
    ensure_loaded()
    n = len(list_tools())
    return n >= 10, f"{n} 个内置工具已注册"


def _check_hand():
    from ..hand import execute_tool
    from ..tools.base import ToolContext
    r = execute_tool("python_eval", {"code": "1+2"}, ToolContext())
    return r.success and r.output.strip() == "3", "工具执行（手）正常"


def _check_brain():
    from ..brain import AgentLoop
    from ..session import Session
    loop = AgentLoop()
    res = loop.run(Session.new("s1"), "hello")
    return res.status.value in ("completed", "max_turns") and res.tool_calls > 0, \
        f"Agent 循环跑通（{res.tool_calls} 次工具调用）"


def _check_scheduler():
    from ..scheduler import SessionManager, PriorityQueue
    m = SessionManager()
    s = m.create("s1")
    q = PriorityQueue()
    q.push("s1", 0)
    return m.get("s1") is not None and len(q) == 1, "会话管理/优先级队列正常"


def _check_dist():
    from ..dist import ShardRouter, hash_shard
    r = ShardRouter(["n1", "n2", "n3"])
    a, b = r.route("x"), r.route("x")
    return a == b, "会话分片一致性哈希稳定"
