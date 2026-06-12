# Qwen Reranker Smoke A/B Report

对同一批 query 分别运行 `RERANK_BACKEND=none` 与 `RERANK_BACKEND=local`。

## gminor_visual

- Query: 给出G小调的吉他指型参考

| Backend | Intent | Sufficient | Confidence | Total | Model Rerank | Top Visual | Top Text |
|---|---|---:|---:|---:|---:|---|---|
| none | `visual_shape_recommendation` | True | 0.71 | 4.887s | 0.000s | `visual_caption:fretboard_answer_E14_6` | `text:fretboard_text_0162` |
| local | `visual_shape_recommendation` | True | 0.71 | 3.645s | 3.558s | `visual_caption:fretboard_answer_E14_6` | `text:fretboard_text_0162` |

### Local rerank top evidence

#### Text

| Rank | Evidence | Score | Delta | Raw | Title |
|---:|---|---:|---:|---:|---|
| 1 | `text:fretboard_text_0162` | 1.4010 | 0.2601 | 1.0625 | 吉他指板手册正文清洗层 |
| 2 | `text:fretboard_text_0037` | 1.1320 | 0.2954 | 1.6875 | 吉他指板手册正文清洗层 |
| 3 | `text:fretboard_text_0044` | 1.0754 | 0.2424 | 0.8125 | 吉他指板手册正文清洗层 |
| 4 | `text:fretboard_text_0041` | 1.0279 | 0.2470 | 0.8750 | 吉他指板手册正文清洗层 |
| 5 | `text:fretboard_text_0042` | 1.0277 | 0.2758 | 1.3125 | 吉他指板手册正文清洗层 |

#### Visual

| Rank | Evidence | Score | Delta | Raw | Title |
|---:|---|---:|---:|---:|---|
| 1 | `visual_caption:fretboard_answer_E14_6` | 5.5582 | 0.3482 | 5.2500 | G 小调指型 4 (Bb 大调指型 3) |
| 2 | `visual_caption:fretboard_answer_E15_5` | 3.6583 | 0.3483 | 5.3125 | Bb Major Pattern 3 (G Minor Pattern 4) |
| 3 | `visual_caption:fretboard_answer_E14_8` | 1.6027 | 0.3249 | 2.5625 | 吉他指板手册：题目级练习答案图 |
| 4 | `visual_caption:fretboard_answer_E57_2` | 1.3641 | 0.3313 | 2.8750 | 吉他指板手册：题目级练习答案图 |
| 5 | `visual_caption:fretboard_answer_E57_5` | 1.3518 | 0.3264 | 2.6250 | 吉他指板手册：题目级练习答案图 |

#### KG

| Rank | Evidence | Score | Delta | Raw | Title |
|---:|---|---:|---:|---:|---|

## funk_groove

- Query: funk 十六分闷音 groove 伴奏怎么编

| Backend | Intent | Sufficient | Confidence | Total | Model Rerank | Top Visual | Top Text |
|---|---|---:|---:|---:|---:|---|---|
| none | `style_arrangement` | True | 0.71 | 0.800s | 0.000s | `-` | `text:chunk_0008` |
| local | `style_arrangement` | True | 0.71 | 2.193s | 2.115s | `-` | `text:chunk_0009` |

### Local rerank top evidence

#### Text

| Rank | Evidence | Score | Delta | Raw | Title |
|---:|---|---:|---:|---:|---|
| 1 | `text:chunk_0009` | 1.3298 | 0.2329 | 0.6875 | Cory Wong Funk 吉他大师课 |
| 2 | `text:chunk_0008` | 1.1152 | 0.0116 | -3.3750 | Cory Wong Funk 吉他大师课 |
| 3 | `text:chunk_0011` | 1.0972 | 0.0063 | -4.0000 | Cory Wong Funk 吉他大师课 |
| 4 | `text:chunk_0007` | 1.0739 | 0.0030 | -4.7500 | Cory Wong Funk 吉他大师课 |
| 5 | `text:chunk_0004` | 1.0159 | 0.0156 | -3.0625 | Cory Wong Funk 吉他大师课 |

#### Visual

| Rank | Evidence | Score | Delta | Raw | Title |
|---:|---|---:|---:|---:|---|

#### KG

| Rank | Evidence | Score | Delta | Raw | Title |
|---:|---|---:|---:|---:|---|
| 1 | `kg:technique:upstroke_hit_downstroke:ENABLES:feature:percussive_ghost_note` | 2.0882 | 0.2682 | 1.1875 | technique:upstroke_hit_downstroke -[ENABLES]-> feature:percussive_ghost_note |
| 2 | `kg:task:funk_comping:ENABLES:technique:m7_to_m6_voice_leading` | 1.8877 | 0.3277 | 2.6875 | task:funk_comping -[ENABLES]-> technique:m7_to_m6_voice_leading |
| 3 | `kg:feature:staccato_bubble:ENABLES:heuristic:make_rhythm_part_a_hook` | 1.8858 | 0.2758 | 1.3125 | feature:staccato_bubble -[ENABLES]-> heuristic:make_rhythm_part_a_hook |
| 4 | `kg:technique:right_hand_constant_motion:ENABLES:feature:sixteenth_note_undercurrent` | 1.7979 | 0.2179 | 0.5000 | technique:right_hand_constant_motion -[ENABLES]-> feature:sixteenth_note_undercurrent |
| 5 | `kg:voicing:sparse_funk_voicing:CONSTRAINS:caution:overcrowded_frequency_range` | 1.7374 | 0.2074 | 0.3750 | voicing:sparse_funk_voicing -[CONSTRAINS]-> caution:overcrowded_frequency_range |

## mathrock_fmaj7

- Query: Fmaj7 做 mathrock riff 怎么结合开放弦和高把位指型

| Backend | Intent | Sufficient | Confidence | Total | Model Rerank | Top Visual | Top Text |
|---|---|---:|---:|---:|---:|---|---|
| none | `mixed_arrangement` | True | 0.89 | 0.242s | 0.000s | `visual_caption:fretboard_answer_E44_6` | `text:chunk_0010` |
| local | `mixed_arrangement` | True | 0.89 | 4.810s | 4.608s | `visual_caption:fretboard_answer_E44_6` | `text:chunk_0010` |

### Local rerank top evidence

#### Text

| Rank | Evidence | Score | Delta | Raw | Title |
|---:|---|---:|---:|---:|---|
| 1 | `text:chunk_0010` | 1.6886 | 0.3235 | 2.5000 | Math Rock Guitar E-book |
| 2 | `text:chunk_0009` | 1.5199 | 0.3035 | 1.8750 | Math Rock Guitar E-book |
| 3 | `text:chunk_0004` | 1.5067 | 0.2794 | 1.3750 | mathrock教学课 |
| 4 | `text:chunk_0002` | 1.3336 | 0.3334 | 3.0000 | mathrock教学课 |
| 5 | `text:chunk_0006` | 1.2970 | 0.3166 | 2.2500 | mathrock教学课 |

#### Visual

| Rank | Evidence | Score | Delta | Raw | Title |
|---:|---|---:|---:|---:|---|
| 1 | `visual_caption:fretboard_answer_E44_6` | 1.4182 | 0.2280 | 0.6250 | 吉他指板手册：题目级练习答案图 |
| 2 | `visual_caption:fretboard_answer_E38_4` | 1.3776 | 0.2074 | 0.3750 | 吉他指板手册：题目级练习答案图 |
| 3 | `visual_caption:fretboard_answer_E38_2` | 1.3118 | 0.2280 | 0.6250 | 吉他指板手册：题目级练习答案图 |
| 4 | `visual_caption:fretboard_answer_E38_3` | 1.2425 | 0.1750 | 0.0000 | 吉他指板手册：题目级练习答案图 |
| 5 | `visual_caption:fretboard_answer_E24_3` | 1.2220 | 0.2179 | 0.5000 | 吉他指板手册：题目级练习答案图 |

#### KG

| Rank | Evidence | Score | Delta | Raw | Title |
|---:|---|---:|---:|---:|---|
| 1 | `kg:chord:m7b5:ENABLES:guitar_idiom:rootless_shell_voicing_on_4_strings` | 1.6426 | 0.1426 | -0.3750 | chord:m7b5 -[ENABLES]-> guitar_idiom:rootless_shell_voicing_on_4_strings |
| 2 | `kg:chord:shell_voicing:ENABLES:guitar_idiom:high_gain_riff_clarity` | 1.6142 | 0.0742 | -1.3125 | chord:shell_voicing -[ENABLES]-> guitar_idiom:high_gain_riff_clarity |
| 3 | `kg:tuning:DAEAC#E:ENABLES:voicing:open_string_maj9_cluster` | 1.5614 | 0.1914 | 0.1875 | tuning:DAEAC#E -[ENABLES]-> voicing:open_string_maj9_cluster |
| 4 | `kg:style:midwest_emo:EVOKES:feature:open_string_drone` | 1.4587 | 0.0187 | -2.8750 | style:midwest_emo -[EVOKES]-> feature:open_string_drone |
| 5 | `kg:chord:major_triad:SUGGESTS:pattern:caged_system_shapes` | 1.4117 | 0.0417 | -2.0000 | chord:major_triad -[SUGGESTS]-> pattern:caged_system_shapes |
