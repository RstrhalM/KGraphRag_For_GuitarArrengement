# Prompt Versioning

本目录存放 Agentic RAG 各子 Agent 的版本化 prompt。

## 当前版本

| Agent | Version | File | 状态 |
|---|---|---|---|
| Query Normalizer | `query_normalizer_v1.1` | `query_normalizer_v1.1.md` | active |
| Answer Composer | `answer_composer_v1.0` | `answer_composer_v1.0.md` | active |
| Answer Verifier | `answer_verifier_v0.1` | `answer_verifier_v0.1.md` | planned |

## 记录规则

每次 Query / RAG / Full Chain 运行都应记录：

```json
{
  "prompt_versions": {
    "query_normalizer": "query_normalizer_v1.1",
    "answer_composer": "answer_composer_v1.0",
    "answer_verifier": "answer_verifier_v0.1"
  }
}
```

## 后续 A/B

新增 prompt 时不覆盖旧文件，新增版本文件并更新 `scripts/prompt_registry.py`。

例：

```text
prompts/query_normalizer_v1.2.md
prompts/answer_composer_v1.1.md
```

前端 A/B 测试可以在后续通过请求字段选择 prompt profile；当前阶段先固定 active registry。
