# Manual Query KG Planning Fix Report

Date: 2026-06-09

## Problem

用户在前端 `RAG Query` 页面连续测试了多条编曲 query，发现最近的 query 结果都没有 KG evidence。

检查 `data/eval/manual_query_log.jsonl` 和最近的 `data/eval/manual_queries/*.json` 后确认：

- 这不是 Neo4j 未命中。
- 也不是 KG 搜索报错。
- 根因是 query analyzer 将这些 query 判断为 `mixed_lookup`，`needs_kg=false`。
- 因此 retrieval plan 根本没有加入 `kg` task。

典型旧结果：

```json
{
  "intent": "mixed_lookup",
  "plan": ["fretboard_text", "visual_caption", "style_text"],
  "kg_count": 0
}
```

## Affected Query Types

受影响的是典型编曲用户 query，例如：

```text
Funk主奏riff，D小调，用Dorian音阶，高把位，需要密集切分和ghost note
编funk伴奏voicing，C调，7#9和7b9和弦，低把位紧凑排列，留出贝斯空间
Math rock riff，E调，用开放弦和tapping，7/8拍，需要高把位指型参考
编math rock对位旋律，G大调，用add9和sus2和弦，交替拍子，要开放弦voicing图示
Math rock分解和弦，D调，用maj7和m9，需要同把位大小调映射参考
```

这些 query 明显是编曲任务，应进入 KG 检索，因为 KG 负责风格关系、技法启发、约束和编配建议。

## Fix

Updated file:

```text
scripts/query_rag_bundle.py
```

### 1. Expanded KG trigger terms

新增会触发 KG 的编曲动作词：

```text
编
写
写一段
伴奏
主奏
分解
对位
改写
生成
推荐
```

并增加规则：

```text
如果 query 有 style_hints，且包含 technique_terms 或 theory_terms，
同时出现 KG / 编曲动作 / riff / voicing / groove 相关词，
则 needs_kg=true。
```

### 2. Expanded visual trigger terms

新增会触发 visual caption 的词：

```text
指型
把位
同把位
映射
参考
排列
```

这修复了：

```text
Math rock分解和弦，D调，用maj7和m9，需要同把位大小调映射参考
```

旧结果没有 visual，新结果会进入 visual caption。

### 3. Style-aware source rerank

之前 Funk query 有时被 mathrock 文本抢占，导致 `possible_style_mismatch`。

新增 `style_source_boost`：

- Funk query 提升 `cory_wong_funk_core` / Cory Wong / funk 来源。
- Mathrock query 提升 `mathrock_text_course` / `mathrock_pdf_steve_h` / math rock / midwest 来源。
- 对明显错风格来源轻微降权。

同时 `style_text` 和 `visual_caption` 检索先取更多候选，再按本地 rerank 截断返回。

## Regression Result

Regression output path:

```text
data/eval/manual_query_regression_kg_fix_v2/
```

| Case | Intent | Plan Includes KG | Text Source Quality | Visual | KG | Judgement |
|---:|---|---|---|---:|---:|---|
| 1 | `mixed_arrangement` | yes | Top text from `cory_wong_funk_core` | 5 | 8 | sufficient |
| 2 | `mixed_arrangement` | yes | Top text from `cory_wong_funk_core` | 5 | 8 | sufficient |
| 3 | `mixed_arrangement` | yes | Top text from `mathrock_text_course` | 5 | 8 | sufficient |
| 4 | `mixed_arrangement` | yes | Top text from mathrock sources | 5 | 8 | sufficient |
| 5 | `mixed_arrangement` | yes | Top text from mathrock sources | 5 | 8 | sufficient |

All regression cases:

```text
plan: fretboard_text + visual_caption + style_text + kg
kg_status: neo4j
kg_count: 8
warnings: []
confidence: 0.89
```

## Remaining Notes

- Visual evidence in these tests is now present, but it should be judged as “指板/voicing/fingering evidence”，not necessarily “style evidence”。Style grounding should mainly come from style text and KG.
- If a query only asks for pure style concept explanation without a concrete arrangement action, KG can remain optional.
- Next useful improvement is to split query evaluation buckets:
  - style arrangement
  - visual shape recommendation
  - voicing / chord shape
  - rhythm / riff design
  - mixed arrangement
