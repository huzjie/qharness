# -*- coding: utf-8 -*-
"""规划器：决定 Agent 循环的执行策略（ReAct / Plan-Execute / Reflect）。"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Plan:
    goal: str
    steps: list = field(default_factory=list)
    meta: dict = field(default_factory=dict)

    def __len__(self):
        return len(self.steps)


class Planner(ABC):
    name = "planner"

    @abstractmethod
    def plan(self, task: str, messages: list) -> Plan:
        ...

    def system_prompt(self) -> str:
        return ""


class ReactPlanner(Planner):
    """ReAct：思考-行动-观察 循环，不预先拆解步骤。"""

    name = "react"

    def plan(self, task: str, messages: list) -> Plan:
        return Plan(goal=task)

    def system_prompt(self) -> str:
        return ("你是编码智能体。按「思考 -> 工具调用 -> 观察结果」循环推进任务，"
                "必要时调用工具，最终给出结论。")


class PlanExecutePlanner(Planner):
    """Plan-Execute：先把任务拆成步骤，再逐步执行。"""

    name = "plan_execute"

    def plan(self, task: str, messages: list) -> Plan:
        # 确定性拆解：按换行/分号/序号拆出子步骤
        import re
        parts = re.split(r"[\n;。]", task)
        steps = [p.strip() for p in parts if p.strip()]
        if not steps:
            steps = [task]
        return Plan(goal=task, steps=steps)

    def system_prompt(self) -> str:
        return ("你是编码智能体。先把任务拆解成可执行步骤，再逐步调用工具完成，"
                "每步完成后复盘，最后汇总。")


class ReflectPlanner(Planner):
    """Reflect：完成后再做一轮自我反思，输出改进建议。"""

    name = "reflect"

    def plan(self, task: str, messages: list) -> Plan:
        return Plan(goal=task, steps=["执行", "反思", "汇总"])

    def system_prompt(self) -> str:
        return ("你是编码智能体。完成任务的每个阶段后都要反思：结果是否达到目标、"
                "有无遗漏，再进入下一阶段。")


_PLANNERS = {ReactPlanner.name: ReactPlanner, PlanExecutePlanner.name: PlanExecutePlanner,
             ReflectPlanner.name: ReflectPlanner}


def get_planner(name: str) -> Planner:
    cls = _PLANNERS.get(name)
    if cls is None:
        raise ValueError(f"未知策略：{name}（可用：{list(_PLANNERS)}）")
    return cls()
