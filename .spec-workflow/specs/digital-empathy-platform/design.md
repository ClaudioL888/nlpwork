# Design Document

## Overview

数字共情平台将基于 FastAPI + Python 服务层与 Vite + TypeScript 前端构建，实现“社会情绪雷达 Dashboard + 在线文本分析/过滤 + WebSocket 实时聊天 + 事件搜索”四大能力。整体架构沿用 Master Plan 中“网关 → 服务编排 → 核心 NLP/规则 → 数据访问 → 存储监控”的分层，并补充事件分析流水线（聚合统计 + 图数据）、规则/模型治理与前端多入口交互。目标是形成一个 Demo 级别即可运行、后续也可扩展至更复杂任务的统一平台。

## Steering Document Alignment

### Technical Standards (tech.md)
- Master Plan 明确 Python 3.10 + FastAPI、SQLAlchemy、PyTorch/Transformers、Tailwind + Chart.js、Docker、GitHub Actions 作为技术栈；本设计沿用这些约定，不引入额外语言或框架。
- 约定的性能指标（REST <300 ms、事件分析 <5 s、WS 延迟 <1 s）通过异步 IO、任务分片与缓存策略在设计层面明确。
- DevOps 要求（CI、监控、日志脱敏）在服务层与基础设施模块中提供插桩点（structlog、Prometheus、审计日志接口）。

### Project Structure (structure.md)
- 假定后端位于 `src/`；按照 `api/routers`, `services/`, `core/`, `data/`, `models/`, `workers/` 分层组织。
- 前端 `frontend/` 采用 `pages/`, `components/`, `hooks/`, `api/clients/`，共享样式与状态（如 Zustand/Context）。
- 规范所有配置/模型/规则路径（`config/`, `models/<name>/<version>`, `rules/`）以利于版本管理和热更新。

## Code Reuse Analysis
- 现有仓库提供的 `digital_empathy_*.md` 文档仅为规划；代码复用需从未来实现中抽象：FastAPI 通用中间件、分析器和规则引擎模块会被多接口共用。
- 内置可重用能力：文本预处理器、情绪分类器、危机检测器、规则匹配器、事件聚合器、可序列化数据模型、日志/监控工具。

### Existing Components to Leverage
- **NLP Heuristics/Model Wrappers**：统一封装 Transformers 模型 + 词典规则，供 `analyze_text`、`filter`、`chat_ws` 共用。
- **Rule Engine YAML Loader**：解析规则并提供匹配 API，供 REST 及 WebSocket。
- **Graph Analytics Helpers**：基于 NetworkX 生成传播网络，用于事件分析及未来扩展。

### Integration Points
- **REST & WS 网关**：`src/api/routers/*.py` 暴露 `/api/analyze_text`, `/api/filter`, `/api/analyze_event`, `/api/search`, `/ws/chat`。
- **数据库**：PostgreSQL/SQLite 通过 SQLAlchemy DAO 操作 `analysis_logs`, `event_snapshots`, `filter_audits`, `chat_messages`。
- **缓存/队列**（可选）：Redis 用于 WebSocket fan-out、分析结果缓存。

## Architecture

```
┌───────────────┐
│  Frontend UI  │  (Dashboard / Chat / Search)
└──────┬────────┘
       │ Axios/WebSocket
┌──────▼────────┐
│  FastAPI API  │
├──────┬────────┤
│ Service Layer │  (AnalyzerService / FilterService / EventService / SearchService / ChatService)
├──────┬────────┤
│ Core NLP/Rule │  (ModelRegistry, RuleMatcher, GraphBuilder, Feature Extractors)
├──────┬────────┤
│ Data Access   │  (Repositories, Audit Loggers)
├──────┬────────┤
│ Storage/Infra │  (PostgreSQL, Redis, Object Storage, Prometheus, Logger)
└───────────────┘
```

### Modular Design Principles
- API Router 文件只负责请求/响应验证与路由；业务逻辑位于 service 类。
- 核心 NLP/规则模块通过接口暴露（如 `SentimentClassifier.predict(text: str) -> SentimentResult`），便于替换模型。
- 数据访问层的 Repository 负责 SQLAlchemy 会话管理；上层只接收 DTO。
- 前端以功能页为单位拆分组件（图表、列表、输入面板）并共享 API 客户端。

## Components and Interfaces

### AnalyzerService
- **Purpose:** 将单条文本通过模型和特征提取流程输出情绪、共情、危机指标。
- **Interfaces:** `analyze_text(payload: AnalyzeTextRequest) -> AnalyzeTextResponse`
- **Dependencies:** `SentimentClassifier`, `EmpathyScorer`, `CrisisDetector`, `EvidenceExtractor`, `AnalysisLogRepo`.
- **Reuses:** NLP pipeline、公用校验工具。

### FilterService
- **Purpose:** 综合模型结果与规则引擎，给出 `allow/deny` 和建议动作，并写入审计日志。
- **Interfaces:** `filter_text(FilterRequest) -> FilterResponse`, `update_ruleset(RuleSetPayload)`
- **Dependencies:** `AnalyzerService`, `RuleMatcher`, `FilterAuditRepo`, `RateLimiter`.

### EventAnalyzerService
- **Purpose:** 基于关键词在历史数据中聚合情绪演化、生成典型语句、构建传播图。
- **Interfaces:** `analyze_event(EventRequest) -> EventInsight`
- **Dependencies:** `EventSnapshotRepo`, `GraphBuilder`, `Summarizer`, `CacheProvider`.

### SearchService
- **Purpose:** 对事件索引或日志表执行关键词搜索/分页排序。
- **Interfaces:** `search(keyword: str, params: SearchQuery) -> SearchResultPage`
- **Dependencies:** `SearchIndexRepo` (SQL/Full-text), `Serializer`.

### ChatGateway
- **Purpose:** 管理 WebSocket 连接、路由消息到 `AnalyzerService` 获取标签后广播。
- **Interfaces:** `handle_connection(WebSocket, room_id, user_id)`, `broadcast(room_id, payload)`
- **Dependencies:** `AnalyzerService`, `ChatHistoryRepo`, `RedisPubSub (optional)`, `RateLimiter`.

### Frontend Modules
- **DashboardPage**：封装关键词输入、分析状态、图表（折线/环形/词云/摘要卡）。
- **ChatPage**：包含 WebSocket Hook、消息列表、风险高亮样式。
- **SearchPage**：关键词输入、结果卡片、分页组件、导出按钮。
- **Shared Components**：`EmotionTrendChart`, `RiskSummaryCard`, `MessageBubble`, `ResultList`, `LoadingState`.

## Data Models

### AnalyzeTextResponse
```
class AnalyzeTextResponse(BaseModel):
    request_id: UUID
    text: str
    label: SentimentLabel
    empathy_score: float
    crisis_probability: float
    evidence: list[EvidenceChunk]
    model_version: str
    rule_version: str | None
    latency_ms: int
```

### FilterLog
```
class FilterLog(SQLModel):
    id: UUID
    text_hash: str
    decision: Literal["allow","deny","review"]
    matched_rules: list[str]
    analyzer_snapshot: JSON
    recommendation: str
    created_at: datetime
```

### EventInsight
```
class EventInsight(BaseModel):
    keyword: str
    time_window: tuple[datetime, datetime]
    emotion_series: list[EmotionPoint]
    crisis_summary: CrisisSummary
    representative_quotes: list[Quote]
    network_graph: GraphPayload
    export_links: list[ExportArtifact]
```

### ChatMessage
```
class ChatMessage(SQLModel):
    id: UUID
    room_id: str
    user_id: str
    text: str
    sentiment: SentimentLabel
    crisis_probability: float
    created_at: datetime
```

## Error Handling

### Error Scenarios
1. **模型推理失败/超时**
   - **Handling:** 捕获异常、返回 `ERR-NLP-001`，降级为词典/规则判断并标记 `fallback=true`。
   - **User Impact:** REST 返回 503 + 友好信息；前端提示“分析服务临时不可用”。

2. **规则文件或模型版本加载失败**
   - **Handling:** 在启动和热更新时校验；失败则回滚至上一个成功版本并发送告警。
   - **User Impact:** 接口仍可用但响应中标记 `rule_version`/`model_version` 为回滚版本。

3. **WebSocket 连接异常或限流触发**
   - **Handling:** 发送 JSON 错误帧 `{type:"error", code:"RATE_LIMIT"}`，记录日志。
   - **User Impact:** Chat UI 显示限流提示，允许重试。

4. **搜索/事件查询无数据**
   - **Handling:** 返回空数组与建议关键词；记录查询用于分析。
   - **User Impact:** 前端显示“暂无结果”，不视为错误。

## Testing Strategy

### Unit Testing
- 测试 NLP 模块：文本预处理、情绪分类、共情评分、危机检测、证据抽取。
- 服务层：AnalyzerService、FilterService、EventAnalyzerService、SearchService 的 happy path + 边界条件。
- 工具类：规则解析、GraphBuilder、RateLimiter、缓存封装。

### Integration Testing
- HTTPX 调用 REST API（analyze_text/filter/analyze_event/search）验证端到端逻辑、schema 与错误码。
- WebSocket 测试：使用 `websockets` 客户端模拟多用户，验证连接、广播、速率限制与标签展示。
- 数据层：使用临时数据库跑 Repository + Alembic 迁移测试。

### End-to-End Testing
- 前端 Playwright/Cypress 脚本覆盖 Dashboard 分析流程、Chat 实时标注、Search 列表与导出。
- Demo 脚本走查：按 Master Plan 的课堂步骤执行，确保 UI/接口/监控状态一致。
- 压测脚本（k6/locust）验证性能指标，附在 CI 或独立性能回归流程。
