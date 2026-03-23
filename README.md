# myIdear

个人工具与示例项目集合。本仓库主要包含 **dShop 零售电商演示**（FastAPI + React），以及虎嗅抓取、OpenClaw Token 监控等子项目。

---

## dShop 零售电商

前后端分离的零售电商演示：用户注册/登录、商品列表、购物车（需登录）、下单、支付 Stub、Prometheus `/metrics`。

### 技术栈

| 部分 | 技术 |
|------|------|
| 后端 | Python 3.9+、FastAPI、SQLAlchemy、SQLite（默认）/ 可换 PostgreSQL、JWT |
| 前端 | React 18、TypeScript、Vite、React Router |
| 文档 | [设计文档](docs/plans/2025-03-17-retail-ecommerce-design.md)、[实施计划](docs/plans/2025-03-17-retail-ecommerce-plan.md) |

### 环境准备

```bash
cd /path/to/myIdear

# 后端虚拟环境（示例使用 .venv_retail）
python3 -m venv .venv_retail
.venv_retail/bin/pip install -r retail_api/requirements.txt

# 前端依赖
cd retail_web && npm install && cd ..
```

### 环境变量（可选）

| 变量 | 说明 | 默认 |
|------|------|------|
| `RETAIL_DATABASE_URL` | 数据库连接串 | `sqlite:///./retail.db` |
| `RETAIL_JWT_SECRET` | JWT 签名密钥 | `change-me-in-production` |
| `RETAIL_JWT_EXPIRE_MINUTES` | Token 过期（分钟） | `10080`（7 天） |

### 商品种子数据

```bash
PYTHONPATH=. .venv_retail/bin/python -m retail_api.scripts.seed_products
```

若 `products` 表已有数据则不会重复插入。

### 启动与停止

```bash
./start.sh    # 后端 http://localhost:8000 ，前端 http://localhost:5173
./stop.sh     # 停止上述服务
```

手动启动示例：

```bash
# 终端 1
PYTHONPATH=. .venv_retail/bin/uvicorn retail_api.main:create_app --factory --host 0.0.0.0 --port 8000

# 终端 2
cd retail_web && npm run dev
```

### 常用链接

- 前端商城：http://localhost:5173  
- OpenAPI 文档：http://localhost:8000/docs  
- 健康检查：http://localhost:8000/health  
- Prometheus 指标：http://localhost:8000/metrics  

### 测试

```bash
PYTHONPATH=. .venv_retail/bin/python -m pytest tests/retail_api/ -v
```

### 目录结构（零售相关）

```
retail_api/          # 后端应用
  common/            # 中间件、鉴权、异常、指标
  user/ product/ cart/ order/ payment/ inventory/
  db/                # 会话与 Base
  scripts/           # 种子数据等
retail_web/          # 前端 Vite 项目
tests/retail_api/    # 后端测试
start.sh / stop.sh   # 一键启停
```

---

## 其他子项目

| 项目 | 说明 |
|------|------|
| [README_虎嗅抓取.md](README_虎嗅抓取.md) | 虎嗅热点抓取 |
| [openclaw_token_monitor/](openclaw_token_monitor/README.md) | OpenClaw Token 用量监控 |

---

## 许可证

个人学习与演示用途；使用第三方站点或 API 时请遵守其条款。
