# Query RAG Bundle Report

- Query: FACGCE 调弦下的 数摇riff,G调要怎么设计
- Intent: `mixed_arrangement`
- Sufficient: `False`
- Confidence: 0.53
- Total latency: 9.548s

## Query Analysis

```json
{
  "query": "Design math rock riffs in G major using FACGCE tuning",
  "intent": "mixed_arrangement",
  "style_hints": [
    "mathrock"
  ],
  "theory_terms": [],
  "technique_terms": [
    "riff"
  ],
  "needs_fretboard_text": false,
  "needs_visual": true,
  "needs_style_text": false,
  "needs_kg": false,
  "confidence": 0.0,
  "matched_rules": [
    "llm_plan:visual_caption"
  ]
}
```

## Retrieval Plan

| Name | Backend | Collection | TopK | Reason | Query |
|---|---|---|---:|---|---|
| `visual_caption` | `chroma` | `guitar_visual_mixed_mathrock_trial_qwen3_06b` | 5 | test | FACGCE tuning G major math rock riff chord shapes |

## Text Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| - | - | - | - | - | - |

## Visual Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `visual_caption:mr_style_002` | `mathrock_pdf` | 2.0971 | Math Rock 吉他教材 | 来源: Math Rock 吉他教材 / mathrock_pdf 视觉角色: style_visual_evidence 页码: 34 图像类型: fretboard_diagram 主题: FACGCE_tuning_major_scale_fingerboard_map 调弦: FACGCE 调性: unknown 根音: unknown 音阶: major scale 技法: tapping, riff construction, melodic phrasing 指型: movable patterns... |
| 2 | `visual_caption:mr_style_001_g7` | `mathrock_pdf` | 1.7634 | Math Rock 吉他教材 | 来源: Math Rock 吉他教材 / mathrock_pdf 视觉角色: style_visual_evidence 页码: 33 图像类型: chord_diagram 主题: FACGCE_tuning_G7_chord_shape 调弦: FACGCE 调性: C major 根音: G 和弦: G7 技法: mute, open_strings 弦组: 6 strings 品位范围: open-3 开放弦: 5th string, 4th string, 3rd string, 2nd string... |
| 3 | `visual_caption:mr_style_001_fmaj9` | `mathrock_pdf` | 1.6334 | Math Rock 吉他教材 | 来源: Math Rock 吉他教材 / mathrock_pdf 视觉角色: style_visual_evidence 页码: 33 图像类型: chord_diagram 主题: FACGCE_tuning_Fmaj9_open_chord 调弦: FACGCE 调性: F major 根音: F 和弦: Fmaj9 技法: open_strings 弦组: 6 strings 品位范围: open position (frets 1-4) 开放弦: 6, 5, 4, 3, 2, 1 包含音: F, A, ... |
| 4 | `visual_caption:mr_style_001_am` | `mathrock_pdf` | 1.5129 | Math Rock 吉他教材 | 来源: Math Rock 吉他教材 / mathrock_pdf 视觉角色: style_visual_evidence 页码: 33 图像类型: chord_diagram 主题: FACGCE_tuning_Am_chord_shape 调弦: FACGCE 调性: A minor 根音: A 和弦: Am 技法: muted_strings 弦组: 6 strings 品位范围: open-3 开放弦: 5th string (C), 4th string (G), 3rd string (C), 2nd... |
| 5 | `visual_caption:mr_style_001_am_add11` | `mathrock_pdf` | 1.4178 | Math Rock 吉他教材 | 来源: Math Rock 吉他教材 / mathrock_pdf 视觉角色: style_visual_evidence 页码: 33 图像类型: chord_diagram 主题: FACGCE_Am_add11_chord_shape 调弦: FACGCE 调性: A minor 根音: A 和弦: Am(add11), Am+11 音程: add11 技法: mute_high_strings 指型: open_position_shape 弦组: 6 strings (low 4 active, hig... |

## KG Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| - | - | - | - | - | - |

## Bundle Judgement

```json
{
  "sufficient": false,
  "confidence": 0.53,
  "missing": [],
  "warnings": [],
  "evidence_type_count": 1,
  "text_count": 0,
  "visual_count": 25,
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
  "top_text_ids": [],
  "top_visual_ids": [
    "visual_caption:mr_style_002",
    "visual_caption:mr_style_001_g7",
    "visual_caption:mr_style_001_fmaj9"
  ],
  "top_kg_ids": [],
  "composer_instruction": "只能基于 evidence_id 引用证据；区分教材明确内容与系统推断；如果 judgement.missing 非空，需要先说明证据不足。",
  "query_plan": {
    "raw_query": "FACGCE 调弦下的 数摇riff,G调要怎么设计",
    "normalized_query": "Design math rock riffs in G major using FACGCE tuning",
    "intent": "mixed_arrangement",
    "style_hints": [
      "mathrock"
    ],
    "target_tuning": "facgce",
    "target_keys": [
      "g_major"
    ],
    "target_roots": [
      "g"
    ],
    "scale_or_mode": [
      "major"
    ],
    "techniques": [
      "riff"
    ],
    "visual_evidence_required": true,
    "allow_alternate_tuning": true,
    "canonical_terms": [
      "tuning:facgce",
      "key:g_major",
      "root:g",
      "scale:major",
      "technique:riff"
    ],
    "required_terms": [
      "tuning:facgce",
      "key:g_major"
    ],
    "retrieval_plan": {
      "visual_caption": {
        "enabled": true,
        "query": "FACGCE tuning G major math rock riff chord shapes",
        "reason": "test"
      },
      "fretboard_text": {
        "enabled": false,
        "query": "",
        "reason": ""
      },
      "style_text": {
        "enabled": false,
        "query": "",
        "reason": ""
      },
      "kg": {
        "enabled": false,
        "query": "",
        "reason": ""
      }
    }
  },
  "visual_collection": "guitar_visual_mixed_mathrock_trial_qwen3_06b",
  "model_rerank": {
    "text": {
      "enabled": false,
      "provider": "none",
      "reason": "disabled"
    },
    "visual": {
      "enabled": false,
      "provider": "none",
      "reason": "disabled"
    },
    "kg": {
      "enabled": false,
      "provider": "none",
      "reason": "disabled"
    }
  }
}
```

## Timings

```json
{
  "model_load_seconds": 7.806453600001987,
  "visual_caption_seconds": 0.6082172000024002,
  "canonical_visual_seconds": 0.035792100010439754,
  "model_rerank_seconds": 3.470000228844583e-05,
  "total_seconds": 9.548131000017747
}
```
