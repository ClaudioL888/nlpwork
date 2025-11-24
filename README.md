# Digital Empathy Platform

FastAPI + React/Vite 的情绪/危机识别与实时演示平台，支持关键词启发式与可选 LLM（GPT-4o 兼容接口）判定，内置 Dashboard / Search / Chat 三大前端入口以及过滤、事件聚合、监控能力。

## 功能概览
- REST：`/api/analyze_text`、`/api/filter`、`/api/analyze_event`、`/api/search`
- WebSocket：`/ws/chat` 实时打标签并存储聊天记录
- Dashboard：事件关键词情绪曲线、危机摘要、代表语句
- Search：快照检索/分页/排序
- Chat：房间内消息情绪/风险实时展示
- Observability：结构化日志 + Prometheus `/metrics`（Grafana 可接入）
- 可选 LLM：调用第三方 GPT-4o API 提升情绪/危机判定，失败时回退关键词模型

## 本地开发模式
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env    # 在 .env 中填好必要变量，切勿提交真实密钥
alembic upgrade head    # 默认 SQLite 即可
uvicorn src.main:app --reload

cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173  # dev 代理 /api /ws 到 8000
```
浏览器访问 `http://localhost:5173`，在 Console 执行一次：
```js
localStorage.setItem('dep_api_key', 'demo-key');
```
刷新后即可请求后端。

## Docker Compose（一键栈：API/前端/Postgres/Redis/Prometheus/Grafana）
```bash
docker compose -f deploy/docker-compose.yml up --build -d
```
默认端口：
- API: http://localhost:8000
- 前端: http://localhost:4173
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 （admin/admin）

## 环境变量（.env，请勿提交）
嵌套字段使用双下划线：
- 核心  
  - `API_PREFIX=/api`  
  - `SECURITY__API_KEY=demo-key`  
  - `DATABASE__URL=sqlite+aiosqlite:///./data/app.db`（或 Postgres 串）  
  - `DATABASE__POOL_SIZE=5`  
  - `DATABASE__MAX_OVERFLOW=5`  
  - `REDIS_URL=redis://localhost:6379/0`  
  - `OBSERVABILITY__LOG_LEVEL=INFO`
- 可选 LLM（不填则回退关键词模型）  
  - `LLM__BASE_URL=https://api.cursorai.art/v1`  
  - `LLM__API_KEY=<你的密钥>`  
  - `LLM__MODEL=gpt-4o-mini`  

## 关键接口
- `POST /api/analyze_text`：单条情绪/危机分析
- `POST /api/filter`：内容过滤 + 审计
- `POST /api/analyze_event`：按关键词聚合情绪/危机/代表语句/图
- `POST /api/search`：事件快照检索
- `WS /ws/chat`：实时聊天打标签
- 健康与指标：`GET /health`，`GET /metrics`（Prometheus）

## 测试与性能
```bash
pytest tests/unit tests/services tests/api tests/integration
cd frontend && npm run test:e2e    # 需前端/后端运行
locust -f tests/perf/locustfile.py # 需 API 运行
```

## 常见问题
- 401：请求需带 `x-api-key`，浏览器可用 localStorage 设置。
- LLM 未生效：确认 `.env` 使用 `LLM__BASE_URL` / `LLM__API_KEY`（双下划线），重启后端。
- Dashboard 无数据：先通过 Chat 或 `/api/analyze_text` 写入包含关键词的日志，再用同关键词点击 Analyze。

## 提交与推送
1) 确保 `.env`、`node_modules/` 等已在 `.gitignore`，不要提交密钥。  
2) 提交：
```bash
git status
git add .
git commit -m "Update docs and configs"
```
3) 推送到远程（示例仓库）：
```bash
git branch -M main
git remote add origin https://github.com/ClaudioL888/nlpwork.git   # 如已存在远程可跳过
git push -u origin main
```
