# qharness · 可嵌入的编码智能体运行时

> 一个**可嵌入自家产品的 Coding Agent 运行时**——把「LLM 推理编排」和「工具执行」彻底解耦，
> 用一条**统一事件总线**串起接入、调度、执行三层，先在一个进程里跑通多会话，再平滑演进到多节点分布式。
> 以 2026-11-11 阿里开源的 **Qwen Code 1.0**（Qoder 与 Qwen Code Harness 融合，提供可嵌入产品的 Agent 运行基础）为技术蓝本，
> 把它的核心架构思想工程化成一个**零依赖、可离线运行、可复现**的参考实现。

---

## 这是什么

qharness 不是一个「模型」，也不是一个「示例脚本」，而是一套**面向编码智能体的运行时框架**。它的核心主张只有一句话：

> **一切交互都是事件，一切组件都通过事件总线通信，脑（推理）与手（执行）分离。**

这句话带来三个直接好处，也是 Qwen Code 1.0 架构设计的精华：

| 设计点 | 解决什么问题 | 落地模块 |
|---|---|---|
| **统一事件模型** | 用户输入、模型输出、工具调用、工具结果、会话生命周期……全部抽象成同一种 `Event`，接口统一 | `events/` |
| **事件总线** | 组件间零耦合通信；进程内用内存总线，多节点时换成分布式总线，业务代码一行不改 | `bus/` |
| **手脑分离** | 推理编排（脑）与工具执行（手）拆开，各自独立扩容、独立沙箱、独立权限 | `brain/` + `hand/` |
| **接入/调度/执行分层** | 协议适配、会话路由、资源隔离各管各的，横向扩展不互相拖累 | `ingress/` + `scheduler/` + `executor/` |
| **单进程 → 多节点演进** | 事件模型不变，只换总线实现，就能从「一个进程多个会话」走到「多个节点更多会话」 | `bus/` + `dist/` |

---

## 为什么值得看（技术原理速览）

**1. 为什么「统一事件模型」是分布式演进的地基？**

自回归式智能体最容易写成「模型对象直接调用工具对象」的强耦合代码——这种写法跑单机没问题，但一旦要拆节点，就得重写调用关系。
qharness 反过来：`brain` 从不直接调用 `hand`，它只往总线发一个 `tool_call` 事件；`hand` 订阅这个事件，执行完再发一个 `tool_result` 事件回去。
**业务逻辑只认识事件，不认识组件**——所以进程内换内存总线、多节点换 socket/redis 总线，`brain` 和 `hand` 的代码零改动。这就是「统一事件模型」把单机架构和分布式架构统一起来的原理。

**2. 为什么「手脑分离」能降风险、能独立扩容？**

推理编排（脑）是低并发、高延迟、吃显存的重活；工具执行（手）是高并发、要隔离、要限资源的杂活。两者混在一个进程里，一个恶意的 `rm -rf` 就能拖垮整个模型服务。
qharness 让「手」跑在独立沙箱、独立进程里，带超时、资源上限和命令白名单；「脑」只管推理。两者靠事件异步通信，于是可以：
脑部署在 GPU 节点、手部署在 CPU 沙箱节点，互不影响，各自独立扩容。

**3. 为什么「分层」是横向扩展的关键？**

`ingress`（接入层）只做协议翻译（OpenAI 兼容 HTTP / WebSocket / Webhook），把外部请求规整成事件；
`scheduler`（调度层）做会话路由、优先级、并发与背压，决定一个事件去哪、谁先跑；
`executor`（执行层）做进程池与资源限制，决定一个任务在什么隔离环境里跑。
三层各司其职，扩容时只需要 scale 对应层，不必动其它层。

---

## 快速开始

```bash
git clone https://github.com/huzjie/qharness.git
cd qharness
pip install -e .            # 零第三方依赖即可跑内核；[api] 安装 FastAPI 控制面

qharness doctor             # 自检：事件模型/总线/脑/手/会话/调度逐项诊断
qharness run "创建一个 Flask TODO 应用，含增删改查接口" --provider mock   # 离线跑通完整 Agent 循环
qharness serve --port 8000  # OpenAI 兼容 HTTP + Web 控制台
```

接真实后端（示例接 Qwen / OpenAI 兼容 API）：

```bash
export QH_PROVIDER=qwen QH_API_KEY=<your-key> QH_MODEL=qwen-max
qharness run "为这个仓库写单测并修复失败的用例" --workdir ./my-repo
```

---

## 仓库结构（240+ 文件）

```
qharness/
├── qharness/               # 核心包（纯标准库内核 + 可选 FastAPI 控制面）
│   ├── events/             # 统一事件模型：Event / EventType / codec / 逻辑时钟
│   ├── bus/                # 事件总线：内存总线 / 分布式总线 / 路由 / 背压
│   ├── session/            # 会话：模型 / 存储 / 检查点断点续跑
│   ├── brain/              # 推理编排（脑）：Agent 循环 / 规划 / 工具选择 / 上下文
│   ├── hand/               # 工具执行（手）：注册表 / 执行器 / 沙箱 / 结果
│   ├── ingress/            # 接入层：OpenAI 兼容 HTTP / WebSocket / Webhook
│   ├── scheduler/          # 调度层：会话管理 / 优先级队列 / 调度策略
│   ├── executor/           # 执行层：进程池 / 资源限制
│   ├── dist/               # 分布式：节点 / 集群 / 会话分片 / 服务发现
│   ├── providers/          # LLM 后端：mock/qwen/openai/deepseek/glm/kimi/ollama/vllm/...
│   ├── tools/              # 内置工具：read/write/search/shell/patch/git/web/python/...
│   ├── security/           # 安全：权限 / 密钥脱敏 / 命令白名单
│   ├── api/                # FastAPI 控制面（OpenAI 兼容）
│   ├── cli/                # doctor / run / serve / agent / bench
│   ├── sdk/                # Python 客户端
│   ├── web/                # Web 控制台
│   └── observability/      # 观测：metrics / tracing / audit
├── sdk/typescript/         # TypeScript 客户端
├── deploy/                 # k8s · Helm（脑/手分离部署拓扑）
├── docs/                   # 40+ 篇技术文档
├── prompts/                # 提示词模板（系统/规划/工具选择/评审）
├── recipes/                # 配方（ReAct / Plan-Execute / 自愈 / 验收）
├── examples/               # 可运行示例
├── scripts/                # 运维脚本
├── benchmarks/             # 基准
├── tests/                  # 单测（纯标准库 unittest）
├── .github/workflows/      # CI / Release / CodeQL
├── Dockerfile              # 多阶段构建（脑/手两镜像）
└── config.example.yaml     # 全量配置模板
```

---

## 许可证

MIT License。参见 [LICENSE](LICENSE)。

> 说明：本项目为**独立开源实现**，与阿里（通义）无隶属关系；`qwen` provider 仅为对接其公开 API 的适配器。
