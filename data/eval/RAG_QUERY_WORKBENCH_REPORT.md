# RAG Query Workbench Execution Report

Date: 2026-06-04

## Scope

本轮将第一版 query 层接入 FastAPI 后端，并在前端增加 `RAG Query` 工作台，用于收集人工 query、给出 query 设计提示、运行本地 evidence bundle，并保存运行报告。

## Backend

Updated file:

- `backend/app.py`

新增接口：

- `GET /api/query/prompts`
  - 返回 query 设计原则、可改写模板和当前评测关注点。
- `GET /api/query/logs`
  - 读取人工 query 历史，默认返回最近 80 条。
- `POST /api/query/save`
  - 保存人工 query 草稿，不运行检索。
- `POST /api/query/run`
  - 调用 `scripts/query_rag_bundle.py` 生成 evidence bundle。
  - 自动写入 Markdown / JSON 报告到 `data/eval/manual_queries/`。
  - 将 query、标签、笔记、意图识别、judgement 和耗时写入 `data/eval/manual_query_log.jsonl`。

## Query Layer Cache

Updated file:

- `scripts/query_rag_bundle.py`

新增缓存：

- `get_cached_embedder`
- `get_cached_chroma_client`

作用：

在 FastAPI 常驻进程内复用本地 embedding 模型和 Chroma client。首次 query 仍会冷加载模型，后续同一进程内的 query 不再重复完整加载。

## Frontend

Updated files:

- `frontend/index.html`
- `frontend/app.js`
- `frontend/styles.css`

新增视图：

- `RAG Query`

前端功能：

- 人工 query 输入。
- tags / top_k / kg_limit / notes。
- 一键保存草稿。
- 一键运行 query 层。
- 展示 Query Analysis、Judgement、Timings。
- 展示 Text Evidence、Visual Evidence、KG Evidence。
- 展示人工 query 历史。
- 提供可点击模板，鼓励使用编曲用户语言，而不是练习编号 query。

## Query Design Guidance

前端提示强调：

- 正式 query 面向吉他编曲用户。
- 练习答案图不是最终用户入口，只作为视觉 caption 回归测试和可视化证据。
- query 应描述风格目标、和声材料、riff/voicing/把位限制。
- 视觉 caption 应服务于具体指型、和弦图、音阶图和可视化推荐。

## Smoke Test

TestClient smoke test:

```text
GET /api/query/prompts -> 200
POST /api/query/save -> 200
POST /api/query/run -> 200
```

Run query:

```text
我想把 Fmaj7 琶音发展成 math rock 风格的开放弦 riff，有哪些把位和指型可选？
```

Result:

```json
{
  "intent": "mixed_arrangement",
  "style": ["mathrock"],
  "judgement": {
    "sufficient": true,
    "confidence": 0.71,
    "missing": [],
    "warnings": [],
    "evidence_type_count": 2,
    "text_count": 6,
    "visual_count": 0,
    "kg_count": 8,
    "next_queries": []
  },
  "returned_text": 6,
  "returned_visual": 0,
  "returned_kg": 5,
  "timings": {
    "model_load_seconds": 6.3079,
    "fretboard_text_seconds": 0.3120,
    "style_text_seconds": 0.0744,
    "kg_seconds": 0.4202,
    "total_seconds": 7.6594,
    "kg_status": "neo4j"
  }
}
```

Generated report:

```text
data/eval/manual_queries/manual_query_20260604_211909_1abaece71c.md
```

## Interpretation

该 query 没有强制要求“给我视觉指型图”，所以视觉证据为 0 可以接受。后续如果 query 包含“可视化指型、和弦图、同把位参考、具体按法”等词，query 层应进入视觉 caption 检索路径。

## Next Steps

1. 在前端连续采集 20 到 50 条编曲用户 query。
2. 将 query 分为 `style_arrangement`、`fretboard_voicing`、`visual_shape_recommendation`、`mixed_arrangement` 等评测桶。
3. 对“应该召回视觉证据”的 query 做专门测试，确认视觉 caption 层不再只是练习校准，而能服务于编曲建议。
4. 后续再加入 composer，把 evidence bundle 生成自然语言编曲建议。
