# OpenClaw Token 用量监控工具 — 设计文档

**日期**: 2025-03-13

## 1. 目标与范围

- **目标**：监控本机 OpenClaw 调用大模型的 token 用量，按会话 / agent 区分，支持多 agent、多会话场景。
- **形态**：独立 Python 项目（Python + HTML），双入口 — 本地 Flask 服务实时查看 + 一键导出静态 HTML 报告。
- **数据来源**：仅解析 OpenClaw 本地 session 文件（不依赖 CLI），路径默认 `~/.openclaw/agents/<agentId>/sessions/*.jsonl`，可通过配置或 CLI 覆盖。

## 2. 技术选型

| 项 | 选型 |
|----|------|
| 服务端 | Flask，路由清晰 |
| 模板 | Jinja2 |
| 前端 | HTML + CSS + Bootstrap，表格与简单 UI 设计排版 |

## 3. 架构与模块

**建议项目目录**：`openclaw_token_monitor/`（可放在 myIdear 下）

| 文件/目录 | 职责 |
|-----------|------|
| `main.py` | 双入口：`serve` / `export`，解析 CLI 并调用对应逻辑 |
| `scanner.py` | 扫描 session 目录，解析 JSONL，提取 usage/cost 等原始记录 |
| `aggregator.py` | 按 agent、session 聚合 token 与成本，输出三层结构 |
| `templates/index.html.j2` | Jinja2 模板：Bootstrap 表格展示按 agent / 按 session 及合计 |
| `server.py` | Flask 应用：`/` 展示页、`/refresh` 重新扫描并刷新、`/export` 导出静态 HTML |
| `requirements.txt` | `flask`、`jinja2` |

## 4. 数据流与字段约定

**数据流**

1. **扫描**：scanner 遍历 `~/.openclaw/agents/<agentId>/sessions/*.jsonl`（跳过 `.deleted.`），逐行解析 JSON，只处理含 `message.usage` 或 `responseUsage` 的行，产出原始记录列表。
2. **聚合**：aggregator 按 `agent_id`、`session_id` 分组，汇总 input_tokens、output_tokens、cache_read/write（若有）、cost（若有），得到「按 agent」「按 session」「全局总计」。
3. **展示/导出**：上述结构传入 Jinja2，Bootstrap 渲染；Flask `/`、`/refresh` 共用「扫描 → 聚合 → 渲染」；`export` 子命令将渲染结果写入静态 HTML。

**聚合后传给模板的结构**

- `by_agent`: `[{ "agent_id", "session_count", "total_input", "total_output", "total_cost" }]`
- `by_session`: `[{ "agent_id", "session_id", "total_input", "total_output", "total_cost", "last_activity" }]`
- `totals`: `{ "total_input", "total_output", "total_cost" }`

**从 JSONL 读取的字段（与 OpenClaw 对齐）**  
`input_tokens`、`output_tokens`，以及若有：`cache_read_tokens`、`cache_write_tokens`、`cost`（或 `message.usage.cost.total` 等）。无 cost 时表格中显示为「—」。

## 5. 错误处理

- **扫描**：数据目录不存在或不可读则报错退出并给出明确提示；单目录无权限则记录警告并跳过；单行 JSON 解析失败则跳过该行并打日志。
- **聚合**：缺失 usage 字段按 0；cost 缺失为 `None`，模板显示「—」。
- **Flask**：未捕获异常返回 500 并记录 traceback。

## 6. 测试

- **单元测试**：scanner 使用 fixture 目录（mock `.jsonl`），断言记录条数与字段；aggregator 固定输入，断言按 agent/session 汇总结果。
- 测试框架：pytest 或 unittest。
- Flask 路由集成测试不做强制要求，可后续补充。

## 7. 文档与后续

- 实现前根据本设计编写 implementation plan（writing-plans）。
- 若 OpenClaw 未来变更 session 格式，仅需调整 scanner 解析与字段映射。
