# Query RAG Bundle Report

- Query: 给我一个Cmaj7两手点弦琶音谱例
- Intent: `mixed_arrangement`
- Sufficient: `True`
- Confidence: 0.89
- Total latency: 6.671s

## Query Analysis

```json
{
  "query": "Cmaj7 two-hand tapping arpeggio pattern diagram",
  "intent": "mixed_arrangement",
  "style_hints": [],
  "theory_terms": [
    "Cmaj7"
  ],
  "technique_terms": [
    "tapping",
    "点弦"
  ],
  "needs_fretboard_text": true,
  "needs_visual": true,
  "needs_style_text": false,
  "needs_kg": true,
  "confidence": 0.79,
  "matched_rules": [
    "llm_plan:fretboard_text",
    "llm_plan:visual_caption",
    "llm_plan:kg"
  ]
}
```

## Retrieval Plan

| Name | Backend | Collection | TopK | Reason | Query |
|---|---|---|---:|---|---|
| `fretboard_text` | `chroma` | `guitar_fretboard_handbook_text_qwen3_06b` | 5 | To retrieve theoretical basis and note composition of Cmaj7 arpeggios suitable for tapping. | Cmaj7 arpeggio notes and intervals for two-hand tapping technique |
| `visual_caption` | `chroma` | `guitar_visual_mixed_mathrock_trial_qwen3_06b` | 5 | User explicitly asked for a 'score/example' (谱例) of a specific physical technique (two-hand tapping), which requires visual evidence of finger positions and tapping points on the fretboard. | Cmaj7 two-hand tapping arpeggio pattern diagram fretboard map |
| `kg` | `neo4j_or_file` | `` | 8 | To provide arrangement heuristics and ergonomic constraints for executing two-hand tapping arpeggios effectively. | two-hand tapping arpeggio voicing constraints and ergonomic patterns for maj7 chords |

## Text Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `text:fretboard_text_0108` | `fretboard_handbook_clean_text` | 0.9220 | 吉他指板手册正文清洗层 | 学习目标：构建七和弦的常备声部。 前面我们已学习了密集和弦，实际上对于三和弦和七和弦而言，开放和弦有时更加悦耳好听并且更加容易弹奏。 对于七和弦来说，密集和弦有时在吉他上是很难弹奏的。按弦的手指有时够不到并按住全部的音符。例如，像Amaj7这样的密集和弦。 和弦中的音符在指板上的跨度太大，以致很难全部按住。同时，这样的和弦中也含有较多相近的低音，使得音色也会变得暗淡浑浊。 为了找到和弦中更有用的和弦音，常常需要将其中的某些音符升高或降低一个八度，这样就可以得到更加宽广的和弦声音。下面来尝试一下。密集大七和弦Ama... |
| 2 | `text:fretboard_text_0130` | `fretboard_handbook_clean_text` | 0.8438 | 吉他指板手册正文清洗层 | ## 练习 录制三分钟下面这些常用的调式和弦进行。演奏时不需要使用任何风格的节奏型，每个和弦仅用清音弹奏一下，然后使其一直在节拍器的四拍中发音即可，反复演奏直至录满三分钟。然后录下一个和弦进行。录完之后进行回放，找出每个和弦进行所对应的调式，并且跟着录下的和弦进行来弹奏。 IC IGIFIGI-C lonian ICma7IDl-C Lydian ICmi7 IF9 ICmi7IDmi7l-C Dorian ICmiIDb1-CPhrygian IC7IBbma7l-CMixolydian ICmiIBb IAb... |
| 3 | `text:fretboard_text_0114` | `fretboard_handbook_clean_text` | 0.8276 | 吉他指板手册正文清洗层 | ## 练习 弹奏本章中学过的所有声部构成，并且再次强调首先要掌握指型4和指型2的声部构成。 然后试着做这样的练习：任意选择一个和弦（比如ma7）和根音（比如C），演奏这个和弦所有指型的所有声部构成。从琴颈上的最低音弹奏到最高音。弹奏的同时，大声说出和弦的名称、指型的序号和声部构成，像这样： “C大七和弦，指型1，‘1、3、7、1’… C大七和弦，指型1，‘3、7、1、5.’. C大七和弦，指型2，‘1、5、3、3’ C大七和弦，指型3，‘5、1、3、7’ C大七和弦，指型4，‘1、7、3、5’ C大七和弦，指型5... |
| 4 | `text:fretboard_text_0119` | `fretboard_handbook_clean_text` | 0.8258 | 吉他指板手册正文清洗层 | ## 练习49 根据给出的声部构成，在下面的图示中构建延伸和弦。 5）F#7(#11) 6Db13 7）A13(#11) 8 E13 10）F9（#11) 弹奏上页练习中的延伸和弦，弹奏时大声说出和弦名称、指型序号和声部构成。 “C九和弦，指型1，‘1、3、b7、. G大十三和弦，指型4，‘1、3、7、13..” [图示引用 10 张，详见 image_refs] |
| 5 | `text:fretboard_text_0028` | `fretboard_handbook_clean_text` | 0.8185 | 吉他指板手册正文清洗层 | ## 练习10 在正确的弦上，画出指板图上方所写的音符。可以运用自然音阶推算的方法，也可以采用五种根音指型的方法。有时可能需要运用各种不同的方法： ·从每根弦的空弦音向上推算 ·从每根弦的第12品向下推算 ·从另外一个熟悉的音符（比如，第7品的D音）向上或者向下推算 ·选择一个临近的音符（比如E音)，首先找到它所在的位置 F VI 2) F# IV II G V A V Eb VII B 三 Db XI 10) C xV [图示引用 10 张，详见 image_refs] |
| 6 | `text:fretboard_text_0033` | `fretboard_handbook_clean_text` | 0.8109 | 吉他指板手册正文清洗层 | ## 练习11 在下图中，以给出的音符为起始音，在一根弦上写出相应的大调音阶。注意应用大调音阶公式和字母表规则。在写出音符的同时大声朗读出来。 2) 4) 5) 10） 现在弹奏上面指板图中的音阶，注意在弹奏的同时要大声地说出音阶的名称和每个音符的名字：“d大调:D…E…·F#…G…A…B…C#…D…” [图示引用 10 张，详见 image_refs] |
| 7 | `text:fretboard_text_0129` | `fretboard_handbook_clean_text` | 0.8081 | 吉他指板手册正文清洗层 | ## 练习54 写出各种调式的音阶，其中Ionian（大调）音阶和Aeolian（自然小调）音阶已经给出。可以参考以上练习中的指板指型，也可以参考之前学过的C大调（Ionian）音阶的全音和半音关系。 [图示引用 1 张，详见 image_refs] |
| 8 | `text:fretboard_text_0112` | `fretboard_handbook_clean_text` | 0.7606 | 吉他指板手册正文清洗层 | ## 练习46 运用指型1画出七和弦“3、7、1、5”的常用声部构成。 1）Dma7 2D7 3）Dmi7 4）Dmi7（b5) 5）Ddim7 某些指型1中的常用声部构成可去掉五度音，而增加一个八度音，这对于多数基本的和弦都是适用的。例如，这时的和弦声部构成为：1、3、7、1。但对于mi7(b5)和dim7和弦不适用，因为对于这两个和弦，b5是影响它们性质的重要音符。 [图示引用 5 张，详见 image_refs] |
| 9 | `text:fretboard_text_0110` | `fretboard_handbook_clean_text` | 0.7604 | 吉他指板手册正文清洗层 | ## 练习44 运用指型2和指型5画出七和弦“1、5、7、3”常用声部构成。 5）Cdim7 6)Fma7 9）Fmi7(b5） 10）Fdim7 [图示引用 10 张，详见 image_refs] |
| 10 | `text:fretboard_text_0099` | `fretboard_handbook_clean_text` | 0.7578 | 吉他指板手册正文清洗层 | ## 练习38 在F大三和弦的基础上增加大七度音，并画出六根弦上D大七和弦琶音的五种指型，根音已圈出。 1）Fma7琶音 = 2)Fma7琶音 指型2 3)Fma7琶音 指型3 V VI 4)Fma7琶音 IX 5)Fma7琶音 XII 弹奏以上这些F大七和弦琶音，弹奏前先大声说出指型的序号。同时，要注意仔细体会大七和弦的色彩。 [图示引用 5 张，详见 image_refs] |

## Visual Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `visual_caption:mr_style_010` | `canonical_visual` | 8.1600 | Cmaj7_tapping_arpeggio | 来源: Math Rock 吉他教材 / mathrock_pdf 视觉角色: style_visual_evidence 页码: 73 图像类型: tab_excerpt 主题: Cmaj7_tapping_arpeggio 调弦: standard 调性: C major 根音: C 和弦: Cmaj7 音程: major_7th, perfect_5th, major_3rd 技法: tapping, pull_off, hammer_on, let_ring, sustained_note 指型: T (... |
| 2 | `visual_caption:mr_style_015` | `canonical_visual` | 6.0800 | math_rock_I_IV_riff_irregular_meters | 来源: Math Rock 吉他教材 / mathrock_pdf 视觉角色: style_visual_evidence 页码: 78 图像类型: tab_excerpt 主题: math_rock_I_IV_riff_irregular_meters 调弦: standard 调性: C major 根音: C 和弦: Cmaj7, Fmaj7 技法: rapid_chord_changes, irregular_meter_grouping 指型: x32000, xx3210, x35453, xx356... |
| 3 | `visual_caption:fretboard_answer_E44_1` | `canonical_visual` | 4.1800 | Cma7 (1 5 7 3) | 来源: 吉他指板手册 练习: 44 小题: 1 证据类型: fretboard_diagram 视觉类型: chord_diagram 对象: Cma7 (1 5 7 3) 根音: C 性质/调式: major seventh 位置/指型: III (3rd position/fret) 音程: 1, 5, 7, 3 方向: vertical 把位: III 品位范围: unknown 可见标签: 1) Cma7, 1 5 7 3, III 按点概述: 垂直指板图，左侧标记罗马数字 III。根音(1)位于第5弦（... |
| 4 | `visual_caption:fretboard_answer_E24_3` | `canonical_visual` | 3.7100 | MA7 (Major 7th) chord shape | 来源: 吉他指板手册 练习: 24 小题: 3 证据类型: fretboard_diagram 视觉类型: chord_diagram 对象: MA7 (Major 7th) chord shape 根音: unknown 性质/调式: Major 7th 答案项: 3): MA7 方向: vertical 品位范围: 推断为开放把位或低把位 可见标签: 3), MA7 按点概述: 6弦空弦(推断)，5弦2品，4弦1品，3弦2品，2弦1品，1弦空弦(推断)。共6个按点/音。 caption: 题号3对应的和弦指法... |
| 5 | `visual_caption:fretboard_answer_E24_8` | `canonical_visual` | 3.7100 | MA7 chord shape | 来源: 吉他指板手册 练习: 24 小题: 8 证据类型: fretboard_diagram 视觉类型: chord_diagram 对象: MA7 chord shape 根音: unknown 性质/调式: Major 7th (MA7) 位置/指型: unknown 答案项: 8: MA7 方向: vertical 可见标签: 8), MA7 按点概述: 6个按点，分布在约5-6根弦上，呈不规则指型排列 caption: 练习24第8题答案图示。垂直吉他指板图，上方标注“MA7”，显示一个包含6个音符的大... |

## KG Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `kg:pattern:shell_voicing_1-7-3-5:SUGGESTS:concept:universal_heuristic` | `GuitarIdiom` | 1.2600 | pattern:shell_voicing_1-7-3-5 -[SUGGESTS]-> concept:universal_heuristic | pattern:shell_voicing_1-7-3-5 -[SUGGESTS]-> concept:universal_heuristic 构建指型4（根音在第6或第5弦）的七和弦常用声部时 提取了具体的通用声部排列逻辑 '1-7-3-5'（即根音、七音、三音、五音），适用于maj7, m7, dom7等多种七和弦类型，是高效的编曲启发式规则。 “1、7、3、5”是ma7、mi7、dom7、mi7(b5)和dim7这些和弦指型4中的常用声部构成。 |
| 2 | `kg:technique:register_specific_triads:CONSTRAINS:voicing:string_set_selection` | `GuitarIdiom` | 1.1900 | technique:register_specific_triads -[CONSTRAINS]-> voicing:string_set_selection | technique:register_specific_triads -[CONSTRAINS]-> voicing:string_set_selection Selecting voicings based on desired tonal range and interaction with other band members. Map triad shapes to specific string sets: Strings 1-2-3 (High/Bright), 2-3-4 (Mid), 3-4-5 ... |
| 3 | `kg:voicing:sparse_funk_voicing:SUGGESTS:heuristic:leave_space_for_band` | `GuitarIdiom` | 1.1900 | voicing:sparse_funk_voicing -[SUGGESTS]-> heuristic:leave_space_for_band | voicing:sparse_funk_voicing -[SUGGESTS]-> heuristic:leave_space_for_band Comping with 'chucks' (muted strums) in a dense band arrangement. Focus on 2-3 string voicings (e.g., minor 7th shapes) and vary the ratio of notes to muted 'chucks' to avoid frequency c... |
| 4 | `kg:heuristic:make_rhythm_part_a_hook:EVOKES:task:riff_writing` | `GuitarIdiom` | 1.1900 | heuristic:make_rhythm_part_a_hook -[EVOKES]-> task:riff_writing | heuristic:make_rhythm_part_a_hook -[EVOKES]-> task:riff_writing Funk/Pop rhythm guitar comping where static strumming feels generic. Transform standard chord comping into a signature hook by integrating melodic lines (pentatonic/scale) within the chord shape,... |
| 5 | `kg:tuning:DAEAC#E:ENABLES:voicing:open_string_maj9_cluster` | `GuitarIdiom` | 1.1800 | tuning:DAEAC#E -[ENABLES]-> voicing:open_string_maj9_cluster | tuning:DAEAC#E -[ENABLES]-> voicing:open_string_maj9_cluster 编配 DAEAC#E 调弦下的和声织体时 图示显示该调弦下，利用空弦（D-A-E-A-C#-E）可轻松构建包含根音、3音、7音及9音的 Maj9 和弦，且无需大跨度指法。这种 Voicing 利用了调弦特性产生的自然共鸣，适合 Math Rock 中清澈、延音长的背景铺底。 Page 38 diagrams show Dmaj9 and Amaj9 shapes utilizing multi... |
| 6 | `kg:style:midwest_emo:EVOKES:feature:open_string_drone` | `GuitarIdiom` | 1.1800 | style:midwest_emo -[EVOKES]-> feature:open_string_drone | style:midwest_emo -[EVOKES]-> feature:open_string_drone B minor 11 voicing utilizing open B (2nd string) and F# (1st/6th strings) as common tones while moving inner voices. Midwest Emo relies on 'jangly' textures created by sustaining open strings that act as... |
| 7 | `kg:extension:#11_or_b13:SUGGESTS:note:natural_5th_and_9th_inclusion` | `GuitarIdiom` | 1.1600 | extension:#11_or_b13 -[SUGGESTS]-> note:natural_5th_and_9th_inclusion | extension:#11_or_b13 -[SUGGESTS]-> note:natural_5th_and_9th_inclusion 构建含有 #11 或 b13 的变化和弦时 与 'alt' 和弦不同，当明确指定 #11 或 b13 时，除非特殊情况，否则应保留自然的五度音和九度音。这为吉他编曲提供了更丰富的声部连接可能性（如保留根-5-9骨架），增加了Voicing的丰满度，而非像alt和弦那样极度精简。 当和弦中出现#11或b13时，除特殊情况外，和弦中的五度音和九度音都是自然音。 |
| 8 | `kg:concept:standard_tuning:CONSTRAINS:pattern:interval_geometry_shift` | `GuitarIdiom` | 1.1600 | concept:standard_tuning -[CONSTRAINS]-> pattern:interval_geometry_shift | concept:standard_tuning -[CONSTRAINS]-> pattern:interval_geometry_shift 在指板上构建双音（Double Stops）、和弦Voicing或跨弦Riff时，涉及第2弦（B弦）与第3弦（G弦）的交互。 吉他标准调弦中唯一的非四度关系（G-B大三度）导致所有跨越这两根弦的音程指法发生几何偏移。编曲时必须应用'补偿规则'：同度/八度需调整品位差，纯四/五度、大六/七度的指型在跨越2-3弦时需额外移动1品（通常是向高音方向多移1品或向低音方向少移1品）... |
| 9 | `kg:concept:standard_tuning:CONSTRAINS:heuristic:interval_shift_exception_g2_b3` | `GuitarIdiom` | 1.1600 | concept:standard_tuning -[CONSTRAINS]-> heuristic:interval_shift_exception_g2_b3 | concept:standard_tuning -[CONSTRAINS]-> heuristic:interval_shift_exception_g2_b3 在指板上构建跨弦音阶、Riff或和弦Voicing时，计算相邻弦的音程位移 吉他标准调弦中，除第2弦(B)与第3弦(G)之间外，相邻弦的同音/同音程关系通常相差3品（全音）或4品（半音）。但在2-3弦组上，由于大三度调弦差异，该位移缩减为2品（全音）或3品（半音）。这是编配跨弦乐句时必须处理的几何异常点。 当从一根弦向上至另外一根弦时...通常是相差3品... |
| 10 | `kg:chord:dom7_alt:CONSTRAINS:note:natural_5th_and_9th_exclusion` | `Caution` | 1.1600 | chord:dom7_alt -[CONSTRAINS]-> note:natural_5th_and_9th_exclusion | chord:dom7_alt -[CONSTRAINS]-> note:natural_5th_and_9th_exclusion 编配标有 'alt' 的属和弦（如 G7alt）时 教材明确指出，当和弦标记为 'alt' 时，必须省略自然五度音和自然九度音。这是为了避免与变化延伸音（b5/#5, b9/#9）产生小二度冲突，确保和声色彩的清晰度。在吉他Voicing中，这意味着不能简单套用标准属七指型，需主动移除3弦或2弦上的自然5/9音。 但是在标有“alt”的和弦中，不会出现自然音阶的五度音和九度音。 |

## Bundle Judgement

```json
{
  "sufficient": true,
  "confidence": 0.89,
  "missing": [],
  "warnings": [],
  "evidence_type_count": 3,
  "text_count": 25,
  "visual_count": 36,
  "kg_count": 23,
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
    "text:fretboard_text_0108",
    "text:fretboard_text_0130",
    "text:fretboard_text_0114"
  ],
  "top_visual_ids": [
    "visual_caption:mr_style_010",
    "visual_caption:mr_style_015",
    "visual_caption:fretboard_answer_E44_1"
  ],
  "top_kg_ids": [
    "kg:pattern:shell_voicing_1-7-3-5:SUGGESTS:concept:universal_heuristic",
    "kg:technique:register_specific_triads:CONSTRAINS:voicing:string_set_selection",
    "kg:voicing:sparse_funk_voicing:SUGGESTS:heuristic:leave_space_for_band",
    "kg:heuristic:make_rhythm_part_a_hook:EVOKES:task:riff_writing",
    "kg:tuning:DAEAC#E:ENABLES:voicing:open_string_maj9_cluster"
  ],
  "composer_instruction": "只能基于 evidence_id 引用证据；区分教材明确内容与系统推断；如果 judgement.missing 非空，需要先说明证据不足。",
  "query_plan": {
    "raw_query": "给我一个Cmaj7两手点弦琶音谱例",
    "normalized_query": "Cmaj7 two-hand tapping arpeggio pattern diagram",
    "intent": "mixed_arrangement",
    "confidence": 0.79,
    "style_hints": [],
    "key_or_tonality": "",
    "meter_or_rhythm": "",
    "tempo_hint": "",
    "target_tuning": "standard",
    "harmonic_materials": [
      "Cmaj7"
    ],
    "melodic_materials": [],
    "techniques": [
      "tapping",
      "点弦"
    ],
    "fretboard_constraints": [],
    "arrangement_goals": [],
    "target_keys": [
      "c_major"
    ],
    "target_roots": [
      "c"
    ],
    "chord_qualities": [
      "maj7"
    ],
    "scale_or_mode": [],
    "fret_region": "",
    "position_constraints": [],
    "requires_exact_key": true,
    "requires_exact_chord": true,
    "visual_evidence_required": true,
    "allow_alternate_tuning": false,
    "allow_exercise_reference": true,
    "canonical_terms": [
      "key:c_major",
      "chord_quality:maj7",
      "technique:two_hand_tapping",
      "concept:arpeggio",
      "tuning:standard",
      "root:c",
      "visual_type:scale_pattern",
      "technique:tapping"
    ],
    "required_terms": [
      "tuning:standard",
      "key:c_major",
      "chord_quality:maj7",
      "visual_type:scale_pattern"
    ],
    "optional_terms": [
      "visual_type:scale_pattern"
    ],
    "negative_constraints": [
      "tuning:dadgad",
      "tuning:facgce",
      "tuning:drop",
      "tuning:drop_d",
      "tuning:open",
      "tuning:alternate"
    ],
    "retrieval_plan": {
      "fretboard_text": {
        "enabled": true,
        "query": "Cmaj7 arpeggio notes and intervals for two-hand tapping technique",
        "reason": "To retrieve theoretical basis and note composition of Cmaj7 arpeggios suitable for tapping."
      },
      "style_text": {
        "enabled": false,
        "query": "Cmaj7 two-hand tapping arpeggio pattern diagram",
        "reason": "User requested a specific technical example rather than a general style course, though tapping is common in math rock, the core request is technical/visual."
      },
      "visual_caption": {
        "enabled": true,
        "query": "Cmaj7 two-hand tapping arpeggio pattern diagram fretboard map",
        "reason": "User explicitly asked for a 'score/example' (谱例) of a specific physical technique (two-hand tapping), which requires visual evidence of finger positions and tapping points on the fretboard."
      },
      "kg": {
        "enabled": true,
        "query": "two-hand tapping arpeggio voicing constraints and ergonomic patterns for maj7 chords",
        "reason": "To provide arrangement heuristics and ergonomic constraints for executing two-hand tapping arpeggios effectively."
      }
    },
    "composer_intent": {
      "answer_type": "",
      "must_include": [],
      "avoid": [],
      "uncertainty_notes": []
    },
    "eval_tags": []
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
  "model_load_seconds": 4.905599699995946,
  "fretboard_text_seconds": 0.3265559999854304,
  "visual_caption_seconds": 0.20267769999918528,
  "kg_seconds": 0.35322329998598434,
  "canonical_visual_seconds": 0.03636569998343475,
  "model_rerank_seconds": 3.809999907389283e-05,
  "total_seconds": 6.671314200008055,
  "kg_status": "neo4j"
}
```
