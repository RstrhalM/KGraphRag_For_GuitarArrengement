# Query RAG Bundle Report

- Query: Fmaj7 math rock riff
- Intent: `mixed_arrangement`
- Sufficient: `True`
- Confidence: 0.89
- Total latency: 6.211s

## Query Analysis

```json
{
  "query": "Fmaj7 琶音 math rock 开放弦 riff 指型 voicing",
  "intent": "mixed_arrangement",
  "style_hints": [
    "mathrock"
  ],
  "theory_terms": [
    "Fmaj7",
    "arpeggio",
    "voicing"
  ],
  "technique_terms": [
    "open string",
    "riff"
  ],
  "needs_fretboard_text": true,
  "needs_visual": true,
  "needs_style_text": true,
  "needs_kg": true,
  "confidence": 0.9,
  "matched_rules": [
    "llm_plan:fretboard_text",
    "llm_plan:style_text",
    "llm_plan:visual_caption",
    "llm_plan:kg"
  ]
}
```

## Retrieval Plan

| Name | Backend | Collection | TopK | Reason | Query |
|---|---|---|---:|---|---|
| `fretboard_text` | `chroma` | `guitar_fretboard_handbook_text_qwen3_06b` | 2 | 指板材料 | Fmaj7 琶音 指板 voicing |
| `style_text` | `chroma` | `guitar_text_chunks_qwen3_06b` | 2 | 风格材料 | math rock open string riff |
| `visual_caption` | `chroma` | `guitar_fretboard_answer_captions_qwen3_06b` | 2 | 视觉指型 | Fmaj7 arpeggio voicing 指型图 |
| `kg` | `neo4j_or_file` | `` | 8 | 关系启发 | Fmaj7 math rock riff 编配 |

## Text Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `text:chunk_0003` | `mathrock_text_course` | 1.0583 | mathrock教学课 | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is that because we can cheat better that way i... |
| 2 | `text:chunk_0006` | `mathrock_text_course` | 1.0372 | mathrock教学课 | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i didn't start with just an idea. I actually ... |
| 3 | `text:fretboard_text_0099` | `fretboard_handbook_clean_text` | 0.8478 | 吉他指板手册正文清洗层 | ## 练习38 在F大三和弦的基础上增加大七度音，并画出六根弦上D大七和弦琶音的五种指型，根音已圈出。 1）Fma7琶音 = 2)Fma7琶音 指型2 3)Fma7琶音 指型3 V VI 4)Fma7琶音 IX 5)Fma7琶音 XII 弹奏以上这些F大七和弦琶音，弹奏前先大声说出指型的序号。同时，要注意仔细体会大七和弦的色彩。 [图示引用 5 张，详见 image_refs] |
| 4 | `text:fretboard_text_0157` | `fretboard_handbook_clean_text` | 0.8347 | 吉他指板手册正文清洗层 | ## 练习38 1）Fma7琶音 指型5 2）Fma7琶音指型1 3）Fma7琶音 指型2 4）Fma7琶音 指型3 5)Fma7琶音 指型4 [图示引用 5 张，详见 image_refs] |

## Visual Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `visual_caption:fretboard_answer_E41_2` | `fretboard_handbook_question_answer` | 0.8693 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 41 小题: 2 证据类型: fretboard_diagram 视觉类型: arpeggio_pattern 对象: Fmi7(b5) 琶音 指型5 根音: F 性质/调式: minor seventh flat five (half-diminished) 位置/指型: 指型 5 方向: horizontal 可见标签: 2) Fmi7(b5) 琶音, 指型 5 按点概述: 横向六线谱，包含6个实心按点（其中两个带双圈标记为根音），分布在约第8至11品区域（推断）。 captio... |
| 2 | `visual_caption:fretboard_answer_E38_2` | `fretboard_handbook_question_answer` | 0.8609 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 38 小题: 2 证据类型: fretboard_diagram 视觉类型: arpeggio_pattern 对象: Fma7 琶音 指型1 根音: F 性质/调式: major seventh arpeggio 位置/指型: 指型1 (Shape 1) 音程: Root, Major 3rd, Perfect 5th, Major 7th 方向: horizontal 品位范围: 约为 1-4 品 可见标签: 2) Fma7 琶音, 指型 1 按点概述: 六线谱横向指板图，包含8... |

## KG Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `kg:chord:shell_voicing:ENABLES:guitar_idiom:high_gain_riff_clarity` | `GuitarIdiom` | 1.5300 | chord:shell_voicing -[ENABLES]-> guitar_idiom:high_gain_riff_clarity | chord:shell_voicing -[ENABLES]-> guitar_idiom:high_gain_riff_clarity 编配高增益（High Gain/Distortion）吉他 Riff 或声部时 图示展示了省略五音、仅保留根/三/七音的 Shell Voicing。这种稀疏排列能有效避免失真音色下的低频浑浊，是 Math Rock 中构建清晰、有力 Riff 的核心手段。 Page 61 diagrams show Dm7/G7 shell voicings (Root-3rd-7th on... |
| 2 | `kg:tuning:DAEAC#E:ENABLES:voicing:open_string_maj9_cluster` | `GuitarIdiom` | 1.4500 | tuning:DAEAC#E -[ENABLES]-> voicing:open_string_maj9_cluster | tuning:DAEAC#E -[ENABLES]-> voicing:open_string_maj9_cluster 编配 DAEAC#E 调弦下的和声织体时 图示显示该调弦下，利用空弦（D-A-E-A-C#-E）可轻松构建包含根音、3音、7音及9音的 Maj9 和弦，且无需大跨度指法。这种 Voicing 利用了调弦特性产生的自然共鸣，适合 Math Rock 中清澈、延音长的背景铺底。 Page 38 diagrams show Dmaj9 and Amaj9 shapes utilizing multi... |
| 3 | `kg:tuning:DADGAD:ENABLES:heuristic:ringing_open_string_anchor` | `GuitarIdiom` | 1.4500 | tuning:DADGAD -[ENABLES]-> heuristic:ringing_open_string_anchor | tuning:DADGAD -[ENABLES]-> heuristic:ringing_open_string_anchor Math Rock/Midwest Emo riffs requiring sustained harmonic beds while moving melodic shapes. DADGAD tuning allows open strings (D, A, D) to act as common tones/pedal points within the key of D mino... |

## Bundle Judgement

```json
{
  "sufficient": true,
  "confidence": 0.89,
  "missing": [],
  "warnings": [],
  "evidence_type_count": 3,
  "text_count": 4,
  "visual_count": 2,
  "kg_count": 8,
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
    "text:chunk_0003",
    "text:chunk_0006",
    "text:fretboard_text_0099"
  ],
  "top_visual_ids": [
    "visual_caption:fretboard_answer_E41_2",
    "visual_caption:fretboard_answer_E38_2"
  ],
  "top_kg_ids": [
    "kg:chord:shell_voicing:ENABLES:guitar_idiom:high_gain_riff_clarity",
    "kg:tuning:DAEAC#E:ENABLES:voicing:open_string_maj9_cluster",
    "kg:tuning:DADGAD:ENABLES:heuristic:ringing_open_string_anchor",
    "kg:technique:tapped_power_chord:CAN_INSPIRE:task:math_rock_riff_writing",
    "kg:tuning:drop_b_fsharp:ENABLES:feature:open_string_drone"
  ],
  "composer_instruction": "只能基于 evidence_id 引用证据；区分教材明确内容与系统推断；如果 judgement.missing 非空，需要先说明证据不足。",
  "query_plan": {
    "fretboard_constraints": [
      "voicing"
    ],
    "techniques": [
      "open string",
      "riff"
    ],
    "melodic_materials": [
      "arpeggio"
    ],
    "intent": "mixed_arrangement",
    "harmonic_materials": [
      "Fmaj7"
    ],
    "confidence": 0.9,
    "raw_query": "Fmaj7 math rock riff",
    "style_hints": [
      "mathrock"
    ],
    "normalized_query": "Fmaj7 琶音 math rock 开放弦 riff 指型 voicing",
    "retrieval_plan": {
      "style_text": {
        "query": "math rock open string riff",
        "reason": "风格材料",
        "enabled": true
      },
      "visual_caption": {
        "query": "Fmaj7 arpeggio voicing 指型图",
        "reason": "视觉指型",
        "enabled": true
      },
      "kg": {
        "query": "Fmaj7 math rock riff 编配",
        "reason": "关系启发",
        "enabled": true
      },
      "fretboard_text": {
        "query": "Fmaj7 琶音 指板 voicing",
        "reason": "指板材料",
        "enabled": true
      }
    },
    "arrangement_goals": [
      "推荐指型和风格写法"
    ]
  }
}
```

## Timings

```json
{
  "model_load_seconds": 4.530292700001155,
  "fretboard_text_seconds": 0.33640569999988656,
  "style_text_seconds": 0.07020689999626484,
  "visual_caption_seconds": 0.19386970000050496,
  "kg_seconds": 0.3473548000038136,
  "total_seconds": 6.211070000004838,
  "kg_status": "neo4j"
}
```
