# Query RAG Bundle Report

- Query: 练习15答案里D大调指型1对应哪个小调指型
- Intent: `visual_voicing_lookup`
- Sufficient: `True`
- Confidence: 0.71
- Total latency: 7.061s

## Query Analysis

```json
{
  "query": "练习15答案里D大调指型1对应哪个小调指型",
  "intent": "visual_voicing_lookup",
  "style_hints": [],
  "theory_terms": [
    "大调",
    "小调",
    "指型"
  ],
  "technique_terms": [],
  "needs_fretboard_text": true,
  "needs_visual": true,
  "needs_style_text": false,
  "needs_kg": false,
  "confidence": 0.65,
  "matched_rules": [
    "fretboard_terms",
    "visual_terms"
  ]
}
```

## Retrieval Plan

| Name | Backend | Collection | TopK | Reason | Query |
|---|---|---|---:|---|---|
| `fretboard_text` | `chroma` | `guitar_fretboard_handbook_text_qwen3_06b` | 5 | 指板/理论/练习题干证据 | 练习15答案里D大调指型1对应哪个小调指型 |
| `visual_caption` | `chroma` | `guitar_fretboard_answer_captions_qwen3_06b` | 5 | 具体图形/指法/voicing/答案图证据 | 练习15答案里D大调指型1对应哪个小调指型 指型图 和弦图 voicing |

## Text Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `text:fretboard_text_0143` | `fretboard_handbook_clean_text` | 1.0687 | 吉他指板手册正文清洗层 | ## 练习15 D大调指型1（B小调指型2） G大调指型4（E小调指型5） C大调指型2（A小调指型3） E大调指型5（C#小调指型1） Bb大调指型3（G小调指型4） [图示引用 5 张，详见 image_refs] |
| 2 | `text:fretboard_text_0045` | `fretboard_handbook_clean_text` | 1.0636 | 吉他指板手册正文清洗层 | ## 练习15 回到第7章中的练习12，在每种大调指型的上方标出其关系小调。然后用方形在指型图中画出其关系小调的根音。例如： D大调指型1 (B小调指型2) 再次弹奏练习12中的各种指型。首先从大调音阶的根音弹奏这个指型，然后从关系小调音阶的根音开始弹奏。弹奏之前先大声说出每种指型的序号。 [图示引用 1 张，详见 image_refs] |
| 3 | `text:fretboard_text_0044` | `fretboard_handbook_clean_text` | 1.0217 | 吉他指板手册正文清洗层 | ## 练习14 回到练习13。在每种指型上方用圆括号写出它的关系大调。在指型图中用方形画出其关系大调的根音。下面是第一个指型的例子。 E小调指型5(G大调指型4） 再次弹奏练习13中的各种指型。首先从小调音阶的根音弹奏这个指型，然后从其关系大调音阶的根音开始弹奏。弹奏之前先大声说出每种指型的序号。 [图示引用 1 张，详见 image_refs] |
| 4 | `text:fretboard_text_0142` | `fretboard_handbook_clean_text` | 0.9905 | 吉他指板手册正文清洗层 | ## 练习13 E小调指型5 2C小调指型2 E小调指型 A小调指型3 D小调指型3 小调指型4 小调指型 Bb小调指型3 小调指型2 F小调指型5 [图示引用 10 张，详见 image_refs] |
| 5 | `text:fretboard_text_0053` | `fretboard_handbook_clean_text` | 0.9881 | 吉他指板手册正文清洗层 | ## 练习19 回到练习17中，写出每个图示中关系大调五声音阶的名称和指型序号，并且用方形画出关系大调五声音阶的根音。第一个图示的例子如右所示。 D小调五声音阶指型2 [图示引用 1 张，详见 image_refs] |

## Visual Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `visual_caption:fretboard_answer_E15_1` | `fretboard_handbook_question_answer` | 1.1062 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 15 小题: 1 证据类型: fretboard_diagram 视觉类型: scale_pattern 对象: D大调指型1 (B小调指型2) 根音: D / B 性质/调式: Major / Minor 位置/指型: 指型1 / 指型2 方向: horizontal 把位: II 品位范围: 约为第2-6品 可见标签: D大调 指型1, B小调 指型2 按点概述: 横向六线谱，包含实心圆点（音阶音）、带圈圆点（根音）和方形框（关系小调根音）。罗马数字II位于第二弦下方。 capt... |
| 2 | `visual_caption:fretboard_answer_E15_4` | `fretboard_handbook_question_answer` | 1.0928 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 15 小题: 4 证据类型: fretboard_diagram 视觉类型: scale_pattern 对象: E 大调指型 5 (C# 小调指型 1) 根音: E / C# 性质/调式: Major / Relative Minor 位置/指型: 指型 5 / 指型 1 方向: horizontal 品位范围: 约为 7-12 品 可见标签: E 大调 指型 5, (C# 小调 指型 1) 按点概述: 横向六线谱，包含 E 大调音阶指型点阵。图中用方框圈出了 C# 小调的根音位置... |
| 3 | `visual_caption:fretboard_answer_E15_8` | `fretboard_handbook_question_answer` | 1.0920 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 15 小题: 8 证据类型: fretboard_diagram 视觉类型: mode_fretboard_map 对象: Gb 大调指型 5 (Eb 小调指型 1) 根音: Gb / Eb 性质/调式: Major / Minor 位置/指型: 指型 5 / 指型 1 方向: horizontal 把位: III 可见标签: Gb 大调 指型 5, Eb 小调 指型 1 按点概述: 横向指板图，罗马数字 III 标记把位。图中包含实心圆点（音阶音）和带方框的圆点（根音）。根据标题推... |
| 4 | `visual_caption:fretboard_answer_E14_3` | `fretboard_handbook_question_answer` | 1.0675 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 14 小题: 3 证据类型: fretboard_diagram 视觉类型: scale_pattern 对象: E小调指型1 (G大调指型5) 根音: E / G 性质/调式: Natural Minor / Major 位置/指型: 指型1 / 指型5 答案项: 3: E小调指型1 (G大调指型5) 方向: horizontal 把位: IV 可见标签: E 小调 指型 1, (G 大调 指型 5) 按点概述: 横向指板图，下方标注罗马数字 IV。图中包含多个实心圆点（音阶音），... |
| 5 | `visual_caption:fretboard_answer_E12_1` | `fretboard_handbook_question_answer` | 1.0436 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 12 小题: 1 证据类型: fretboard_diagram 视觉类型: scale_pattern 对象: D大调 指型1 根音: D 性质/调式: Major Scale (Ionian) 位置/指型: 指型1 (Pattern 1) 方向: horizontal 品位范围: 约为第5-8品 可见标签: 1) D大调 指型1 按点概述: 图中展示了D大调音阶在指板上的分布，包含多个按点（黑点）和两个圈出的根音（Root notes）。根据D大调指型1的常见把位推断，根音位于5... |

## KG Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| - | - | - | - | - | - |

## Bundle Judgement

```json
{
  "sufficient": true,
  "confidence": 0.71,
  "missing": [],
  "warnings": [],
  "evidence_type_count": 2,
  "text_count": 5,
  "visual_count": 5,
  "kg_count": 0,
  "next_queries": []
}
```

## Answer Seed

```json
{
  "recommended_structure": [
    "结论",
    "相关教材证据",
    "视觉/指法证据",
    "KG/风格关系",
    "可操作编配建议",
    "不确定点"
  ],
  "top_text_ids": [
    "text:fretboard_text_0143",
    "text:fretboard_text_0045",
    "text:fretboard_text_0044"
  ],
  "top_visual_ids": [
    "visual_caption:fretboard_answer_E15_1",
    "visual_caption:fretboard_answer_E15_4",
    "visual_caption:fretboard_answer_E15_8"
  ],
  "top_kg_ids": [],
  "composer_instruction": "只能基于 evidence_id 引用证据；区分教材明确内容与系统推断；如果 judgement.missing 非空，需要先说明证据不足。"
}
```

## Timings

```json
{
  "model_load_seconds": 6.47684410000511,
  "fretboard_text_seconds": 0.3063311000005342,
  "visual_caption_seconds": 0.22012189999804832,
  "total_seconds": 7.060622800010606
}
```
