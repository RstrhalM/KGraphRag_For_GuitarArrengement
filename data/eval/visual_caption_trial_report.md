# Visual Caption Retrieval Trial

## Summary

- Collection: `guitar_visual_captions_qwen3_06b` (20 docs)
- Model: `models\embedding\qwen3-embedding-0.6b` on `cuda`, dim=1024
- Tests: 10, TopK: 5
- Hit@1: 10/10
- Hit@K: 10/10
- Avg total latency/query: 0.076s
- Median total latency/query: 0.050s

## Cases

### b6_no_7_chord - PASS

- Query: B6 六和弦指法，不包含七度音，根音在九品附近
- Expected any: B6_chord_shape, B6
- First hit rank: 1
- Latency: total 0.309s = embed 0.264s + chroma 0.045s

| Rank | Expected | Distance | Topic | Page | Type | Caption |
|---:|:---:|---:|---|---:|---|---|
| 1 | Y | 0.1088 | `B6_chord_shape` | 69 | chord_diagram | 标准调弦下B6和弦指板图，根音位于第9品。图示标注了构成音程：1、5、6、3。该和弦由三和弦加入大六度音构成，不含七度音，属于六和弦家族。 |
| 2 | Y | 0.1538 | `Gsus2_chord_shape_exercise` | 69 | exercise_diagram | 练习58中的Gsus2和弦填空题。图示为吉他指板局部，标有品数1、2、5及罗马数字II（二品）。图中仅给出一个黑点作为根音或参考音位置，要求学习者根据Gsus2构成音（1-2-5）补全剩余按弦位置并设计指法。 |
| 3 |  | 0.1683 | `Fm7b5_arpeggio_shape_1` | 54 | fretboard_diagram | 标准调弦下F小七减五和弦（Fm7b5）的六根弦琶音指型图。图示为指型1，覆盖1至5品区域。双圈标记根音F（位于6弦1品与4弦3品），单圈黑点表示和弦构成音（b3、b5、b7）。该图展示了半减七和弦在低把位的完整指板分布。 |
| 4 | Y | 0.1700 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 标准调弦下D大三和弦琶音指型1（根音在6弦）。图示为全六弦指板，黑点表示构成音（根音、三音、五音），空心圆可能指示其他把位根音或参考点。属于第13章三和弦琶音练习内容。 |
| 5 |  | 0.1712 | `FACGCE_chord_shape_5th_string_root` | 33 | chord_diagram | FACGCE特殊调弦下的和弦指型图，根音位于第五弦。图示显示六弦 mute（X），五弦至二弦有四个按音点，构成密集的和弦 voicing。属于“从第五弦起始的和弦指型”系列，适用于 Math Rock 风格中复杂的和声进行。 |

### fm7b5_arpeggio_shape - PASS

- Query: F小七减五 Fm7b5 琶音指型，低把位，半减七和弦
- Expected any: Fm7b5_arpeggio_shape_1, F half-diminished
- First hit rank: 1
- Latency: total 0.046s = embed 0.045s + chroma 0.002s

| Rank | Expected | Distance | Topic | Page | Type | Caption |
|---:|:---:|---:|---|---:|---|---|
| 1 | Y | 0.1127 | `Fm7b5_arpeggio_shape_1` | 54 | fretboard_diagram | 标准调弦下F小七减五和弦（Fm7b5）的六根弦琶音指型图。图示为指型1，覆盖1至5品区域。双圈标记根音F（位于6弦1品与4弦3品），单圈黑点表示和弦构成音（b3、b5、b7）。该图展示了半减七和弦在低把位的完整指板分布。 |
| 2 |  | 0.1636 | `FACGCE_chord_shape_5th_string_root` | 33 | chord_diagram | FACGCE特殊调弦下的和弦指型图，根音位于第五弦。图示显示六弦 mute（X），五弦至二弦有四个按音点，构成密集的和弦 voicing。属于“从第五弦起始的和弦指型”系列，适用于 Math Rock 风格中复杂的和声进行。 |
| 3 |  | 0.1747 | `FACGCE_tuning_chord_voicings_progressions` | 33 | chord_diagram | FACGCE特殊调弦下的和弦指型库。包含Fmaj9、G7、Am、Am+11、Bm7b5等基础和弦，以及从第五弦起始的Am7、Bm7b5、Cmaj7、Cadd9、G9指型。底部展示了多组未标注名称的FACGCE调式和弦进行范例（涉及空弦与高把位），用于探索该调式下的声部连接。 |
| 4 |  | 0.1865 | `DAEAC#E_tuning_chord_voicings_progressions` | 38 | chord_diagram | DAEAC#E特殊调弦下的和弦指型库。包含以第六弦（如D大九、F#m9、E7）和第五弦（如A小九、Bm7、E7）为根音的指法，以及G#小七降五等高把位和弦。底部展示了该调弦下的两组和弦进行示例，涵盖大九、小九及减五和弦色彩。 |
| 5 |  | 0.1892 | `CM7_GM7_Bm7_voicings_comparison` | 51 | chord_diagram | Math Rock风格教材第51页，展示CM7、GM7、Bm7的三种不同把位指型。第一组为开放/低把位指法；第二组为高把位封闭和弦（8-10品）；第三组为练习题，给出10品CM7变体，要求匹配后续GM7/Bm7指型。包含详细左手按弦数字标注及闷音符号。 |

### d_major_arpeggio - PASS

- Query: D大三和弦琶音 指型1 根音三音五音
- Expected any: D_major_triad_arpeggio_shape_1
- First hit rank: 1
- Latency: total 0.050s = embed 0.048s + chroma 0.002s

| Rank | Expected | Distance | Topic | Page | Type | Caption |
|---:|:---:|---:|---|---:|---|---|
| 1 | Y | 0.1082 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 标准调弦下D大三和弦琶音指型1（根音在6弦）。图示为全六弦指板，黑点表示构成音（根音、三音、五音），空心圆可能指示其他把位根音或参考点。属于第13章三和弦琶音练习内容。 |
| 2 | Y | 0.1136 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | D大调三和弦琶音指型1示意图。图中展示了两个构成音在指板上的相对位置（空心圆点），属于大三和弦基础练习，用于构建D大三和弦的分解演奏模式。 |
| 3 |  | 0.1416 | `D_augmented_triad_arpeggio_shape_1` | 47 | fretboard_diagram | 标准调弦下D增三和弦（D Augmented）琶音指型1的指板图。图示包含三个构成音，分布在低音弦与高音弦区域，展示跨弦的大三度与增五度音程结构，用于构建增和弦琶音练习。 |
| 4 |  | 0.1442 | `D_minor_triad_arpeggio_shape_5` | 46 | fretboard_diagram | D小三和弦（Dm）琶音指型5的指板图示。图中展示了包含根音、小三度及纯五度的三音符结构，分布在六根琴弦上。配合文字说明，用于练习大声朗读和弦名称与指型序号，并听辨音程性质。 |
| 5 |  | 0.1493 | `open_major_triad_voicings` | 48 | chord_diagram | 展示C、A、G、E、D五个开放大三和弦的标准指法图。图中明确标注了根音（空心圈）、三度与五度音（实心点）及闷音（x）。这些是吉他基础“牛仔和弦”形态，涵盖六根弦上的音符分布，用于构建密集声部三和弦的基础素材。 |

### d_diminished_arpeggio - PASS

- Query: D减三和弦琶音，根音小三度减五度，制造紧张经过感
- Expected any: D_diminished_triad_arpeggio_shape, D diminished
- First hit rank: 1
- Latency: total 0.048s = embed 0.047s + chroma 0.002s

| Rank | Expected | Distance | Topic | Page | Type | Caption |
|---:|:---:|---:|---|---:|---|---|
| 1 | Y | 0.1110 | `D_diminished_triad_arpeggio_shape` | 46 | fretboard_diagram | 标准调弦下D减三和弦（D diminished triad）的指板琶音图示。图中展示了该和弦在指板上的双音或片段构成，配合文字说明用于练习大声朗读和弦名称及指型序号，强调听辨减三和弦特有的音程性质。 |
| 2 |  | 0.1446 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 标准调弦下D大三和弦琶音指型1（根音在6弦）。图示为全六弦指板，黑点表示构成音（根音、三音、五音），空心圆可能指示其他把位根音或参考点。属于第13章三和弦琶音练习内容。 |
| 3 |  | 0.1469 | `D_augmented_triad_arpeggio_shape_1` | 47 | fretboard_diagram | 标准调弦下D增三和弦（D Augmented）琶音指型1的指板图。图示包含三个构成音，分布在低音弦与高音弦区域，展示跨弦的大三度与增五度音程结构，用于构建增和弦琶音练习。 |
| 4 |  | 0.1486 | `D_minor_triad_arpeggio_shape_5` | 46 | fretboard_diagram | D小三和弦（Dm）琶音指型5的指板图示。图中展示了包含根音、小三度及纯五度的三音符结构，分布在六根琴弦上。配合文字说明，用于练习大声朗读和弦名称与指型序号，并听辨音程性质。 |
| 5 |  | 0.1493 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | D大调三和弦琶音指型1示意图。图中展示了两个构成音在指板上的相对位置（空心圆点），属于大三和弦基础练习，用于构建D大三和弦的分解演奏模式。 |

### facgce_fifth_string_root - PASS

- Query: FACGCE 调弦，从第五弦起始的 math rock 和弦指型
- Expected any: FACGCE_chord_shape_5th_string_root, FACGCE
- First hit rank: 1
- Latency: total 0.049s = embed 0.048s + chroma 0.002s

| Rank | Expected | Distance | Topic | Page | Type | Caption |
|---:|:---:|---:|---|---:|---|---|
| 1 | Y | 0.0911 | `FACGCE_chord_shape_5th_string_root` | 33 | chord_diagram | FACGCE特殊调弦下的和弦指型图，根音位于第五弦。图示显示六弦 mute（X），五弦至二弦有四个按音点，构成密集的和弦 voicing。属于“从第五弦起始的和弦指型”系列，适用于 Math Rock 风格中复杂的和声进行。 |
| 2 | Y | 0.1088 | `FACGCE_tuning_chord_voicings_progressions` | 33 | chord_diagram | FACGCE特殊调弦下的和弦指型库。包含Fmaj9、G7、Am、Am+11、Bm7b5等基础和弦，以及从第五弦起始的Am7、Bm7b5、Cmaj7、Cadd9、G9指型。底部展示了多组未标注名称的FACGCE调式和弦进行范例（涉及空弦与高把位），用于探索该调式下的声部连接。 |
| 3 | Y | 0.1120 | `FACGCE_tuning_minor_scale_pattern` | 35 | fretboard_diagram | FACGCE特殊调弦下的指板音型图（标题：FACGCE调音小调实用笔记）。展示0-7品范围内的音符分布，包含大量空弦音及3、5品的按弦位置。配合下方谱例“Idea 1”，演示了结合变调夹3品、点弦（T）与持续延音的Math Rock风格乐句编写思路。 |
| 4 | Y | 0.1136 | `FACGCE_tuning_scale_patterns` | 34 | fretboard_diagram | FACGCE特殊调弦下的五种可移动音阶指型图（含大调与小调）。图示展示了基于第六弦根音起始的音符分布，包含开放弦利用及低把位密集排列。适用于Math Rock风格的主奏旋律、点弦Riff构建及乐句过渡，强调听觉导向的非连续音符选择。 |
| 5 | Y | 0.1310 | `FACGCE_major_scale_pattern` | 34 | fretboard_diagram | FACGCE特殊调弦下的大调实用音阶指板图。展示了一个覆盖开放弦至第7品的可移动音阶指型，黑色圆点标记根音位置（位于6弦、2弦及5弦特定品位），空心圆为其他音阶音。该指型专为Math Rock主奏、旋律创作及点弦Riff设计，音符分布非完全连续以提供更多选择。 |

### facgce_minor_pattern - PASS

- Query: FACGCE 特殊调弦 小调音阶 指板音型 空弦共鸣 点弦
- Expected any: FACGCE_tuning_minor_scale_pattern
- First hit rank: 1
- Latency: total 0.051s = embed 0.049s + chroma 0.002s

| Rank | Expected | Distance | Topic | Page | Type | Caption |
|---:|:---:|---:|---|---:|---|---|
| 1 | Y | 0.1184 | `FACGCE_tuning_minor_scale_pattern` | 35 | fretboard_diagram | FACGCE特殊调弦下的指板音型图（标题：FACGCE调音小调实用笔记）。展示0-7品范围内的音符分布，包含大量空弦音及3、5品的按弦位置。配合下方谱例“Idea 1”，演示了结合变调夹3品、点弦（T）与持续延音的Math Rock风格乐句编写思路。 |
| 2 |  | 0.1276 | `FACGCE_tuning_scale_patterns` | 34 | fretboard_diagram | FACGCE特殊调弦下的五种可移动音阶指型图（含大调与小调）。图示展示了基于第六弦根音起始的音符分布，包含开放弦利用及低把位密集排列。适用于Math Rock风格的主奏旋律、点弦Riff构建及乐句过渡，强调听觉导向的非连续音符选择。 |
| 3 |  | 0.1318 | `FACGCE_chord_shape_5th_string_root` | 33 | chord_diagram | FACGCE特殊调弦下的和弦指型图，根音位于第五弦。图示显示六弦 mute（X），五弦至二弦有四个按音点，构成密集的和弦 voicing。属于“从第五弦起始的和弦指型”系列，适用于 Math Rock 风格中复杂的和声进行。 |
| 4 |  | 0.1418 | `FACGCE_major_scale_pattern` | 34 | fretboard_diagram | FACGCE特殊调弦下的大调实用音阶指板图。展示了一个覆盖开放弦至第7品的可移动音阶指型，黑色圆点标记根音位置（位于6弦、2弦及5弦特定品位），空心圆为其他音阶音。该指型专为Math Rock主奏、旋律创作及点弦Riff设计，音符分布非完全连续以提供更多选择。 |
| 5 |  | 0.1432 | `FACGCE_tuning_chord_voicings_progressions` | 33 | chord_diagram | FACGCE特殊调弦下的和弦指型库。包含Fmaj9、G7、Am、Am+11、Bm7b5等基础和弦，以及从第五弦起始的Am7、Bm7b5、Cmaj7、Cadd9、G9指型。底部展示了多组未标注名称的FACGCE调式和弦进行范例（涉及空弦与高把位），用于探索该调式下的声部连接。 |

### daeacse_scale - PASS

- Query: DAEAC#E 调弦的大调与小调音阶，0到7品，开放弦
- Expected any: DAEAC#E_tuning_major_minor_scales
- First hit rank: 1
- Latency: total 0.054s = embed 0.052s + chroma 0.002s

| Rank | Expected | Distance | Topic | Page | Type | Caption |
|---:|:---:|---:|---|---:|---|---|
| 1 | Y | 0.1047 | `DAEAC#E_tuning_major_minor_scales` | 39 | fretboard_diagram | DAEAC#E特殊调弦下的指板图，展示大调与小调实用音符分布（0-7品）。黑色圆点标记根音位置，空心圆为音阶内其他音符。设计用于主奏、旋律创作及点弦连复段，提供非连续排列的音符选择以辅助听觉导向的乐句构建。 |
| 2 |  | 0.1208 | `DAEAC#E_tuning_chord_voicings_progressions` | 38 | chord_diagram | DAEAC#E特殊调弦下的和弦指型库。包含以第六弦（如D大九、F#m9、E7）和第五弦（如A小九、Bm7、E7）为根音的指法，以及G#小七降五等高把位和弦。底部展示了该调弦下的两组和弦进行示例，涵盖大九、小九及减五和弦色彩。 |
| 3 |  | 0.1250 | `DAEAC#E_tuning_chord_progression_and_arpeggios` | 37 | tab_excerpt | DAEAC#E特殊调弦下的吉他六线谱与五线谱对照练习。包含基于开放弦的饱满和弦指型（大/小/属七/半减七）及分解琶音乐句。大量使用击弦（H）技法连接空弦音，展示该调弦法下利用开放弦共鸣构建Math Rock风格织体的典型语汇。 |
| 4 |  | 0.1364 | `DAEAC#E_tuning_arpeggio_phrasing` | 37 | tab_excerpt | DAEAC#E特殊调弦下的吉他谱例（第17-22小节），展示基于开放弦的分解和弦乐句。大量使用击勾弦（H/P）与滑音（sl.）技法，结合空弦音构成流畅的连奏线条，体现Math Rock风格中利用非标准调弦构建复杂织体的特征。 |
| 5 |  | 0.1650 | `FACGCE_tuning_chord_voicings_progressions` | 33 | chord_diagram | FACGCE特殊调弦下的和弦指型库。包含Fmaj9、G7、Am、Am+11、Bm7b5等基础和弦，以及从第五弦起始的Am7、Bm7b5、Cmaj7、Cadd9、G9指型。底部展示了多组未标注名称的FACGCE调式和弦进行范例（涉及空弦与高把位），用于探索该调式下的声部连接。 |

### daeacse_tab_hammer_pull - PASS

- Query: DAEAC#E 调弦谱例，击弦勾弦滑音，开放弦分解和弦
- Expected any: DAEAC#E_tuning_arpeggio_phrasing, DAEAC#E_tuning_chord_progression_and_arpeggios
- First hit rank: 1
- Latency: total 0.051s = embed 0.050s + chroma 0.002s

| Rank | Expected | Distance | Topic | Page | Type | Caption |
|---:|:---:|---:|---|---:|---|---|
| 1 | Y | 0.0986 | `DAEAC#E_tuning_arpeggio_phrasing` | 37 | tab_excerpt | DAEAC#E特殊调弦下的吉他谱例（第17-22小节），展示基于开放弦的分解和弦乐句。大量使用击勾弦（H/P）与滑音（sl.）技法，结合空弦音构成流畅的连奏线条，体现Math Rock风格中利用非标准调弦构建复杂织体的特征。 |
| 2 | Y | 0.1151 | `DAEAC#E_tuning_chord_progression_and_arpeggios` | 37 | tab_excerpt | DAEAC#E特殊调弦下的吉他六线谱与五线谱对照练习。包含基于开放弦的饱满和弦指型（大/小/属七/半减七）及分解琶音乐句。大量使用击弦（H）技法连接空弦音，展示该调弦法下利用开放弦共鸣构建Math Rock风格织体的典型语汇。 |
| 3 |  | 0.1286 | `DAEAC#E_tuning_major_minor_scales` | 39 | fretboard_diagram | DAEAC#E特殊调弦下的指板图，展示大调与小调实用音符分布（0-7品）。黑色圆点标记根音位置，空心圆为音阶内其他音符。设计用于主奏、旋律创作及点弦连复段，提供非连续排列的音符选择以辅助听觉导向的乐句构建。 |
| 4 |  | 0.1310 | `DAEAC#E_tuning_chord_voicings_progressions` | 38 | chord_diagram | DAEAC#E特殊调弦下的和弦指型库。包含以第六弦（如D大九、F#m9、E7）和第五弦（如A小九、Bm7、E7）为根音的指法，以及G#小七降五等高把位和弦。底部展示了该调弦下的两组和弦进行示例，涵盖大九、小九及减五和弦色彩。 |
| 5 |  | 0.1499 | `FACGCE_tuning_minor_scale_pattern` | 35 | fretboard_diagram | FACGCE特殊调弦下的指板音型图（标题：FACGCE调音小调实用笔记）。展示0-7品范围内的音符分布，包含大量空弦音及3、5品的按弦位置。配合下方谱例“Idea 1”，演示了结合变调夹3品、点弦（T）与持续延音的Math Rock风格乐句编写思路。 |

### mathrock_voicing_connection - PASS

- Query: Math Rock 里 CM7 GM7 Bm7 不同把位 voicing 连接
- Expected any: CM7_GM7_Bm7_voicings_comparison
- First hit rank: 1
- Latency: total 0.047s = embed 0.046s + chroma 0.002s

| Rank | Expected | Distance | Topic | Page | Type | Caption |
|---:|:---:|---:|---|---:|---|---|
| 1 | Y | 0.1400 | `CM7_GM7_Bm7_voicings_comparison` | 51 | chord_diagram | Math Rock风格教材第51页，展示CM7、GM7、Bm7的三种不同把位指型。第一组为开放/低把位指法；第二组为高把位封闭和弦（8-10品）；第三组为练习题，给出10品CM7变体，要求匹配后续GM7/Bm7指型。包含详细左手按弦数字标注及闷音符号。 |
| 2 |  | 0.1873 | `FACGCE_tuning_chord_voicings_progressions` | 33 | chord_diagram | FACGCE特殊调弦下的和弦指型库。包含Fmaj9、G7、Am、Am+11、Bm7b5等基础和弦，以及从第五弦起始的Am7、Bm7b5、Cmaj7、Cadd9、G9指型。底部展示了多组未标注名称的FACGCE调式和弦进行范例（涉及空弦与高把位），用于探索该调式下的声部连接。 |
| 3 |  | 0.2078 | `DAEAC#E_tuning_chord_voicings_progressions` | 38 | chord_diagram | DAEAC#E特殊调弦下的和弦指型库。包含以第六弦（如D大九、F#m9、E7）和第五弦（如A小九、Bm7、E7）为根音的指法，以及G#小七降五等高把位和弦。底部展示了该调弦下的两组和弦进行示例，涵盖大九、小九及减五和弦色彩。 |
| 4 |  | 0.2163 | `FACGCE_chord_shape_5th_string_root` | 33 | chord_diagram | FACGCE特殊调弦下的和弦指型图，根音位于第五弦。图示显示六弦 mute（X），五弦至二弦有四个按音点，构成密集的和弦 voicing。属于“从第五弦起始的和弦指型”系列，适用于 Math Rock 风格中复杂的和声进行。 |
| 5 |  | 0.2240 | `FACGCE_tuning_minor_scale_pattern` | 35 | fretboard_diagram | FACGCE特殊调弦下的指板音型图（标题：FACGCE调音小调实用笔记）。展示0-7品范围内的音符分布，包含大量空弦音及3、5品的按弦位置。配合下方谱例“Idea 1”，演示了结合变调夹3品、点弦（T）与持续延音的Math Rock风格乐句编写思路。 |

### sus2_fill_exercise - PASS

- Query: Gsus2 挂二和弦 1 2 5 构成音，在图上补全指法的练习
- Expected any: Gsus2_chord_shape_exercise
- First hit rank: 1
- Latency: total 0.050s = embed 0.048s + chroma 0.002s

| Rank | Expected | Distance | Topic | Page | Type | Caption |
|---:|:---:|---:|---|---:|---|---|
| 1 | Y | 0.1225 | `Gsus2_chord_shape_exercise` | 69 | exercise_diagram | 练习58中的Gsus2和弦填空题。图示为吉他指板局部，标有品数1、2、5及罗马数字II（二品）。图中仅给出一个黑点作为根音或参考音位置，要求学习者根据Gsus2构成音（1-2-5）补全剩余按弦位置并设计指法。 |
| 2 |  | 0.2026 | `augmented_triad_arpeggio_shape_4` | 47 | fretboard_diagram | 吉他指板图展示增三和弦琶音的“指型4”。图中包含三个空心圆圈标记的音符位置，分别位于第6弦、第4弦和第2弦上，构成跨弦组的三音结构。结合上下文，此图为D增三和弦琶音练习的一部分，用于记忆特定把位下的增和弦指法分布。 |
| 3 |  | 0.2100 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 标准调弦下D大三和弦琶音指型1（根音在6弦）。图示为全六弦指板，黑点表示构成音（根音、三音、五音），空心圆可能指示其他把位根音或参考点。属于第13章三和弦琶音练习内容。 |
| 4 |  | 0.2104 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | D大调三和弦琶音指型1示意图。图中展示了两个构成音在指板上的相对位置（空心圆点），属于大三和弦基础练习，用于构建D大三和弦的分解演奏模式。 |
| 5 |  | 0.2121 | `CM7_GM7_Bm7_voicings_comparison` | 51 | chord_diagram | Math Rock风格教材第51页，展示CM7、GM7、Bm7的三种不同把位指型。第一组为开放/低把位指法；第二组为高把位封闭和弦（8-10品）；第三组为练习题，给出10品CM7变体，要求匹配后续GM7/Bm7指型。包含详细左手按弦数字标注及闷音符号。 |
