# 零售电商网站 Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现前后端分离的零售电商后端（FastAPI）+ 前端（React），具备健康检查、统一错误与可观测基线，以及 C 端浏览→加购→下单主链路与可观测性扩展能力。

**Architecture:** 后端单 FastAPI 应用，按领域分包（common、db、user、product、order、payment、inventory 等）；统一 REST API `/api/v1/*`，JWT 鉴权；请求级 request_id/trace_id、结构化日志、/health、/metrics。前端单 React 应用，C 端与管理后台同仓库路由区分，共享 API 客户端与类型。

**Tech Stack:** Python 3.11+、FastAPI、SQLAlchemy 2、PostgreSQL、Redis、Pydantic、pytest；React、TypeScript、Vite；OpenAPI 3；可选 OpenTelemetry、Prometheus、Loki/Jaeger。

**Spec:** `docs/plans/2025-03-17-retail-ecommerce-design.md`

---

## File Structure

**Backend (`retail_api/`)** — 与 myIdear 仓库根目录平级或置于 `retail/backend/`，由执行时决定；下例以 `retail_api/` 为根。

| 路径 | 职责 |
|------|------|
| `retail_api/__init__.py` | 包标记 |
| `retail_api/main.py` | FastAPI 应用工厂、lifespan、挂载路由与中间件 |
| `retail_api/common/__init__.py` | 公共包 |
| `retail_api/common/middleware.py` | request_id、trace_id 注入与响应头、结构化请求日志 |
| `retail_api/common/response.py` | 统一成功响应结构、分页包装 |
| `retail_api/common/exceptions.py` | 业务异常类与 FastAPI 异常处理器 |
| `retail_api/common/pagination.py` | page/page_size 解析与校验 |
| `retail_api/common/auth.py` | JWT 依赖与当前用户解析 |
| `retail_api/db/__init__.py` | 数据库包 |
| `retail_api/db/session.py` | 引擎、会话、get_db 依赖 |
| `retail_api/user/router.py` | 用户路由：注册、登录 |
| `retail_api/user/service.py` | 用户业务逻辑 |
| `retail_api/user/schemas.py` | Pydantic 模型 |
| `retail_api/user/models.py` | SQLAlchemy 模型（可选与 schemas 同文件或分文件） |
| `retail_api/product/router.py` | 商品列表、详情 |
| `retail_api/product/service.py` | 商品查询逻辑 |
| `retail_api/product/schemas.py` | 请求/响应模型 |
| `retail_api/product/models.py` | 商品表模型 |
| `retail_api/order/router.py` | 下单、查询订单 |
| `retail_api/order/service.py` | 订单创建、状态、与库存协作 |
| `retail_api/order/schemas.py` | 订单请求/响应 |
| `retail_api/order/models.py` | 订单表模型 |
| `retail_api/inventory/service.py` | 库存占用/释放/回滚 |
| `retail_api/inventory/models.py` | 库存表或与 product 合并 |
| `retail_api/cart/router.py` | 购物车增删改查（或合并到 order 域，按实现偏好） |
| `retail_api/payment/router.py` | 支付入口与回调（可先 stub） |
| `retail_api/config.py` | 配置（环境变量、默认值） |
| `tests/` | 与 `retail_api/` 同级的测试目录，镜像包结构 |

**Frontend (`retail_web/`)** — 同仓库下前端项目。

| 路径 | 职责 |
|------|------|
| `retail_web/package.json` | 依赖：react、typescript、vite、react-router-dom、fetch/axios |
| `retail_web/src/main.tsx` | 入口、路由挂载 |
| `retail_web/src/api/client.ts` | API 基 URL、请求拦截器、Bearer 注入 |
| `retail_web/src/api/products.ts` | 商品列表、详情接口封装 |
| `retail_web/src/pages/ProductList.tsx` | 商品列表页 |
| `retail_web/src/pages/ProductDetail.tsx` | 商品详情页 |
| `retail_web/src/pages/Cart.tsx` | 购物车页 |
| `retail_web/src/pages/Checkout.tsx` | 下单/收银台 |
| `retail_web/src/types/api.ts` | 与 OpenAPI 一致的 TS 类型（可手写或生成） |

**Config / 部署**

| 路径 | 职责 |
|------|------|
| `retail_api/requirements.txt` 或 `pyproject.toml` | 后端依赖 |
| `retail_api/Dockerfile` | 多阶段构建，运行 uvicorn |
| `.env.example` | 环境变量示例（DB URL、Redis、JWT secret） |

---

## Chunk 1: 后端脚手架 + 健康检查 + request_id 与结构化日志

**Files:**
- Create: `retail_api/main.py`
- Create: `retail_api/common/middleware.py`
- Create: `retail_api/common/__init__.py`
- Create: `retail_api/__init__.py`
- Create: `retail_api/config.py`
- Create: `retail_api/requirements.txt`
- Create: `tests/conftest.py`
- Create: `tests/test_health.py`
- Create: `tests/test_request_id.py`

- [ ] **Step 1.1: 创建后端目录与依赖**

创建 `retail_api/requirements.txt`：

```text
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic-settings>=2.0.0
```

创建 `retail_api/config.py`：

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "retail-api"
    debug: bool = False

    class Config:
        env_prefix = "RETAIL_"

settings = Settings()
```

- [ ] **Step 1.2: 编写健康检查与 request_id 的失败测试**

创建 `tests/conftest.py`：

```python
import pytest
from fastapi.testclient import TestClient
from retail_api.main import create_app

@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)
```

创建 `tests/test_health.py`：

```python
def test_health_returns_200(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert "status" in r.json()
```

创建 `tests/test_request_id.py`：

```python
def test_response_includes_request_id(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert "x-request-id" in r.headers
    assert len(r.headers["x-request-id"]) > 0
```

- [ ] **Step 1.3: 运行测试确认失败（无 create_app、无 /health、无 request_id）**

Run: `cd /path/to/repo && pip install -r retail_api/requirements.txt && pytest tests/test_health.py tests/test_request_id.py -v`  
Expected: FAIL（import 或 404）

- [ ] **Step 1.4: 实现 main.py 与 create_app、/health**

在 `retail_api/main.py` 中实现：

- `create_app()` 创建 `FastAPI(app_name=settings.app_name)`。
- 注册中间件：从 `common.middleware` 挂载 request_id 中间件。
- 注册路由：`@app.get("/health")` 返回 `{"status": "ok"}`。

- [ ] **Step 1.5: 实现 request_id 中间件**

在 `retail_api/common/middleware.py` 中：

- 使用 `uuid.uuid4().hex` 生成 request_id；若请求头已有 `X-Request-Id` 则复用。
- 在 request.state 上设置 `request_id`；在响应头中加 `X-Request-Id`。
- 请求进入时用结构化格式打一条日志（JSON：timestamp、level、message、request_id），可先打 stdout。

- [ ] **Step 1.6: 运行测试确认通过**

Run: `pytest tests/test_health.py tests/test_request_id.py -v`  
Expected: PASS

- [ ] **Step 1.7: Commit**

```bash
git add retail_api/ tests/
git commit -m "feat(retail): add FastAPI scaffold, /health, request_id middleware"
```

---

## Chunk 2: 统一错误响应与异常处理

**Files:**
- Create: `retail_api/common/exceptions.py`
- Create: `retail_api/common/response.py`
- Modify: `retail_api/main.py`（注册异常处理器、挂载通用错误处理）
- Create: `tests/test_errors.py`

- [ ] **Step 2.1: 编写统一错误格式的测试**

在 `tests/test_errors.py` 中：

- 请求一个不存在的路径如 `GET /api/v1/notfound`，断言返回 404 且 body 含 `code`、`message`。
- 可选：在某个测试用路由中主动抛出业务异常，断言 HTTP 状态码与 body 结构一致。

- [ ] **Step 2.2: 实现 exceptions 与 response**

在 `retail_api/common/exceptions.py` 中定义 `AppException`（含 code、message、status_code）及子类如 `NotFoundError`。  
在 `retail_api/common/response.py` 中定义错误响应模型：`{"code": str, "message": str, "details": optional}`。

- [ ] **Step 2.3: 在 main 中注册异常处理器**

对 `AppException` 返回统一 JSON 与对应 status_code；对 `RequestValidationError` 返回 422 与统一结构；对未捕获 Exception 返回 500 且不暴露内部信息，并打日志（带 request_id）。

- [ ] **Step 2.4: 运行测试并提交**

Run: `pytest tests/test_errors.py -v`  
Then: `git add retail_api/common/exceptions.py retail_api/common/response.py retail_api/main.py tests/test_errors.py && git commit -m "feat(retail): unified error response and exception handlers"`

---

## Chunk 3: 数据库会话与用户域（注册、登录、JWT）

**Files:**
- Create: `retail_api/db/session.py`
- Create: `retail_api/common/auth.py`
- Create: `retail_api/user/router.py`, `service.py`, `schemas.py`, `models.py`
- Modify: `retail_api/main.py`（挂载 `/api/v1/users`、依赖 get_db）
- Create: `tests/test_user.py`
- Add: `retail_api/requirements.txt` — `sqlalchemy>=2.0`, `asyncpg` 或 `psycopg2-binary`, `python-jose[cryptography]`, `passlib[bcrypt]`

- [ ] **Step 3.1: 配置 DB 与 get_db**

在 `config.py` 增加 `database_url`；在 `db/session.py` 创建引擎与 `get_db()` 依赖（或同步 Session 依赖），在 `main.py` lifespan 或依赖中注入。

- [ ] **Step 3.2: 用户模型与迁移**

定义 User 表（id、email、hashed_password、created_at 等）；可使用 Alembic 或首期在测试中用 SQLite 内存库。若使用 PostgreSQL，在 .env 中配置 DATABASE_URL。

- [ ] **Step 3.3: 用户注册与登录接口**

- `POST /api/v1/users/register`：body 含 email、password；校验后写库，返回 201 及用户信息（不含密码）。
- `POST /api/v1/users/login`：校验密码，签发 JWT，返回 `{"access_token", "token_type": "bearer"}`。

- [ ] **Step 3.4: JWT 依赖**

在 `common/auth.py` 中实现 `get_current_user`：从 Authorization Bearer 解析 token，校验签名与过期，返回当前用户或 401。

- [ ] **Step 3.5: 测试**

- 单元测试：service 层注册、登录逻辑（mock 或真实 test DB）。
- 集成测试：TestClient 调 register、login，断言状态码与 body；带 token 调一个需鉴权路由断言 200/401。

- [ ] **Step 3.6: Commit**

`git add retail_api/db/ retail_api/common/auth.py retail_api/user/ retail_api/config.py tests/test_user.py && git commit -m "feat(retail): db session, user register/login, JWT auth"`

---

## Chunk 4: 商品 API（列表、详情、分页）

**Files:**
- Create: `retail_api/product/router.py`, `service.py`, `schemas.py`, `models.py`
- Modify: `retail_api/main.py`（挂载 `/api/v1/products`）
- Create: `tests/test_product.py`

- [ ] **Step 4.1: 商品模型与分页约定**

Product 表含 id、name、slug、description、price、stock、created_at 等；列表接口支持 `page`、`page_size`，响应 `{"items": [...], "total": N, "page": P}`。

- [ ] **Step 4.2: GET /api/v1/products 与 GET /api/v1/products/:id**

实现列表（分页、可选排序）与详情；未找到返回 404 并走统一错误格式。

- [ ] **Step 4.3: 测试与提交**

pytest 覆盖列表分页与详情、404；commit: `feat(retail): product list and detail API with pagination`

---

## Chunk 5: 购物车 API

**Files:**
- Create: `retail_api/cart/router.py`, `service.py`, `schemas.py`（或与 order 合并，按设计偏好）
- 购物车存储：可 Redis（key 按 user_id 或 anonymous_id）或 DB 表；需支持未登录用户时用临时 ID（请求头或 cookie）。
- Create: `tests/test_cart.py`

- [ ] **Step 5.1: POST/PATCH/DELETE /api/v1/cart/items**

- 增加：sku_id、quantity；返回当前 cart 摘要。
- 修改：更新数量或删除项。
- 查询：GET /api/v1/cart 返回当前购物车。

- [ ] **Step 5.2: 测试与提交**

覆盖增删改查；commit: `feat(retail): cart API`

---

## Chunk 6: 订单与库存（下单、占用/释放）

**Files:**
- Create: `retail_api/order/router.py`, `service.py`, `schemas.py`, `models.py`
- Create: `retail_api/inventory/service.py`, `models.py`（或与 product 同表/关联）
- Modify: `retail_api/main.py`（挂载 `/api/v1/orders`）
- Create: `tests/test_order.py`, `tests/test_inventory.py`

- [ ] **Step 6.1: 下单流程**

- `POST /api/v1/orders`：body 为 cart 选中项或 sku+quantity 列表；校验库存、计算金额、创建订单、扣减/占用库存；返回订单号与金额。
- 库存不足时返回 409 与统一错误格式；事务内完成订单创建与库存扣减，失败则回滚。

- [ ] **Step 6.2: 订单查询**

- `GET /api/v1/orders/:id`：当前用户只能查自己的订单；404 统一格式。

- [ ] **Step 6.3: 测试**

- 单元测试：inventory 占用/释放/回滚逻辑。
- 集成测试：下单成功、库存不足 409、订单查询 200/404。

- [ ] **Step 6.4: Commit**

`feat(retail): order creation with inventory reserve/release`

---

## Chunk 7: 支付回调（Stub 或真实对接）

**Files:**
- Create: `retail_api/payment/router.py`, `service.py`
- Modify: `retail_api/main.py`（挂载 `/api/v1/payment` 或 `/api/v1/orders/:id/pay`、支付回调 URL）
- Create: `tests/test_payment.py`

- [ ] **Step 7.1: 支付入口与回调**

- `POST /api/v1/orders/:id/pay`：可选 body 指定渠道；返回支付参数（如跳转 URL 或二维码 URL）— 首期可 stub 返回固定格式。
- 回调：接收支付渠道 POST，校验签名、更新订单与支付状态、若失败则释放库存；幂等处理。

- [ ] **Step 7.2: 测试与提交**

Stub 时测试状态更新与幂等；commit: `feat(retail): payment entry and callback stub`

---

## Chunk 8: 可观测性 — /metrics 与 OpenTelemetry（可选）

**Files:**
- Create: `retail_api/common/metrics.py` 或使用 `prometheus_client`
- Modify: `retail_api/main.py`（挂载 `/metrics`，可选 OpenTelemetry 中间件）
- Add: `retail_api/requirements.txt` — `prometheus-client`；可选 `opentelemetry-api`, `opentelemetry-sdk`, `opentelemetry-instrumentation-fastapi`
- Create: `tests/test_metrics.py`

- [ ] **Step 8.1: /metrics**

使用 `prometheus_client` 暴露 HTTP 请求计数与延迟（按 method、path 打标签）；在中间件或 lifespan 中注册。

- [ ] **Step 8.2: OpenTelemetry（可选）**

配置 TracerProvider、FastAPI 自动插桩；将 trace_id/span_id 注入 request.state 与响应头、写入日志字段；OTLP exporter 可环境变量配置，默认不导出也可。

- [ ] **Step 8.3: 测试与提交**

GET /metrics 返回 200 且含 `http_requests_total` 或等价；commit: `feat(retail): Prometheus /metrics and optional OpenTelemetry`

---

## Chunk 9: 前端脚手架 + 商品列表 + 购物车页

**Files:**
- Create: `retail_web/` 下 Vite + React + TypeScript 项目（`npm create vite@latest retail_web -- --template react-ts`）
- Create: `retail_web/src/api/client.ts`, `retail_web/src/api/products.ts`
- Create: `retail_web/src/pages/ProductList.tsx`, `retail_web/src/pages/Cart.tsx`
- Create: `retail_web/src/types/api.ts`（与后端 OpenAPI 一致的类型）
- 配置代理：开发时请求 `/api` 代理到后端 base URL

- [ ] **Step 9.1: 初始化前端项目**

Run: `npm create vite@latest retail_web -- --template react-ts`，进入 `retail_web` 安装依赖；安装 `react-router-dom`。

- [ ] **Step 9.2: API 客户端与商品接口**

在 `src/api/client.ts` 中封装 fetch，baseURL 从 env 读取，请求头可加 Authorization（从 localStorage 或 context 取 token）。  
在 `src/api/products.ts` 中实现 `getProductList(params)`、`getProductById(id)`，返回类型使用 `src/types/api.ts`。

- [ ] **Step 9.3: 商品列表页与路由**

ProductList 请求 `/api/v1/products`，展示分页列表；点击进入详情（ProductDetail）；路由 `/`、`/products/:id`。

- [ ] **Step 9.4: 购物车页**

Cart 页请求 `/api/v1/cart`，展示项与数量；可调用增删改接口；导航栏含「购物车」入口。

- [ ] **Step 9.5: 提交**

`feat(retail): frontend scaffold, product list, cart page`

---

## Chunk 10: 前端下单流程与管理后台占位

**Files:**
- Create: `retail_web/src/pages/Checkout.tsx`
- Create: `retail_web/src/api/orders.ts`, `retail_web/src/api/cart.ts`
- 路由：`/checkout`；下单成功后跳转订单结果页或订单详情
- 管理后台：可选 `/admin` 路由，占位页「商品管理」「订单管理」链接（后续实现）

- [ ] **Step 10.1: 收银台与下单**

Checkout 展示当前购物车汇总、收货信息（可简化为单表单）；提交调用 `POST /api/v1/orders`，成功后跳转并清空/更新购物车。

- [ ] **Step 10.2: 管理后台占位**

`/admin` 需登录（从 token 判断），布局为侧栏 + 占位内容；链接「商品管理」「订单管理」指向占位路由。

- [ ] **Step 10.3: E2E（可选）**

使用 Playwright 或 Cypress：打开商品列表 → 加购 → 进入购物车 → 去结算 → 填写并提交 → 断言成功或订单号展示。

- [ ] **Step 10.4: Commit**

`feat(retail): checkout flow and admin placeholder`

---

## 执行与复查

- 按 Chunk 顺序执行；每 Chunk 内按步骤勾选，测试通过再提交。
- 若使用 subagent：每 Task 或每 Chunk 完成后由 subagent 执行，主 agent 做两阶段复查。
- 实现完成后可运行全量测试与本地前后端联调，并更新 README 说明如何启动后端、前端与依赖（PostgreSQL、Redis、.env）。

---

**Plan complete and saved to `docs/plans/2025-03-17-retail-ecommerce-plan.md`. Ready to execute?**

执行方式：若环境支持 subagent，使用 subagent-driven-development 按 Chunk/Task 分配；否则使用 executing-plans 在当前会话中按步骤执行，并在每个 Chunk 结束时做一次复查。
