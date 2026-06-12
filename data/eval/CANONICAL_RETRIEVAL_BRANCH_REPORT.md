# Canonical Retrieval Branch Report
## Date

2026-06-10

## Objective

将已审核通过的视觉 caption canonical sidecar 接入 RAG bundle，新增一条标准术语精确召回分支。

## Inputs

- Canonical sidecar:
  - `data/processed/fretboard_handbook/question_answer_visual_caption_canonical/fretboard_answer_visual_caption_canonical_terms.jsonl`
- Source caption layer:
  - `data/processed/fretboard_handbook/question_answer_visual_caption_layer/fretboard_answer_visual_caption_accepted_all.jsonl`

## Changes

### Accepted Sidecar

用户确认后，将合并 sidecar 中 389 条记录标记为：

```json
"status": "accepted"
```

### Query Bundle

更新文件：

- `scripts/query_rag_bundle.py`

新增能力：

- 读取 accepted canonical visual sidecar。
- 根据 QueryPlan 的：
  - `canonical_terms`
  - `required_terms`
  - `optional_terms`
  - `negative_constraints`
  进行本地精确术语召回。
- 将 canonical hit 转成 `EvidenceItem`，并合并进 `visual_caption` 候选池。
- 对向量召回得到的 visual evidence，根据 `visual_id` 自动补充 sidecar 中的 canonical terms。
- domain rerank 会同时使用 canonical terms 和原有文本/metadata 规则。

## Smoke Test

测试 query：

```text
给出G小调的吉他指型参考
```

固定 QueryPlan：

```json
{
  "canonical_terms": [
    "key:g_minor",
    "scale:natural_minor",
    "visual_type:scale_pattern"
  ],
  "required_terms": [
    "key:g_minor",
    "visual_type:scale_pattern"
  ],
  "negative_constraints": [
    "tuning:dadgad",
    "tuning:drop",
    "tuning:open"
  ]
}
```

输出：

- `data/eval/canonical_visual_gminor_smoke.md`
- `data/eval/canonical_visual_gminor_smoke.json`

### Result

```json
{
  "sufficient": true,
  "text_count": 25,
  "visual_count": 26,
  "kg_count": 0,
  "canonical_visual_seconds": 0.024
}
```

Top visual evidence:

1. `fretboard_answer_E14_6`
   - Title: `G 小调指型 4 (Bb 大调指型 3)`
   - Matched required terms: `key:g_minor`, `visual_type:scale_pattern`

2. `fretboard_answer_E15_5`
   - Title: `Bb Major Pattern 3 (G Minor Pattern 4)`
   - Matched required terms: `key:g_minor`

This confirms canonical retrieval can pull exact G minor visual evidence into top ranks.

## Notes

- The branch is local-only during query time; it does not call external APIs.
- Runtime overhead is small in smoke test: about `0.024s`.
- Canonical retrieval does not replace vector retrieval. It supplements it by preventing exact music-term targets from being missed.

## Next

1. Add frontend display for `canonical_retrieval` details if needed.
2. Run the same test through the frontend Query Workbench.
3. Test chord-specific queries:
   - `Ab m11 maj9#11 高把位图示`
   - `C调 7#9 7b9 低把位 funk voicing`
4. Start Evidence Selector design after retrieval stability improves.
