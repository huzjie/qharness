# @qharness/sdk

qharness 编码智能体运行时的 TypeScript 客户端。

## 使用

```ts
import { QHarnessClient } from "@qharness/sdk";

const client = new QHarnessClient("http://127.0.0.1:8000");
const resp = await client.chat("创建一个 TODO 应用");
console.log(resp.choices[0].message.content);
```

## 构建

```bash
npm install
npm run build
```
