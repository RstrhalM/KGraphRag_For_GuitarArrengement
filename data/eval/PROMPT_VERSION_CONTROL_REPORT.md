# Prompt Version Control Report

日期：2026-06-10

## 目标

将 Agentic RAG 中的关键 prompt 从脚本内静态字符串抽离为版本化文件，并在 Query / RAG / Full Chain 运行日志中记录 prompt 版本。

## 已完成

新增目录：

```text
prompts/
  query_normalizer_v1.1.md
  answer_composer_v1.0.md
  answer_verifier_v0.1.md
  PROMPT_VERSIONING.md
```

新增 registry：

```text
scripts/prompt_registry.py
```

当前 registry：

```json
{
  "query_normalizer": "query_normalizer_v1.1",
  "answer_composer": "answer_composer_v1.0",
  "answer_verifier": "answer_verifier_v0.1"
}
```

其中 `answer_verifier_v0.1` 为 planned，用于下一阶段 Critic Agent。

## 代码接入

### Query Normalizer

文件：`scripts/query_normalizer.py`

- `SYSTEM_PROMPT` 改为从 `prompts/query_normalizer_v1.1.md` 加载。
- `sanitize_query_plan()` 会在 QueryPlan 中写入：

```json
{
  "prompt_versions": {
    "query_normalizer": "query_normalizer_v1.1"
  }
}
```

### Answer Composer

文件：`scripts/answer_composer.py`

- `SYSTEM_PROMPT` 改为从 `prompts/answer_composer_v1.0.md` 加载。
- `compose_answer()` 会在 answer 中写入：

```json
{
  "composer": {
    "prompt_version": "answer_composer_v1.0"
  },
  "prompt_versions": {
    "answer_composer": "answer_composer_v1.0"
  }
}
```

### Backend

文件：`backend/app.py`

新增接口：

```text
GET /api/prompts/versions
```

返回当前 active prompt 和 registry。

`/api/query/normalize`、`/api/query/run` 的日志、报告 payload 和 Session Memory 会记录 `prompt_versions`。

### Frontend

文件：`frontend/app.js`

- Query 结果面板显示 Prompt Versions。
- Full Chain 结果面板显示 Prompt Versions。

## 验证

已通过静态编译：

```text
scripts/prompt_registry.py
scripts/query_normalizer.py
scripts/answer_composer.py
backend/app.py
```

本地 sanity check：

```json
{
  "prompt_versions": {
    "query_normalizer": "query_normalizer_v1.1"
  },
  "target_tuning": "standard",
  "required_terms": [
    "tuning:standard",
    "chord_quality:dominant7",
    "visual_type:chord_diagram"
  ]
}
```

## 后续 A/B 预留

下一步可以增加请求字段：

```json
{
  "prompt_profile": "composer_v1.0|composer_v1.1"
}
```

并由 registry 选择不同 prompt 文件。

当前阶段先固定 active registry，确保所有运行可追踪。
