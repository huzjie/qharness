# -*- coding: utf-8 -*-
"""OpenAI 兼容客户端：调用本地控制面（需先 `qharness serve`）。"""
from qharness.sdk import QHarnessClient

client = QHarnessClient("http://127.0.0.1:8000")
print(client.health())
resp = client.chat("运行一个编码任务")
print(resp["choices"][0]["message"]["content"])
