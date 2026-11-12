# -*- coding: utf-8 -*-
"""会话管理器：创建/查找/回收会话，控制并发上限。"""
from __future__ import annotations

import threading
import uuid
from typing import Optional

from ..session.model import Session
from ..session.store import MemoryStore, SessionStore


class SessionManager:
    def __init__(self, store: Optional[SessionStore] = None, max_sessions: int = 64):
        self.store = store or MemoryStore()
        self.max_sessions = max_sessions
        self._lock = threading.RLock()

    def create(self, session_id: Optional[str] = None) -> Session:
        with self._lock:
            if len(self.store.list_ids()) >= self.max_sessions:
                raise RuntimeError(f"会话数已达上限 {self.max_sessions}")
            s = Session.new(session_id)
            self.store.put(s)
            return s

    def get(self, session_id: str) -> Optional[Session]:
        return self.store.get(session_id)

    def save(self, session: Session) -> None:
        self.store.put(session)

    def close(self, session_id: str) -> None:
        self.store.delete(session_id)

    def list_ids(self) -> list:
        return self.store.list_ids()
