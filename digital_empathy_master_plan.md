# 数字共情系统总体方案（Master Plan）

> 目标：按照“可落地、可扩展、可演示”的标准，构建一个完整的社会情绪雷达与内容过滤平台，贯通需求、架构、技术栈、开发路径与运维规范。

---

## 1. 愿景与业务定位

- **使命**：实时洞察互联网文本中的共情、情绪与危机信号，辅助教学演示、研究分析与内容治理。
- **核心价值**：
  1. 让“事件 → 情绪动态 → 风险告警”实现闭环。
  2. 输出可复用 API，支撑课堂 Demo、研究项目或上层业务集成。
  3. 建立合规、可追溯的数据与模型治理方式。
- **成功指标**：
  - 情绪分类 F1 ≥ 0.80；危机识别 Recall ≥ 0.85。
  - 单条 REST 推理 < 300 ms；事件分析整体 < 5 s。
  - WebSocket 延迟 < 1 s，支持 ≥ 100 并发连接。
  - 发布时具备自动化测试、日志/监控与回滚预案。

---

## 2. 角色画像与使用场景

| 角色           | 核心目标                               | 关键操作                                                                 |
| -------------- | -------------------------------------- | ------------------------------------------------------------------------ |
| 运营/研究人员  | 追踪事件情绪脉络、生成报告             | 在 Dashboard 中输入关键词、导出图表/数据                                 |
| 内容审核员     | 过滤攻击/危机文本，快速响应            | 调用 `/api/filter` 或 WebSocket 聊天页面，查看命中日志                   |
| 开发/集成方    | 对接 API 与 WebSocket，构建二次应用    | 通过 OpenAPI 文档集成 REST；WebSocket 获取实时带标签消息                 |
| 教学演示者     | 课堂演示“社会情绪雷达”                 | 按 Demo 脚本展示 Dashboard→Chat→Search，全程需要稳定、可视化效果良好     |
| 系统管理员     | 维护模型、数据、规则，保障稳定与合规  | 导入数据、热更新规则、监控服务、处理审计请求                             |

---

## 3. 范围界定与验收标准

- **范围内**：文本情绪/共情/危机识别、规则+模型过滤、事件统计与可视化、WebSocket 实时监控、历史搜索、基础 DevOps。
- **暂不涉及**：音视频/多模态输入、跨语言实时翻译、大规模分布式训练。
- **验收 checklist**：
  1. 全部 REST/WebSocket API 在统一环境可用，并通过自动化测试。
  2. Dashboard/Chat/Search 三个前端页面功能完整、交互流畅。
  3. 数据管道与模型加载具备版本记录与回滚机制。
  4. 安全合规措施落实（脱敏、鉴权、日志、审批流程）。
  5. Demo 脚本走通，监控/告警可用。

---

## 4. 系统架构

```
┌────────────────────┐
│     Web Frontend   │  Vite + TS + Tailwind + Chart.js
└──────────┬─────────┘
           │ HTTP/WebSocket
┌──────────▼─────────┐
│   FastAPI Gateway   │  REST & WS, CORS, Auth, Rate Limit
├──────────┬─────────┤
│ Service Layer       │  analyzer/filter/search orchestrations
├──────────┼─────────┤
│ Core Modules        │  NLP heuristics/models, rule engine, graph analytics
├──────────┬─────────┤
│ Data Access         │  Repository/DAO (Postgres/SQLite, Redis cache)
├──────────┴─────────┤
│ Storage & Assets    │  DB, data lake, model registry, logs/metrics
└────────────────────┘
```

---

## 5. 技术栈速览

| 层级        | 技术选型                                                                                       |
| ----------- | ---------------------------------------------------------------------------------------------- |
| 前端        | TypeScript、Vite、Tailwind CSS、Chart.js、Axios、WebSocket API                                 |
| 后端        | Python 3.10、FastAPI、Uvicorn、Pydantic、AsyncIO、SQLAlchemy、Alembic、Redis（可选）           |
| NLP & 过滤 | PyTorch/Transformers、Hugging Face Datasets、规则引擎（YAML/JSON）、scikit-learn/ONNX（可选）  |
| 数据/图分析 | PostgreSQL/SQLite、NetworkX、Pandas                                                            |
| DevOps      | Docker、docker-compose、GitHub Actions、Prometheus、Grafana、structlog/Loguru、pre-commit      |
| 测试        | Pytest、HTTPX、Playwright/Cypress、Ruff、Mypy                                                   |

> 详见 `digital_empathy_tech_stack.md`、`digital_empathy_dev_environment.md`。

---

## 6. 功能需求详情

### 6.1 社会情绪雷达 Dashboard
- 输入事件关键词/时间窗 → 调用 `/api/analyze_event`。
- 展示情绪演化折线、传播网络气泡图、典型共情/危机语句、风险摘要、相关事件联想。
- 支持导出图表/CSV、筛选情绪类别、切换明暗主题。

### 6.2 在线情绪分析与过滤
- `/api/analyze_text`：文本 → 情绪标签、共情得分、危机概率、证据。
- `/api/filter`：输出 `allow`、标签、建议动作（阻断/人工复核/监控）、命中证据；记录日志。
- 规则+模型可热更新；支持批量分析、错误码体系。

### 6.3 WebSocket 实时聊天
- 路径 `/ws/chat`，支持房间/用户标识、消息历史与速率限制。
- 每条消息附情绪/危机标签、置信度；前端 UI 高亮风险消息。

### 6.4 事件搜索
- `/api/search?keyword=`：模糊检索事件，返回情绪分布、风险等级、时间窗口、代表语句。
- 支持分页、排序（热度/风险）、导出摘要。

### 6.5 管理与扩展
- 后台任务：数据导入、模型刷新、规则配置管理（可 CLI/简易管理页）。
- 健康检查 `/health`、指标 `/metrics`，用于监控。

---

## 7. 数据与模型策略

1. **数据来源**：公开社交平台、论坛等，经脱敏与合规审批后使用；示例数据位于 `data/`.
2. **处理流程**：采集 → 清洗（去噪/切分/脱敏）→ 标注（情绪/共情/危机）→ 存储 → 推理/可视化。
3. **模型管理**：
   - 采用 Transformers 微调模型（如 `bert-base-chinese`），并提供轻量 Lexicon 回退逻辑（已实现）。
   - 模型版本化（`models/<model_name>/<version>`），加载失败可自动回滚。
   - 规则库 YAML/JSON，热更新需写入审计日志。
4. **图数据**：NetworkX 构建传播图，未来可接入真正的社交图谱或使用 graph DB。

---

## 8. API & 接口规范

| 方法 & 路径            | 说明                           | 请求参数                             | 响应主体                                       |
| ---------------------- | ------------------------------ | ------------------------------------ | ---------------------------------------------- |
| `POST /api/analyze_text` | 单条文本情绪/危机分析          | `{ "text": "..." }`                  | `{ label, empathy scores, crisis_prob, ... }`  |
| `POST /api/filter`       | 敏感/垃圾过滤                  | `{ "text": "..." }`                  | `{ allow, labels, recommendation, sentiment }` |
| `POST /api/analyze_event`| 事件情绪+网络分析              | `{ "keyword": "...", "event_id": "" }`| 结构化统计、图谱、典型语句                      |
| `GET /api/search`        | 事件检索                       | `?keyword=xxx`                       | `results[]`，含情绪分布/标签                    |
| `WS /ws/chat`            | 聊天+实时情绪标签              | JSON `{text, user}`                  | 广播 `{user, text, sentiment}`                 |

- OpenAPI 自动生成，提供 Swagger/Redoc 页面。
- 鉴权：API Key + 可扩展 JWT/OAuth；默认 Demo 开放。
- 错误码：`ERR-NLP-001`、`ERR-FILTER-001` 等统一格式。

---

## 9. 前端体验设计

1. **入口页面**：Tabs 切换 Dashboard / Chat / Search，保持一致视觉风格（深色大屏风格）。
2. **Dashboard**：输入关键词按钮、分析状态提示；Chart.js 折线+环形图；卡片展示危机/共情示例；后续可添加传播网络可视化（D3/Force layout）。
3. **Chat**：用户名 + 消息输入框；消息列表带情绪 badge；异常提示（连接断开、文本为空等）。
4. **Search**：关键词输入、结果卡片、分页控件；可扩展情绪过滤、导出按钮。
5. **可用性**：移动端适配、键盘可用、loading/error 状态明确。

---

## 10. 开发流程与里程碑

详见 `digital_empathy_development_steps.md`，核心阶段：
1. 需求冻结与合规准备。
2. 数据/模型构建：采集、标注、训练、规则库。
3. 后端核心：FastAPI、NLP/过滤、事件分析、DB/缓存。
4. 前端实现：Dashboard、Chat、Search。
5. 测试 & 性能优化。
6. 部署与课堂 Demo。

每阶段结束需：
- 代码评审 & 自动化测试通过。
- 文档/配置更新。
- 风险评估与下一阶段计划。

---

## 11. 开发环境与工具

- 参考 `digital_empathy_dev_environment.md`：列出了 OS/版本要求、目录结构、依赖安装、环境变量示例、运行命令、测试、Docker/生产注意事项。
- 关键命令：
  ```bash
  # 后端
  uvicorn src.main:app --reload --port 8000

  # 前端
  cd frontend && npm run dev -- --port 5173

  # 测试
  pytest
  npm run test
  ```

---

## 12. 测试与质量保障

- **单元测试**：NLP/过滤/DAO/服务逻辑（Pytest）。
- **集成测试**：HTTPX 调用 REST；WebSocket 客户端模拟。
- **前端测试**：组件单测 + Playwright/Cypress E2E（Dashboard、Chat、Search 流程）。
- **性能**：`locust`/`k6` 压测 `analyze_text`、`analyze_event`、WebSocket 广播。
- **静态分析**：Ruff、Mypy、ESLint、Stylelint；pre-commit 强制执行。
- **覆盖率**：关键模块 ≥ 80%，关键路径（过滤、事件分析）需重点关注。

---

## 13. 安全、合规与伦理

- 输入过滤、防 XSS/CSRF、WebSocket 鉴权、速率限制。
- 日志脱敏（用户名/ID 哈希化）、敏感字段加密存储。
- 数据使用范围说明、伦理声明、PII 清洗流程；敏感操作需审批。
- API Key 管理与密钥轮换；最小权限原则。
- 风险提示：模型误判、数据偏差、滥用风险，需要在文档中明确。

---

## 14. 部署与运维

- **容器化**：Docker 多阶段构建；`docker-compose` 管理 API、DB、前端、监控。
- **CI/CD**：GitHub Actions（lint/test → build → 发布镜像 → 部署）。
- **监控**：Prometheus + Grafana 指标（请求延迟、错误率、模型耗时、WS 连接数）；集中日志（ELK/Loki）。
- **回滚策略**：镜像/模型版本回滚；数据库备份与恢复演练。
- **告警**：响应链路含 on-call 机制。

---

## 15. Demo 脚本与未来扩展

1. **课堂 Demo**：
   - Step 1：Dashboard 输入“地震”，展示情绪折线、典型语句、风险概览。
   - Step 2：切到 Chat，实时输入正面/负面/危机语句，观察标签变化。
   - Step 3：Search 搜索“霸凌”，展示历史事件列表与情绪分布。
2. **未来工作**：
   - 引入真正的深度模型（多模态、长文本）。
   - 支持事件订阅、告警推送、复杂检索/推荐。
   - 与外部系统对接（内容审核、知识图谱）。
   - 增强伦理策略（危机干预联动）。

---

## 16. 文档与交付物索引

| 文档                                   | 内容摘要                                   |
| -------------------------------------- | ------------------------------------------ |
| `digital_empathy_system_design.md`     | 原始系统设计方案（目标、功能、架构）       |
| `digital_empathy_requirement_spec.md`  | 高规格需求规格说明                         |
| `digital_empathy_development_steps.md` | 阶段化实施步骤                             |
| `digital_empathy_tech_stack.md`        | 技术栈与选型说明                           |
| `digital_empathy_dev_environment.md`   | 开发环境配置与运行指南                     |
| `digital_empathy_master_plan.md`        | （当前文档）统一方案与执行蓝图             |

---

> 通过以上统一方案，可直接指导团队自需求→实现→测试→部署全流程执行，确保项目具备实际工程价值与扩展潜力。后续若有新增需求，可在本 Master Plan 基础上持续迭代。*** End Patch
