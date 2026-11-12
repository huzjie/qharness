# -*- coding: utf-8 -*-
"""会话检查点：保存与恢复。"""
from qharness.session import Session, Message, Role
from qharness.session.checkpoint import Checkpoint, save_checkpoint, load_checkpoint

s = Session.new("s1")
s.append(Message(Role.USER, "开始任务"))

cp = Checkpoint(session_id=s.id, turn_count=1, messages=[m.to_dict() for m in s.messages])
save_checkpoint(cp, "/tmp/qharness_cp.json")

cp2 = load_checkpoint("/tmp/qharness_cp.json")
print("恢复的轮数：", cp2.turn_count)
print("恢复的消息：", cp2.messages)
