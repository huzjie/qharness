# Faq

# FAQ

**Q：mock 后端能干什么？**
验证编排链路、写单测、离线演示，不接真实模型也能跑通完整 Agent 循环。

**Q：如何新增一个工具？**
继承 `Tool`，实现 `run`，在模块里 `register`，放入 `tools/` 即可自动被发现。

**Q：如何新增一个 provider？**
继承 `OpenAICompatProvider`，设置 `base_url/default_model/api_key_env` 并 `register`。

**Q：手脑分离到底分什么？**
分「推理」和「执行」两个关注点，让它们独立部署、独立沙箱、独立扩容。

