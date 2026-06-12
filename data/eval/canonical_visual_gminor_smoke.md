# Query RAG Bundle Report

- Query: 给出G小调的吉他指型参考
- Intent: `visual_shape_recommendation`
- Sufficient: `True`
- Confidence: 0.71
- Total latency: 5.440s

## Query Analysis

```json
{
  "query": "G minor scale guitar fingerings and position diagrams",
  "intent": "visual_shape_recommendation",
  "style_hints": [],
  "theory_terms": [],
  "technique_terms": [],
  "needs_fretboard_text": true,
  "needs_visual": true,
  "needs_style_text": false,
  "needs_kg": false,
  "confidence": 0.9,
  "matched_rules": [
    "llm_plan:fretboard_text",
    "llm_plan:visual_caption"
  ]
}
```

## Retrieval Plan

| Name | Backend | Collection | TopK | Reason | Query |
|---|---|---|---:|---|---|
| `fretboard_text` | `chroma` | `guitar_fretboard_handbook_text_qwen3_06b` | 5 | 指板文本解释 G 小调音阶与把位逻辑 | G minor scale guitar fingerings and fretboard positions |
| `visual_caption` | `chroma` | `guitar_fretboard_answer_captions_qwen3_06b` | 5 | 需要具体指型图证据 | G minor scale pattern fingering diagram |

## Text Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `text:fretboard_text_0162` | `fretboard_handbook_clean_text` | 1.1409 | 吉他指板手册正文清洗层 | ## 练习50 2)和弦Bb9 指型4或5 3）和弦Gmi11 P指型1 [图示引用 6 张，详见 image_refs] |
| 2 | `text:fretboard_text_0037` | `fretboard_handbook_clean_text` | 0.8366 | 吉他指板手册正文清洗层 | ## 练习12 利用大调音阶公式并根据下图中给出的根音画出各大调音阶指型中的其他音符。画音符时，不要按照品位标记进行，要尽可能使用最小的把位移动。圈出指型中的所有根音，并且用指型的序号标记出来。 2 G大调指型\_ 3)C大调指型一 = 51 Bb大调指型\_ = G大调指型 IV A大调指型\_ 8 Gb大调指型 I三I 101 Eb大调指型 三 弹奏每种指型。先大声说出每种音阶的名称和指型的序号。弹奏的时候也可以同时说出音符在音阶中的级数（第1一7级）。从每种指型中最低的根音开始弹奏，然后弹至最高的音符，接着... |
| 3 | `text:fretboard_text_0044` | `fretboard_handbook_clean_text` | 0.8330 | 吉他指板手册正文清洗层 | ## 练习14 回到练习13。在每种指型上方用圆括号写出它的关系大调。在指型图中用方形画出其关系大调的根音。下面是第一个指型的例子。 E小调指型5(G大调指型4） 再次弹奏练习13中的各种指型。首先从小调音阶的根音弹奏这个指型，然后从其关系大调音阶的根音开始弹奏。弹奏之前先大声说出每种指型的序号。 [图示引用 1 张，详见 image_refs] |
| 4 | `text:fretboard_text_0028` | `fretboard_handbook_clean_text` | 0.8254 | 吉他指板手册正文清洗层 | ## 练习10 在正确的弦上，画出指板图上方所写的音符。可以运用自然音阶推算的方法，也可以采用五种根音指型的方法。有时可能需要运用各种不同的方法： ·从每根弦的空弦音向上推算 ·从每根弦的第12品向下推算 ·从另外一个熟悉的音符（比如，第7品的D音）向上或者向下推算 ·选择一个临近的音符（比如E音)，首先找到它所在的位置 F VI 2) F# IV II G V A V Eb VII B 三 Db XI 10) C xV [图示引用 10 张，详见 image_refs] |
| 5 | `text:fretboard_text_0033` | `fretboard_handbook_clean_text` | 0.8233 | 吉他指板手册正文清洗层 | ## 练习11 在下图中，以给出的音符为起始音，在一根弦上写出相应的大调音阶。注意应用大调音阶公式和字母表规则。在写出音符的同时大声朗读出来。 2) 4) 5) 10） 现在弹奏上面指板图中的音阶，注意在弹奏的同时要大声地说出音阶的名称和每个音符的名字：“d大调:D…E…·F#…G…A…B…C#…D…” [图示引用 10 张，详见 image_refs] |
| 6 | `text:fretboard_text_0118` | `fretboard_handbook_clean_text` | 0.8228 | 吉他指板手册正文清洗层 | ## 10） Bb13 指型 11)Fmi11(b5) XI 12)Cma13(#11) 三 13) G9 VlI 14)D11 15)Ami13 XI 弹奏以上练习中的琶音，演奏时大声说出和弦名称、指型序号和声部构成。 “G大九和弦，指型4，‘1、3、5、7、9... D小九和弦，指型” 在指板上构建延伸和弦时，采用与七和弦一样的方法：升高八度或者降低八度，以使每根琴弦上仅有一个和弦音。通常，让延伸音在和弦的最高处比较好。 之前也曾提到过，在指板上弹奏延伸和弦时，可以根据演奏者的需要，忽略部分音符，从而获得更好... |
| 7 | `text:fretboard_text_0133` | `fretboard_handbook_clean_text` | 0.7894 | 吉他指板手册正文清洗层 | ## 练习56 在下面的图示中画出E和声小调音阶的五种指型。 1）E和声小调 2)E和声小调 3)E和声小调 4）E和声小调 5）E和声小调 弹奏上面练习中的和声小调音阶指型。大声说出指型的序号，并且说出所弹奏的音在音阶中的级数。 [图示引用 5 张，详见 image_refs] |
| 8 | `text:fretboard_text_0041` | `fretboard_handbook_clean_text` | 0.7809 | 吉他指板手册正文清洗层 | ## 练习13 下面的指板图中给出了把位的标识和音阶的根音，在图中使用小调音阶公式构建相应的自然小调音阶指型。音符不要低于把位标识。圈出指型中的根音，标出音阶的名称和指型的序号。 E小调指型5 2 C小调指型\_ 3 E小调指型 4）\_小调指型\_ 51\_小调指型 VII 6 ）\_小调指型\_ = 7\_小调指型\_ V 8)\_小调指型\_ 91\_小调指型\_ VIII 10）\_小调指型\_ IV 弹奏上面每种小调音阶指型。大声说出音阶的名称和指型的序号。同样，弹奏的时候也从最低的根音开始，弹至最高音... |
| 9 | `text:fretboard_text_0045` | `fretboard_handbook_clean_text` | 0.7720 | 吉他指板手册正文清洗层 | ## 练习15 回到第7章中的练习12，在每种大调指型的上方标出其关系小调。然后用方形在指型图中画出其关系小调的根音。例如： D大调指型1 (B小调指型2) 再次弹奏练习12中的各种指型。首先从大调音阶的根音弹奏这个指型，然后从关系小调音阶的根音开始弹奏。弹奏之前先大声说出每种指型的序号。 [图示引用 1 张，详见 image_refs] |
| 10 | `text:fretboard_text_0142` | `fretboard_handbook_clean_text` | 0.7701 | 吉他指板手册正文清洗层 | ## 练习13 E小调指型5 2C小调指型2 E小调指型 A小调指型3 D小调指型3 小调指型4 小调指型 Bb小调指型3 小调指型2 F小调指型5 [图示引用 10 张，详见 image_refs] |

## Visual Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `visual_caption:fretboard_answer_E14_6` | `canonical_visual` | 5.2100 | G 小调指型 4 (Bb 大调指型 3) | 来源: 吉他指板手册 练习: 14 小题: 6 证据类型: fretboard_diagram 视觉类型: scale_pattern 对象: G 小调指型 4 (Bb 大调指型 3) 根音: G 性质/调式: minor / Aeolian 位置/指型: 指型 4 (Pattern 4) / Bb Major Pattern 3 答案项: 6: G 小调指型 4 (Bb 大调指型 3) 方向: horizontal 品位范围: 约为 3-7 品 可见标签: G 小调 指型 4, (Bb 大调 指型 3) 按点概... |
| 2 | `visual_caption:fretboard_answer_E15_5` | `canonical_visual` | 3.3100 | Bb Major Pattern 3 (G Minor Pattern 4) | 来源: 吉他指板手册 练习: 15 小题: 5 证据类型: fretboard_diagram 视觉类型: scale_pattern 对象: Bb Major Pattern 3 (G Minor Pattern 4) 根音: Bb / G 性质/调式: Major / Natural Minor 位置/指型: Pattern 3 / Pattern 4 方向: horizontal 把位: II 品位范围: unknown 可见标签: Bb 大调 指型 3, (G 小调 指型 4) 按点概述: 横向指板图，包... |
| 3 | `visual_caption:fretboard_answer_E14_8` | `fretboard_handbook_question_answer` | 1.2777 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 14 小题: 8 证据类型: fretboard_diagram 视觉类型: scale_pattern 对象: Bb minor 指型3 (Db major 指型2) 根音: Bb 性质/调式: minor / relative major Db 位置/指型: Shape 3 (Minor) / Shape 2 (Major), Position III 答案项: 8: Bb 小调 指型3 (Db 大调 指型2) 方向: horizontal 把位: III 品位范围: unkno... |
| 4 | `visual_caption:fretboard_answer_E05_1` | `fretboard_handbook_question_answer` | 1.0373 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 5 小题: 1 证据类型: fretboard_diagram 视觉类型: scale_pattern 对象: C大调音阶指型1 (C Major Scale Pattern 1) 根音: C 性质/调式: Major / Ionian 位置/指型: Pattern 1 (指型1) 答案项: 1: Pattern 1 diagram shown 方向: horizontal 品位范围: 3rd-7th frets (approx) 可见标签: 1), 4, 5, 1, 2, 3, 4... |
| 5 | `visual_caption:fretboard_answer_E57_2` | `fretboard_handbook_question_answer` | 1.0328 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 57 小题: 2 证据类型: fretboard_diagram 视觉类型: scale_pattern 对象: Ab旋律小调 指型2 根音: Ab 性质/调式: melodic minor 位置/指型: 指型2 (Pattern 2) 方向: vertical 可见标签: X 按点概述: 垂直指板图，显示Ab旋律小调指型2的按点分布。包含两个带双圈的主音（Root）标记，以及一个标有'X'的不可用弦位置。 caption: Ab旋律小调（Ab Melodic Minor）指型2的垂... |

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
  "text_count": 25,
  "visual_count": 26,
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
    "text:fretboard_text_0162",
    "text:fretboard_text_0037",
    "text:fretboard_text_0044"
  ],
  "top_visual_ids": [
    "visual_caption:fretboard_answer_E14_6",
    "visual_caption:fretboard_answer_E15_5",
    "visual_caption:fretboard_answer_E14_8"
  ],
  "top_kg_ids": [],
  "composer_instruction": "只能基于 evidence_id 引用证据；区分教材明确内容与系统推断；如果 judgement.missing 非空，需要先说明证据不足。",
  "query_plan": {
    "raw_query": "给出G小调的吉他指型参考",
    "normalized_query": "G minor scale guitar fingerings and position diagrams",
    "intent": "visual_shape_recommendation",
    "confidence": 0.9,
    "style_hints": [],
    "target_keys": [
      "G minor"
    ],
    "target_roots": [
      "G"
    ],
    "chord_qualities": [],
    "scale_or_mode": [
      "natural minor"
    ],
    "fret_region": "",
    "requires_exact_key": true,
    "requires_exact_chord": false,
    "visual_evidence_required": true,
    "allow_alternate_tuning": false,
    "canonical_terms": [
      "key:g_minor",
      "scale:natural_minor",
      "visual_type:scale_pattern"
    ],
    "required_terms": [
      "key:g_minor",
      "visual_type:scale_pattern"
    ],
    "optional_terms": [
      "scale:natural_minor"
    ],
    "negative_constraints": [
      "tuning:dadgad",
      "tuning:drop",
      "tuning:open"
    ],
    "techniques": [],
    "fretboard_constraints": [],
    "retrieval_plan": {
      "fretboard_text": {
        "enabled": true,
        "query": "G minor scale guitar fingerings and fretboard positions",
        "reason": "指板文本解释 G 小调音阶与把位逻辑"
      },
      "style_text": {
        "enabled": false,
        "query": "",
        "reason": "未指定风格"
      },
      "visual_caption": {
        "enabled": true,
        "query": "G minor scale pattern fingering diagram",
        "reason": "需要具体指型图证据"
      },
      "kg": {
        "enabled": false,
        "query": "",
        "reason": "静态指型参考不需要 KG"
      }
    }
  }
}
```

## Timings

```json
{
  "model_load_seconds": 4.181526900007157,
  "fretboard_text_seconds": 0.3179543000005651,
  "visual_caption_seconds": 0.18926610000198707,
  "canonical_visual_seconds": 0.023977600008947775,
  "total_seconds": 5.439929899992421
}
```
