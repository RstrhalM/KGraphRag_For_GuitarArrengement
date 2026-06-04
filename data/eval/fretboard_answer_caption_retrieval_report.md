# Visual Caption Retrieval Trial

## Summary

- Collection: `guitar_fretboard_answer_captions_qwen3_06b` (389 docs)
- Model: `models\embedding\qwen3-embedding-0.6b` on `cuda`, dim=1024
- Tests: 8, TopK: 5
- Rerank: `True`, candidates: 30
- Hit@1: 8/8
- Hit@K: 8/8
- Avg total latency/query: 0.092s
- Median total latency/query: 0.040s

## Cases

### fretboard_g_major_single_string - PASS

- Query: G大调 单弦音阶 G A B C D E F# G 指板图
- Expected any: fretboard_answer_E11_1
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.453s = embed 0.256s + chroma 0.196s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1174 | -0.0154 | `G Major Scale (G Ionian)` | data/练习解答（图片）/练习10-练习11.png | scale_pattern | f#, 单弦音阶, 大调, 指板图, 音阶 | 横向指板图展示单弦 G 大调音阶（G Major）。起始与结束音均为 G（圈出），中间音符依次为 A、B、C、D、E、F#。符合全全半全全全半的大调音程结构。 |
| 2 | 2 |  | 0.1190 | -0.0170 | `G大调自然音阶 (G Major Scale) - 第6弦单弦指型` | data/练习解答（图片）/练习6-练习9.png | scale_pattern | f#, 大调, 指板图, 音阶 | 吉他第6弦（低音E弦）上的G大调自然音阶指板图。展示了从空弦G音开始，经过A、B、C、D、E、F(实际为F#)、至高八度G及九度A的单弦音符分布与对应音名。 |
| 3 | 5 |  | 0.1470 | -0.0360 | `D Major Scale (D大调音阶)` | data/练习解答（图片）/练习10-练习11.png | scale_pattern | f#, 单弦音阶, 大调, 指板图, 音阶 | D大调音阶（D Major）单弦指法图示。以D为根音，按全全半全全全半公式排列：D-E-F#-G-A-B-C#-D。图中可见首尾圈出的D音及中间各音名，用于演示单弦大调音阶构成与字母表规则。 |
| 4 | 9 |  | 0.1585 | -0.0375 | `D 自然大调音阶 (单弦指板图)` | data/练习解答（图片）/练习6-练习9.png | scale_pattern | 大调, 指板图, 音阶 | 吉他第4弦（D弦）自然大调音阶指板图。展示了从空弦D开始的自然音阶音符排列：空弦D、1品E、2品F、3品G，并延伸至更高把位的A、B、C、D、E、F。用于记忆单弦上的全全半全全全半音程关系。 |
| 5 | 3 |  | 0.1390 | -0.0430 | `G自然大调音阶 (G Major Scale)` | data/练习解答（图片）/练习6-练习9.png | scale_pattern | 单弦音阶, 大调, 指板图, 音阶 | 吉他指板第3弦（G弦）上的G自然大调音阶图示。展示了从空弦G开始的自然音阶音符排列：G(空弦)-A-B-C-D-E-F-G。图中标注了各音符对应的音名，并用箭头指示音高上行方向。用于练习单弦上的全音/半音关系及音符记忆。 |

### fretboard_a_major_pentatonic_shape4 - PASS

- Query: A大调五声音阶 指型4 IV把位 根音A
- Expected any: fretboard_answer_E16_1
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.040s = embed 0.036s + chroma 0.004s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0971 | 0.0829 | `A 大调五声音阶 指型4` | data/练习解答（图片）/练习16-练习19.png | scale_pattern | 4, iv, 大调, 大调五声音阶, 把位, 指型, 根音, 音阶 | 练习 16-1 答案图示：A 大调五声音阶指型 4。垂直指板图展示 IV 把位音阶形态，根音 A 以双圈高亮，通过叉号标记剔除 4 级与 7 级音后的五声结构。 |
| 2 | 3 |  | 0.1065 | 0.0735 | `A大调五声音阶指型4 (F#小调五声音阶指型5)` | data/练习解答（图片）/练习16-练习19.png | scale_pattern | 4, iv, 大调, 大调五声音阶, 把位, 指型, 根音, 音阶 | 练习18第1题答案图示：A大调五声音阶指型4（对应关系小调F#小调五声音阶指型5）。垂直指板图显示IV把位，用方框标出了F#根音位置。 |
| 3 | 4 |  | 0.1137 | 0.0663 | `F# 小调五声音阶指型5 / A 大调五声音阶指型4` | data/练习解答（图片）/练习22.png | scale_pattern | 4, iv, 大调, 大调五声音阶, 把位, 指型, 根音, 音阶 | 练习22-7答案图示：展示 F# 小调五声音阶（指型5）与 A 大调五声音阶（指型4）的垂直指板图。图中标注了 IV 把位，并用方框圈出了关系大小调中的根音位置。 |
| 4 | 20 |  | 0.1269 | 0.0501 | `B 小调五声音阶 指型5 / D 大调五声音阶 指型4` | data/练习解答（图片）/练习16-练习19.png | scale_pattern | 4, iv, 大调, 大调五声音阶, 把位, 指型, 根音, 音阶 | 练习19第3题答案：B小调五声音阶指型5（对应关系大调D大调五声音阶指型4）。图示为垂直指板，把位标记为IX，方框标出根音位置。 |
| 5 | 11 |  | 0.1223 | 0.0487 | `G# 小调五声音阶 指型1 (关系大调: B 大调五声音阶 指型5)` | data/练习解答（图片）/练习16-练习19.png | scale_pattern | 4, iv, 大调, 大调五声音阶, 把位, 指型, 根音, 音阶 | 练习19第4题答案：G#小调五声音阶指型1图示。位于第VIII把位，底部备注其关系大调为B大调五声音阶指型5。图中用方框标出了根音位置。 |

### fretboard_relative_pentatonic_c_a - PASS

- Query: 练习22第6题 C大调五声音阶指型3 A小调五声音阶指型4 把位V
- Expected any: fretboard_answer_E22_6
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.040s = embed 0.035s + chroma 0.004s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 5 | Y | 0.0977 | 0.1603 | `C大调五声音阶指型3 / A小调五声音阶指型4` | data/练习解答（图片）/练习22.png | scale_pattern | 22, 3, 4, 6, 大调, 大调五声音阶指型, 小调, 小调五声音阶指型, 把位, 指型, 练习, 音阶 | 练习22第6题答案：展示 C 大调五声音阶指型3 与 A 小调五声音阶指型4 的垂直指板图。位于把位 V，方框标记了关系大小调的根音 C 和 A。 |
| 2 | 3 |  | 0.0936 | 0.1554 | `A 小调五声音阶指型4 / C 大调五声音阶指型3` | data/练习解答（图片）/练习22.png | scale_pattern | 22, 3, 4, 6, 大调, 大调五声音阶指型, 小调, 小调五声音阶指型, 把位, 指型, 练习, 音阶 | 练习22第3题答案图示。展示了 A 小调五声音阶（指型4）与 C 大调五声音阶（指型3）的指板位置关系。图中标注罗马数字 V 把位，并用方框圈出了关系大小调的根音。 |
| 3 | 1 |  | 0.0850 | 0.1490 | `C大调五声音阶指型2 (A小调五声音阶指型3)` | data/练习解答（图片）/练习16-练习19.png | scale_pattern | 3, 4, 6, 大调, 大调五声音阶指型, 小调, 小调五声音阶指型, 把位, 指型, 练习, 音阶 | 练习18第4题答案图示：C大调五声音阶指型2（对应关系小调A小调五声音阶指型3）。垂直指板图显示II把位，方框明确标记了A小调的根音位置。 |
| 4 | 16 | Y | 0.1112 | 0.1438 | `D 小调五声音阶指型4 / F 大调五声音阶指型3` | data/练习解答（图片）/练习22.png | scale_pattern | 22, 3, 4, 6, 大调, 大调五声音阶指型, 小调, 小调五声音阶指型, 把位, 指型, 练习, 音阶 | 练习22第6题答案：展示D小调五声音阶指型4及其关系大调F大调五声音阶指型3的垂直指板图。图中用圆圈标出根音，并用方框特别标记了关系调中的根音位置，符合题目“写出对应关系调并画方框”的要求。 |
| 5 | 7 |  | 0.1012 | 0.1398 | `Eb大调五声音阶指型5 / C小调五声音阶指型1` | data/练习解答（图片）/练习22.png | scale_pattern | 22, 3, 4, 6, 大调, 大调五声音阶指型, 小调, 小调五声音阶指型, 把位, 指型, 练习, 音阶 | 练习22答案图示：垂直指板图展示Eb大调五声音阶（指型5）与C小调五声音阶（指型1）的关系。把位标记为XII品。图中用方框标出了各自的根音（Eb和C），两者共享相同的指法位置，体现关系大小调五声音阶的同构性。 |

### fretboard_sharp_11_interval - PASS

- Query: #11 升十一度 音程 指板 复合音程
- Expected any: fretboard_answer_E28_5
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.039s = embed 0.035s + chroma 0.004s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1326 | -0.0396 | `#11 (升十一度) 音程指型` | data/练习解答（图片）/练习28-29.png | scale_pattern | 11, 升十一度, 复合音程, 指板, 音程 | 练习28第5题答案图示：#11（升十一度）复合音程指板图解。图中以空心圆为根音参考，标记出三个不同把位的#11音位置（实心点），直观展示从根音向上构建升十一度音程的指法形态。 |
| 2 | 2 |  | 0.1773 | -0.1053 | `指板音程关系图（根音与上方音）` | data/练习解答（图片）/练习28-29.png | scale_pattern | 11, 复合音程, 指板, 音程 | 垂直指板局部图，展示以第6弦空心圆为根音的相对音程位置。可见两个目标音：第5弦向右2格（大二度/9度位置）和第4弦向右3格（纯四度/11度位置）。结合题干“构建复合音程”，此图为寻找9、11、13度音的指法参考。 |
| 3 | 4 |  | 0.1836 | -0.1056 | `复合音程构建指法图 (9, 13, #11, 6, 3)` | data/练习解答（图片）/练习28-29.png | scale_pattern | 11, 复合音程, 指板, 音程 | 吉他指板垂直图示，展示复合音程构建指法。图中包含一个空心圆作为基准音，以及两个实心圆表示目标音位置。结合题目要求，该图演示了如何在指板上定位并构建 9、13、#11、6、3 等复合音程（即简单音程加八度）。 |
| 4 | 3 |  | 0.1809 | -0.1089 | `指板音程构建图示` | data/练习解答（图片）/练习28-29.png | fretboard_diagram | 11, 复合音程, 指板, 音程 | 练习28第8题答案图示：垂直吉他指板局部图。显示一个空心基准音（约3弦）与三个实心目标音的相对位置关系，用于可视化构建9度、13度、#11度等复合音程的指法形态。 |
| 5 | 5 |  | 0.1916 | -0.1196 | `复合音程构建指法图 (Compound Intervals)` | data/练习解答（图片）/练习28-29.png | scale_pattern | 11, 复合音程, 指板, 音程 | 练习28第9题答案图示：垂直吉他指板局部图，展示构建复合音程（9, 13, #11, 6, 3）的指法位置。图中包含三个关键按点，分别位于不同弦的高把位区域，用于演示简单音程增加八度后的指板形态。 |

### fretboard_f7_arpeggio_shape1 - PASS

- Query: F7 属七和弦琶音 指型1 根音F
- Expected any: fretboard_answer_E40_2
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.040s = embed 0.035s + chroma 0.005s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 2 | Y | 0.1130 | 0.0680 | `F7 琶音 指型1` | data/练习解答（图片）/练习39-42.png | arpeggio_pattern | 1, f7, 和弦, 属七和弦琶音, 指型, 根音, 琶音 | F7属七和弦琶音指型1图解。图中展示了F7琶音在吉他指板上的第一种指法排列，根音F以双圈高亮显示（6弦1品、4弦3品），包含降七度音Eb。底部标注罗马数字V，对应练习要求的五种指型之一。 |
| 2 | 3 |  | 0.1210 | 0.0540 | `F7 琶音 指型3` | data/练习解答（图片）/练习39-42.png | arpeggio_pattern | 1, f7, 和弦, 属七和弦琶音, 指型, 根音, 琶音 | F7属七和弦琶音指型3的指板图示。图中展示了F7琶音在指板上的具体按法，黑点代表构成音，双圈黑点明确标示出根音F的位置。该指型覆盖了约第8至12品的把位区域，用于练习F7琶音的第三种指型排列。 |
| 3 | 1 |  | 0.1113 | 0.0507 | `F7琶音 指型2` | data/练习解答（图片）/练习39-42.png | arpeggio_pattern | 1, f7, 和弦, 属七和弦琶音, 指型, 根音, 琶音 | F7属七和弦琶音指型2图解，标注于VII把位。图中以双圈明确标示根音F的位置（6弦与4弦），单圈表示3音、5音及降7音，展示该指型在指板上的具体按点分布。 |
| 4 | 5 |  | 0.1279 | 0.0471 | `F7 琶音 指型4` | data/练习解答（图片）/练习39-42.png | arpeggio_pattern | 1, f7, 和弦, 属七和弦琶音, 指型, 根音, 琶音 | F7属七和弦琶音指型4图示。把位标记为XII（12品）。图中展示了该指型在指板上的按点分布，双圈标示根音F的位置，用于F7琶音的高把位练习与视奏记忆。 |
| 5 | 4 |  | 0.1261 | 0.0389 | `F7 琶音 指型5` | data/练习解答（图片）/练习39-42.png | arpeggio_pattern | 1, f7, 和弦, 属七和弦琶音, 指型, 根音, 琶音 | F7属七和弦琶音指型5图示。标题标注“1) F7 琶音 指型 5”。图中为横向吉他指板局部，显示该指型的按点分布，其中两个音被双圆圈出作为根音（Root），其余为和弦内音（3度、降7度等）。 |

### fretboard_ebmi13_voicing - PASS

- Query: Ebmi13 和弦 指型2 VI把位 b7 11 13
- Expected any: fretboard_answer_E48_9
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.039s = embed 0.034s + chroma 0.005s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0999 | 0.0771 | `Ebmi13 指型2` | data/练习解答（图片）/练习47-48.png | chord_diagram | 11, 13, 2, b7, ebmi13, vi, 和弦, 把位, 指型 | Ebmi13和弦指板图，标注为指型2，位于VI把位。图示包含6个音符：6弦根音Eb，以及b7、3、11、5、13度延伸音，展示横向指法排列。 |
| 2 | 3 |  | 0.1224 | 0.0276 | `Bb13 指型 4` | data/练习解答（图片）/练习47-48.png | chord_diagram | 11, 13, 2, b7, ebmi13, vi, 和弦, 把位, 指型 | 横向吉他指板图，标注为 Bb13 和弦，使用指型 4。图示显示 V 把位位置，包含 6 个黑点表示的按弦位置，根音位于低音区，用于构建降B属十三和弦琶音或伴奏。 |
| 3 | 6 |  | 0.1348 | 0.0132 | `Fmi11(b5) 指型3` | data/练习解答（图片）/练习47-48.png | chord_diagram | 11, 13, 2, ebmi13, vi, 和弦, 把位, 指型 | Fmi11(b5)和弦琶音图示，标注为指型3，位于第XI把位。根音位于6弦11品(F)，按点分布呈现半减七和弦延伸结构，包含b9或11音色彩。 |
| 4 | 5 |  | 0.1319 | 0.0131 | `Ami13 指型 3` | data/练习解答（图片）/练习47-48.png | chord_diagram | 11, 13, 2, ebmi13, vi, 和弦, 把位, 指型 | 吉他指板图示：Ami13（A小十三和弦）指型3。根音位于6弦5品（双圈强调），其余音符分布在5-7品区域，展示完整的六音和弦voicing。 |
| 5 | 2 |  | 0.1220 | 0.0130 | `Bb13` | data/练习解答（图片）/练习49-51.png | chord_diagram | 11, 13, 2, b7, vi, 和弦, 把位, 指型 | 题号3的 Bb13 和弦指法图。把位标记为 VI。声部构成显示为 1、b7、3、13。按点分布在第6、5、4、3弦上，对应根音、降七音、三音和十三音。 |

### fretboard_cmi_bb_slash - PASS

- Query: Cmi/Bb slash chord VIII把位 b7 b3 5 1
- Expected any: fretboard_answer_E59_7
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.041s = embed 0.037s + chroma 0.004s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 2 | Y | 0.1255 | 0.0485 | `Cmi/Bb (C小三和弦第一转位)` | data/练习解答（图片）/练习58-59.png | chord_diagram | 1, 5, b3, b7, bb, chord, cmi/bb, slash, viii, 把位 | Cmi/Bb和弦指法图，位于VIII把位。图示标注了声部构成：b7(Bb)、b3(Eb)、5(G)、1(C)。这是一个C小三和弦的第一转位，低音为Bb。 |
| 2 | 1 |  | 0.1193 | 0.0227 | `Cmi/B (C minor triad over B bass)` | data/练习解答（图片）/练习58-59.png | chord_diagram | 1, 5, b3, bb, chord, slash, viii, 把位 | 垂直指板图展示 Cmi/B Slash 和弦，位于 VIII 把位（8品）。图示标注声部构成 7 b3 5 1。按点分布：6弦8品(B)、4弦10品(Eb)、3弦10品(G)、2弦10品(C)。 |
| 3 | 3 |  | 0.1397 | 0.0113 | `C/Bb (C major triad over Bb bass)` | data/练习解答（图片）/练习58-59.png | chord_diagram | 1, 5, b7, bb, chord, slash, viii, 把位 | C/Bb Slash和弦指法图，位于第VIII把位。图示标注了声部构成：A弦10品为降七音(b7)，D弦9品为三音(3)，G弦10品为五音(5)，B弦11品圈出根音(1)。 |
| 4 | 5 |  | 0.1455 | -0.0135 | `Cmi/Eb (Slash Chord)` | data/练习解答（图片）/练习58-59.png | chord_diagram | 1, 5, b3, bb, chord, slash, 把位 | Cmi/Eb Slash和弦指法图，位于第V把位。图示标注声部构成为b3、5、1（相对于根音Eb）。按点显示：A弦为根音Eb（双圈强调），D弦为小三度Gb，G弦为五度Bb。 |
| 5 | 8 |  | 0.1565 | -0.0155 | `Cmi7 (1 5 b7 b3)` | data/练习解答（图片）/练习43-46.png | chord_diagram | 1, 5, b3, b7, bb, chord, 把位 | 垂直指板图展示 Cmi7 和弦在 III 把位的指型。顶部标注和弦名“Cmi7”及声部构成“1 5 b7 b3”。图中可见四个按点，其中第5弦上的根音用双圈/空心圈强调，其余音分布在相邻弦上，符合七和弦常用声部排列。 |

### fretboard_eb13_b9_slash - PASS

- Query: C/Eb 等同 Eb13(b9) XII把位 1 3 13 b9
- Expected any: fretboard_answer_E59_12
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.044s = embed 0.039s + chroma 0.004s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1760 | 0.0440 | `C/Eb = Eb13(b9)` | data/练习解答（图片）/练习58-59.png | chord_diagram | 1, 13, 3, b9, c/eb, eb, eb13, xii, 把位, 等同 | 垂直指板图展示 C/Eb 和弦，等同于 Eb13(b9)。位于 XII 把位（12品）。按点分布：12品根音(Eb)，13品3音(G)，14品b9音(F)，15品13音(C)。上方标注音程结构 1 3 13 b9。 |
| 2 | 3 |  | 0.2308 | -0.1018 | `Ebmi13 指型2` | data/练习解答（图片）/练习47-48.png | chord_diagram | 1, 13, 3, b9, eb, 把位 | Ebmi13和弦指板图，标注为指型2，位于VI把位。图示包含6个音符：6弦根音Eb，以及b7、3、11、5、13度延伸音，展示横向指法排列。 |
| 3 | 4 |  | 0.2328 | -0.1058 | `C13(b9)` | data/练习解答（图片）/练习49-51.png | chord_diagram | 1, 13, 3, b9, 把位 | 第8把位 C13(b9) 和弦指法图。根音在6弦8品，包含b7、3、13、b9四个延伸/变化音程，构成属十三降九和弦结构。 |
| 4 | 2 |  | 0.2282 | -0.1102 | `E13` | data/练习解答（图片）/练习49-51.png | chord_diagram | 1, 13, 3, eb, 把位 | 练习49第8题答案图示：E13和弦指法图。位于V把位（5品区域），声部构成为b7、3、13、9。图中显示四音按法，3弦处标记空括号表示制音或不弹，用于构建E属十三和弦的特定Voicing。 |
| 5 | 6 |  | 0.2518 | -0.1218 | `C/Gb = Gb7(b5, b9)` | data/练习解答（图片）/练习58-59.png | chord_diagram | 1, 13, 3, b9, xii, 把位, 等同 | 第12把位垂直指板图，展示Slash和弦 C/Gb 等同于 Gb7(b5, b9)。图中标注了b7、b9、b5音程位置，6弦12品为根音。 |
