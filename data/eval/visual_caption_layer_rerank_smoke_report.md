# Visual Caption Retrieval Trial

## Summary

- Collection: `guitar_visual_captions_qwen3_06b` (60 docs)
- Model: `models\embedding\qwen3-embedding-0.6b` on `cuda`, dim=1024
- Tests: 10, TopK: 5
- Rerank: `True`, candidates: 20
- Hit@1: 10/10
- Hit@K: 10/10
- Avg total latency/query: 0.066s
- Median total latency/query: 0.038s

## Cases

### b6_no_7_chord - PASS

- Query: B6 六和弦指法，不包含七度音，根音在九品附近
- Expected any: B6_chord_shape, B6
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.269s = embed 0.218s + chroma 0.051s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1088 | -0.0208 | `B6_chord_shape` | 69 | chord_diagram | b6, 不包含七度音, 和弦, 指法 | 标准调弦下B6和弦指板图，根音位于第9品。图示标注了构成音程：1、5、6、3。该和弦由三和弦加入大六度音构成，不含七度音，属于六和弦家族。 |
| 2 | 3 | Y | 0.1421 | -0.0541 | `high_fret_jazz_voicings_progression` | 67 | chord_diagram | b6, 和弦, 指法 | 展示了一组高把位（7-10品）的爵士风格六和弦与九和弦指型图。包含C6(IV)、G6/9(I)、Bm7(三级)、Dm6/9(V)及Am7(ii)。所有和弦均标注了根音位置或级数功能，且多采用 mute 1、6 弦的封闭指法，强调中间四弦的和声色彩。 |
| 3 | 2 | Y | 0.1389 | -0.0669 | `E6/9_chord_root_position` | 69 | exercise_diagram | b6, 不包含七度音, 和弦, 指法 | 练习58中的E6/9和弦指板图，标注了构成音级（1、3、6、9、5）。图示仅标出位于VI弦的根音位置，要求学习者根据六九和弦定义（1-3-5-6-9，无七度音）自行推导并画出完整指法。 |
| 4 | 4 | Y | 0.1486 | -0.0696 | `Asus4_chord_shape` | 69 | chord_diagram | b6, 不包含七度音, 和弦, 指法 | 标准调弦下Asus4和弦指板图。图示为开放把位，仅标记了3弦4品（D音）作为挂四音，其余各弦均为空弦音（E-A-D-G-B-E），构成根音A与四度音D的音响结构。 |
| 5 | 5 | Y | 0.1538 | -0.0718 | `Gsus2_chord_shape_exercise` | 69 | exercise_diagram | b6, 不包含七度音, 和弦, 指法 | 练习58中的Gsus2和弦填空题。图示为吉他指板局部，标有品数1、2、5及罗马数字II（二品）。图中仅给出一个黑点作为根音或参考音位置，要求学习者根据Gsus2构成音（1-2-5）补全剩余按弦位置并设计指法。 |

### fm7b5_arpeggio_shape - PASS

- Query: F小七减五 Fm7b5 琶音指型，低把位，半减七和弦
- Expected any: Fm7b5_arpeggio_shape_1, F half-diminished
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.038s = embed 0.036s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1127 | 0.0653 | `Fm7b5_arpeggio_shape_1` | 54 | fretboard_diagram | fm7b5, 低把位, 半减七和弦, 和弦, 小七减五, 指型, 琶音, 琶音指型 | 标准调弦下F小七减五和弦（Fm7b5）的六根弦琶音指型图。图示为指型1，覆盖1至5品区域。双圈标记根音F（位于6弦1品与4弦3品），单圈黑点表示和弦构成音（b3、b5、b7）。该图展示了半减七和弦在低把位的完整指板分布。 |
| 2 | 2 |  | 0.1474 | -0.0334 | `Fdim7_arpeggio_shape_5` | 54 | fretboard_diagram | 和弦, 小七减五, 指型, 琶音, 琶音指型 | 吉他标准调弦下Fdim7（减七和弦）的指板琶音指型图，标注为“指型5”。图中展示了该和弦在指板上的完整把位分布，双圈标记指示根音F的位置，黑点表示构成音，涵盖六根琴弦。 |
| 3 | 4 |  | 0.1590 | -0.0380 | `diminished_7th_arpeggio_shape_4_root_position` | 54 | fretboard_diagram | 低把位, 和弦, 小七减五, 指型, 琶音 | 吉他指板图展示减七和弦（Dim7）琶音的“指型4”。图中黑点标记根音位置，位于第6弦第1品（对应F音）。结合上下文，此图为F减七和弦（Fdim7）琶音练习的基础指法图示，用于定位和弦内音在指板上的分布。 |
| 4 | 5 |  | 0.1607 | -0.0587 | `Fmaj7_arpeggio_shape_2` | 52 | fretboard_diagram | 和弦, 指型, 琶音, 琶音指型 | 标准调弦下F大七和弦（Fmaj7）琶音指型图，对应教材“指型2”。图示为双圈空心标记的根音位置，分别位于第5弦和第3弦，展示跨弦琶音的基础把位结构。 |
| 5 | 6 |  | 0.1620 | -0.0600 | `Fmi7_arpeggio_root_position` | 53 | fretboard_diagram | 和弦, 指型, 琶音, 琶音指型 | F小七和弦（Fmi7）琶音指板图示，标记了根音位置（黑圈）。结合文本为练习39/40的一部分，用于定位Fmi7琶音指型1的起始点，强调体会小七和弦色彩。 |

### d_major_arpeggio - PASS

- Query: D大三和弦琶音 指型1 根音三音五音
- Expected any: D_major_triad_arpeggio_shape_1
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.090s = embed 0.087s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1082 | 0.0148 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 1, 和弦, 大三和弦琶音, 指型, 琶音 | 标准调弦下D大三和弦琶音指型1（根音在6弦）。图示为全六弦指板，黑点表示构成音（根音、三音、五音），空心圆可能指示其他把位根音或参考点。属于第13章三和弦琶音练习内容。 |
| 2 | 2 | Y | 0.1117 | 0.0113 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 1, 和弦, 大三和弦琶音, 指型, 琶音 | 标准调弦下D大三和弦琶音指型1的指板图。图示包含三个空心圆圈标记的音符，分别位于不同弦上，构成根音、三音与五音的分解和弦结构，对应教材第13章练习30内容。 |
| 3 | 3 | Y | 0.1136 | 0.0064 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 1, 和弦, 大三和弦琶音, 指型, 琶音 | D大调三和弦琶音指型1示意图。图中展示了两个构成音在指板上的相对位置（空心圆点），属于大三和弦基础练习，用于构建D大三和弦的分解演奏模式。 |
| 4 | 4 |  | 0.1352 | -0.0082 | `C_major_triad_arpeggio_shape_2` | 45 | fretboard_diagram | 1, 和弦, 大三和弦琶音, 指型, 琶音 | 标准调弦下C大三和弦琶音指型2（练习30）。图示为六线谱指板图，根音(R)位于5弦3品与3弦5品。包含组成音1、3、5（即C、E、G），音符分布在3至5品之间，展示跨弦的大三和弦琶音结构。 |
| 5 | 6 |  | 0.1416 | -0.0336 | `D_augmented_triad_arpeggio_shape_1` | 47 | fretboard_diagram | 1, 和弦, 指型, 琶音 | 标准调弦下D增三和弦（D Augmented）琶音指型1的指板图。图示包含三个构成音，分布在低音弦与高音弦区域，展示跨弦的大三度与增五度音程结构，用于构建增和弦琶音练习。 |

### d_diminished_arpeggio - PASS

- Query: D减三和弦琶音，根音小三度减五度，制造紧张经过感
- Expected any: D_diminished_triad_arpeggio_shape, D diminished
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.038s = embed 0.035s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1110 | -0.0270 | `D_diminished_triad_arpeggio_shape` | 46 | fretboard_diagram | 减三和弦琶音, 和弦, 琶音 | 标准调弦下D减三和弦（D diminished triad）的指板琶音图示。图中展示了该和弦在指板上的双音或片段构成，配合文字说明用于练习大声朗读和弦名称及指型序号，强调听辨减三和弦特有的音程性质。 |
| 2 | 2 | Y | 0.1260 | -0.0390 | `D_diminished_triad_arpeggio_pattern_2` | 46 | fretboard_diagram | 减三和弦琶音, 和弦, 琶音 | 吉他指板图展示D减三和弦琶音的指型2（共五种根音指型之一）。图中包含两个空心圆圈标记，代表该把位内的关键音符位置。练习要求构建D减三和弦型式，强调左手把位内演奏，避免使用品位标记以下音符，且横向跨度不超过1品，部分情况需越弦。 |
| 3 | 3 |  | 0.1297 | -0.0577 | `D_minor_triad_arpeggio_shape` | 46 | fretboard_diagram | 和弦, 琶音 | D小三和弦琶音指板图示（对应练习31）。图中展示了该和弦在指板上的双音结构，包含根音与降三度音程关系。作为基础琶音练习素材，用于构建D小调的和声骨架及旋律线条。 |
| 4 | 4 |  | 0.1446 | -0.0726 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 和弦, 琶音 | 标准调弦下D大三和弦琶音指型1（根音在6弦）。图示为全六弦指板，黑点表示构成音（根音、三音、五音），空心圆可能指示其他把位根音或参考点。属于第13章三和弦琶音练习内容。 |
| 5 | 6 |  | 0.1467 | -0.0747 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 和弦, 琶音 | 标准调弦下D大三和弦琶音指型1的指板图。图示包含三个空心圆圈标记的音符，分别位于不同弦上，构成根音、三音与五音的分解和弦结构，对应教材第13章练习30内容。 |

### facgce_fifth_string_root - PASS

- Query: FACGCE 调弦，从第五弦起始的 math rock 和弦指型
- Expected any: FACGCE_chord_shape_5th_string_root, FACGCE
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.038s = embed 0.035s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 2 | Y | 0.0963 | 0.0757 | `FACGCE_chord_shape_5th_string_root` | 33 | chord_diagram | facgce, math, rock, 从第五弦起始的, 和弦, 和弦指型, 指型, 调弦 | FACGCE特殊调弦下的和弦指型图，起始于第5弦（A弦）第9品。图示为横按指法，覆盖第5至第1弦的第9至11品区域，第6弦与第1弦标记为不发声（X）。属于教材中“从第五弦起始的和弦指型”部分，用于构建Math Rock风格的复杂和声色彩。 |
| 2 | 1 | Y | 0.0911 | 0.0709 | `FACGCE_chord_shape_5th_string_root` | 33 | chord_diagram | facgce, math, rock, 从第五弦起始的, 和弦, 和弦指型, 指型, 调弦 | FACGCE特殊调弦下的和弦指型图，根音位于第五弦。图示显示六弦 mute（X），五弦至二弦有四个按音点，构成密集的和弦 voicing。属于“从第五弦起始的和弦指型”系列，适用于 Math Rock 风格中复杂的和声进行。 |
| 3 | 4 | Y | 0.1076 | 0.0554 | `FACGCE_chord_shape_5th_string_root` | 33 | chord_diagram | facgce, math, rock, 从第五弦起始的, 和弦, 和弦指型, 指型, 调弦 | FACGCE特殊调弦下的和弦指型图，基于第五弦起始的和弦形状。图示显示第6、5弦制音（X），第4、3弦有按品黑点，第2、1弦为空弦音，包含横按技法标记。 |
| 4 | 9 | Y | 0.1136 | 0.0154 | `FACGCE_tuning_scale_patterns` | 34 | fretboard_diagram | facgce, math, rock, 和弦, 指型, 调弦 | FACGCE特殊调弦下的五种可移动音阶指型图（含大调与小调）。图示展示了基于第六弦根音起始的音符分布，包含开放弦利用及低把位密集排列。适用于Math Rock风格的主奏旋律、点弦Riff构建及乐句过渡，强调听觉导向的非连续音符选择。 |
| 5 | 5 | Y | 0.1088 | 0.0112 | `FACGCE_tuning_chord_voicings_progressions` | 33 | chord_diagram | facgce, math, rock, 从第五弦起始的, 和弦, 和弦指型, 指型, 调弦 | FACGCE特殊调弦下的和弦指型库。包含Fmaj9、G7、Am、Am+11、Bm7b5等基础和弦，以及从第五弦起始的Am7、Bm7b5、Cmaj7、Cadd9、G9指型。底部展示了多组未标注名称的FACGCE调式和弦进行范例（涉及空弦与高把位），用于探索该调式下的声部连接。 |

### facgce_minor_pattern - PASS

- Query: FACGCE 特殊调弦 小调音阶 指板音型 空弦共鸣 点弦
- Expected any: FACGCE_tuning_minor_scale_pattern
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.038s = embed 0.035s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1184 | 0.0316 | `FACGCE_tuning_minor_scale_pattern` | 35 | fretboard_diagram | facgce, 小调, 指板音型, 点弦, 特殊调弦, 空弦共鸣, 调弦, 音阶 | FACGCE特殊调弦下的指板音型图（标题：FACGCE调音小调实用笔记）。展示0-7品范围内的音符分布，包含大量空弦音及3、5品的按弦位置。配合下方谱例“Idea 1”，演示了结合变调夹3品、点弦（T）与持续延音的Math Rock风格乐句编写思路。 |
| 2 | 2 |  | 0.1276 | 0.0104 | `FACGCE_tuning_scale_patterns` | 34 | fretboard_diagram | facgce, 小调, 点弦, 特殊调弦, 空弦共鸣, 调弦, 音阶 | FACGCE特殊调弦下的五种可移动音阶指型图（含大调与小调）。图示展示了基于第六弦根音起始的音符分布，包含开放弦利用及低把位密集排列。适用于Math Rock风格的主奏旋律、点弦Riff构建及乐句过渡，强调听觉导向的非连续音符选择。 |
| 3 | 3 |  | 0.1278 | -0.0048 | `FACGCE_tuning_major_scale_fingering` | 34 | fretboard_diagram | facgce, 点弦, 特殊调弦, 空弦共鸣, 调弦, 音阶 | FACGCE特殊调弦下的大调实用音符指板图（0-7品）。展示基于6弦根音的可移动音阶指型，包含空弦音与按弦音分布。适用于Math Rock风格的主奏、旋律创作及点弦Riff构建，强调非连续排列以提供多音符选择。 |
| 4 | 4 |  | 0.1311 | -0.0081 | `FACGCE_minor_scale_pattern` | 35 | fretboard_diagram | facgce, 小调, 特殊调弦, 空弦共鸣, 调弦, 音阶 | FACGCE特殊调弦下的指板音阶图，标题为“FACGCE调音小调实用笔记”。图示展示了开放弦至第7品的音位分布，包含大量空弦音（E/C/G/C/A）及按弦音（黑点），用于构建小调乐句与把位模式。 |
| 5 | 10 |  | 0.1457 | -0.0257 | `FACGCE_tapping_arpeggios_sustain` | 36 | tab_excerpt | facgce, 点弦, 特殊调弦, 空弦共鸣, 调弦, 音阶 | FACGCE特殊调弦吉他谱例（变调夹第4品）。包含两组Math Rock风格乐句：上方为带击勾滑音的分解和弦与点弦旋律；下方展示持续震音/发音技法，结合空弦延音与高把位点弦琶音（如9-10-12-14序列），强调声部延续与余音控制。 |

### daeacse_scale - PASS

- Query: DAEAC#E 调弦的大调与小调音阶，0到7品，开放弦
- Expected any: DAEAC#E_tuning_major_minor_scales, DAEAC#E_tuning_major_minor_scale_patterns
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.038s = embed 0.035s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 6 | Y | 0.1256 | 0.0554 | `DAEAC#E_tuning_major_minor_scale_patterns` | 39 | fretboard_diagram | 0, 7, daeac#e, 大调, 小调, 开放弦, 调弦, 音阶 | DAEAC#E特殊调弦下的指板音阶分布图（0-7品）。展示大调与小调实用音符位置，包含空弦音及黑点标记的根音/关键音。音符非连续排列，设计用于主奏、旋律创作及点弦连复段，强调听觉引导的音符走向梳理。 |
| 2 | 1 | Y | 0.1047 | 0.0403 | `DAEAC#E_tuning_major_minor_scales` | 39 | fretboard_diagram | 0, 7, daeac#e, 大调, 小调, 开放弦, 调弦, 音阶 | DAEAC#E特殊调弦下的指板图，展示大调与小调实用音符分布（0-7品）。黑色圆点标记根音位置，空心圆为音阶内其他音符。设计用于主奏、旋律创作及点弦连复段，提供非连续排列的音符选择以辅助听觉导向的乐句构建。 |
| 3 | 7 |  | 0.1262 | 0.0398 | `DAEAC#E_tuning_major_scale_pattern` | 39 | fretboard_diagram | 0, 7, daeac#e, 大调, 开放弦, 调弦, 音阶 | DAEAC#E特殊调弦下的大调实用音符指板图。展示0至7品范围内的音阶分布，包含空弦音（6、2、1弦）及黑点标记的根音位置。该图谱并非连续排列，旨在提供主奏、旋律创作及点弦连复段时的多音符选择，利用听觉梳理走向。 |
| 4 | 9 |  | 0.1296 | 0.0034 | `DAEAC#E_tuning_math_rock_phrases` | 40 | tab_excerpt | 0, 7, daeac#e, 开放弦, 调弦, 音阶 | Math Rock吉他教材第40页，展示DAEAC#E特殊调弦下的练习乐句（Ideas 1-4）。包含五线谱与六线谱对照，涉及变调夹第2品和第7品的应用。技法涵盖点弦（T）、击勾弦、持续音及开放弦利用，呈现典型的Midwest Emo风格织体。 |
| 5 | 8 |  | 0.1267 | -0.0067 | `FACGCE_tuning_ideas_and_DAEAC#E_chord_theory` | 37 | tab_excerpt | 0, 7, daeac#e, 开放弦, 调弦, 音阶 | Math Rock吉他教材第37页，包含FACGCE调弦下的两个乐句谱例（Idea 4 & 5），大量使用击勾弦、滑音及空弦技巧。底部文字介绍DAEAC#E调弦法，涵盖基于开放弦的大/小三和弦、属七及半减七指型，强调音色浑厚与可移动变调特性。 |

### daeacse_tab_hammer_pull - PASS

- Query: DAEAC#E 调弦谱例，击弦勾弦滑音，开放弦分解和弦
- Expected any: DAEAC#E_tuning_arpeggio_phrasing, DAEAC#E_tuning_chord_progression_and_arpeggios
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.038s = embed 0.036s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0986 | 0.0004 | `DAEAC#E_tuning_arpeggio_phrasing` | 37 | tab_excerpt | daeac#e, 和弦, 开放弦, 调弦, 谱例 | DAEAC#E特殊调弦下的吉他谱例（第17-22小节），展示基于开放弦的分解和弦乐句。大量使用击勾弦（H/P）与滑音（sl.）技法，结合空弦音构成流畅的连奏线条，体现Math Rock风格中利用非标准调弦构建复杂织体的特征。 |
| 2 | 3 |  | 0.1143 | -0.0153 | `FACGCE_tuning_ideas_and_DAEAC#E_chord_theory` | 37 | tab_excerpt | daeac#e, 和弦, 开放弦, 调弦, 谱例 | Math Rock吉他教材第37页，包含FACGCE调弦下的两个乐句谱例（Idea 4 & 5），大量使用击勾弦、滑音及空弦技巧。底部文字介绍DAEAC#E调弦法，涵盖基于开放弦的大/小三和弦、属七及半减七指型，强调音色浑厚与可移动变调特性。 |
| 3 | 2 |  | 0.1033 | -0.0223 | `DAEAC#E_tuning_chord_shape` | 38 | chord_diagram | daeac#e, 和弦, 开放弦, 调弦 | DAEAC#E特殊调弦下的和弦指法图。图示为六线谱网格，第6、5、4弦为空弦（标记O），第3弦被横按（Barre）覆盖，第2弦某品位有单音按压（黑点），第1弦未发声（标记X）。属于该调式下的基础开放和弦形状之一。 |
| 4 | 5 | Y | 0.1151 | -0.0311 | `DAEAC#E_tuning_chord_progression_and_arpeggios` | 37 | tab_excerpt | daeac#e, 和弦, 开放弦, 调弦 | DAEAC#E特殊调弦下的吉他六线谱与五线谱对照练习。包含基于开放弦的饱满和弦指型（大/小/属七/半减七）及分解琶音乐句。大量使用击弦（H）技法连接空弦音，展示该调弦法下利用开放弦共鸣构建Math Rock风格织体的典型语汇。 |
| 5 | 4 |  | 0.1149 | -0.0339 | `DAEAC#E_tuning_math_rock_phrases` | 40 | tab_excerpt | daeac#e, 和弦, 开放弦, 调弦 | Math Rock吉他教材第40页，展示DAEAC#E特殊调弦下的练习乐句（Ideas 1-4）。包含五线谱与六线谱对照，涉及变调夹第2品和第7品的应用。技法涵盖点弦（T）、击勾弦、持续音及开放弦利用，呈现典型的Midwest Emo风格织体。 |

### mathrock_voicing_connection - PASS

- Query: Math Rock 里 CM7 GM7 Bm7 不同把位 voicing 连接
- Expected any: CM7_GM7_Bm7_voicings_comparison
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.038s = embed 0.035s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1400 | 0.0080 | `CM7_GM7_Bm7_voicings_comparison` | 51 | chord_diagram | bm7, cm7, gm7, math, rock, voicing, 不同把位, 连接 | Math Rock风格教材第51页，展示CM7、GM7、Bm7的三种不同把位指型。第一组为开放/低把位指法；第二组为高把位封闭和弦（8-10品）；第三组为练习题，给出10品CM7变体，要求匹配后续GM7/Bm7指型。包含详细左手按弦数字标注及闷音符号。 |
| 2 | 3 |  | 0.1748 | -0.0328 | `AM9_E6_F#m7_GM7_voicings` | 67 | chord_diagram | bm7, gm7, math, rock, voicing, 连接 | 四组标准调弦和弦指法图：AM9（根音6弦5品，4品位置）、E6（根音6弦空弦/5品把位）、F#m7（根音6弦2品，4品位置）、GM7（根音6弦3品，5品位置）。包含高弦mute标记(x)，展示Math Rock风格中常见的封闭和弦Voicing。 |
| 3 | 2 |  | 0.1493 | -0.0433 | `CM7_Am7_G7_FM7_voicings_variations` | 50 | chord_diagram | cm7, math, rock, voicing, 不同把位, 连接 | 展示CM7、Am7、G7、FM7四种七和弦的三种不同把位指型（开放/低把位、中把位5-8品、高把位8-12品）。包含根音位置变化及横按技法，用于演示同一和弦在指板不同区域的Voicing选择与声部连接逻辑。 |
| 4 | 8 |  | 0.1954 | -0.0804 | `high_fret_jazz_voicings_progression` | 67 | chord_diagram | bm7, math, rock, voicing, 连接 | 展示了一组高把位（7-10品）的爵士风格六和弦与九和弦指型图。包含C6(IV)、G6/9(I)、Bm7(三级)、Dm6/9(V)及Am7(ii)。所有和弦均标注了根音位置或级数功能，且多采用 mute 1、6 弦的封闭指法，强调中间四弦的和声色彩。 |
| 5 | 6 |  | 0.1921 | -0.0921 | `Dm7_Bm7b5_voicings_by_string_set` | 49 | chord_diagram | bm7, cm7, math, rock, voicing, 连接 | 展示Dm7与Bm7b5（小七降五）和弦的多种指板配置。按根音所在弦组分类：第六弦、第五弦及第四弦根音位置。包含Dm7在10品、5品、12品的变体，以及Bm7b5在6品、9品的变体。文本提及C大调I-vi-V-IV进行(CM7/Am7/G7/FM7)作为应用背景。 |

### sus2_fill_exercise - PASS

- Query: Gsus2 挂二和弦 1 2 5 构成音，在图上补全指法的练习
- Expected any: Gsus2_chord_shape_exercise
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.037s = embed 0.034s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1225 | 0.0225 | `Gsus2_chord_shape_exercise` | 69 | exercise_diagram | 1, 2, 5, gsus2, 和弦, 指法, 构成音 | 练习58中的Gsus2和弦填空题。图示为吉他指板局部，标有品数1、2、5及罗马数字II（二品）。图中仅给出一个黑点作为根音或参考音位置，要求学习者根据Gsus2构成音（1-2-5）补全剩余按弦位置并设计指法。 |
| 2 | 2 |  | 0.1574 | -0.0784 | `Gsus4_voicings / FM9_Am9_G7_progression` | 56 | chord_diagram | 1, 2, 5, 和弦, 指法 | 展示三种不同把位的Gsus4和弦指型图（含开放、5品、10品位），以及FM9(7品)、Am9(10品)与G7(10品)的和弦进行图示。文字说明在数学摇滚中，使用挂四和弦替换属七和弦（V级）可消除突兀感，优化声部连接。 |
| 3 | 3 |  | 0.1788 | -0.0878 | `Asus4_chord_shape` | 69 | chord_diagram | 1, 2, 5, 和弦, 指法 | 标准调弦下Asus4和弦指板图。图示为开放把位，仅标记了3弦4品（D音）作为挂四音，其余各弦均为空弦音（E-A-D-G-B-E），构成根音A与四度音D的音响结构。 |
| 4 | 6 |  | 0.2096 | -0.0946 | `high_fret_jazz_voicings_progression` | 67 | chord_diagram | 1, 2, 5, 和弦, 指法 | 展示了一组高把位（7-10品）的爵士风格六和弦与九和弦指型图。包含C6(IV)、G6/9(I)、Bm7(三级)、Dm6/9(V)及Am7(ii)。所有和弦均标注了根音位置或级数功能，且多采用 mute 1、6 弦的封闭指法，强调中间四弦的和声色彩。 |
| 5 | 17 |  | 0.2209 | -0.0999 | `DAEAC#E_tuning_chord_shape` | 38 | chord_diagram | 1, 2, 5, 和弦, 指法 | DAEAC#E特殊调弦下的和弦指法图。图示为六线谱网格，第6、5、4弦为空弦（标记O），第3弦被横按（Barre）覆盖，第2弦某品位有单音按压（黑点），第1弦未发声（标记X）。属于该调式下的基础开放和弦形状之一。 |
