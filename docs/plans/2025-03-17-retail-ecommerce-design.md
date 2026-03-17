# 零售电商网站 — 设计文档

**日期**: 2025-03-17

## 1. 目标与范围

- **目标**：中大型、长期演进的零售电商系统，支持多端（先 Web，架构为小程序/App 留扩展）、多角色、营销/库存/多商户等复杂业务。
- **形态**：前后端分离；前端 React，后端 FastAPI；统一 REST API 供 Web 与后续多端复用。
- **技术栈**：方案三 — Python FastAPI + React + TypeScript + 统一 API（PostgreSQL + Redis + Elasticsearch）。

## 2. 技术选型

| 层级 | 选型 |
|------|------|
| 前端（Web） | React + TypeScript + Vite 或 Next.js |
| 后端 | Python 3.11+ / FastAPI，REST + OpenAPI 3 |
| 数据 | PostgreSQL（主库）、Redis（缓存/会话）、Elasticsearch（商品/订单搜索） |
| 部署 | 前端静态资源；后端 Docker，多实例或 K8s/云托管 |
| 可观测 | 结构化日志 + Loki；OpenTelemetry + Jaeger/Tempo；Prometheus + Grafana |

## 3. 整体架构与边界

- **前后端分离**：浏览器只访问前端；前端只调后端 API；后端不渲染页面，仅提供 REST API。
- **多端预留**：同一套 REST API 供 Web、后续小程序/App 使用；需要时再增加网关或按端 BFF。
- **后端边界**：单 FastAPI 应用，内部按领域分模块，便于日后拆服务；首期单进程多 worker，DB/Redis/ES 独立部署。
- **前端边界**：单 React 应用，按路由区分 C 端商城与管理后台；共享 API 客户端与类型；后续多端可复用契约与类型。
- **部署**：前端构建为静态资源（CDN/对象存储）；后端容器化，数据库/Redis/ES 单独部署。

## 4. 后端与前端模块划分

**后端（FastAPI）**

- 按领域拆包：`user`、`product`、`order`、`payment`、`inventory`、`merchant`、`marketing`；公共：`common`（统一响应、异常、分页、鉴权）、`db`（连接、会话、迁移）。
- 路由前缀：`/api/v1/users`、`/api/v1/products` 等，多端统一调用。

**前端（React）**

- 按应用入口：C 端商城（商品、购物车、下单、个人中心）、管理后台（商品/订单/商户/营销管理）；共享 API 客户端、公共组件、类型定义。
- 按页面/功能模块拆分，避免单文件过大。

## 5. 关键数据流与接口约定

**核心链路（C 端）**

1. **浏览**：`GET /api/v1/products`（分页、筛选、排序），`GET /api/v1/products/:id` 详情；搜索可走 ES，后端封装为 REST。
2. **加购**：`POST /api/v1/cart/items` 增、`PATCH`/`DELETE` 改删；购物车归属登录用户或临时 ID。
3. **下单**：`POST /api/v1/orders`，后端校验库存与价格、生成订单、扣减/占用库存，返回订单号与应付金额。
4. **支付**：统一支付入口与回调，更新订单与支付状态，必要时回滚库存。

**多端共用约定**

- 鉴权：JWT（Bearer token）统一请求头。
- 列表：分页参数 `page`、`page_size`；响应含 `items`、`total` 及可选 `page`。
- 错误响应：`{ "code", "message", "details" }`，HTTP 状态码与业务一致；前端按 code 做提示或跳转。

## 6. 错误处理与可观测性

**统一错误响应**

- 所有接口出错返回统一 JSON 与对应 HTTP 状态码；FastAPI 异常处理器集中映射；未捕获异常返回 500 并记录 traceback，对外不暴露内部信息；敏感字段不落日志。

**日志**

- 结构化 JSON：`timestamp`、`level`、`message`、`request_id`、`trace_id`、`service` 及业务字段；错误必带 `request_id` 与异常信息；入口中间件生成/透传 `request_id`，注入 `trace_id`/`span_id` 到日志与响应头；输出 stdout，由部署层采集至 Loki 或 ELK，按 `trace_id`/`request_id` 检索。

**链路追踪（Tracing）**

- OpenTelemetry：FastAPI 使用 OTLP SDK，为 HTTP、DB、Redis、外部调用建 span；trace_id 贯穿请求；`trace_id`/`span_id` 写日志并可响应头返回前端；OTLP 导出至 Jaeger 或 Tempo；与日志通过 trace_id 关联（如 Grafana 中 Loki + Tempo 联动）；首期可仅后端，前端 BFF 后续接入。

**监控（Metrics + 告警）**

- Prometheus 客户端暴露 `/metrics`（请求量、延迟、错误率、按 path/method）；业务指标（订单数、支付成功、库存失败等）按需打点；Prometheus 拉取，Grafana 大盘与告警（钉钉/邮件等）；`/health`（及可选 `/ready`）供负载均衡与 K8s 探针，仅检查进程与 DB/Redis 可达性。

**部署与依赖**

- 观测栈：Loki + Prometheus + Grafana + Jaeger/Tempo，Docker Compose 或 K8s；或使用云厂商等效服务。首期优先：结构化日志 + request_id/trace_id、健康检查、基础 HTTP 指标与错误率告警；全量 Tracing 与业务指标随迭代补齐。

## 7. 测试与质量

- **后端**：pytest；领域服务与仓储单元测试（mock DB/Redis）；关键 API 集成测试（TestClient + 测试库或 SQLite）；库存与订单状态变更需覆盖冲突与回滚场景。
- **前端**：组件与页面单元测试（React Testing Library）；关键流程 E2E（Playwright 或 Cypress）覆盖浏览→加购→下单主路径；API 契约与类型与 OpenAPI 一致，可考虑契约测试。
- **质量门禁**：CI 中跑单元与集成测试；MR 前通过；覆盖率目标按模块约定，核心领域不低于设定阈值。

## 8. 文档与后续

- 实现前根据本设计编写 implementation plan（writing-plans）。
- 多端扩展时复用同一 API 契约与 trace_id 透传；若拆微服务，各服务接入 OpenTelemetry 与统一日志格式。
