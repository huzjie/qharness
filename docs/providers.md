# Providers

# Provider 后端

统一 `Provider.chat(messages, tools) -> ModelResponse`，其中 `ModelResponse` 要么是文本、要么是工具调用。

内置 12 个后端：`mock / qwen / openai / deepseek / glm / kimi / ollama / vllm / sglang / anthropic / mistral`。

## 工程技巧

用 `OpenAICompatProvider` 基类把差异收敛到三个字段：`base_url` / `default_model` / `api_key_env`。新增后端只需一个 5 行的子类。

