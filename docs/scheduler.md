# Scheduler

# 调度层

- `SessionManager`：会话生命周期 + 并发上限。
- `PriorityQueue`：堆实现，数字越小越优先。
- `SchedulingPolicy`：FIFO / Priority / Fair（按排队次数加权防饥饿）。

## 可复用要点

优先级队列的稳定排序用「(priority, seq)」元组，seq 单调递增保证同优先级 FIFO。

