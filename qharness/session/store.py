# -*- coding: utf-8 -*-
"""会话存储：内存 / 文件。"""
from __future__ import annotations

import json
import os
import threading
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from .model import Session


class SessionStore(ABC):
    @abstractmethod
    def get(self, session_id: str) -> Optional[Session]:
        ...

    @abstractmethod
    def put(self, session: Session) -> None:
        ...

    @abstractmethod
    def delete(self, session_id: str) -> None:
        ...

    @abstractmethod
    def list_ids(self) -> list:
        ...


class MemoryStore(SessionStore):
    def __init__(self):
        self._data: dict = {}
        self._lock = threading.RLock()

    def get(self, session_id: str) -> Optional[Session]:
        with self._lock:
            return self._data.get(session_id)

    def put(self, session: Session) -> None:
        with self._lock:
            self._data[session.id] = session

    def delete(self, session_id: str) -> None:
        with self._lock:
            self._data.pop(session_id, None)

    def list_ids(self) -> list:
        with self._lock:
            return list(self._data.keys())


class FileStore(SessionStore):
    """把会话持久化到磁盘（每会话一个 JSON 文件）。"""

    def __init__(self, root: str):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, session_id: str) -> Path:
        return self.root / f"{session_id}.json"

    def get(self, session_id: str) -> Optional[Session]:
        p = self._path(session_id)
        if not p.exists():
            return None
        with open(p, encoding="utf-8") as f:
            return Session.from_dict(json.load(f))

    def put(self, session: Session) -> None:
        with open(self._path(session.id), "w", encoding="utf-8") as f:
            json.dump(session.to_dict(), f, ensure_ascii=False)

    def delete(self, session_id: str) -> None:
        p = self._path(session_id)
        if p.exists():
            os.remove(p)

    def list_ids(self) -> list:
        return [p.stem for p in self.root.glob("*.json")]
