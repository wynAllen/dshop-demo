# OpenClaw Token 用量监控

解析本机 OpenClaw session JSONL，按 agent / session 统计 token 与成本，通过 Flask + Bootstrap 提供本地查看与静态导出。

## 依赖

```bash
pip install -r openclaw_token_monitor/requirements.txt
```

## 使用

- **本地服务**（默认 http://127.0.0.1:5050）  
  `python3 -m openclaw_token_monitor.main serve`  
  可选：`--openclaw-data-dir <path>`、`--port <port>`

- **导出静态 HTML**  
  `python3 -m openclaw_token_monitor.main export --output report.html`  
  可选：`--openclaw-data-dir <path>`

- 数据目录默认：`~/.openclaw/agents`，也可设置环境变量 `OPENCLAW_AGENTS_ROOT`。

## 测试

在项目根（myIdear）执行：

```bash
pytest tests/ -v
```
