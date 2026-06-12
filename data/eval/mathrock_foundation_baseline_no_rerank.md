# Visual Caption Retrieval Trial

## Summary

- Collection: `guitar_fretboard_answer_captions_qwen3_06b` (389 docs)
- Model: `D:\Guitar Arrangement Inspiration Agent\KGraphRag2\models\embedding\qwen3-embedding-0.6b` on `cuda`, dim=1024
- Tests: 7, TopK: 5
- Rerank: `False`, candidates: 5
- Hit@1: 6/7
- Hit@K: 7/7
- Avg total latency/query: 0.204s
- Median total latency/query: 0.073s

## Cases

### foundation_b6 - PASS

- Query: B6 六和弦指法，不包含七度音，根音在九品附近
- Expected any: B6_chord_shape, B6
- First hit rank: 1
- Rerank: `False`, candidates: 5
- Latency: total 0.455s = embed 0.262s + chroma 0.193s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1439 | -0.1439 | `B6` | data/练习解答（图片）/练习58-59.png | chord_diagram |  | B6和弦垂直指板图，位于IX（第9）把位。图示包含四个按点，根音位于低音区第9品（双圈强调）。上方标注指法数字1、5、6、3，对应和弦内音排列。 |
| 2 | 2 |  | 0.1508 | -0.1508 | `指板音程关系图（根音与上方音）` | data/练习解答（图片）/练习28-29.png | scale_pattern |  | 垂直指板局部图，展示以第6弦空心圆为根音的相对音程位置。可见两个目标音：第5弦向右2格（大二度/9度位置）和第4弦向右3格（纯四度/11度位置）。结合题干“构建复合音程”，此图为寻找9、11、13度音的指法参考。 |
| 3 | 3 |  | 0.1540 | -0.1540 | `Bbmi6/9` | data/练习解答（图片）/练习58-59.png | chord_diagram |  | Bbmi6/9和弦指板图，把位XI（11品）。声部构成标注为1、b3、6、9。根音Bb在5弦11品，其余音分布在4-2弦的12品位置。 |
| 4 | 4 |  | 0.1553 | -0.1553 | `G大调自然音阶 (G Major Scale) - 第6弦单弦指型` | data/练习解答（图片）/练习6-练习9.png | scale_pattern |  | 吉他第6弦（低音E弦）上的G大调自然音阶指板图。展示了从空弦G音开始，经过A、B、C、D、E、F(实际为F#)、至高八度G及九度A的单弦音符分布与对应音名。 |
| 5 | 5 | Y | 0.1556 | -0.1556 | `指板音程构建图示 (根音-3度-6度)` | data/练习解答（图片）/练习28-29.png | scale_pattern |  | 垂直指板图展示复合音程构建基础：空心圆为根音，相邻品格实心点为3度音，下方弦实心点为6度音。结合题干要求构建9、13、#11等复合音程，此图为音程关系的视觉参照。 |

### foundation_fm7b5 - PASS

- Query: F小七减五 Fm7b5 琶音指型，低把位，半减七和弦
- Expected any: Fm7b5_arpeggio_shape_1, F half-diminished
- First hit rank: 1
- Rerank: `False`, candidates: 5
- Latency: total 0.046s = embed 0.043s + chroma 0.004s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1287 | -0.1287 | `Fmi7(b5) 琶音 指型2` | data/练习解答（图片）/练习39-42.png | arpeggio_pattern |  | Fmi7(b5)半减七和弦琶音指型2图示，位于VII把位。图中标注了六个按点位置，并用双圈特别标出了根音F的位置，用于展示该和弦在指板上的第二种排列形态。 |
| 2 | 2 | Y | 0.1305 | -0.1305 | `Fmi7(b5) 琶音 指型3` | data/练习解答（图片）/练习39-42.png | arpeggio_pattern |  | Fmi7(b5)琶音指型3的吉他指板图示。图中展示了F半减七和弦在指板上的分布，根音F以双圈特别标出。该指型覆盖了约5个品位的跨度，用于练习F小七减五和弦的色彩与把位记忆。 |
| 3 | 3 | Y | 0.1389 | -0.1389 | `Fmi7(b5) 琶音 指型5` | data/练习解答（图片）/练习39-42.png | arpeggio_pattern |  | Fmi7(b5)和弦琶音指板图，标注为“指型5”。图中展示了该半减七和弦在指板上的五种指型之一，包含六个音符位置，其中两个音符被双圈高亮标记为根音F。 |
| 4 | 4 | Y | 0.1414 | -0.1414 | `Fmi7(b5) 琶音 指型1` | data/练习解答（图片）/练习39-42.png | arpeggio_pattern |  | Fmi7(b5)半减七和弦琶音指型1图解。图中标注罗马数字VI表示把位位置，双圈标示根音F。该指型展示了F小七减五和弦在指板上的第一种排列方式，适用于构建爵士乐句或即兴伴奏。 |
| 5 | 5 | Y | 0.1461 | -0.1461 | `Fmi7(b5) 琶音 指型4` | data/练习解答（图片）/练习39-42.png | arpeggio_pattern |  | Fmi7(b5)半减七和弦琶音指型4图解。图中展示了该和弦在吉他指板上的四种八度内分布形态，明确标注了“指型4”。6弦、4弦及1弦上的F音（根音）使用双圈特别标识，用于辅助记忆根音位置及把位结构。 |

### foundation_d_major - PASS

- Query: D大三和弦琶音 指型1 根音三音五音
- Expected any: D_major_triad_arpeggio_shape_1, D大三和弦琶音, D major triad arpeggio
- First hit rank: 1
- Rerank: `False`, candidates: 5
- Latency: total 0.043s = embed 0.039s + chroma 0.004s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1097 | -0.1097 | `D大三和弦琶音 指型1` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern |  | 练习30答案图：D大三和弦琶音指型1。横向指板图显示该指型的音符分布，包含4个按点与2个标示根音的空心圈，对应D Major Triad Arpeggio Shape 1的把位按法。 |
| 2 | 2 | Y | 0.1118 | -0.1118 | `D大三和弦琶音 指型4` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern |  | 练习30第4题答案：D大三和弦(D Major Triad)琶音指型4。图示为横向指板局部，包含根音D(空心)、三音F#(实心)、五音A(空心)。根据D音位置推断约为10-12把位区域，展示该指型下的完整琶音音符分布。 |
| 3 | 3 | Y | 0.1153 | -0.1153 | `D大三和弦琶音 指型2` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern |  | D大三和弦琶音指型2的指板图示。包含根音(D)、三音(F#)、五音(A)的分布位置。图中以空心圆标示根音，实心点标示其他和弦内音，展示了该指型在指板上的具体按法结构。 |
| 4 | 4 | Y | 0.1234 | -0.1234 | `D大三和弦琶音 指型5` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern |  | 练习30第5题答案：D大三和弦琶音指型5图示。图中展示了D Major Arpeggio在指板上的分布，包含根音（空心圈）及三音、五音（实心点），对应教材中的第五种指法形态。 |
| 5 | 5 |  | 0.1239 | -0.1239 | `D小三和弦琶音 指型1` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern |  | D小三和弦（D minor triad）琶音指型1的指板图示。图中展示了该和弦在吉他指板上的第一种按法分布，包含根音（空心圆）及三音、五音（实心点）。用于构建Dm和弦的基础琶音指型记忆与演奏。 |

### foundation_d_dim - PASS

- Query: D减三和弦琶音，根音小三度减五度，制造紧张经过感
- Expected any: D_diminished_triad_arpeggio_shape, D diminished
- First hit rank: 1
- Rerank: `False`, candidates: 5
- Latency: total 0.120s = embed 0.114s + chroma 0.006s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1219 | -0.1219 | `D减三和弦琶音 指型1` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern |  | D减三和弦(D diminished triad)琶音指型1图示。水平指板图显示六线谱按点分布，包含空心圆(可能为根音或起始音)与实心黑点。根据题目语境，该指型覆盖约4个品格跨度，展示D-F-Ab音程结构的指板排列。 |
| 2 | 2 | Y | 0.1377 | -0.1377 | `D减三和弦 指型5` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern |  | 吉他指板图示：D减三和弦（D diminished triad）琶音指型5。图中标注“5) D减三和弦 指型5”，显示横向指板上的音符排列，包含实心按点与空心圈，对应练习要求的第10-11把位区域。 |
| 3 | 3 | Y | 0.1389 | -0.1389 | `D减三和弦琶音 指型2` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern |  | 吉他指板图示：D减三和弦（D diminished triad）琶音指型2。图中显示横向指板，标有5个实心按点和2个空心根音标记，对应练习32第2小题答案。 |
| 4 | 4 | Y | 0.1417 | -0.1417 | `D减三和弦琶音 指型4` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern |  | 吉他指板图解：D减三和弦（D diminished triad）琶音指型4。图中展示了该和弦在指板上的按法分布，包含根音（空心圆）及组成音（实心点），适用于构建Ddim琶音练习。 |
| 5 | 5 |  | 0.1466 | -0.1466 | `D增三和弦琶音 指型1` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern |  | D增三和弦(D Augmented Triad)琶音指型1的吉他指板图示。图中展示了该和弦在低把位（推断为2-6品区域）的指法分布，包含根音D的空心标记与其他组成音的实心标记，用于构建增三和弦琶音练习。 |

### foundation_gsus2 - PASS

- Query: Gsus2 挂二和弦 1 2 5 构成音，在图上补全指法
- Expected any: Gsus2_chord_shape_exercise, Gsus2, 挂二和弦
- First hit rank: 1
- Rerank: `False`, candidates: 5
- Latency: total 0.073s = embed 0.068s + chroma 0.005s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1414 | -0.1414 | `Gsus2` | data/练习解答（图片）/练习58-59.png | chord_diagram |  | Gsus2和弦指法图，位于第II把位。图示包含根音标记及声部编号1、2、5，展示了该挂留和弦在指板上的具体按点位置与构成音分布。 |
| 2 | 2 |  | 0.2054 | -0.2054 | `C/G (C major triad over G bass)` | data/练习解答（图片）/练习58-59.png | chord_diagram |  | 吉他指板图示展示 C/G 和弦指型。位于第 V 把位（约第5品），指法标记为 5-1-3。构成音为低音 G 加上 C 大三和弦（C-E-G），属于 Slash 和弦 voicing。 |
| 3 | 3 |  | 0.2161 | -0.2161 | `aug2 (增二度) 音程指型` | data/练习解答（图片）/练习24-26.png | scale_pattern |  | 吉他指板垂直图示，标注“aug2”（增二度）。图中展示了跨越三根弦的音符排列，重点标示了上方两音之间的增二度音程关系（黑点与空心圈），用于演示在指板上构建和识别增二度音程的指法形态。 |
| 4 | 4 |  | 0.2174 | -0.2174 | `D小三和弦琶音 指型2` | data/练习解答（图片）/练习30-33.png | arpeggio_pattern |  | D小三和弦(Dm)琶音指型2图示。横向指板图显示约第5把位附近的按法，包含6个音符（黑点与白圈），覆盖D、F、A三个和弦内音，符合Dm triad结构。 |
| 5 | 5 |  | 0.2188 | -0.2188 | `Gbma13` | data/练习解答（图片）/练习49-51.png | chord_diagram |  | Gbma13和弦指法图，位于第II把位。图示标注了声部构成：1(根音)、7、3、13。6弦2品为根音Gb，配合5、4、3弦的延伸音构成大十三和弦。 |

### foundation_plain_g7 - PASS

- Query: 标准调弦 G7 属七和弦普通指型图
- Expected any: G7
- First hit rank: 2
- Rerank: `False`, candidates: 5
- Latency: total 0.620s = embed 0.596s + chroma 0.024s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 |  | 0.1569 | -0.1569 | `G大调自然音阶 (G Major Scale) - 第6弦单弦指型` | data/练习解答（图片）/练习6-练习9.png | scale_pattern |  | 吉他第6弦（低音E弦）上的G大调自然音阶指板图。展示了从空弦G音开始，经过A、B、C、D、E、F(实际为F#)、至高八度G及九度A的单弦音符分布与对应音名。 |
| 2 | 2 | Y | 0.1604 | -0.1604 | `G7(#5)` | data/练习解答（图片）/练习49-51.png | chord_diagram |  | 练习51第8题答案：G7(#5)和弦指法图。根音位于III把位（3品6弦），构成音标注为b7、3、#5，分别位于4品5弦、5品4弦和5品3弦。 |
| 3 | 3 |  | 0.1673 | -0.1673 | `G自然大调音阶 (G Major Scale)` | data/练习解答（图片）/练习6-练习9.png | scale_pattern |  | 吉他指板第3弦（G弦）上的G自然大调音阶图示。展示了从空弦G开始的自然音阶音符排列：G(空弦)-A-B-C-D-E-F-G。图中标注了各音符对应的音名，并用箭头指示音高上行方向。用于练习单弦上的全音/半音关系及音符记忆。 |
| 4 | 4 | Y | 0.1701 | -0.1701 | `G7(b9)` | data/练习解答（图片）/练习49-51.png | chord_diagram |  | 垂直指板图展示 G7(b9) 和弦，位于第 IX 把位（9品）。上方标注声部构成：1、3、b7、b9。按点分布：6弦9品为根音（双圈强调），4弦9品，3弦10品，2弦10品。 |
| 5 | 5 |  | 0.1729 | -0.1729 | `G Major Scale (G Ionian)` | data/练习解答（图片）/练习10-练习11.png | scale_pattern |  | 横向指板图展示单弦 G 大调音阶（G Major）。起始与结束音均为 G（圈出），中间音符依次为 A、B、C、D、E、F#。符合全全半全全全半的大调音程结构。 |

### foundation_plain_cmaj7 - PASS

- Query: 标准调弦 Cmaj7 大七和弦基础指型，不需要点弦谱例
- Expected any: Cmaj7, Cma7, C major seventh, MA7
- First hit rank: 1
- Rerank: `False`, candidates: 5
- Latency: total 0.072s = embed 0.067s + chroma 0.006s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1407 | -0.1407 | `MA7 (Major 7th) chord shape` | data/练习解答（图片）/练习24-26.png | chord_diagram |  | 题号3对应的和弦指法图，上方标注答案为“MA7”。图示为垂直六线格，包含6个黑点表示的按弦位置，推测为大七和弦（Major 7th）的一种常见封闭或开放指型。 |
| 2 | 2 | Y | 0.1451 | -0.1451 | `Cma7(#5)` | data/练习解答（图片）/练习49-51.png | chord_diagram |  | 练习51第10题答案：Cma7(#5)和弦指法图。位于第VIII把位（8品），根音在6弦8品。图示标注了构成音程：1(根音)、7(七音)、3(三音)、#5(升五音)。指型显示6弦8品为根音，4、3、2弦9品分别为七音、三音和升五音。 |
| 3 | 3 | Y | 0.1462 | -0.1462 | `MA7 chord shape` | data/练习解答（图片）/练习24-26.png | chord_diagram |  | 练习24第8题答案图示。垂直吉他指板图，上方标注“MA7”，显示一个包含6个音符的大七和弦（Major 7th）指法形状。 |
| 4 | 4 | Y | 0.1481 | -0.1481 | `Cma7 (1 5 7 3)` | data/练习解答（图片）/练习43-46.png | chord_diagram |  | 题号1) Cma7和弦指法图，标注声部构成“1 5 7 3”。图示为垂直指板，把位标记为罗马数字 III。根音1以双圈强调，其余按点分布显示该把位下的C大七和弦常用声部排列。 |
| 5 | 5 |  | 0.1519 | -0.1519 | `A小调 指型3 (C大调 指型2)` | data/练习解答（图片）/练习13-练习14.png | scale_pattern |  | 吉他指板图展示A小调自然小音阶指型3，上方标注对应关系大调为C大调指型2。图中用方框标出了关系大调C大调的根音位置（位于5弦5品和3弦7品），其余为A小调音阶构成音。 |
