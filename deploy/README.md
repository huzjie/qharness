# 部署

qharness 的「手脑分离」拓扑：

- **brain（脑）**：承载推理编排，低并发、高延迟、吃显存，可部署在 GPU 节点，副本数少。
- **hand（手）**：承载工具执行，高并发、要隔离、限资源，部署在 CPU 沙箱节点，副本数多。

## Kubernetes

```bash
kubectl apply -f deploy/k8s/namespace.yaml
kubectl apply -f deploy/k8s/
```

## Helm

```bash
helm install qharness deploy/helm/qharness --set config.provider=qwen --set config.model=qwen-max
```

## Docker

```bash
docker build -t qharness:latest .
docker run -p 8000:8000 qharness:latest serve --port 8000
```
