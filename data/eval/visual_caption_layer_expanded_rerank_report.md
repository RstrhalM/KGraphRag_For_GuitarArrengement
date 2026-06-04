# Visual Caption Retrieval Trial

## Summary

- Collection: `guitar_visual_captions_qwen3_06b` (60 docs)
- Model: `models\embedding\qwen3-embedding-0.6b` on `cuda`, dim=1024
- Tests: 30, TopK: 5
- Rerank: `True`, candidates: 20
- Hit@1: 30/30
- Hit@K: 30/30
- Avg total latency/query: 0.048s
- Median total latency/query: 0.037s

## Cases

### fretboard_e69_no_seventh - PASS

- Query: E6/9 和弦指板图，不含七度音，构成音是 1 3 5 6 9
- Expected any: E6/9_chord_root_position, E6/9
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.268s = embed 0.214s + chroma 0.054s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0702 | 0.1188 | `E6/9_chord_root_position` | 69 | exercise_diagram | 1, 3, 5, 6, 9, e6, e6/9, 不含七度音, 和弦, 和弦指板图 | 练习58中的E6/9和弦指板图，标注了构成音级（1、3、6、9、5）。图示仅标出位于VI弦的根音位置，要求学习者根据六九和弦定义（1-3-5-6-9，无七度音）自行推导并画出完整指法。 |
| 2 | 3 |  | 0.1181 | 0.0379 | `B6_chord_shape` | 69 | chord_diagram | 1, 3, 5, 6, 9, e6, 不含七度音, 和弦, 和弦指板图 | 标准调弦下B6和弦指板图，根音位于第9品。图示标注了构成音程：1、5、6、3。该和弦由三和弦加入大六度音构成，不含七度音，属于六和弦家族。 |
| 3 | 4 |  | 0.1231 | -0.0001 | `DAEAC#E_tuning_chord_shape_9th_fret` | 38 | chord_diagram | 1, 3, 5, 6, 9, e6, 和弦 | DAEAC#E特殊调弦下的五弦和弦指法图，起始于第9品。图示为四音和弦形状，按压第5至2弦（A-E-A-C#），第6弦与第1弦标记为X（不发声）。结合附近文本，该指型对应A小九和弦(Am9)或升G小七降五和弦(G#m7b5)，属于Math Rock风格中常见的封闭和弦Voicing。 |
| 4 | 2 |  | 0.1141 | -0.0031 | `Asus4_chord_shape` | 69 | chord_diagram | 1, 3, 5, 6, 9, 和弦, 和弦指板图 | 标准调弦下Asus4和弦指板图。图示为开放把位，仅标记了3弦4品（D音）作为挂四音，其余各弦均为空弦音（E-A-D-G-B-E），构成根音A与四度音D的音响结构。 |
| 5 | 11 |  | 0.1413 | -0.0033 | `AM9_E6_F#m7_GM7_voicings` | 67 | chord_diagram | 1, 3, 5, 6, 9, e6, 和弦 | 四组标准调弦和弦指法图：AM9（根音6弦5品，4品位置）、E6（根音6弦空弦/5品把位）、F#m7（根音6弦2品，4品位置）、GM7（根音6弦3品，5品位置）。包含高弦mute标记(x)，展示Math Rock风格中常见的封闭和弦Voicing。 |

### fretboard_asus4_open - PASS

- Query: Asus4 开放把位，很多空弦，挂四音 D 的和弦图
- Expected any: Asus4_chord_shape, Asus4
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.038s = embed 0.035s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1648 | -0.0708 | `Asus4_chord_shape` | 69 | chord_diagram | asus4, 和弦, 开放把位, 挂四音 | 标准调弦下Asus4和弦指板图。图示为开放把位，仅标记了3弦4品（D音）作为挂四音，其余各弦均为空弦音（E-A-D-G-B-E），构成根音A与四度音D的音响结构。 |
| 2 | 3 |  | 0.2091 | -0.1481 | `DAEAC#E_tuning_chord_shape` | 38 | chord_diagram | 和弦 | DAEAC#E特殊调弦下的和弦指法图。图示为六线谱网格，第6、5、4弦为空弦（标记O），第3弦被横按（Barre）覆盖，第2弦某品位有单音按压（黑点），第1弦未发声（标记X）。属于该调式下的基础开放和弦形状之一。 |
| 3 | 5 |  | 0.2215 | -0.1635 | `Amaj7_open_voicing` | 55 | chord_diagram | 和弦, 开放把位 | A大调七和弦（Amaj7）的开放把位指法图。根音位于6弦空弦，包含3弦2品（B音位置上方，实际为C#? 不，3弦2品是B，3弦1品是C，3弦2品是B... 等等，标准调弦3弦空弦G，1品G#，2品A。图中黑点在3弦2品？不，看图：6弦空弦(A)，5弦空弦(E)? 不，5弦有黑点吗？没有。4弦有黑点吗？没有。仔细看图：6弦空弦(圈)，5弦无，4弦2品(黑点)... |
| 4 | 11 |  | 0.2298 | -0.1688 | `AM9_E6_F#m7_GM7_voicings` | 67 | chord_diagram | 和弦 | 四组标准调弦和弦指法图：AM9（根音6弦5品，4品位置）、E6（根音6弦空弦/5品把位）、F#m7（根音6弦2品，4品位置）、GM7（根音6弦3品，5品位置）。包含高弦mute标记(x)，展示Math Rock风格中常见的封闭和弦Voicing。 |
| 5 | 14 |  | 0.2339 | -0.1729 | `high_fret_jazz_voicings_progression` | 67 | chord_diagram | 和弦 | 展示了一组高把位（7-10品）的爵士风格六和弦与九和弦指型图。包含C6(IV)、G6/9(I)、Bm7(三级)、Dm6/9(V)及Am7(ii)。所有和弦均标注了根音位置或级数功能，且多采用 mute 1、6 弦的封闭指法，强调中间四弦的和声色彩。 |

### fretboard_c_major_arpeggio_shape2 - PASS

- Query: C 大三和弦琶音 指型2 根音大三度纯五度
- Expected any: C_major_triad_arpeggio_shape_2
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.037s = embed 0.035s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1097 | 0.0233 | `C_major_triad_arpeggio_shape_2` | 45 | fretboard_diagram | 2, 和弦, 大三和弦琶音, 指型, 琶音 | 标准调弦下C大三和弦琶音指型2（练习30）。图示为六线谱指板图，根音(R)位于5弦3品与3弦5品。包含组成音1、3、5（即C、E、G），音符分布在3至5品之间，展示跨弦的大三和弦琶音结构。 |
| 2 | 2 |  | 0.1225 | -0.0085 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 2, 和弦, 大三和弦琶音, 指型, 琶音 | 标准调弦下D大三和弦琶音指型1（根音在6弦）。图示为全六弦指板，黑点表示构成音（根音、三音、五音），空心圆可能指示其他把位根音或参考点。属于第13章三和弦琶音练习内容。 |
| 3 | 4 |  | 0.1254 | -0.0114 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 2, 和弦, 大三和弦琶音, 指型, 琶音 | 标准调弦下D大三和弦琶音指型1的指板图。图示包含三个空心圆圈标记的音符，分别位于不同弦上，构成根音、三音与五音的分解和弦结构，对应教材第13章练习30内容。 |
| 4 | 3 |  | 0.1236 | -0.0126 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 2, 和弦, 大三和弦琶音, 指型, 琶音 | D大调三和弦琶音指型1示意图。图中展示了两个构成音在指板上的相对位置（空心圆点），属于大三和弦基础练习，用于构建D大三和弦的分解演奏模式。 |
| 5 | 10 |  | 0.1585 | -0.0405 | `D_diminished_triad_arpeggio_pattern_2` | 46 | fretboard_diagram | 2, 和弦, 指型, 琶音 | 吉他指板图展示D减三和弦琶音的指型2（共五种根音指型之一）。图中包含两个空心圆圈标记，代表该把位内的关键音符位置。练习要求构建D减三和弦型式，强调左手把位内演奏，避免使用品位标记以下音符，且横向跨度不超过1品，部分情况需越弦。 |

### fretboard_d_minor_arpeggio - PASS

- Query: D 小三和弦琶音，D F A，小调三和弦指板图
- Expected any: D_minor_triad_arpeggio_shape, Dm
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.037s = embed 0.034s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0930 | 0.0090 | `D_minor_triad_arpeggio_shape` | 46 | fretboard_diagram | 和弦, 小三和弦琶音, 小调, 琶音 | D小三和弦琶音指板图示（对应练习31）。图中展示了该和弦在指板上的双音结构，包含根音与降三度音程关系。作为基础琶音练习素材，用于构建D小调的和声骨架及旋律线条。 |
| 2 | 3 | Y | 0.1064 | -0.0104 | `D_minor_triad_arpeggio_shape_5` | 46 | fretboard_diagram | 和弦, 小三和弦琶音, 小调, 琶音 | D小三和弦（Dm）琶音指型5的指板图示。图中展示了包含根音、小三度及纯五度的三音符结构，分布在六根琴弦上。配合文字说明，用于练习大声朗读和弦名称与指型序号，并听辨音程性质。 |
| 3 | 2 |  | 0.1055 | -0.0335 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 和弦, 琶音 | D大调三和弦琶音指型1示意图。图中展示了两个构成音在指板上的相对位置（空心圆点），属于大三和弦基础练习，用于构建D大三和弦的分解演奏模式。 |
| 4 | 4 |  | 0.1071 | -0.0351 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 和弦, 琶音 | 标准调弦下D大三和弦琶音指型1（根音在6弦）。图示为全六弦指板，黑点表示构成音（根音、三音、五音），空心圆可能指示其他把位根音或参考点。属于第13章三和弦琶音练习内容。 |
| 5 | 5 |  | 0.1089 | -0.0369 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 和弦, 琶音 | 标准调弦下D大三和弦琶音指型1的指板图。图示包含三个空心圆圈标记的音符，分别位于不同弦上，构成根音、三音与五音的分解和弦结构，对应教材第13章练习30内容。 |

### fretboard_d_diminished_position - PASS

- Query: D 减三和弦琶音，注意左手把位，避免用品位标记以下音符
- Expected any: D_diminished_triad_arpeggio_pattern_2, D diminished
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.038s = embed 0.035s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1083 | -0.0113 | `D_diminished_triad_arpeggio_pattern_2` | 46 | fretboard_diagram | 减三和弦琶音, 和弦, 琶音 | 吉他指板图展示D减三和弦琶音的指型2（共五种根音指型之一）。图中包含两个空心圆圈标记，代表该把位内的关键音符位置。练习要求构建D减三和弦型式，强调左手把位内演奏，避免使用品位标记以下音符，且横向跨度不超过1品，部分情况需越弦。 |
| 2 | 2 | Y | 0.1300 | -0.0460 | `D_diminished_triad_arpeggio_shape` | 46 | fretboard_diagram | 减三和弦琶音, 和弦, 琶音 | 标准调弦下D减三和弦（D diminished triad）的指板琶音图示。图中展示了该和弦在指板上的双音或片段构成，配合文字说明用于练习大声朗读和弦名称及指型序号，强调听辨减三和弦特有的音程性质。 |
| 3 | 5 |  | 0.1546 | -0.0726 | `diminished_7th_arpeggio_shape_4_root_position` | 54 | fretboard_diagram | 和弦, 琶音 | 吉他指板图展示减七和弦（Dim7）琶音的“指型4”。图中黑点标记根音位置，位于第6弦第1品（对应F音）。结合上下文，此图为F减七和弦（Fdim7）琶音练习的基础指法图示，用于定位和弦内音在指板上的分布。 |
| 4 | 4 |  | 0.1518 | -0.0798 | `augmented_triad_arpeggio_shape_4` | 47 | fretboard_diagram | 和弦, 琶音 | 吉他指板图展示增三和弦琶音的“指型4”。图中包含三个空心圆圈标记的音符位置，分别位于第6弦、第4弦和第2弦上，构成跨弦组的三音结构。结合上下文，此图为D增三和弦琶音练习的一部分，用于记忆特定把位下的增和弦指法分布。 |
| 5 | 6 |  | 0.1551 | -0.0831 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 和弦, 琶音 | 标准调弦下D大三和弦琶音指型1（根音在6弦）。图示为全六弦指板，黑点表示构成音（根音、三音、五音），空心圆可能指示其他把位根音或参考点。属于第13章三和弦琶音练习内容。 |

### fretboard_d_augmented_shape - PASS

- Query: D 增三和弦琶音，增五度，练习增三和弦音程性质
- Expected any: D_augmented_arpeggio_shape_1, augmented_triad_arpeggio_shape_5, D augmented
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.038s = embed 0.035s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1158 | -0.0138 | `augmented_triad_arpeggio_shape_5` | 47 | fretboard_diagram | 和弦, 增三和弦琶音, 增五度, 琶音 | 吉他指板图展示D增三和弦（D Augmented）琶音指型5。图中包含两个空心圆圈标记的音符位置，代表该指型下的根音或构成音分布。配合文字说明，用于练习增三和弦琶音及听辨大三度与增五度音程性质。 |
| 2 | 2 | Y | 0.1163 | -0.0173 | `D_augmented_triad_arpeggio_shape_1` | 47 | fretboard_diagram | 和弦, 增三和弦琶音, 增五度, 琶音 | 标准调弦下D增三和弦（D Augmented）琶音指型1的指板图。图示包含三个构成音，分布在低音弦与高音弦区域，展示跨弦的大三度与增五度音程结构，用于构建增和弦琶音练习。 |
| 3 | 3 | Y | 0.1245 | -0.0255 | `D_augmented_arpeggio_shape_1` | 47 | fretboard_diagram | 和弦, 增三和弦琶音, 增五度, 琶音 | 吉他指板图展示D增三和弦（D Augmented）琶音指型1。图示包含两个空心圆圈标记的音符位置，分别位于不同弦组上，对应D增三和弦构成音（根音、大三度、增五度）。结合文本提示，此为练习33的一部分，用于掌握增三和弦在指板上的分布与把位连接。 |
| 4 | 5 |  | 0.1499 | -0.0629 | `augmented_triad_arpeggio_shape_4` | 47 | fretboard_diagram | 和弦, 增三和弦琶音, 琶音 | 吉他指板图展示增三和弦琶音的“指型4”。图中包含三个空心圆圈标记的音符位置，分别位于第6弦、第4弦和第2弦上，构成跨弦组的三音结构。结合上下文，此图为D增三和弦琶音练习的一部分，用于记忆特定把位下的增和弦指法分布。 |
| 5 | 4 |  | 0.1476 | -0.0756 | `D_diminished_triad_arpeggio_shape` | 46 | fretboard_diagram | 和弦, 琶音 | 标准调弦下D减三和弦（D diminished triad）的指板琶音图示。图中展示了该和弦在指板上的双音或片段构成，配合文字说明用于练习大声朗读和弦名称及指型序号，强调听辨减三和弦特有的音程性质。 |

### fretboard_open_major_triad_voicings - PASS

- Query: 开放大三和弦声部，牛仔和弦，空弦构建密集三和弦
- Expected any: open_major_triad_voicings, open_major_triad_voicings_finger_patterns
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.037s = embed 0.034s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1187 | -0.0407 | `open_major_triad_voicings_finger_patterns` | 48 | fretboard_diagram | 和弦, 声部, 开放大三和弦声部, 牛仔和弦 | 吉他指板开放大三和弦声部图示，包含“指型4”与“指型2”两种排列。利用空弦音（E、B）构建密集三和弦转位，展示如何在不同弦组上同时扫奏或拨奏构成完整和弦，属于基础牛仔和弦形态。 |
| 2 | 2 | Y | 0.1416 | -0.0666 | `open_major_triad_voicings` | 48 | chord_diagram | 和弦, 声部, 开放大三和弦声部, 牛仔和弦 | 展示C、A、G、E、D五个开放大三和弦的标准指法图。图中明确标注了根音（空心圈）、三度与五度音（实心点）及闷音（x）。这些是吉他基础“牛仔和弦”形态，涵盖六根弦上的音符分布，用于构建密集声部三和弦的基础素材。 |
| 3 | 3 |  | 0.1691 | -0.1241 | `Asus4_chord_shape` | 69 | chord_diagram | 和弦, 声部 | 标准调弦下Asus4和弦指板图。图示为开放把位，仅标记了3弦4品（D音）作为挂四音，其余各弦均为空弦音（E-A-D-G-B-E），构成根音A与四度音D的音响结构。 |
| 4 | 4 |  | 0.1771 | -0.1321 | `DAEAC#E_tuning_chord_progression_and_arpeggios` | 37 | tab_excerpt | 和弦, 声部 | DAEAC#E特殊调弦下的吉他六线谱与五线谱对照练习。包含基于开放弦的饱满和弦指型（大/小/属七/半减七）及分解琶音乐句。大量使用击弦（H）技法连接空弦音，展示该调弦法下利用开放弦共鸣构建Math Rock风格织体的典型语汇。 |
| 5 | 7 |  | 0.1855 | -0.1405 | `high_fret_jazz_voicings_progression` | 67 | chord_diagram | 和弦, 声部 | 展示了一组高把位（7-10品）的爵士风格六和弦与九和弦指型图。包含C6(IV)、G6/9(I)、Bm7(三级)、Dm6/9(V)及Am7(ii)。所有和弦均标注了根音位置或级数功能，且多采用 mute 1、6 弦的封闭指法，强调中间四弦的和声色彩。 |

### fretboard_fmaj7_arpeggio - PASS

- Query: Fmaj7 大七和弦琶音 指型2 跨弦根音位置
- Expected any: Fmaj7_arpeggio_shape_2, Fmaj7_arpeggio_shapes
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.037s = embed 0.035s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0900 | 0.0390 | `Fmaj7_arpeggio_shape_2` | 52 | fretboard_diagram | 2, fmaj7, 和弦, 指型, 琶音 | 标准调弦下F大七和弦（Fmaj7）琶音指型图，对应教材“指型2”。图示为双圈空心标记的根音位置，分别位于第5弦和第3弦，展示跨弦琶音的基础把位结构。 |
| 2 | 2 | Y | 0.0947 | 0.0283 | `Fmaj7_arpeggio_shapes` | 52 | fretboard_diagram | 2, fmaj7, 和弦, 指型, 琶音 | 吉他指板图展示F大七和弦（Fmaj7）的琶音指型。根据附近文字提示，该图对应练习38中的Fmaj7琶音及其不同把位指型（如指型2、指型3）。图中黑点标记了构成音在指板上的位置，用于构建F调的大七和弦声部。 |
| 3 | 3 |  | 0.1336 | -0.0346 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 2, 和弦, 指型, 琶音 | 标准调弦下D大三和弦琶音指型1（根音在6弦）。图示为全六弦指板，黑点表示构成音（根音、三音、五音），空心圆可能指示其他把位根音或参考点。属于第13章三和弦琶音练习内容。 |
| 4 | 7 |  | 0.1437 | -0.0347 | `Fm7b5_arpeggio_shape_1` | 54 | fretboard_diagram | 2, 和弦, 指型, 琶音 | 标准调弦下F小七减五和弦（Fm7b5）的六根弦琶音指型图。图示为指型1，覆盖1至5品区域。双圈标记根音F（位于6弦1品与4弦3品），单圈黑点表示和弦构成音（b3、b5、b7）。该图展示了半减七和弦在低把位的完整指板分布。 |
| 5 | 5 |  | 0.1403 | -0.0383 | `F7_arpeggio_shape` | 53 | fretboard_diagram | 2, 和弦, 指型, 琶音 | 标准调弦下F7属七和弦琶音指板图。图中包含双圈标记的根音（F）位置，黑点表示构成音，覆盖六根琴弦。结合文本“指型1/2/3”及“练习39”，展示属七和弦在指板上的多把位分布与连接逻辑。 |

### fretboard_f7_dominant_arpeggio - PASS

- Query: F7 属七和弦琶音 指板多把位连接
- Expected any: F7_arpeggio_shape, F7
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.038s = embed 0.035s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1011 | 0.0069 | `F7_arpeggio_shape` | 53 | fretboard_diagram | f7, 和弦, 属七和弦琶音, 琶音 | 标准调弦下F7属七和弦琶音指板图。图中包含双圈标记的根音（F）位置，黑点表示构成音，覆盖六根琴弦。结合文本“指型1/2/3”及“练习39”，展示属七和弦在指板上的多把位分布与连接逻辑。 |
| 2 | 2 |  | 0.1241 | -0.0521 | `Fmaj7_arpeggio_shape_2` | 52 | fretboard_diagram | 和弦, 琶音 | 标准调弦下F大七和弦（Fmaj7）琶音指型图，对应教材“指型2”。图示为双圈空心标记的根音位置，分别位于第5弦和第3弦，展示跨弦琶音的基础把位结构。 |
| 3 | 3 |  | 0.1287 | -0.0567 | `Fmaj7_arpeggio_shapes` | 52 | fretboard_diagram | 和弦, 琶音 | 吉他指板图展示F大七和弦（Fmaj7）的琶音指型。根据附近文字提示，该图对应练习38中的Fmaj7琶音及其不同把位指型（如指型2、指型3）。图中黑点标记了构成音在指板上的位置，用于构建F调的大七和弦声部。 |
| 4 | 7 | Y | 0.1415 | -0.0575 | `diminished_7th_arpeggio_shape_4_root_position` | 54 | fretboard_diagram | f7, 和弦, 琶音 | 吉他指板图展示减七和弦（Dim7）琶音的“指型4”。图中黑点标记根音位置，位于第6弦第1品（对应F音）。结合上下文，此图为F减七和弦（Fdim7）琶音练习的基础指法图示，用于定位和弦内音在指板上的分布。 |
| 5 | 4 |  | 0.1369 | -0.0649 | `Fdim7_arpeggio_shape_5` | 54 | fretboard_diagram | 和弦, 琶音 | 吉他标准调弦下Fdim7（减七和弦）的指板琶音指型图，标注为“指型5”。图中展示了该和弦在指板上的完整把位分布，双圈标记指示根音F的位置，黑点表示构成音，涵盖六根琴弦。 |

### fretboard_fdim7_arpeggio - PASS

- Query: Fdim7 减七和弦琶音，指型4或指型5
- Expected any: Fdim7_arpeggio_shape_5, diminished_7th_arpeggio_shape_4_root_position
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.041s = embed 0.038s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0874 | 0.0696 | `diminished_7th_arpeggio_shape_4_root_position` | 54 | fretboard_diagram | 4, 5, fdim7, 减七和弦琶音, 和弦, 指型, 琶音 | 吉他指板图展示减七和弦（Dim7）琶音的“指型4”。图中黑点标记根音位置，位于第6弦第1品（对应F音）。结合上下文，此图为F减七和弦（Fdim7）琶音练习的基础指法图示，用于定位和弦内音在指板上的分布。 |
| 2 | 2 | Y | 0.0988 | 0.0422 | `Fdim7_arpeggio_shape_5` | 54 | fretboard_diagram | 4, 5, fdim7, 和弦, 指型, 琶音 | 吉他标准调弦下Fdim7（减七和弦）的指板琶音指型图，标注为“指型5”。图中展示了该和弦在指板上的完整把位分布，双圈标记指示根音F的位置，黑点表示构成音，涵盖六根琴弦。 |
| 3 | 3 |  | 0.1279 | 0.0051 | `Fm7b5_arpeggio_shape_1` | 54 | fretboard_diagram | 4, 5, 和弦, 指型, 琶音 | 标准调弦下F小七减五和弦（Fm7b5）的六根弦琶音指型图。图示为指型1，覆盖1至5品区域。双圈标记根音F（位于6弦1品与4弦3品），单圈黑点表示和弦构成音（b3、b5、b7）。该图展示了半减七和弦在低把位的完整指板分布。 |
| 4 | 5 |  | 0.1376 | -0.0166 | `D_diminished_triad_arpeggio_pattern_2` | 46 | fretboard_diagram | 4, 5, 和弦, 指型, 琶音 | 吉他指板图展示D减三和弦琶音的指型2（共五种根音指型之一）。图中包含两个空心圆圈标记，代表该把位内的关键音符位置。练习要求构建D减三和弦型式，强调左手把位内演奏，避免使用品位标记以下音符，且横向跨度不超过1品，部分情况需越弦。 |
| 5 | 4 |  | 0.1356 | -0.0246 | `D_diminished_triad_arpeggio_shape` | 46 | fretboard_diagram | 4, 5, 和弦, 指型, 琶音 | 标准调弦下D减三和弦（D diminished triad）的指板琶音图示。图中展示了该和弦在指板上的双音或片段构成，配合文字说明用于练习大声朗读和弦名称及指型序号，强调听辨减三和弦特有的音程性质。 |

### fretboard_amaj7_open - PASS

- Query: Amaj7 开放和弦图，开放弦的大七和弦声部
- Expected any: Amaj7_open_voicing, Amaj7
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.040s = embed 0.038s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1502 | -0.0722 | `Amaj7_open_voicing` | 55 | chord_diagram | amaj7, 和弦, 声部, 开放弦 | A大调七和弦（Amaj7）的开放把位指法图。根音位于6弦空弦，包含3弦2品（B音位置上方，实际为C#? 不，3弦2品是B，3弦1品是C，3弦2品是B... 等等，标准调弦3弦空弦G，1品G#，2品A。图中黑点在3弦2品？不，看图：6弦空弦(A)，5弦空弦(E)? 不，5弦有黑点吗？没有。4弦有黑点吗？没有。仔细看图：6弦空弦(圈)，5弦无，4弦2品(黑点)... |
| 2 | 2 |  | 0.1511 | -0.0911 | `DAEAC#E_tuning_chord_progression_and_arpeggios` | 37 | tab_excerpt | 和弦, 声部, 开放弦 | DAEAC#E特殊调弦下的吉他六线谱与五线谱对照练习。包含基于开放弦的饱满和弦指型（大/小/属七/半减七）及分解琶音乐句。大量使用击弦（H）技法连接空弦音，展示该调弦法下利用开放弦共鸣构建Math Rock风格织体的典型语汇。 |
| 3 | 3 |  | 0.1550 | -0.0950 | `FACGCE_tuning_chord_voicings_progressions` | 33 | chord_diagram | 和弦, 声部, 开放弦 | FACGCE特殊调弦下的和弦指型库。包含Fmaj9、G7、Am、Am+11、Bm7b5等基础和弦，以及从第五弦起始的Am7、Bm7b5、Cmaj7、Cadd9、G9指型。底部展示了多组未标注名称的FACGCE调式和弦进行范例（涉及空弦与高把位），用于探索该调式下的声部连接。 |
| 4 | 5 |  | 0.1635 | -0.1035 | `CM7_Am7_G7_FM7_voicings_variations` | 50 | chord_diagram | 和弦, 声部, 开放弦 | 展示CM7、Am7、G7、FM7四种七和弦的三种不同把位指型（开放/低把位、中把位5-8品、高把位8-12品）。包含根音位置变化及横按技法，用于演示同一和弦在指板不同区域的Voicing选择与声部连接逻辑。 |
| 5 | 6 |  | 0.1638 | -0.1068 | `DAEAC#E_tuning_chord_voicings_progressions` | 38 | chord_diagram | 和弦, 声部, 开放弦 | DAEAC#E特殊调弦下的和弦指型库。包含以第六弦（如D大九、F#m9、E7）和第五弦（如A小九、Bm7、E7）为根音的指法，以及G#小七降五等高把位和弦。底部展示了该调弦下的两组和弦进行示例，涵盖大九、小九及减五和弦色彩。 |

### fretboard_bb13_exercise - PASS

- Query: Bb13 琶音指法练习，十三和弦构成音指板图
- Expected any: Bb13_arpeggio_fingering_exercise, Bb13
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.038s = embed 0.035s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1052 | 0.0128 | `Bb13_arpeggio_fingering_exercise` | 60 | exercise_diagram | bb13, 和弦, 指法, 琶音 | 《吉他指板手册》第60页练习49：Bb13和弦琶音指法填空图。图示为空白六线指板网格，仅在低音弦某品标记一个根音位置（黑点），上方留有“指型__”横线供填写。配合文字要求弹奏琶音并口述和弦名、指型序号及声部构成（如1-3-5-7-9）。 |
| 2 | 4 |  | 0.1799 | -0.0979 | `Fm7b5_arpeggio_shape_1` | 54 | fretboard_diagram | 和弦, 琶音 | 标准调弦下F小七减五和弦（Fm7b5）的六根弦琶音指型图。图示为指型1，覆盖1至5品区域。双圈标记根音F（位于6弦1品与4弦3品），单圈黑点表示和弦构成音（b3、b5、b7）。该图展示了半减七和弦在低把位的完整指板分布。 |
| 3 | 10 |  | 0.1859 | -0.1019 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 和弦, 指法, 琶音 | 标准调弦下D大三和弦琶音指型1的指板图。图示包含三个空心圆圈标记的音符，分别位于不同弦上，构成根音、三音与五音的分解和弦结构，对应教材第13章练习30内容。 |
| 4 | 3 |  | 0.1777 | -0.1057 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 和弦, 琶音 | 标准调弦下D大三和弦琶音指型1（根音在6弦）。图示为全六弦指板，黑点表示构成音（根音、三音、五音），空心圆可能指示其他把位根音或参考点。属于第13章三和弦琶音练习内容。 |
| 5 | 6 |  | 0.1821 | -0.1101 | `D_major_triad_arpeggio_shape_1` | 45 | fretboard_diagram | 和弦, 琶音 | D大调三和弦琶音指型1示意图。图中展示了两个构成音在指板上的相对位置（空心圆点），属于大三和弦基础练习，用于构建D大三和弦的分解演奏模式。 |

### fretboard_c_minor_close_voicing - PASS

- Query: C 小三和弦密集排列，闭合把位，识别指法
- Expected any: C_minor_triad_fingering_identification, C_minor_triad_close_voicing_identification
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.038s = embed 0.035s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1167 | -0.0687 | `C_minor_triad_fingering_identification` | 49 | exercise_diagram | 和弦, 指法 | 吉他指板练习图，要求识别密集排列的C小三和弦（Cm）指型。图中展示了包含根音（双圈标记）的和弦把位，右侧提供“指型2”和“指型3”作为选项，用于训练和弦构成音与指法编号的对应关系。 |
| 2 | 2 | Y | 0.1177 | -0.0847 | `C_minor_triad_close_voicing_identification` | 49 | exercise_diagram | 和弦 | 吉他指板练习图，要求识别密集排列的C小三和弦（Cm）指型。图中显示一个三音和弦结构，根音已用圆圈特别标记，右侧留有空白横线供填写对应的指型编号（如XI等）。 |
| 3 | 3 |  | 0.1418 | -0.0988 | `C_diminished_triad_fingering_exercise` | 50 | exercise_diagram | 和弦 | 吉他指板练习图，展示第VII把位（约7品起）的密集声部C减三和弦指型。图中包含三个按弦点，其中两个根音位置被圆圈标记，要求学习者识别并填写对应的和弦指型序号。 |
| 4 | 16 |  | 0.2016 | -0.1256 | `DAEAC#E_tuning_chord_shape` | 38 | chord_diagram | 和弦, 指法 | DAEAC#E特殊调弦下的和弦指法图。图示为六线谱网格，第6、5、4弦为空弦（标记O），第3弦被横按（Barre）覆盖，第2弦某品位有单音按压（黑点），第1弦未发声（标记X）。属于该调式下的基础开放和弦形状之一。 |
| 5 | 4 |  | 0.1741 | -0.1311 | `C_major_triad_arpeggio_shape_2` | 45 | fretboard_diagram | 和弦 | 标准调弦下C大三和弦琶音指型2（练习30）。图示为六线谱指板图，根音(R)位于5弦3品与3弦5品。包含组成音1、3、5（即C、E、G），音符分布在3至5品之间，展示跨弦的大三和弦琶音结构。 |

### fretboard_c_diminished_exercise - PASS

- Query: C 减三和弦指法练习，减三和弦密集声部
- Expected any: C_diminished_triad_fingering_exercise, C diminished triad
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.037s = embed 0.035s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1152 | -0.0572 | `C_diminished_triad_fingering_exercise` | 50 | exercise_diagram | 和弦, 声部 | 吉他指板练习图，展示第VII把位（约7品起）的密集声部C减三和弦指型。图中包含三个按弦点，其中两个根音位置被圆圈标记，要求学习者识别并填写对应的和弦指型序号。 |
| 2 | 3 |  | 0.1454 | -0.0854 | `C_minor_triad_fingering_identification` | 49 | exercise_diagram | 和弦, 声部, 指法 | 吉他指板练习图，要求识别密集排列的C小三和弦（Cm）指型。图中展示了包含根音（双圈标记）的和弦把位，右侧提供“指型2”和“指型3”作为选项，用于训练和弦构成音与指法编号的对应关系。 |
| 3 | 2 |  | 0.1417 | -0.0967 | `C_minor_triad_close_voicing_identification` | 49 | exercise_diagram | 和弦, 声部 | 吉他指板练习图，要求识别密集排列的C小三和弦（Cm）指型。图中显示一个三音和弦结构，根音已用圆圈特别标记，右侧留有空白横线供填写对应的指型编号（如XI等）。 |
| 4 | 5 |  | 0.1583 | -0.1033 | `D_diminished_triad_arpeggio_pattern_2` | 46 | fretboard_diagram | 和弦, 声部 | 吉他指板图展示D减三和弦琶音的指型2（共五种根音指型之一）。图中包含两个空心圆圈标记，代表该把位内的关键音符位置。练习要求构建D减三和弦型式，强调左手把位内演奏，避免使用品位标记以下音符，且横向跨度不超过1品，部分情况需越弦。 |
| 5 | 4 |  | 0.1503 | -0.1053 | `D_diminished_triad_arpeggio_shape` | 46 | fretboard_diagram | 和弦, 声部 | 标准调弦下D减三和弦（D diminished triad）的指板琶音图示。图中展示了该和弦在指板上的双音或片段构成，配合文字说明用于练习大声朗读和弦名称及指型序号，强调听辨减三和弦特有的音程性质。 |

### mathrock_facgce_chord_progressions - PASS

- Query: FACGCE 调弦下 Fmaj9 G7 Am Bm7b5 Cmaj7 的和弦进行与 voicing
- Expected any: FACGCE_tuning_chord_voicings_progressions
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.037s = embed 0.035s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0959 | 0.0631 | `FACGCE_tuning_chord_voicings_progressions` | 33 | chord_diagram | am, bm7b5, cmaj7, facgce, fmaj9, g7, voicing, 和弦, 调弦, 调弦下 | FACGCE特殊调弦下的和弦指型库。包含Fmaj9、G7、Am、Am+11、Bm7b5等基础和弦，以及从第五弦起始的Am7、Bm7b5、Cmaj7、Cadd9、G9指型。底部展示了多组未标注名称的FACGCE调式和弦进行范例（涉及空弦与高把位），用于探索该调式下的声部连接。 |
| 2 | 8 |  | 0.1536 | -0.0246 | `FACGCE_chord_shape_5th_string_root` | 33 | chord_diagram | am, facgce, voicing, 和弦, 调弦, 调弦下 | FACGCE特殊调弦下的和弦指型图，根音位于第五弦。图示显示六弦 mute（X），五弦至二弦有四个按音点，构成密集的和弦 voicing。属于“从第五弦起始的和弦指型”系列，适用于 Math Rock 风格中复杂的和声进行。 |
| 3 | 11 |  | 0.1631 | -0.0271 | `FACGCE_chord_shape_5th_string_root` | 33 | chord_diagram | am, facgce, voicing, 和弦, 调弦, 调弦下 | FACGCE特殊调弦下的和弦指型图，起始于第5弦（A弦）第9品。图示为横按指法，覆盖第5至第1弦的第9至11品区域，第6弦与第1弦标记为不发声（X）。属于教材中“从第五弦起始的和弦指型”部分，用于构建Math Rock风格的复杂和声色彩。 |
| 4 | 6 |  | 0.1506 | -0.0296 | `DAEAC#E_tuning_chord_shape_9th_fret` | 38 | chord_diagram | am, voicing, 和弦, 调弦, 调弦下 | DAEAC#E特殊调弦下的五弦和弦指法图，起始于第9品。图示为四音和弦形状，按压第5至2弦（A-E-A-C#），第6弦与第1弦标记为X（不发声）。结合附近文本，该指型对应A小九和弦(Am9)或升G小七降五和弦(G#m7b5)，属于Math Rock风格中常见的封闭和弦Voicing。 |
| 5 | 5 |  | 0.1479 | -0.0299 | `AM9_E6_F#m7_GM7_voicings` | 67 | chord_diagram | am, voicing, 和弦, 调弦 | 四组标准调弦和弦指法图：AM9（根音6弦5品，4品位置）、E6（根音6弦空弦/5品把位）、F#m7（根音6弦2品，4品位置）、GM7（根音6弦3品，5品位置）。包含高弦mute标记(x)，展示Math Rock风格中常见的封闭和弦Voicing。 |

### mathrock_facgce_5th_string_root - PASS

- Query: FACGCE 从第五弦起始的和弦指型，五弦根音，密集 voicing
- Expected any: FACGCE_chord_shape_5th_string_root
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.037s = embed 0.035s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0728 | 0.0712 | `FACGCE_chord_shape_5th_string_root` | 33 | chord_diagram | facgce, voicing, 五弦根音, 从第五弦起始的和弦指型, 和弦, 密集, 指型 | FACGCE特殊调弦下的和弦指型图，根音位于第五弦。图示显示六弦 mute（X），五弦至二弦有四个按音点，构成密集的和弦 voicing。属于“从第五弦起始的和弦指型”系列，适用于 Math Rock 风格中复杂的和声进行。 |
| 2 | 2 | Y | 0.0745 | 0.0615 | `FACGCE_chord_shape_5th_string_root` | 33 | chord_diagram | facgce, voicing, 从第五弦起始的和弦指型, 和弦, 密集, 指型 | FACGCE特殊调弦下的和弦指型图，起始于第5弦（A弦）第9品。图示为横按指法，覆盖第5至第1弦的第9至11品区域，第6弦与第1弦标记为不发声（X）。属于教材中“从第五弦起始的和弦指型”部分，用于构建Math Rock风格的复杂和声色彩。 |
| 3 | 3 | Y | 0.0915 | 0.0295 | `FACGCE_chord_shape_5th_string_root` | 33 | chord_diagram | facgce, voicing, 从第五弦起始的和弦指型, 和弦, 指型 | FACGCE特殊调弦下的和弦指型图，基于第五弦起始的和弦形状。图示显示第6、5弦制音（X），第4、3弦有按品黑点，第2、1弦为空弦音，包含横按技法标记。 |
| 4 | 7 |  | 0.1147 | -0.0157 | `FACGCE_tuning_scale_patterns` | 34 | fretboard_diagram | facgce, 和弦, 密集, 指型 | FACGCE特殊调弦下的五种可移动音阶指型图（含大调与小调）。图示展示了基于第六弦根音起始的音符分布，包含开放弦利用及低把位密集排列。适用于Math Rock风格的主奏旋律、点弦Riff构建及乐句过渡，强调听觉导向的非连续音符选择。 |
| 5 | 4 |  | 0.1089 | -0.0159 | `FACGCE_tuning_chord_voicings_progressions` | 33 | chord_diagram | facgce, voicing, 从第五弦起始的和弦指型, 和弦, 密集, 指型 | FACGCE特殊调弦下的和弦指型库。包含Fmaj9、G7、Am、Am+11、Bm7b5等基础和弦，以及从第五弦起始的Am7、Bm7b5、Cmaj7、Cadd9、G9指型。底部展示了多组未标注名称的FACGCE调式和弦进行范例（涉及空弦与高把位），用于探索该调式下的声部连接。 |

### mathrock_facgce_major_scale - PASS

- Query: FACGCE 大调音阶指板图，用于 tapping riff 和旋律写作
- Expected any: FACGCE_tuning_major_scale_fingering, FACGCE_major_scale_pattern
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.037s = embed 0.035s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0910 | 0.0320 | `FACGCE_tuning_major_scale_fingering` | 34 | fretboard_diagram | facgce, riff, tapping, 大调, 用于, 音阶 | FACGCE特殊调弦下的大调实用音符指板图（0-7品）。展示基于6弦根音的可移动音阶指型，包含空弦音与按弦音分布。适用于Math Rock风格的主奏、旋律创作及点弦Riff构建，强调非连续排列以提供多音符选择。 |
| 2 | 2 |  | 0.0953 | 0.0277 | `FACGCE_tuning_scale_patterns` | 34 | fretboard_diagram | facgce, riff, tapping, 大调, 用于, 音阶 | FACGCE特殊调弦下的五种可移动音阶指型图（含大调与小调）。图示展示了基于第六弦根音起始的音符分布，包含开放弦利用及低把位密集排列。适用于Math Rock风格的主奏旋律、点弦Riff构建及乐句过渡，强调听觉导向的非连续音符选择。 |
| 3 | 3 | Y | 0.1006 | 0.0074 | `FACGCE_major_scale_pattern` | 34 | fretboard_diagram | facgce, riff, tapping, 大调, 音阶 | FACGCE特殊调弦下的大调实用音阶指板图。展示了一个覆盖开放弦至第7品的可移动音阶指型，黑色圆点标记根音位置（位于6弦、2弦及5弦特定品位），空心圆为其他音阶音。该指型专为Math Rock主奏、旋律创作及点弦Riff设计，音符分布非完全连续以提供更多选择。 |
| 4 | 4 |  | 0.1082 | -0.0152 | `FACGCE_minor_scale_pattern` | 35 | fretboard_diagram | facgce, riff, 用于, 音阶 | FACGCE特殊调弦下的指板音阶图，标题为“FACGCE调音小调实用笔记”。图示展示了开放弦至第7品的音位分布，包含大量空弦音（E/C/G/C/A）及按弦音（黑点），用于构建小调乐句与把位模式。 |
| 5 | 5 |  | 0.1085 | -0.0215 | `FACGCE_tuning_minor_scale_pattern` | 35 | fretboard_diagram | facgce, tapping, 用于, 音阶 | FACGCE特殊调弦下的指板音型图（标题：FACGCE调音小调实用笔记）。展示0-7品范围内的音符分布，包含大量空弦音及3、5品的按弦位置。配合下方谱例“Idea 1”，演示了结合变调夹3品、点弦（T）与持续延音的Math Rock风格乐句编写思路。 |

### mathrock_facgce_minor_scale - PASS

- Query: FACGCE 小调音阶 pattern，开放弦共鸣，math rock 乐句素材
- Expected any: FACGCE_tuning_minor_scale_pattern, FACGCE_minor_scale_pattern
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.036s = embed 0.034s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0962 | 0.0418 | `FACGCE_tuning_minor_scale_pattern` | 35 | fretboard_diagram | facgce, math, pattern, rock, 小调, 开放弦, 音阶 | FACGCE特殊调弦下的指板音型图（标题：FACGCE调音小调实用笔记）。展示0-7品范围内的音符分布，包含大量空弦音及3、5品的按弦位置。配合下方谱例“Idea 1”，演示了结合变调夹3品、点弦（T）与持续延音的Math Rock风格乐句编写思路。 |
| 2 | 2 | Y | 0.0985 | 0.0395 | `FACGCE_minor_scale_pattern` | 35 | fretboard_diagram | facgce, math, pattern, rock, 小调, 开放弦, 音阶 | FACGCE特殊调弦下的指板音阶图，标题为“FACGCE调音小调实用笔记”。图示展示了开放弦至第7品的音位分布，包含大量空弦音（E/C/G/C/A）及按弦音（黑点），用于构建小调乐句与把位模式。 |
| 3 | 5 |  | 0.1099 | 0.0341 | `FACGCE_tuning_scale_patterns` | 34 | fretboard_diagram | facgce, math, pattern, rock, 小调, 开放弦, 音阶 | FACGCE特殊调弦下的五种可移动音阶指型图（含大调与小调）。图示展示了基于第六弦根音起始的音符分布，包含开放弦利用及低把位密集排列。适用于Math Rock风格的主奏旋律、点弦Riff构建及乐句过渡，强调听觉导向的非连续音符选择。 |
| 4 | 8 |  | 0.1215 | 0.0195 | `FACGCE_major_scale_pattern` | 34 | fretboard_diagram | facgce, math, pattern, rock, 开放弦, 开放弦共鸣, 音阶 | FACGCE特殊调弦下的大调实用音阶指板图。展示了一个覆盖开放弦至第7品的可移动音阶指型，黑色圆点标记根音位置（位于6弦、2弦及5弦特定品位），空心圆为其他音阶音。该指型专为Math Rock主奏、旋律创作及点弦Riff设计，音符分布非完全连续以提供更多选择。 |
| 5 | 3 |  | 0.1037 | 0.0043 | `FACGCE_tuning_ideas_and_DAEAC#E_chord_theory` | 37 | tab_excerpt | facgce, math, rock, 开放弦, 音阶 | Math Rock吉他教材第37页，包含FACGCE调弦下的两个乐句谱例（Idea 4 & 5），大量使用击勾弦、滑音及空弦技巧。底部文字介绍DAEAC#E调弦法，涵盖基于开放弦的大/小三和弦、属七及半减七指型，强调音色浑厚与可移动变调特性。 |

### mathrock_facgce_tapping_sustain - PASS

- Query: FACGCE 点弦琶音谱例，hammer on pull off slide let ring 延音
- Expected any: FACGCE_tapping_arpeggios_sustain
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.039s = embed 0.036s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1138 | 0.0752 | `FACGCE_tapping_arpeggios_sustain` | 36 | tab_excerpt | facgce, hammer, let, off, on, pull, ring, slide, 延音, 点弦, 琶音, 谱例 | FACGCE特殊调弦吉他谱例（变调夹第4品）。包含两组Math Rock风格乐句：上方为带击勾滑音的分解和弦与点弦旋律；下方展示持续震音/发音技法，结合空弦延音与高把位点弦琶音（如9-10-12-14序列），强调声部延续与余音控制。 |
| 2 | 6 |  | 0.1485 | -0.0135 | `DAEAC#E_tuning_arpeggio_phrasing` | 37 | tab_excerpt | hammer, off, on, pull, ring, slide, 延音, 琶音, 谱例 | DAEAC#E特殊调弦下的吉他谱例（第17-22小节），展示基于开放弦的分解和弦乐句。大量使用击勾弦（H/P）与滑音（sl.）技法，结合空弦音构成流畅的连奏线条，体现Math Rock风格中利用非标准调弦构建复杂织体的特征。 |
| 3 | 2 |  | 0.1283 | -0.0203 | `FACGCE_tuning_ideas_and_DAEAC#E_chord_theory` | 37 | tab_excerpt | facgce, hammer, off, on, pull, ring, slide, 谱例 | Math Rock吉他教材第37页，包含FACGCE调弦下的两个乐句谱例（Idea 4 & 5），大量使用击勾弦、滑音及空弦技巧。底部文字介绍DAEAC#E调弦法，涵盖基于开放弦的大/小三和弦、属七及半减七指型，强调音色浑厚与可移动变调特性。 |
| 4 | 3 |  | 0.1371 | -0.0471 | `FACGCE_tuning_minor_scale_pattern` | 35 | fretboard_diagram | facgce, on, ring, 延音, 点弦, 谱例 | FACGCE特殊调弦下的指板音型图（标题：FACGCE调音小调实用笔记）。展示0-7品范围内的音符分布，包含大量空弦音及3、5品的按弦位置。配合下方谱例“Idea 1”，演示了结合变调夹3品、点弦（T）与持续延音的Math Rock风格乐句编写思路。 |
| 5 | 11 |  | 0.1562 | -0.0812 | `DAEAC#E_tuning_math_rock_phrases` | 40 | tab_excerpt | hammer, off, on, pull, ring, 点弦 | Math Rock吉他教材第40页，展示DAEAC#E特殊调弦下的练习乐句（Ideas 1-4）。包含五线谱与六线谱对照，涉及变调夹第2品和第7品的应用。技法涵盖点弦（T）、击勾弦、持续音及开放弦利用，呈现典型的Midwest Emo风格织体。 |

### mathrock_daeacse_chord_voicings - PASS

- Query: DAEAC#E 调弦 Dmaj9 F#m9 E7 G#m7b5 Am9 的和弦指型
- Expected any: DAEAC#E_tuning_chord_voicings_progressions
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.084s = embed 0.082s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0896 | 0.0574 | `DAEAC#E_tuning_chord_voicings_progressions` | 38 | chord_diagram | am9, daeac#e, dmaj9, e7, f#m9, g#m7b5, 和弦, 指型, 的和弦指型, 调弦 | DAEAC#E特殊调弦下的和弦指型库。包含以第六弦（如D大九、F#m9、E7）和第五弦（如A小九、Bm7、E7）为根音的指法，以及G#小七降五等高把位和弦。底部展示了该调弦下的两组和弦进行示例，涵盖大九、小九及减五和弦色彩。 |
| 2 | 2 |  | 0.1092 | 0.0328 | `DAEAC#E_tuning_chord_shape_9th_fret` | 38 | chord_diagram | am9, daeac#e, g#m7b5, 和弦, 指型, 调弦 | DAEAC#E特殊调弦下的五弦和弦指法图，起始于第9品。图示为四音和弦形状，按压第5至2弦（A-E-A-C#），第6弦与第1弦标记为X（不发声）。结合附近文本，该指型对应A小九和弦(Am9)或升G小七降五和弦(G#m7b5)，属于Math Rock风格中常见的封闭和弦Voicing。 |
| 3 | 8 |  | 0.1482 | -0.0342 | `DAEAC#E_tuning_chord_progression_and_arpeggios` | 37 | tab_excerpt | daeac#e, e7, 和弦, 指型, 调弦 | DAEAC#E特殊调弦下的吉他六线谱与五线谱对照练习。包含基于开放弦的饱满和弦指型（大/小/属七/半减七）及分解琶音乐句。大量使用击弦（H）技法连接空弦音，展示该调弦法下利用开放弦共鸣构建Math Rock风格织体的典型语汇。 |
| 4 | 6 |  | 0.1447 | -0.0357 | `AM9_E6_F#m7_GM7_voicings` | 67 | chord_diagram | am9, 和弦, 指型, 调弦 | 四组标准调弦和弦指法图：AM9（根音6弦5品，4品位置）、E6（根音6弦空弦/5品把位）、F#m7（根音6弦2品，4品位置）、GM7（根音6弦3品，5品位置）。包含高弦mute标记(x)，展示Math Rock风格中常见的封闭和弦Voicing。 |
| 5 | 5 |  | 0.1390 | -0.0420 | `DAEAC#E_tuning_chord_shape` | 38 | chord_diagram | daeac#e, 和弦, 调弦 | DAEAC#E特殊调弦下的和弦指法图。图示为六线谱网格，第6、5、4弦为空弦（标记O），第3弦被横按（Barre）覆盖，第2弦某品位有单音按压（黑点），第1弦未发声（标记X）。属于该调式下的基础开放和弦形状之一。 |

### mathrock_daeacse_9th_fret_shape - PASS

- Query: DAEAC#E 第九品附近的 Am9 G#m7b5 和弦图
- Expected any: DAEAC#E_tuning_chord_shape_9th_fret
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.037s = embed 0.035s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 2 | Y | 0.1377 | 0.0613 | `DAEAC#E_tuning_chord_shape_9th_fret` | 38 | chord_diagram | 9, 9th, 9th_fret, 9品, am9, daeac#e, g#m7b5, 和弦, 第9品 | DAEAC#E特殊调弦下的五弦和弦指法图，起始于第9品。图示为四音和弦形状，按压第5至2弦（A-E-A-C#），第6弦与第1弦标记为X（不发声）。结合附近文本，该指型对应A小九和弦(Am9)或升G小七降五和弦(G#m7b5)，属于Math Rock风格中常见的封闭和弦Voicing。 |
| 2 | 1 |  | 0.1377 | -0.0507 | `DAEAC#E_tuning_chord_voicings_progressions` | 38 | chord_diagram | 9, 9th, am9, daeac#e, g#m7b5, 和弦 | DAEAC#E特殊调弦下的和弦指型库。包含以第六弦（如D大九、F#m9、E7）和第五弦（如A小九、Bm7、E7）为根音的指法，以及G#小七降五等高把位和弦。底部展示了该调弦下的两组和弦进行示例，涵盖大九、小九及减五和弦色彩。 |
| 3 | 4 |  | 0.1708 | -0.0768 | `DAEAC#E_tuning_chord_shape` | 38 | chord_diagram | 9, daeac#e, 和弦 | DAEAC#E特殊调弦下的和弦指法图。图示为六线谱网格，第6、5、4弦为空弦（标记O），第3弦被横按（Barre）覆盖，第2弦某品位有单音按压（黑点），第1弦未发声（标记X）。属于该调式下的基础开放和弦形状之一。 |
| 4 | 7 |  | 0.1804 | -0.0774 | `AM9_E6_F#m7_GM7_voicings` | 67 | chord_diagram | 9, am9, 和弦 | 四组标准调弦和弦指法图：AM9（根音6弦5品，4品位置）、E6（根音6弦空弦/5品把位）、F#m7（根音6弦2品，4品位置）、GM7（根音6弦3品，5品位置）。包含高弦mute标记(x)，展示Math Rock风格中常见的封闭和弦Voicing。 |
| 5 | 11 |  | 0.2070 | -0.1010 | `FACGCE_chord_shape_5th_string_root` | 33 | chord_diagram | 9, 9品, 和弦, 第9品 | FACGCE特殊调弦下的和弦指型图，起始于第5弦（A弦）第9品。图示为横按指法，覆盖第5至第1弦的第9至11品区域，第6弦与第1弦标记为不发声（X）。属于教材中“从第五弦起始的和弦指型”部分，用于构建Math Rock风格的复杂和声色彩。 |

### mathrock_daeacse_major_minor_scales - PASS

- Query: DAEAC#E 大调小调音阶，0到7品，开放弦重复音选择
- Expected any: DAEAC#E_tuning_major_minor_scales, DAEAC#E_tuning_major_minor_scale_patterns
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.089s = embed 0.086s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 3 | Y | 0.1111 | 0.0549 | `DAEAC#E_tuning_major_minor_scale_patterns` | 39 | fretboard_diagram | 0, 7, daeac#e, 大调, 小调, 开放弦, 音阶 | DAEAC#E特殊调弦下的指板音阶分布图（0-7品）。展示大调与小调实用音符位置，包含空弦音及黑点标记的根音/关键音。音符非连续排列，设计用于主奏、旋律创作及点弦连复段，强调听觉引导的音符走向梳理。 |
| 2 | 4 |  | 0.1158 | 0.0352 | `DAEAC#E_tuning_major_scale_pattern` | 39 | fretboard_diagram | 0, 7, daeac#e, 大调, 开放弦, 音阶 | DAEAC#E特殊调弦下的大调实用音符指板图。展示0至7品范围内的音阶分布，包含空弦音（6、2、1弦）及黑点标记的根音位置。该图谱并非连续排列，旨在提供主奏、旋律创作及点弦连复段时的多音符选择，利用听觉梳理走向。 |
| 3 | 1 | Y | 0.0973 | 0.0327 | `DAEAC#E_tuning_major_minor_scales` | 39 | fretboard_diagram | 0, 7, daeac#e, 大调, 小调, 开放弦, 音阶 | DAEAC#E特殊调弦下的指板图，展示大调与小调实用音符分布（0-7品）。黑色圆点标记根音位置，空心圆为音阶内其他音符。设计用于主奏、旋律创作及点弦连复段，提供非连续排列的音符选择以辅助听觉导向的乐句构建。 |
| 4 | 11 |  | 0.1564 | -0.0084 | `FACGCE_minor_scale_pattern` | 35 | fretboard_diagram | 0, 7, 小调, 开放弦, 音阶 | FACGCE特殊调弦下的指板音阶图，标题为“FACGCE调音小调实用笔记”。图示展示了开放弦至第7品的音位分布，包含大量空弦音（E/C/G/C/A）及按弦音（黑点），用于构建小调乐句与把位模式。 |
| 5 | 9 |  | 0.1307 | -0.0127 | `DAEAC#E_tuning_math_rock_phrases` | 40 | tab_excerpt | 0, 7, daeac#e, 开放弦, 音阶 | Math Rock吉他教材第40页，展示DAEAC#E特殊调弦下的练习乐句（Ideas 1-4）。包含五线谱与六线谱对照，涉及变调夹第2品和第7品的应用。技法涵盖点弦（T）、击勾弦、持续音及开放弦利用，呈现典型的Midwest Emo风格织体。 |

### mathrock_daeacse_tapping_phrase - PASS

- Query: DAEAC#E tapping phrase，击弦勾弦和持续音的 math rock 谱例
- Expected any: DAEAC#E_tuning_math_rock_phrases, DAEAC#E_tuning_arpeggio_phrasing
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.037s = embed 0.035s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1208 | -0.0098 | `DAEAC#E_tuning_math_rock_phrases` | 40 | tab_excerpt | daeac#e, math, phrase, rock, tapping | Math Rock吉他教材第40页，展示DAEAC#E特殊调弦下的练习乐句（Ideas 1-4）。包含五线谱与六线谱对照，涉及变调夹第2品和第7品的应用。技法涵盖点弦（T）、击勾弦、持续音及开放弦利用，呈现典型的Midwest Emo风格织体。 |
| 2 | 2 | Y | 0.1449 | -0.0609 | `DAEAC#E_tuning_arpeggio_phrasing` | 37 | tab_excerpt | daeac#e, math, rock, 谱例 | DAEAC#E特殊调弦下的吉他谱例（第17-22小节），展示基于开放弦的分解和弦乐句。大量使用击勾弦（H/P）与滑音（sl.）技法，结合空弦音构成流畅的连奏线条，体现Math Rock风格中利用非标准调弦构建复杂织体的特征。 |
| 3 | 3 |  | 0.1458 | -0.0648 | `FACGCE_tapping_arpeggios_sustain` | 36 | tab_excerpt | math, rock, tapping, 谱例 | FACGCE特殊调弦吉他谱例（变调夹第4品）。包含两组Math Rock风格乐句：上方为带击勾滑音的分解和弦与点弦旋律；下方展示持续震音/发音技法，结合空弦延音与高把位点弦琶音（如9-10-12-14序列），强调声部延续与余音控制。 |
| 4 | 5 |  | 0.1526 | -0.0686 | `FACGCE_tuning_ideas_and_DAEAC#E_chord_theory` | 37 | tab_excerpt | daeac#e, math, rock, 谱例 | Math Rock吉他教材第37页，包含FACGCE调弦下的两个乐句谱例（Idea 4 & 5），大量使用击勾弦、滑音及空弦技巧。底部文字介绍DAEAC#E调弦法，涵盖基于开放弦的大/小三和弦、属七及半减七指型，强调音色浑厚与可移动变调特性。 |
| 5 | 4 |  | 0.1460 | -0.0830 | `DAEAC#E_tuning_chord_shape` | 38 | chord_diagram | daeac#e, math, rock | DAEAC#E特殊调弦下的和弦指法图。图示为六线谱网格，第6、5、4弦为空弦（标记O），第3弦被横按（Barre）覆盖，第2弦某品位有单音按压（黑点），第1弦未发声（标记X）。属于该调式下的基础开放和弦形状之一。 |

### mathrock_dm7_bm7b5_nearest_voicing - PASS

- Query: Dm7 到 Bm7b5 的最近邻和弦移动，不同弦组 voicing
- Expected any: Dm7_Bm7b5_voicings_by_string_set
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.037s = embed 0.035s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0943 | -0.0093 | `Dm7_Bm7b5_voicings_by_string_set` | 49 | chord_diagram | bm7b5, dm7, voicing, 和弦 | 展示Dm7与Bm7b5（小七降五）和弦的多种指板配置。按根音所在弦组分类：第六弦、第五弦及第四弦根音位置。包含Dm7在10品、5品、12品的变体，以及Bm7b5在6品、9品的变体。文本提及C大调I-vi-V-IV进行(CM7/Am7/G7/FM7)作为应用背景。 |
| 2 | 2 |  | 0.1288 | -0.0618 | `shell_voicings_Dm7_G7_m7_progression` | 61 | chord_diagram | dm7, voicing, 和弦 | 展示属七与小七和弦的壳式按法（Shell Voicings），包含Dm7、G7及下行m7进行（G#m7-F#m7-A#m7-Bmaj7）。图示强调由根音、三音、七音构成的三音结构，省略五音，覆盖4至10品区域。文本说明此类排列同样适用于小七降五和弦，并建议用于构建Math Rock即兴Riff基础框架。 |
| 3 | 7 |  | 0.1480 | -0.0660 | `AM9_E6_F#m7_GM7_voicings` | 67 | chord_diagram | voicing, 和弦 | 四组标准调弦和弦指法图：AM9（根音6弦5品，4品位置）、E6（根音6弦空弦/5品把位）、F#m7（根音6弦2品，4品位置）、GM7（根音6弦3品，5品位置）。包含高弦mute标记(x)，展示Math Rock风格中常见的封闭和弦Voicing。 |
| 4 | 6 |  | 0.1467 | -0.0677 | `high_fret_jazz_voicings_progression` | 67 | chord_diagram | voicing, 和弦 | 展示了一组高把位（7-10品）的爵士风格六和弦与九和弦指型图。包含C6(IV)、G6/9(I)、Bm7(三级)、Dm6/9(V)及Am7(ii)。所有和弦均标注了根音位置或级数功能，且多采用 mute 1、6 弦的封闭指法，强调中间四弦的和声色彩。 |
| 5 | 12 |  | 0.1634 | -0.0874 | `DAEAC#E_tuning_chord_shape_9th_fret` | 38 | chord_diagram | voicing, 和弦 | DAEAC#E特殊调弦下的五弦和弦指法图，起始于第9品。图示为四音和弦形状，按压第5至2弦（A-E-A-C#），第6弦与第1弦标记为X（不发声）。结合附近文本，该指型对应A小九和弦(Am9)或升G小七降五和弦(G#m7b5)，属于Math Rock风格中常见的封闭和弦Voicing。 |

### mathrock_cm7_am7_g7_fm7 - PASS

- Query: CM7 Am7 G7 FM7 的 drop2 或横按 voicing 变化
- Expected any: CM7_Am7_G7_FM7_voicings_variations
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.036s = embed 0.034s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1529 | -0.0109 | `CM7_Am7_G7_FM7_voicings_variations` | 50 | chord_diagram | am7, cm7, drop2, fm7, g7, voicing, 变化 | 展示CM7、Am7、G7、FM7四种七和弦的三种不同把位指型（开放/低把位、中把位5-8品、高把位8-12品）。包含根音位置变化及横按技法，用于演示同一和弦在指板不同区域的Voicing选择与声部连接逻辑。 |
| 2 | 3 |  | 0.1839 | -0.1049 | `AM9_E6_F#m7_GM7_voicings` | 67 | chord_diagram | am7, voicing | 四组标准调弦和弦指法图：AM9（根音6弦5品，4品位置）、E6（根音6弦空弦/5品把位）、F#m7（根音6弦2品，4品位置）、GM7（根音6弦3品，5品位置）。包含高弦mute标记(x)，展示Math Rock风格中常见的封闭和弦Voicing。 |
| 3 | 2 |  | 0.1805 | -0.1315 | `CM7_GM7_Bm7_voicings_comparison` | 51 | chord_diagram | cm7, voicing | Math Rock风格教材第51页，展示CM7、GM7、Bm7的三种不同把位指型。第一组为开放/低把位指法；第二组为高把位封闭和弦（8-10品）；第三组为练习题，给出10品CM7变体，要求匹配后续GM7/Bm7指型。包含详细左手按弦数字标注及闷音符号。 |
| 4 | 12 |  | 0.2200 | -0.1320 | `Dm7_Bm7b5_voicings_by_string_set` | 49 | chord_diagram | am7, cm7, fm7, g7, voicing | 展示Dm7与Bm7b5（小七降五）和弦的多种指板配置。按根音所在弦组分类：第六弦、第五弦及第四弦根音位置。包含Dm7在10品、5品、12品的变体，以及Bm7b5在6品、9品的变体。文本提及C大调I-vi-V-IV进行(CM7/Am7/G7/FM7)作为应用背景。 |
| 5 | 9 |  | 0.2155 | -0.1365 | `high_fret_jazz_voicings_progression` | 67 | chord_diagram | am7, voicing | 展示了一组高把位（7-10品）的爵士风格六和弦与九和弦指型图。包含C6(IV)、G6/9(I)、Bm7(三级)、Dm6/9(V)及Am7(ii)。所有和弦均标注了根音位置或级数功能，且多采用 mute 1、6 弦的封闭指法，强调中间四弦的和声色彩。 |

### mathrock_minor_69_shell_voicing - PASS

- Query: Dm6/9 和 CM7 的 shell voicing，扩展和弦声部
- Expected any: minor_6/9_voicings, maj7_shell_voicings
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.037s = embed 0.035s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1651 | -0.0471 | `minor_6/9_voicings / maj7_shell_voicings` | 60 | chord_diagram | cm7, dm6, dm6/9, shell, voicing, 和弦, 声部 | 展示Dm6/9（8、10品）与CM7（7、9品）的扩展和弦及壳式和弦指型图。重点在于保留核心音（3度、7度）并添加延伸音（6度、9度），采用中间四弦排列，省略五音，适用于数学摇滚风格的密集和声语境。 |
| 2 | 7 |  | 0.1971 | -0.0761 | `high_fret_jazz_voicings_progression` | 67 | chord_diagram | dm6, dm6/9, voicing, 和弦, 声部 | 展示了一组高把位（7-10品）的爵士风格六和弦与九和弦指型图。包含C6(IV)、G6/9(I)、Bm7(三级)、Dm6/9(V)及Am7(ii)。所有和弦均标注了根音位置或级数功能，且多采用 mute 1、6 弦的封闭指法，强调中间四弦的和声色彩。 |
| 3 | 2 |  | 0.1754 | -0.0964 | `shell_voicings_Dm7_G7_m7_progression` | 61 | chord_diagram | shell, voicing, 和弦, 声部 | 展示属七与小七和弦的壳式按法（Shell Voicings），包含Dm7、G7及下行m7进行（G#m7-F#m7-A#m7-Bmaj7）。图示强调由根音、三音、七音构成的三音结构，省略五音，覆盖4至10品区域。文本说明此类排列同样适用于小七降五和弦，并建议用于构建Math Rock即兴Riff基础框架。 |
| 4 | 4 |  | 0.1917 | -0.0977 | `AM9_E6_F#m7_GM7_voicings` | 67 | chord_diagram | voicing, 和弦, 声部 | 四组标准调弦和弦指法图：AM9（根音6弦5品，4品位置）、E6（根音6弦空弦/5品把位）、F#m7（根音6弦2品，4品位置）、GM7（根音6弦3品，5品位置）。包含高弦mute标记(x)，展示Math Rock风格中常见的封闭和弦Voicing。 |
| 5 | 5 |  | 0.1933 | -0.1113 | `CM7_Am7_G7_FM7_voicings_variations` | 50 | chord_diagram | cm7, voicing, 和弦, 声部 | 展示CM7、Am7、G7、FM7四种七和弦的三种不同把位指型（开放/低把位、中把位5-8品、高把位8-12品）。包含根音位置变化及横按技法，用于演示同一和弦在指板不同区域的Voicing选择与声部连接逻辑。 |

### mathrock_shell_voicing_progression - PASS

- Query: shell voicing 构建 Dm7 G7 G#m7 F#m7 Bmaj7 进行
- Expected any: shell_voicings_Dm7_G7_m7_progression
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.037s = embed 0.035s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1583 | 0.0107 | `shell_voicings_Dm7_G7_m7_progression` | 61 | chord_diagram | bmaj7, dm7, f#m7, g#m7, g7, shell, voicing, 构建, 进行 | 展示属七与小七和弦的壳式按法（Shell Voicings），包含Dm7、G7及下行m7进行（G#m7-F#m7-A#m7-Bmaj7）。图示强调由根音、三音、七音构成的三音结构，省略五音，覆盖4至10品区域。文本说明此类排列同样适用于小七降五和弦，并建议用于构建Math Rock即兴Riff基础框架。 |
| 2 | 5 |  | 0.1918 | -0.0918 | `AM9_E6_F#m7_GM7_voicings` | 67 | chord_diagram | f#m7, voicing, 构建 | 四组标准调弦和弦指法图：AM9（根音6弦5品，4品位置）、E6（根音6弦空弦/5品把位）、F#m7（根音6弦2品，4品位置）、GM7（根音6弦3品，5品位置）。包含高弦mute标记(x)，展示Math Rock风格中常见的封闭和弦Voicing。 |
| 3 | 8 |  | 0.2019 | -0.1109 | `Dm7_Bm7b5_voicings_by_string_set` | 49 | chord_diagram | dm7, g7, voicing, 构建, 进行 | 展示Dm7与Bm7b5（小七降五）和弦的多种指板配置。按根音所在弦组分类：第六弦、第五弦及第四弦根音位置。包含Dm7在10品、5品、12品的变体，以及Bm7b5在6品、9品的变体。文本提及C大调I-vi-V-IV进行(CM7/Am7/G7/FM7)作为应用背景。 |
| 4 | 7 |  | 0.1996 | -0.1116 | `high_fret_jazz_voicings_progression` | 67 | chord_diagram | voicing, 构建, 进行 | 展示了一组高把位（7-10品）的爵士风格六和弦与九和弦指型图。包含C6(IV)、G6/9(I)、Bm7(三级)、Dm6/9(V)及Am7(ii)。所有和弦均标注了根音位置或级数功能，且多采用 mute 1、6 弦的封闭指法，强调中间四弦的和声色彩。 |
| 5 | 4 |  | 0.1909 | -0.1149 | `CM7_Am7_G7_FM7_voicings_variations` | 50 | chord_diagram | g7, voicing, 构建, 进行 | 展示CM7、Am7、G7、FM7四种七和弦的三种不同把位指型（开放/低把位、中把位5-8品、高把位8-12品）。包含根音位置变化及横按技法，用于演示同一和弦在指板不同区域的Voicing选择与声部连接逻辑。 |

### mathrock_extended_chord_progressions - PASS

- Query: CM9 Dsus4 Em9 Gsus2 C6/9 Am9 扩展和弦进行
- Expected any: extended_chord_voicings_progressions
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.037s = embed 0.034s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1454 | -0.0154 | `extended_chord_voicings_progressions` | 64 | chord_diagram | am9, c6, c6/9, cm9, dsus4, em9, gsus2, 和弦 | 标准调弦下三组扩展和弦指型图。第一组含CM9、Dsus4(5品)、Em9(5品)、Gsus2(3品)；第二组为C大调IV-ii-I-ii进行(C6/9-Am7-G6)；第三组为F大调IV-V-vi-V高把位进行(FM9 7品-G6/9 9品-Am9 10品)。 |
| 2 | 7 |  | 0.1919 | -0.0979 | `AM9_E6_F#m7_GM7_voicings` | 67 | chord_diagram | am9, c6, 和弦 | 四组标准调弦和弦指法图：AM9（根音6弦5品，4品位置）、E6（根音6弦空弦/5品把位）、F#m7（根音6弦2品，4品位置）、GM7（根音6弦3品，5品位置）。包含高弦mute标记(x)，展示Math Rock风格中常见的封闭和弦Voicing。 |
| 3 | 8 |  | 0.1967 | -0.1087 | `DAEAC#E_tuning_chord_shape_9th_fret` | 38 | chord_diagram | am9, c6, 和弦 | DAEAC#E特殊调弦下的五弦和弦指法图，起始于第9品。图示为四音和弦形状，按压第5至2弦（A-E-A-C#），第6弦与第1弦标记为X（不发声）。结合附近文本，该指型对应A小九和弦(Am9)或升G小七降五和弦(G#m7b5)，属于Math Rock风格中常见的封闭和弦Voicing。 |
| 4 | 10 |  | 0.1997 | -0.1237 | `high_fret_jazz_voicings_progression` | 67 | chord_diagram | c6, 和弦 | 展示了一组高把位（7-10品）的爵士风格六和弦与九和弦指型图。包含C6(IV)、G6/9(I)、Bm7(三级)、Dm6/9(V)及Am7(ii)。所有和弦均标注了根音位置或级数功能，且多采用 mute 1、6 弦的封闭指法，强调中间四弦的和声色彩。 |
| 5 | 2 |  | 0.1742 | -0.1282 | `Gsus4_voicings / FM9_Am9_G7_progression` | 56 | chord_diagram | am9, 和弦 | 展示三种不同把位的Gsus4和弦指型图（含开放、5品、10品位），以及FM9(7品)、Am9(10品)与G7(10品)的和弦进行图示。文字说明在数学摇滚中，使用挂四和弦替换属七和弦（V级）可消除突兀感，优化声部连接。 |

### mathrock_jazz_voicings_high_fret - PASS

- Query: 高把位 jazz voicing，C6 G6/9 Bm7 Dm6/9 Am7
- Expected any: high_fret_jazz_voicings_progression
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.036s = embed 0.034s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1324 | 0.0696 | `high_fret_jazz_voicings_progression` | 67 | chord_diagram | am7, bm7, c6, dm6, dm6/9, g6, g6/9, jazz, voicing, 高把位 | 展示了一组高把位（7-10品）的爵士风格六和弦与九和弦指型图。包含C6(IV)、G6/9(I)、Bm7(三级)、Dm6/9(V)及Am7(ii)。所有和弦均标注了根音位置或级数功能，且多采用 mute 1、6 弦的封闭指法，强调中间四弦的和声色彩。 |
| 2 | 2 |  | 0.1532 | -0.0502 | `extended_chord_voicings_progressions` | 64 | chord_diagram | am7, c6, g6, g6/9, voicing, 高把位 | 标准调弦下三组扩展和弦指型图。第一组含CM9、Dsus4(5品)、Em9(5品)、Gsus2(3品)；第二组为C大调IV-ii-I-ii进行(C6/9-Am7-G6)；第三组为F大调IV-V-vi-V高把位进行(FM9 7品-G6/9 9品-Am9 10品)。 |
| 3 | 4 |  | 0.1695 | -0.0545 | `AM9_E6_F#m7_GM7_voicings` | 67 | chord_diagram | am7, bm7, c6, voicing, 高把位 | 四组标准调弦和弦指法图：AM9（根音6弦5品，4品位置）、E6（根音6弦空弦/5品把位）、F#m7（根音6弦2品，4品位置）、GM7（根音6弦3品，5品位置）。包含高弦mute标记(x)，展示Math Rock风格中常见的封闭和弦Voicing。 |
| 4 | 5 |  | 0.1712 | -0.1052 | `jazz_voicings_progressions_4_5` | 65 | chord_diagram | am7, jazz, voicing, 高把位 | 展示两组爵士风格吉他指法图：进行四(IV-ii-I)包含CM7、Am11、GM7；进行五(I-IV-vi)包含CM9、FM9、Am7。涉及高把位封闭和弦与根音省略，强调6/9和弦作为属七替代的优雅方案及上行模式的振奋感。 |
| 5 | 9 |  | 0.1826 | -0.1096 | `DAEAC#E_tuning_chord_shape_9th_fret` | 38 | chord_diagram | c6, voicing | DAEAC#E特殊调弦下的五弦和弦指法图，起始于第9品。图示为四音和弦形状，按压第5至2弦（A-E-A-C#），第6弦与第1弦标记为X（不发声）。结合附近文本，该指型对应A小九和弦(Am9)或升G小七降五和弦(G#m7b5)，属于Math Rock风格中常见的封闭和弦Voicing。 |

### mathrock_gsus4_fm9_am9_g7 - PASS

- Query: Gsus4 FM9 Am9 G7 的 voicing substitution 和和弦进行
- Expected any: Gsus4_voicings, FM9_Am9_G7_progression
- First hit rank: 1
- Rerank: `True`, candidates: 20
- Latency: total 0.036s = embed 0.034s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1619 | -0.0229 | `Gsus4_voicings / FM9_Am9_G7_progression` | 56 | chord_diagram | am9, fm9, g7, gsus4, substitution, voicing, 和弦 | 展示三种不同把位的Gsus4和弦指型图（含开放、5品、10品位），以及FM9(7品)、Am9(10品)与G7(10品)的和弦进行图示。文字说明在数学摇滚中，使用挂四和弦替换属七和弦（V级）可消除突兀感，优化声部连接。 |
| 2 | 2 |  | 0.1941 | -0.0911 | `AM9_E6_F#m7_GM7_voicings` | 67 | chord_diagram | am9, voicing, 和弦 | 四组标准调弦和弦指法图：AM9（根音6弦5品，4品位置）、E6（根音6弦空弦/5品把位）、F#m7（根音6弦2品，4品位置）、GM7（根音6弦3品，5品位置）。包含高弦mute标记(x)，展示Math Rock风格中常见的封闭和弦Voicing。 |
| 3 | 3 |  | 0.1989 | -0.1259 | `extended_chord_voicings_progressions` | 64 | chord_diagram | am9, fm9, voicing, 和弦 | 标准调弦下三组扩展和弦指型图。第一组含CM9、Dsus4(5品)、Em9(5品)、Gsus2(3品)；第二组为C大调IV-ii-I-ii进行(C6/9-Am7-G6)；第三组为F大调IV-V-vi-V高把位进行(FM9 7品-G6/9 9品-Am9 10品)。 |
| 4 | 5 |  | 0.2039 | -0.1369 | `CM7_Am7_G7_FM7_voicings_variations` | 50 | chord_diagram | g7, voicing, 和弦 | 展示CM7、Am7、G7、FM7四种七和弦的三种不同把位指型（开放/低把位、中把位5-8品、高把位8-12品）。包含根音位置变化及横按技法，用于演示同一和弦在指板不同区域的Voicing选择与声部连接逻辑。 |
| 5 | 7 |  | 0.2190 | -0.1400 | `high_fret_jazz_voicings_progression` | 67 | chord_diagram | voicing, 和弦 | 展示了一组高把位（7-10品）的爵士风格六和弦与九和弦指型图。包含C6(IV)、G6/9(I)、Bm7(三级)、Dm6/9(V)及Am7(ii)。所有和弦均标注了根音位置或级数功能，且多采用 mute 1、6 弦的封闭指法，强调中间四弦的和声色彩。 |
