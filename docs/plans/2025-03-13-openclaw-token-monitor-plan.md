# OpenClaw Token 用量监控 — 实现计划

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在本机通过解析 OpenClaw session JSONL 统计 token 与成本，用 Flask + Jinja2 + Bootstrap 提供本地服务与静态 HTML 导出。

**Architecture:** 独立 Python 包：scanner 读 `~/.openclaw/agents/<agentId>/sessions/*.jsonl` 产出原始记录，aggregator 按 agent/session 聚合，Flask 渲染 Jinja2 模板并支持 `/refresh` 与导出。

**Tech Stack:** Python 3, Flask, Jinja2, Bootstrap (CDN), pytest。

**设计文档:** `docs/plans/2025-03-13-openclaw-token-monitor-design.md`

---

## 文件结构

| 操作 | 路径 | 职责 |
|------|------|------|
| Create | `openclaw_token_monitor/__init__.py` | 空包 |
| Create | `openclaw_token_monitor/scanner.py` | 扫描 session 目录、解析 JSONL、产出原始 usage 记录 |
| Create | `openclaw_token_monitor/aggregator.py` | 按 agent_id、session_id 聚合，输出 by_agent / by_session / totals |
| Create | `openclaw_token_monitor/server.py` | Flask app：/、/refresh、/export，调用 scanner+aggregator+render |
| Create | `openclaw_token_monitor/templates/index.html.j2` | Jinja2 + Bootstrap 表格与排版 |
| Create | `openclaw_token_monitor/main.py` | CLI：serve \| export，可选 --openclaw-data-dir |
| Create | `openclaw_token_monitor/requirements.txt` | flask, jinja2 |
| Create | `tests/test_scanner.py` | scanner 单元测试 |
| Create | `tests/test_aggregator.py` | aggregator 单元测试 |
| Create | `tests/fixtures/sessions/` | mock .jsonl 用于测试 |

---

## Task 1: 项目骨架与依赖

**Files:**
- Create: `openclaw_token_monitor/__init__.py`
- Create: `openclaw_token_monitor/requirements.txt`

- [ ] **Step 1: 创建包与依赖**

在项目根（即 `openclaw_token_monitor` 的父目录）创建目录与文件。

`openclaw_token_monitor/__init__.py` 可为空或仅 `"""OpenClaw token usage monitor."""`。

`openclaw_token_monitor/requirements.txt` 内容：

```
flask>=3.0
jinja2>=3.1
```

- [ ] **Step 2: 提交**

```bash
git add openclaw_token_monitor/__init__.py openclaw_token_monitor/requirements.txt
git commit -m "chore: add openclaw_token_monitor package and requirements"
```

---

## Task 2: Scanner — 解析单行 JSONL 与 usage 提取

**Files:**
- Create: `tests/fixtures/sessions/agent_a/session_1.jsonl`
- Create: `tests/test_scanner.py`
- Create: `openclaw_token_monitor/scanner.py`

- [ ] **Step 1: 编写 fixture 与失败测试**

在 `tests/fixtures/sessions/agent_a/` 下创建 `session_1.jsonl`，至少一行包含 `message.usage` 或 `responseUsage` 的 JSON（字段含 input_tokens、output_tokens，可选 cost）。再写 `tests/test_scanner.py`：从该 fixture 目录扫描，断言返回记录数 ≥ 1，且单条记录含 `input_tokens`、`output_tokens`（及可选 `cost`）。

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_scanner.py -v`  
Expected: FAIL（无 scanner 或函数未实现）

- [ ] **Step 3: 实现 scanner 最小逻辑**

在 `openclaw_token_monitor/scanner.py` 中实现：  
- 函数 `ScanSessionDir(session_dir_path)` 或等价：遍历目录下 `.jsonl`（排除含 `.deleted.`），逐行读 JSON，若存在 `message.usage` 或 `responseUsage` 则提取 input_tokens、output_tokens、cost 等，返回 list of dict。  
- 支持通过参数传入数据根目录（默认 `~/.openclaw/agents`），遍历所有 `agents/<agentId>/sessions/`。

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_scanner.py -v`  
Expected: PASS

- [ ] **Step 5: 提交**

```bash
git add tests/fixtures/sessions/ tests/test_scanner.py openclaw_token_monitor/scanner.py
git commit -m "feat: add scanner to parse OpenClaw session JSONL for usage"
```

---

## Task 3: Aggregator — 按 agent / session 聚合

**Files:**
- Create: `tests/test_aggregator.py`
- Create: `openclaw_token_monitor/aggregator.py`

- [ ] **Step 1: 编写失败测试**

在 `tests/test_aggregator.py` 中：构造固定 scanner 风格的一条或多条记录（含 agent_id、session_id、input_tokens、output_tokens、cost），调用 aggregator，断言 `by_agent`、`by_session`、`totals` 结构与数值符合预期。

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_aggregator.py -v`  
Expected: FAIL

- [ ] **Step 3: 实现 aggregator**

在 `openclaw_token_monitor/aggregator.py` 中实现：输入为 scanner 产出的记录列表，输出 `by_agent`、`by_session`、`totals`（字段与设计文档一致），缺失 cost 用 None。

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_aggregator.py -v`  
Expected: PASS

- [ ] **Step 5: 提交**

```bash
git add tests/test_aggregator.py openclaw_token_monitor/aggregator.py
git commit -m "feat: add aggregator for token usage by agent and session"
```

---

## Task 4: Jinja2 模板与 Bootstrap 表格

**Files:**
- Create: `openclaw_token_monitor/templates/index.html.j2`

- [ ] **Step 1: 实现模板**

使用 Jinja2 接收 `by_agent`、`by_session`、`totals`。页面包含：Bootstrap 引入（CDN）、全局合计（totals）、按 agent 汇总表、按 session 明细表（可折叠或分表）。cost 为 None 时显示「—」。

- [ ] **Step 2: 提交**

```bash
git add openclaw_token_monitor/templates/index.html.j2
git commit -m "feat: add Jinja2+Bootstrap template for usage report"
```

---

## Task 5: Flask 服务与路由

**Files:**
- Create: `openclaw_token_monitor/server.py`
- Create: `openclaw_token_monitor/main.py`

- [ ] **Step 1: 实现 server.py**

Flask app：  
- `GET /`：执行扫描 → 聚合 → 渲染 index.html.j2，返回 HTML。  
- `GET /refresh` 或 `POST /refresh`：同上，可重定向回 `/` 或直接返回新 HTML。  
- `GET /export`：同上，返回 HTML 或触发下载（或由 main export 子命令写文件）。  
数据目录可通过环境变量或 Flask config 传入（与 scanner 一致）。

- [ ] **Step 2: 实现 main.py**

CLI（argparse 或 click）：  
- `serve`：启动 Flask（默认 host/port），可选 `--openclaw-data-dir`。  
- `export`：执行一次扫描+聚合+渲染，将 HTML 写入指定文件（如 `openclaw_usage.html`），可选 `--openclaw-data-dir`、`--output`。

- [ ] **Step 3: 手动验证**

启动 `python -m openclaw_token_monitor.main serve`，浏览器访问 `/` 与 `/refresh`；运行 `python -m openclaw_token_monitor.main export --output report.html`，打开 report.html 检查。

- [ ] **Step 4: 提交**

```bash
git add openclaw_token_monitor/server.py openclaw_token_monitor/main.py
git commit -m "feat: add Flask server and CLI serve/export"
```

---

## Task 6: 错误处理与边界

**Files:**
- Modify: `openclaw_token_monitor/scanner.py`
- Modify: `openclaw_token_monitor/server.py`

- [ ] **Step 1: 扫描错误处理**

数据目录不存在或不可读时抛出明确异常或 sys.exit(1) 并打印提示；单目录无权限时打 warning 并跳过；单行 JSON 解析失败时跳过该行并打日志。

- [ ] **Step 2: Flask 500 处理**

在 server 中注册全局异常处理，未捕获异常时返回 500 并记录 traceback（logging）。

- [ ] **Step 3: 提交**

```bash
git add openclaw_token_monitor/scanner.py openclaw_token_monitor/server.py
git commit -m "fix: scanner error handling and Flask 500 handler"
```

---

## 执行与验收

- 在项目根安装依赖：`pip install -r openclaw_token_monitor/requirements.txt`（或使用 venv）。
- 运行全部测试：`pytest tests/ -v`。
- 若本机存在 `~/.openclaw/agents/` 下 session，用 `serve` 与 `export` 做一次端到端验证。

Plan 已保存至 `docs/plans/2025-03-13-openclaw-token-monitor-plan.md`。需要开始按该计划执行实现吗？
