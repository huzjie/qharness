# -*- coding: utf-8 -*-
"""命令行入口：qharness [doctor|run|serve|agent|bench]。"""
from __future__ import annotations

import argparse
import sys


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="qharness", description="可嵌入的编码智能体运行时")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("doctor", help="逐项自检各子系统")

    r = sub.add_parser("run", help="运行一个编码任务")
    r.add_argument("prompt")
    r.add_argument("--provider", default="mock")
    r.add_argument("--model", default=None)
    r.add_argument("--workdir", default=".")
    r.add_argument("--strategy", default="react")
    r.add_argument("--max-turns", type=int, default=40)

    s = sub.add_parser("serve", help="启动 OpenAI 兼容控制面")
    s.add_argument("--port", type=int, default=8000)
    s.add_argument("--provider", default="mock")
    s.add_argument("--model", default=None)
    s.add_argument("--workdir", default=".")
    s.add_argument("--auth-token", default=None)

    args = p.parse_args(argv)

    if args.cmd == "doctor":
        from .doctor import run_doctor
        return run_doctor()
    if args.cmd == "run":
        from .run import run_task
        return run_task(args.prompt, args.provider, args.model, args.workdir, args.strategy, args.max_turns)
    if args.cmd == "serve":
        from .serve import serve
        return serve(args.port, args.provider, args.model, args.workdir, args.auth_token)
    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
