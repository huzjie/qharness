# -*- coding: utf-8 -*-
"""把文件存储的会话导出为 JSONL。"""
import json
import sys
from qharness.session.store import FileStore

root = sys.argv[1] if len(sys.argv) > 1 else "./data/sessions"
store = FileStore(root)
for sid in store.list_ids():
    s = store.get(sid)
    print(json.dumps(s.to_dict(), ensure_ascii=False))
