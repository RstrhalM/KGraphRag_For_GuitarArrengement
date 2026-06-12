# 项目记忆系统设计与第一版实现

日期：2026-06-10

本文固定当前项目的第一版记忆系统。它的目标不是立刻做复杂用户画像，而是先把每次人工 query、Query Normalizer、RAG、Full Chain、反馈评分沉淀成可复盘的 session memory。

## 1. 为什么先做 Session Memory

当前项目已经有：

- 前端人工 query。
- Query Normalizer。
- Text / Visual / KG 多路召回。
- rule rerank / Qwen rerank。
- Answer Composer。
- 人工反馈评分。
- Markdown / JSON 报告。

但这些结果原本分散在 query log、feedback log、manual query report 中。Session Memory 的作用是把同一次测试串起来：

```text
query
-> normalized query / query plan
-> RAG bundle
-> rerank config
-> answer composer
-> theory checks
-> report paths
-> human feedback events
```

这样后续做 Answer Verifier、Rerank A/B、GP5 接入时，就能基于同一个 session 做复盘。

## 2. 当前实现

新增文件：

```text
backend/session_memory.py
```

新增数据目录：

```text
data/eval/session_memory/
  sessions.jsonl
  session_events.jsonl
```

当前采用 append-only JSONL，而不是直接上 SQLite。原因：

- 便于人工查看。
- 便于归档。
- 不需要迁移已有数据。
- 很适合早期 Agentic RAG 研发台账。

## 3. Session Schema v1

每条 session 主要字段：

```json
{
  "schema_version": "session_memory.v1",
  "session_id": "session_...",
  "timestamp": "...",
  "status": "draft|normalized|ran|run_error",
  "memory_type": "query_draft|query_normalization|rag_run|full_chain_run|rag_run_error",
  "source": "frontend_manual_query_workbench|frontend_full_chain_test",
  "query": "...",
  "normalized_query": "...",
  "notes": "...",
  "tags": [],
  "intent": "...",
  "style_hints": [],
  "query_plan": {},
  "judgement": {},
  "timings": {},
  "rerank_config": {},
  "bundle_summary": {},
  "compose_answer": true,
  "answer_status": "ok|error|not_requested",
  "answer_summary": "...",
  "report_md": "data/eval/manual_queries/xxx.md",
  "report_json": "data/eval/manual_queries/xxx.json"
}
```

`bundle_summary` 当前只保存摘要，不把完整 bundle 重复写入 memory：

```json
{
  "text_count": 5,
  "visual_count": 5,
  "kg_count": 8,
  "sufficient": true,
  "confidence": 0.72,
  "model_rerank": {},
  "answer_summary": "...",
  "theory_check_count": 3
}
```

完整结果仍保存在 `report_json` 指向的文件中。

## 4. Event Log

事件日志：

```text
data/eval/session_memory/session_events.jsonl
```

当前事件：

- `query_draft`
- `query_normalization`
- `rag_run`
- `full_chain_run`
- `rag_run_error`
- `feedback_saved`

反馈会以事件形式挂到已有 session：

```json
{
  "timestamp": "...",
  "session_id": "...",
  "event_type": "feedback_saved",
  "payload": {
    "scores": {},
    "failure_tags": [],
    "notes": "..."
  }
}
```

## 5. 新增后端接口

### `GET /api/memory/sessions`

参数：

- `limit`
- `status`
- `q`
- `tag`

作用：

- 列出 session memory。
- 支持按状态、关键词、tag 过滤。

### `GET /api/memory/session`

参数：

- `session_id`

作用：

- 返回单条 session。
- 附带该 session 的事件流。

## 6. 前端页面

新增导航：

```text
Memory
```

页面功能：

- 搜索 session。
- 按状态过滤。
- 查看 session_id、时间、状态、来源。
- 查看 query / normalized query。
- 查看 tags / intent。
- 查看 bundle summary。
- 查看 report_md / report_json。
- 查看 query_plan。
- 查看 feedback 等事件。
- 查看 raw session。

## 7. 与现有日志的关系

当前并不替代旧日志：

```text
manual_query_log.jsonl
query_normalizer_feedback.jsonl
manual_queries/*.md
manual_queries/*.json
```

Session Memory 是新的统一索引层：

```text
旧日志：保留兼容
Session Memory：用于复盘和 Agentic 后续模块
```

## 8. 后续扩展计划

### 8.1 Answer Verifier

未来在 session 中新增：

```json
{
  "verifier": {
    "pass": true,
    "issues": [],
    "risk_level": "low"
  }
}
```

### 8.2 Rerank A/B

未来在 session 中新增：

```json
{
  "ab_test": {
    "baseline": "rule",
    "candidate": "rule+qwen",
    "human_winner": "candidate"
  }
}
```

### 8.3 GP5 Context

未来在 session 中新增：

```json
{
  "score_context": {
    "file": "...gp5",
    "bpm": 120,
    "key": "A minor",
    "chord_progression": [],
    "riff_features": []
  }
}
```

### 8.4 SQLite 升级

当 session 数量扩大后，可以升级为 SQLite：

```text
sessions
events
feedback
evidence_usage
score_contexts
```

但当前 JSONL 更适合快速迭代。

## 9. 当前边界

- 不做长期用户画像。
- 不自动总结用户偏好。
- 不把完整大 bundle 复制进 memory，避免文件膨胀。
- 不改变现有 RAG/Full Chain 输出路径。
- 先服务研发评测，再服务最终用户体验。

## 10. 下一步

建议下一步接 Answer Verifier：

```text
Session Memory
-> 读取 answer + evidence bundle
-> Verifier 检查证据引用和乐理错误
-> 写回 session event
-> 前端 Memory / Full Chain 展示 verifier 结果
```

这会让项目从“能生成答案”进一步变成“能审查自己答案”的 Agentic RAG。

## 11. 实际验证记录

2026-06-10 已完成以下烟测：

```text
Python:
  backend/app.py py_compile passed
  backend/session_memory.py py_compile passed

JavaScript:
  frontend/app.js node --check passed

HTTP:
  GET /api/health -> 200
  GET /api/memory/sessions -> 200
  POST /api/query/save -> session created
  GET /api/memory/session -> session + events returned
  GET / -> Memory nav and section present
  GET /static/app.js -> loadMemorySessions / showMemorySession present
```

验证生成的测试 session 使用标签：

```text
memory-smoke
```

UTC 修复后的记录：

```text
session_time: 2026-06-10T07:43:23Z
event_time:   2026-06-10T07:43:23Z
```

当前本地服务：

```text
http://127.0.0.1:8765
```
