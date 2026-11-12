# Getting Started

# 快速上手

```bash
pip install -e .
qharness doctor
qharness run "创建 TODO 应用" --provider mock
qharness serve --port 8000
```

接真实后端：

```bash
export QH_PROVIDER=qwen QH_API_KEY=xxx QH_MODEL=qwen-max
qharness run "为仓库写单测" --workdir ./repo
```

