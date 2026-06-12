# Visual Caption Retrieval Trial

## Summary

- Collection: `guitar_fretboard_answer_captions_qwen3_06b` (389 docs)
- Model: `D:\Guitar Arrangement Inspiration Agent\KGraphRag2\models\embedding\qwen3-embedding-0.6b` on `cuda`, dim=1024
- Tests: 7, TopK: 5
- Rerank: `True`, candidates: 30
- Hit@1: 7/7
- Hit@K: 7/7
- Avg total latency/query: 0.295s
- Median total latency/query: 0.122s

## Cases

### foundation_b6 - PASS

- Query: B6 六和弦指法，不包含七度音，根音在九品附近
- Expected any: B6_chord_shape, B6
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 1.281s = embed 0.854s + chroma 0.427s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1439 | -0.0649 | `B6` | data/练习解答（图片）/练习58-59.png | chord_diagram | b6, 和弦, 指法 | B6和弦垂直指板图，位于IX（第9）把位。图示包含四个按点，根音位于低音区第9品（双圈强调）。上方标注指法数字1、5、6、3，对应和弦内音排列。 |
| 2 | 3 |  | 0.1540 | -0.0990 | `Bbmi6/9` | data/练习解答（图片）/练习58-59.png | chord_diagram | 和弦, 指法 | Bbmi6/9和弦指板图，把位XI（11品）。声部构成标注为1、b3、6、9。根音Bb在5弦11品，其余音分布在4-2弦的12品位置。 |
| 3 | 5 | Y | 0.1556 | -0.1036 | `指板音程构建图示 (根音-3度-6度)` | data/练习解答（图片）/练习28-29.png | scale_pattern | b6, 和弦 | 垂直指板图展示复合音程构建基础：空心圆为根音，相邻品格实心点为3度音，下方弦实心点为6度音。结合题干要求构建9、13、#11等复合音程，此图为音程关系的视觉参照。 |
| 4 | 7 |  | 0.1573 | -0.1053 | `第6弦（低音E弦）自然音阶音符分布图` | data/练习解答（图片）/练习6-练习9.png | fretboard_diagram | 和弦, 指法 | 吉他第6弦（低音E弦）前四品自然音阶指板图。展示了从空弦E开始，依次经过F(1品)、G(3品)、A(5品推断/图中未显全但逻辑连续)、B、C、D等音的线性排列。图中明确标出空弦至3品内的音名为：E, F, G, A, B, C, D, E, F, G。用于记忆单弦音阶位置。 |
| 5 | 2 |  | 0.1508 | -0.1058 | `指板音程关系图（根音与上方音）` | data/练习解答（图片）/练习28-29.png | scale_pattern | 和弦, 指法 | 垂直指板局部图，展示以第6弦空心圆为根音的相对音程位置。可见两个目标音：第5弦向右2格（大二度/9度位置）和第4弦向右3格（纯四度/11度位置）。结合题干“构建复合音程”，此图为寻找9、11、13度音的指法参考。 |

### foundation_fm7b5 - PASS

- Query: F小七减五 Fm7b5 琶音指型，低把位，半减七和弦
- Expected any: Fm7b5_arpeggio_shape_1, F half-diminished
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.117s = embed 0.098s + chroma 0.019s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 2 | Y | 0.1305 | 0.0355 | `Fmi7(b5) 琶音 指型3` | data/练习解答（图片）/练习39-42.png | arpeggio_pattern | 低把位, 半减七和弦, 和弦, 小七减五, 指型, 琶音, 琶音指型 | Fmi7(b5)琶音指型3的吉他指板图示。图中展示了F半减七和弦在指板上的分布，根音F以双圈特别标出。该指型覆盖了约5个品位的跨度，用于练习F小七减五和弦的色彩与把位记忆。 |
| 2 | 1 | Y | 0.1287 | 0.0123 | `Fmi7(b5) 琶音 指型2` | data/练习解答（图片）/练习39-42.png | arpeggio_pattern | 半减七和弦, 和弦, 小七减五, 指型, 琶音, 琶音指型 | Fmi7(b5)半减七和弦琶音指型2图示，位于VII把位。图中标注了六个按点位置，并用双圈特别标出了根音F的位置，用于展示该和弦在指板上的第二种排列形态。 |
| 3 | 5 | Y | 0.1461 | 0.0069 | `Fmi7(b5) 琶音 指型4` | data/练习解答（图片）/练习39-42.png | arpeggio_pattern | fm7b5, 半减七和弦, 和弦, 小七减五, 指型, 琶音, 琶音指型 | Fmi7(b5)半减七和弦琶音指型4图解。图中展示了该和弦在吉他指板上的四种八度内分布形态，明确标注了“指型4”。6弦、4弦及1弦上的F音（根音）使用双圈特别标识，用于辅助记忆根音位置及把位结构。 |
| 4 | 4 | Y | 0.1414 | 0.0026 | `Fmi7(b5) 琶音 指型1` | data/练习解答（图片）/练习39-42.png | arpeggio_pattern | 半减七和弦, 和弦, 小七减五, 指型, 琶音, 琶音指型 | Fmi7(b5)半减七和弦琶音指型1图解。图中标注罗马数字VI表示把位位置，双圈标示根音F。该指型展示了F小七减五和弦在指板上的第一种排列方式，适用于构建爵士乐句或即兴伴奏。 |
| 5 | 3 | Y | 0.1389 | -0.0009 | `Fmi7(b5) 琶音 指型5` | data/练习解答（图片）/练习39-42.png | arpeggio_pattern | 半减七和弦, 和弦, 小七减五, 指型, 琶音, 琶音指型 | Fmi7(b5)和弦琶音指板图，标注为“指型5”。图中展示了该半减七和弦在指板上的五种指型之一，包含六个音符位置，其中两个音符被双圈高亮标记为根音F。 |

### foundation_d_major - PASS

- Query: D大三和弦琶音 指型1 根音三音五音
- Expected any: D_major_triad_arpeggio_shape_1, D大三和弦琶音, D major triad arpeggio
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.129s = embed 0.106s + chroma 0.023s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1097 | 0.0373 | `D大三和弦琶音 指型1` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern | 1, 和弦, 大三和弦琶音, 指型, 琶音 | 练习30答案图：D大三和弦琶音指型1。横向指板图显示该指型的音符分布，包含4个按点与2个标示根音的空心圈，对应D Major Triad Arpeggio Shape 1的把位按法。 |
| 2 | 2 | Y | 0.1118 | 0.0262 | `D大三和弦琶音 指型4` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern | 1, 和弦, 大三和弦琶音, 指型, 琶音 | 练习30第4题答案：D大三和弦(D Major Triad)琶音指型4。图示为横向指板局部，包含根音D(空心)、三音F#(实心)、五音A(空心)。根据D音位置推断约为10-12把位区域，展示该指型下的完整琶音音符分布。 |
| 3 | 3 | Y | 0.1153 | 0.0227 | `D大三和弦琶音 指型2` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern | 1, 和弦, 大三和弦琶音, 指型, 琶音 | D大三和弦琶音指型2的指板图示。包含根音(D)、三音(F#)、五音(A)的分布位置。图中以空心圆标示根音，实心点标示其他和弦内音，展示了该指型在指板上的具体按法结构。 |
| 4 | 4 | Y | 0.1234 | 0.0146 | `D大三和弦琶音 指型5` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern | 1, 和弦, 大三和弦琶音, 指型, 琶音 | 练习30第5题答案：D大三和弦琶音指型5图示。图中展示了D Major Arpeggio在指板上的分布，包含根音（空心圈）及三音、五音（实心点），对应教材中的第五种指法形态。 |
| 5 | 6 | Y | 0.1244 | 0.0136 | `D大三和弦琶音 指型3` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern | 1, 和弦, 大三和弦琶音, 指型, 琶音 | 练习30答案：D大三和弦琶音指型3。图示为横向指板，标记VII把位。包含3个实心和2个空心根音节点，展示D Major Triad在第7把位的指法排列，用于构建D和弦琶音。 |

### foundation_d_dim - PASS

- Query: D减三和弦琶音，根音小三度减五度，制造紧张经过感
- Expected any: D_diminished_triad_arpeggio_shape, D diminished
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.122s = embed 0.111s + chroma 0.010s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1219 | -0.0199 | `D减三和弦琶音 指型1` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern | 减三和弦琶音, 和弦, 琶音 | D减三和弦(D diminished triad)琶音指型1图示。水平指板图显示六线谱按点分布，包含空心圆(可能为根音或起始音)与实心黑点。根据题目语境，该指型覆盖约4个品格跨度，展示D-F-Ab音程结构的指板排列。 |
| 2 | 3 | Y | 0.1389 | -0.0369 | `D减三和弦琶音 指型2` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern | 减三和弦琶音, 和弦, 琶音 | 吉他指板图示：D减三和弦（D diminished triad）琶音指型2。图中显示横向指板，标有5个实心按点和2个空心根音标记，对应练习32第2小题答案。 |
| 3 | 4 | Y | 0.1417 | -0.0397 | `D减三和弦琶音 指型4` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern | 减三和弦琶音, 和弦, 琶音 | 吉他指板图解：D减三和弦（D diminished triad）琶音指型4。图中展示了该和弦在指板上的按法分布，包含根音（空心圆）及组成音（实心点），适用于构建Ddim琶音练习。 |
| 4 | 6 | Y | 0.1486 | -0.0466 | `D减三和弦琶音 指型3` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern | 减三和弦琶音, 和弦, 琶音 | 吉他指板图示：D减三和弦（D diminished triad）琶音指型3。图示为横向六线谱局部，下方标注罗马数字 VII（第七把位）。包含5个实心按点与2个空心圈音符，展示该和弦在指板上的特定排列形态。 |
| 5 | 2 | Y | 0.1377 | -0.0477 | `D减三和弦 指型5` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern | 减三和弦琶音, 和弦, 琶音 | 吉他指板图示：D减三和弦（D diminished triad）琶音指型5。图中标注“5) D减三和弦 指型5”，显示横向指板上的音符排列，包含实心按点与空心圈，对应练习要求的第10-11把位区域。 |

### foundation_gsus2 - PASS

- Query: Gsus2 挂二和弦 1 2 5 构成音，在图上补全指法
- Expected any: Gsus2_chord_shape_exercise, Gsus2, 挂二和弦
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.092s = embed 0.080s + chroma 0.012s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1414 | -0.0064 | `Gsus2` | data/练习解答（图片）/练习58-59.png | chord_diagram | 1, 2, 5, gsus2, 和弦, 指法, 构成音 | Gsus2和弦指法图，位于第II把位。图示包含根音标记及声部编号1、2、5，展示了该挂留和弦在指板上的具体按点位置与构成音分布。 |
| 2 | 2 |  | 0.2054 | -0.0904 | `C/G (C major triad over G bass)` | data/练习解答（图片）/练习58-59.png | chord_diagram | 1, 2, 5, 和弦, 指法, 构成音 | 吉他指板图示展示 C/G 和弦指型。位于第 V 把位（约第5品），指法标记为 5-1-3。构成音为低音 G 加上 C 大三和弦（C-E-G），属于 Slash 和弦 voicing。 |
| 3 | 18 |  | 0.2292 | -0.1052 | `G13` | data/练习解答（图片）/练习49-51.png | chord_diagram | 1, 2, 5, 和弦, 指法, 构成音 | G13和弦指法图，位于第3把位（III）。图示标注了声部构成音程：b7、3、13、1。按点分布在6弦3品、5弦5品、4弦4品及2弦3品（双圈强调）。 |
| 4 | 21 |  | 0.2306 | -0.1096 | `G7(#5)` | data/练习解答（图片）/练习49-51.png | chord_diagram | 1, 2, 5, 和弦, 指法, 构成音 | 练习51第8题答案：G7(#5)和弦指法图。根音位于III把位（3品6弦），构成音标注为b7、3、#5，分别位于4品5弦、5品4弦和5品3弦。 |
| 5 | 5 |  | 0.2188 | -0.1098 | `Gbma13` | data/练习解答（图片）/练习49-51.png | chord_diagram | 1, 2, 5, 和弦, 指法 | Gbma13和弦指法图，位于第II把位。图示标注了声部构成：1(根音)、7、3、13。6弦2品为根音Gb，配合5、4、3弦的延伸音构成大十三和弦。 |

### foundation_plain_g7 - PASS

- Query: 标准调弦 G7 属七和弦普通指型图
- Expected any: G7
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.209s = embed 0.180s + chroma 0.029s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 2 | Y | 0.1604 | -0.0844 | `G7(#5)` | data/练习解答（图片）/练习49-51.png | chord_diagram | g7, 和弦, 指型 | 练习51第8题答案：G7(#5)和弦指法图。根音位于III把位（3品6弦），构成音标注为b7、3、#5，分别位于4品5弦、5品4弦和5品3弦。 |
| 2 | 4 | Y | 0.1701 | -0.0941 | `G7(b9)` | data/练习解答（图片）/练习49-51.png | chord_diagram | g7, 和弦, 指型 | 垂直指板图展示 G7(b9) 和弦，位于第 IX 把位（9品）。上方标注声部构成：1、3、b7、b9。按点分布：6弦9品为根音（双圈强调），4弦9品，3弦10品，2弦10品。 |
| 3 | 24 |  | 0.1894 | -0.1174 | `吉他标准调弦音名与弦号对应答案` | data/练习解答（图片）/练习1-练习5.png | text_answer | 和弦, 标准调弦, 调弦 | 练习3填空题答案列表：1.G(3弦), 2.2(B弦), 3.A(4弦), 4.3(G弦), 5.E(6弦), 6.5(A弦), 7.B(2弦), 8.6+1(E弦), 9.E(1弦), 10.4(D弦)。涵盖标准调弦各弦音名与序号对应关系。 |
| 4 | 6 |  | 0.1753 | -0.1213 | `G9 指型 1` | data/练习解答（图片）/练习47-48.png | chord_diagram | 和弦, 指型 | G9和弦指板图示，标注为“3) G9 指型 1”，位于VII把位。图中展示了该延伸和弦在指板上的具体按法，根音以双圈强调，用于构建属九和弦琶音或伴奏Voicing。 |
| 5 | 12 |  | 0.1837 | -0.1227 | `G 自然小调 指型4` | data/练习解答（图片）/练习13-练习14.png | scale_pattern | 和弦, 指型 | 练习13第6题答案：G 小调指型4。横向指板图显示 II 把位（约2-5品）的 G 自然小调音阶排列。可见三个圈出的根音 G，以及完整的单八度加延伸音指型结构。 |

### foundation_plain_cmaj7 - PASS

- Query: 标准调弦 Cmaj7 大七和弦基础指型，不需要点弦谱例
- Expected any: Cmaj7, Cma7, C major seventh, MA7
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.112s = embed 0.097s + chroma 0.015s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 2 | Y | 0.1451 | -0.0751 | `Cma7(#5)` | data/练习解答（图片）/练习49-51.png | chord_diagram | cmaj7, 和弦, 指型 | 练习51第10题答案：Cma7(#5)和弦指法图。位于第VIII把位（8品），根音在6弦8品。图示标注了构成音程：1(根音)、7(七音)、3(三音)、#5(升五音)。指型显示6弦8品为根音，4、3、2弦9品分别为七音、三音和升五音。 |
| 2 | 1 | Y | 0.1407 | -0.0927 | `MA7 (Major 7th) chord shape` | data/练习解答（图片）/练习24-26.png | chord_diagram | 和弦, 指型 | 题号3对应的和弦指法图，上方标注答案为“MA7”。图示为垂直六线格，包含6个黑点表示的按弦位置，推测为大七和弦（Major 7th）的一种常见封闭或开放指型。 |
| 3 | 17 |  | 0.1650 | -0.0980 | `C大调音阶（或A小调自然音阶）指板全貌图示` | data/练习解答（图片）/练习1-练习5.png | scale_pattern | 和弦, 指型, 调弦 | 吉他指板C大调音阶全颈分布图。横向展示0-12品，空心圆圈标记所有C音（根音）位置，覆盖开放把位至高把位。图上方标注数字1-5及1-3，对应不同的指型分区或把位划分，用于演示全指板根音型式。 |
| 4 | 14 |  | 0.1640 | -0.1000 | `C大三和弦 (C Major Triad)` | data/练习解答（图片）/练习34-37.png | chord_diagram | 和弦, 指型 | 练习34第3题答案：C大三和弦在吉他指板第12品(XII)的密集声部排列。图示为垂直指板，包含5个按点，其中两个根音被圈出。明确标注为“指型1”。 |
| 5 | 3 | Y | 0.1462 | -0.1012 | `MA7 chord shape` | data/练习解答（图片）/练习24-26.png | chord_diagram | 和弦, 指型 | 练习24第8题答案图示。垂直吉他指板图，上方标注“MA7”，显示一个包含6个音符的大七和弦（Major 7th）指法形状。 |
