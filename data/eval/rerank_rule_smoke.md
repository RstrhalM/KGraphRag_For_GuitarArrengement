# Query RAG Bundle Report

- Query: D 大调旋律想转成 B 小调色彩时，有没有同把位指型可以参考，并说明适合怎样的 riff 写法？
- Intent: `mixed_arrangement`
- Sufficient: `True`
- Confidence: 0.89
- Total latency: 6.945s

## Query Analysis

```json
{
  "query": "D 大调旋律想转成 B 小调色彩时，有没有同把位指型可以参考，并说明适合怎样的 riff 写法？",
  "intent": "mixed_arrangement",
  "style_hints": [],
  "theory_terms": [
    "B",
    "D",
    "大调",
    "小调",
    "指型"
  ],
  "technique_terms": [
    "riff"
  ],
  "needs_fretboard_text": true,
  "needs_visual": true,
  "needs_style_text": true,
  "needs_kg": true,
  "confidence": 0.85,
  "matched_rules": [
    "fretboard_terms",
    "visual_terms",
    "style_or_technique_terms",
    "arrangement_or_relation_terms"
  ]
}
```

## Retrieval Plan

| Name | Backend | Collection | TopK | Reason | Query |
|---|---|---|---:|---|---|
| `fretboard_text` | `chroma` | `guitar_fretboard_handbook_text_qwen3_06b` | 5 | 指板/理论/练习题干证据 | D 大调旋律想转成 B 小调色彩时，有没有同把位指型可以参考，并说明适合怎样的 riff 写法？ |
| `visual_caption` | `chroma` | `guitar_fretboard_answer_captions_qwen3_06b` | 5 | 具体图形/指法/voicing/答案图证据 | D 大调旋律想转成 B 小调色彩时，有没有同把位指型可以参考，并说明适合怎样的 riff 写法？ 指型图 和弦图 voicing |
| `style_text` | `chroma` | `guitar_text_chunks_qwen3_06b` | 5 | 风格/riff/节奏/技法文本证据 | D 大调旋律想转成 B 小调色彩时，有没有同把位指型可以参考，并说明适合怎样的 riff 写法？ |
| `kg` | `neo4j_or_file` | `` | 8 | 技法关系/风格迁移/编配启发 | D 大调旋律想转成 B 小调色彩时，有没有同把位指型可以参考，并说明适合怎样的 riff 写法？ B D 大调 小调 指型 riff |

## Text Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `text:chunk_0003` | `cory_wong_funk_core` | 1.2407 | Cory Wong Funk 吉他大师课 | this next series of lessons is about cord voicings and cord moves that I use in my playing.especially,in the context of funk,music now most of these voice o icings start from the caged system if you're not familiar with the caged system.there's an introductio... |
| 2 | `text:chunk_0006` | `mathrock_text_course` | 1.0862 | mathrock教学课 | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i didn't start with just an idea. I actually ... |
| 3 | `text:fretboard_text_0045` | `fretboard_handbook_clean_text` | 1.0405 | 吉他指板手册正文清洗层 | ## 练习15 回到第7章中的练习12，在每种大调指型的上方标出其关系小调。然后用方形在指型图中画出其关系小调的根音。例如： D大调指型1 (B小调指型2) 再次弹奏练习12中的各种指型。首先从大调音阶的根音弹奏这个指型，然后从关系小调音阶的根音开始弹奏。弹奏之前先大声说出每种指型的序号。 [图示引用 1 张，详见 image_refs] |
| 4 | `text:fretboard_text_0143` | `fretboard_handbook_clean_text` | 1.0035 | 吉他指板手册正文清洗层 | ## 练习15 D大调指型1（B小调指型2） G大调指型4（E小调指型5） C大调指型2（A小调指型3） E大调指型5（C#小调指型1） Bb大调指型3（G小调指型4） [图示引用 5 张，详见 image_refs] |
| 5 | `text:chunk_0010` | `mathrock_pdf_steve_h` | 0.9757 | Math Rock Guitar E-book | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V - ii - vi 5. G⼤调 - B⼩调 - C⼤调 - C⼩调 = G⼤... |
| 6 | `text:md_chunk_0021` | `fretboard_handbook_mineru` | 0.9636 | 吉他指板手册 | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边构建C小调的两个和弦若干次： [IMAGE_BLOCK:images/82991... |
| 7 | `text:chunk_0009` | `mathrock_pdf_steve_h` | 0.9550 | Math Rock Guitar E-book | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是我常⽤的七和弦壳式按法指型，许多数学摇滚⻛格的乐队也广泛使⽤这些指型。 ⼤七和弦... |
| 8 | `text:fretboard_text_0033` | `fretboard_handbook_clean_text` | 0.9343 | 吉他指板手册正文清洗层 | ## 练习11 在下图中，以给出的音符为起始音，在一根弦上写出相应的大调音阶。注意应用大调音阶公式和字母表规则。在写出音符的同时大声朗读出来。 2) 4) 5) 10） 现在弹奏上面指板图中的音阶，注意在弹奏的同时要大声地说出音阶的名称和每个音符的名字：“d大调:D…E…·F#…G…A…B…C#…D…” [图示引用 10 张，详见 image_refs] |
| 9 | `text:fretboard_text_0121` | `fretboard_handbook_clean_text` | 0.9311 | 吉他指板手册正文清洗层 | 学习目标：在指板上构建变化和弦。 当和弦中的音符或者延伸音出现升降的情况时就形成了变化和弦。变化和弦经常出现在属和弦和一些大和弦中。变化和弦的规则同样适用于变化和弦的琶音。 常用的变化和弦的音符有：b5、#5、b9、#9、#11和b13。通常将这些音符应写在圆括号里，避免同和弦的根音混淆。例如： B(b5)=B大三和弦和b5=1、3、b5 (B-D-F) Bb5=Bb强力和弦（仅根音和五度音）=1、5（B-F) |
| 10 | `text:fretboard_text_0079` | `fretboard_handbook_clean_text` | 0.9194 | 吉他指板手册正文清洗层 | ## 练习30 运用五种大调音阶指型中的音符，构建D大三和弦琶音的五种指型。注意不要使用品位标记以下的音符，并且在画出音符时，保证所有的音符都在左手所在的把位以内，最多不要超出1品以外。 1）D大三和弦琶音 指型1 2)D大三和弦琶音 指型2 3)D大三和弦琶音 = 指型3 4)D大三和弦琶音 IV VII 指型4 5)D大三和弦琶音 指型5 IX 弹奏以上这些D大三和弦琶音，演奏时要大声说出和弦名称及指型序号。弹奏时，从每一指型中最低的根音开始，弹至最高音，再向下弹至最低音，最后回到根音。同时，要注意仔细聆听琶... |

## Visual Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `visual_caption:fretboard_answer_E15_8` | `fretboard_handbook_question_answer` | 1.4967 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 15 小题: 8 证据类型: fretboard_diagram 视觉类型: mode_fretboard_map 对象: Gb 大调指型 5 (Eb 小调指型 1) 根音: Gb / Eb 性质/调式: Major / Minor 位置/指型: 指型 5 / 指型 1 方向: horizontal 把位: III 可见标签: Gb 大调 指型 5, Eb 小调 指型 1 按点概述: 横向指板图，罗马数字 III 标记把位。图中包含实心圆点（音阶音）和带方框的圆点（根音）。根据标题推... |
| 2 | `visual_caption:fretboard_answer_E12_1` | `fretboard_handbook_question_answer` | 1.4202 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 12 小题: 1 证据类型: fretboard_diagram 视觉类型: scale_pattern 对象: D大调 指型1 根音: D 性质/调式: Major Scale (Ionian) 位置/指型: 指型1 (Pattern 1) 方向: horizontal 品位范围: 约为第5-8品 可见标签: 1) D大调 指型1 按点概述: 图中展示了D大调音阶在指板上的分布，包含多个按点（黑点）和两个圈出的根音（Root notes）。根据D大调指型1的常见把位推断，根音位于5... |
| 3 | `visual_caption:fretboard_answer_E19_2` | `fretboard_handbook_question_answer` | 1.3967 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 19 小题: 2 证据类型: fretboard_diagram 视觉类型: scale_pattern 对象: Bb 小调五声音阶 指型4 / Db 大调五声音阶 指型3 根音: Bb 性质/调式: minor pentatonic 位置/指型: 指型4 (Shape 4) 答案项: 2: Bb 小调五声音阶 指型4 方向: vertical 把位: V 可见标签: Bb 小调五声音阶, 指型 4, Db 大调五声音阶, 指型 3 按点概述: 垂直指板图，第5把位（罗马数字V）。包... |
| 4 | `visual_caption:fretboard_answer_E14_8` | `fretboard_handbook_question_answer` | 1.3749 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 14 小题: 8 证据类型: fretboard_diagram 视觉类型: scale_pattern 对象: Bb minor 指型3 (Db major 指型2) 根音: Bb 性质/调式: minor / relative major Db 位置/指型: Shape 3 (Minor) / Shape 2 (Major), Position III 答案项: 8: Bb 小调 指型3 (Db 大调 指型2) 方向: horizontal 把位: III 品位范围: unkno... |
| 5 | `visual_caption:fretboard_answer_E22_9_part2` | `fretboard_handbook_question_answer` | 1.3315 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 22 小题: 9 证据类型: fretboard_diagram 视觉类型: scale_pattern 对象: Bb 小调五声音阶指型2 / Db 大调五声音阶指型1 根音: Bb, Db 性质/调式: minor pentatonic, major pentatonic 位置/指型: 指型2 (XIII把位), 指型1 答案项: 1: Bb 小调五声音阶 指型2; 2: Db 大调五声音阶 指型1 方向: vertical 把位: XIII 品位范围: 约为 13-16品 可见标... |

## KG Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `kg:concept:standard_tuning:CONSTRAINS:pattern:interval_geometry_shift` | `GuitarIdiom` | 1.4800 | concept:standard_tuning -[CONSTRAINS]-> pattern:interval_geometry_shift | concept:standard_tuning -[CONSTRAINS]-> pattern:interval_geometry_shift 在指板上构建双音（Double Stops）、和弦Voicing或跨弦Riff时，涉及第2弦（B弦）与第3弦（G弦）的交互。 吉他标准调弦中唯一的非四度关系（G-B大三度）导致所有跨越这两根弦的音程指法发生几何偏移。编曲时必须应用'补偿规则'：同度/八度需调整品位差，纯四/五度、大六/七度的指型在跨越2-3弦时需额外移动1品（通常是向高音方向多移1品或向低音方向少移1品）... |
| 2 | `kg:scale:pentatonic_minor:SUGGESTS:pattern:box_1_root_on_6th_string_heavy_riffing` | `GuitarIdiom` | 1.4700 | scale:pentatonic_minor -[SUGGESTS]-> pattern:box_1_root_on_6th_string_heavy_rif... | scale:pentatonic_minor -[SUGGESTS]-> pattern:box_1_root_on_6th_string_heavy_riffing 编写摇滚/金属风格的强力和弦（Power Chord）衔接或低音Riff时 练习17/19/21显示，小调五声指型1（Box 1）的根音位于6弦和5弦。该指型几何结构与强力和弦指法高度重合。编曲时应利用此特性，在失真音色下将单音Riff与双音强力和弦无缝切换，构建具有驱动力的低频声部。 练习17/19/21中小调五声指型1在6/5弦的低把位形态 |
| 3 | `kg:scale:pentatonic_major:ENABLES:heuristic:two_notes_per_string_geometry` | `GuitarIdiom` | 1.4400 | scale:pentatonic_major -[ENABLES]-> heuristic:two_notes_per_string_geometry | scale:pentatonic_major -[ENABLES]-> heuristic:two_notes_per_string_geometry 编配快速独奏乐句（licks）或跨弦 Riff 时 大调五声音阶在吉他指板上呈现“每根弦2个音符”的几何规律。这种对称性消除了七声音阶中常见的“3-2”或“2-3”音符分布带来的指法切换障碍，极大简化了横向移动和跨弦演奏的物理难度，是构建高可玩性（playability）Solo的基础语汇。 在五声音阶的每种指型中，每根琴弦上都只有2个音符...这让五声音阶演奏起... |
| 4 | `kg:pattern:octave_shape_low_strings:CONSTRAINS:interval:major_7th_dissonance` | `Caution` | 1.4300 | pattern:octave_shape_low_strings -[CONSTRAINS]-> interval:major_7th_dissonance | pattern:octave_shape_low_strings -[CONSTRAINS]-> interval:major_7th_dissonance 在 D 弦和 G 弦上构建八度音程（Octave Riff）时 吉他指板物理特性导致 D/G 弦组的八度指型间距（4品）与 E/A/D 弦组（3品）不同。若在 D/G 弦错误使用 3 品间距，会奏出极不协和的大七度而非八度，这是编写跨弦 Riff 时的常见陷阱。 若在D弦和G弦起始时误⽤三品间距（⽽非四品），会产⽣不和谐的⼤七度音程 |
| 5 | `kg:concept:standard_tuning:CONSTRAINS:heuristic:interval_shift_exception_g2_b3` | `GuitarIdiom` | 1.4000 | concept:standard_tuning -[CONSTRAINS]-> heuristic:interval_shift_exception_g2_b3 | concept:standard_tuning -[CONSTRAINS]-> heuristic:interval_shift_exception_g2_b3 在指板上构建跨弦音阶、Riff或和弦Voicing时，计算相邻弦的音程位移 吉他标准调弦中，除第2弦(B)与第3弦(G)之间外，相邻弦的同音/同音程关系通常相差3品（全音）或4品（半音）。但在2-3弦组上，由于大三度调弦差异，该位移缩减为2品（全音）或3品（半音）。这是编配跨弦乐句时必须处理的几何异常点。 当从一根弦向上至另外一根弦时...通常是相差3品... |
| 6 | `kg:concept:fretboard_geometry:ENABLES:heuristic:octave_symmetry_at_12th_fret` | `GuitarIdiom` | 1.3900 | concept:fretboard_geometry -[ENABLES]-> heuristic:octave_symmetry_at_12th_fret | concept:fretboard_geometry -[ENABLES]-> heuristic:octave_symmetry_at_12th_fret 编配高把位独奏或和弦Voicing时，需要快速定位同音异弦位置 利用第12品与空弦音相同的八度对称性，可作为指板导航的绝对锚点。在编曲中，若需将低音线条移至高音区（如Octave Riff），可直接以12品为镜像参考，简化跨把位计算。 练习8图示及文字：'吉他弦的第12品和空弦的音符是相同的...可以从第12品向前推算' |
| 7 | `kg:concept:interval_mapping:CONSTRAINS:guitar_idiom:string_crossing_offset_rule` | `GuitarIdiom` | 1.3600 | concept:interval_mapping -[CONSTRAINS]-> guitar_idiom:string_crossing_offset_ru... | concept:interval_mapping -[CONSTRAINS]-> guitar_idiom:string_crossing_offset_rule 编配跨弦乐句、双音（Double Stops）或构建和弦 Voicing 时，需快速定位相邻弦上的音程指型。 提取了吉他指板的核心几何规则：除2-3弦因大三度定弦导致偏移量不同外，其他相邻弦的同度/音程指型具有统一的平移规律（如纯四度同品、纯五度+2品等）。这是编写流畅跨弦 Riff 和避免指法断裂的基础启发式规则。 纯四度在相邻的弦上为同一品...纯... |
| 8 | `kg:chord:shell_voicing:ENABLES:guitar_idiom:high_gain_riff_clarity` | `GuitarIdiom` | 1.2800 | chord:shell_voicing -[ENABLES]-> guitar_idiom:high_gain_riff_clarity | chord:shell_voicing -[ENABLES]-> guitar_idiom:high_gain_riff_clarity 编配高增益（High Gain/Distortion）吉他 Riff 或声部时 图示展示了省略五音、仅保留根/三/七音的 Shell Voicing。这种稀疏排列能有效避免失真音色下的低频浑浊，是 Math Rock 中构建清晰、有力 Riff 的核心手段。 Page 61 diagrams show Dm7/G7 shell voicings (Root-3rd-7th on... |
| 9 | `kg:concept:interval_geometry:CONSTRAINS:heuristic:2nd_string_offset_rule` | `GuitarIdiom` | 1.2800 | concept:interval_geometry -[CONSTRAINS]-> heuristic:2nd_string_offset_rule | concept:interval_geometry -[CONSTRAINS]-> heuristic:2nd_string_offset_rule 编配跨弦音程、双音（Double Stops）或构建和弦 Voicing 时 吉他指板在第3弦与第2弦之间存在大三度调弦差异。除同度音外，所有跨越这两根弦的音程指法均需进行“+1品”或“-1品”的几何修正（如纯五度在相邻弦为+2品，但在3-2弦间为+3品）。这是编写流畅跨弦 Riff 和避免按错音的核心物理约束。 练习23文本：'只要跨越了第2弦...由于2弦调弦方... |
| 10 | `kg:heuristic:make_rhythm_part_a_hook:EVOKES:task:riff_writing` | `GuitarIdiom` | 1.2800 | heuristic:make_rhythm_part_a_hook -[EVOKES]-> task:riff_writing | heuristic:make_rhythm_part_a_hook -[EVOKES]-> task:riff_writing Funk/Pop rhythm guitar comping where static strumming feels generic. Transform standard chord comping into a signature hook by integrating melodic lines (pentatonic/scale) within the chord shape,... |

## Bundle Judgement

```json
{
  "sufficient": true,
  "confidence": 0.89,
  "missing": [],
  "warnings": [],
  "evidence_type_count": 3,
  "text_count": 41,
  "visual_count": 25,
  "kg_count": 24,
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
    "text:fretboard_text_0045"
  ],
  "top_visual_ids": [
    "visual_caption:fretboard_answer_E15_8",
    "visual_caption:fretboard_answer_E12_1",
    "visual_caption:fretboard_answer_E19_2"
  ],
  "top_kg_ids": [
    "kg:concept:standard_tuning:CONSTRAINS:pattern:interval_geometry_shift",
    "kg:scale:pentatonic_minor:SUGGESTS:pattern:box_1_root_on_6th_string_heavy_riffing",
    "kg:scale:pentatonic_major:ENABLES:heuristic:two_notes_per_string_geometry",
    "kg:pattern:octave_shape_low_strings:CONSTRAINS:interval:major_7th_dissonance",
    "kg:concept:standard_tuning:CONSTRAINS:heuristic:interval_shift_exception_g2_b3"
  ],
  "composer_instruction": "只能基于 evidence_id 引用证据；区分教材明确内容与系统推断；如果 judgement.missing 非空，需要先说明证据不足。"
}
```

## Timings

```json
{
  "model_load_seconds": 5.236119199995301,
  "fretboard_text_seconds": 0.29146349999064114,
  "visual_caption_seconds": 0.2010273999912897,
  "style_text_seconds": 0.07258469999942463,
  "kg_seconds": 0.3695410000073025,
  "total_seconds": 6.945125500002177,
  "kg_status": "neo4j"
}
```
