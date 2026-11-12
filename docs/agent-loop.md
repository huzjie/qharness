# Agent Loop

# Agent 循环

```
messages.append(user)
for _ in range(max_turns):
    resp = provider.chat(messages, tools)
    if resp.has_tool_calls:
        for tc in resp.tool_calls:
            result = execute_tool(tc)
            messages.append(assistant(tool_calls))
            messages.append(tool(result))
        continue
    return resp.content
```

## 关键参数

- `max_turns`：防止无限循环（恶意/失控的工具调用）。
- `temperature`：编码任务建议 0.0（确定性、可复现）。
- 每轮都回传完整工具结果，模型才能基于结果继续推理。

