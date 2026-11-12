# Contributing

欢迎贡献。流程：

1. Fork 本仓库，创建 feature 分支
2. 提交前运行 `make lint` 与 `make test`
3. 提交 PR，说明动机与改动点

内核原则：`qharness/qharness` 包的核心内核（events/bus/session/brain/hand/...）**保持零第三方运行时依赖**，仅依赖 Python 标准库，保证离线可跑、可复现。
