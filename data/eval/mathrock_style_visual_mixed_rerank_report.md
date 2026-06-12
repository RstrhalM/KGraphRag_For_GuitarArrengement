# Visual Caption Retrieval Trial

## Summary

- Collection: `guitar_visual_mixed_mathrock_trial_qwen3_06b` (398 docs)
- Model: `D:\Guitar Arrangement Inspiration Agent\KGraphRag2\models\embedding\qwen3-embedding-0.6b` on `cuda`, dim=1024
- Tests: 14, TopK: 5
- Rerank: `True`, candidates: 30
- Hit@1: 12/14
- Hit@K: 13/14
- Avg total latency/query: 1.007s
- Median total latency/query: 0.089s

## Misses

`foundation_plain_cmaj7`

## Cases

### style_facgce_fmaj9 - PASS

- Query: FACGCE 调弦的 Fmaj9 全开放弦 Math Rock 和弦指型
- Expected any: mr_style_001_fmaj9, FACGCE_tuning_Fmaj9_open_chord
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.741s = embed 0.480s + chroma 0.261s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0870 | 0.0850 | `FACGCE_tuning_Fmaj9_open_chord` | 33 | chord_diagram | facgce, fmaj9, math, rock, 和弦, 和弦指型, 开放弦, 指型, 调弦 | FACGCE特殊调弦下的Fmaj9和弦指型图。图示显示该和弦在开放把位演奏，六根弦均为空弦音（oooooo），无需左手按品。利用FACGCE调弦特性，空弦音直接构成F大九和弦（根音F、三音A、五音C、九音G、七音E），是Math Rock风格中典型的开放和声Voicing。 |
| 2 | 2 |  | 0.1124 | 0.0566 | `FACGCE_tuning_Am_chord_shape` | 33 | chord_diagram | facgce, math, rock, 和弦, 和弦指型, 开放弦, 指型, 调弦, 调弦的 | FACGCE调弦下的Am和弦指型图。图示显示6弦与1弦标记为闷音（X），根音A位于6弦3品，其余按弦点分布在5、4、3弦的低把位区域。该指型利用开放弦共鸣，构成完整的A小三和弦结构，是Math Rock风格中基于特殊调弦的基础和声素材。 |
| 3 | 3 |  | 0.1145 | 0.0515 | `FACGCE_tuning_G7_chord_shape` | 33 | chord_diagram | facgce, math, rock, 和弦, 和弦指型, 开放弦, 指型, 调弦, 调弦的 | FACGCE特殊调弦下的G7和弦指型图。利用该调弦特性，通过6弦3品按弦配合多根开放弦构成属七和弦 voicing。1、2弦标注闷音（xx），保留中低频开放弦共鸣，呈现Math Rock风格特有的开放、清脆且具张力的和声色彩。 |
| 4 | 5 |  | 0.1325 | 0.0185 | `FACGCE_Bm7b5_chord_shape` | 33 | chord_diagram | facgce, math, rock, 和弦, 和弦指型, 开放弦, 指型, 调弦 | FACGCE特殊调弦下的Bm7b5（半减七）和弦指型图。图示标记起始品位为5品，展示该调弦体系中Bm7b5的特定按法与把位分布，包含根音B及降五度音F的排列结构，适用于Math Rock风格编配。 |
| 5 | 6 |  | 0.1350 | 0.0130 | `FACGCE_tuning_major_scale_fingerboard_map` | 34 | fretboard_diagram | facgce, math, rock, 和弦, 开放弦, 指型, 调弦, 调弦的 | FACGCE调弦下的大调实用音符指板图，覆盖0-7品。图中黑色圆点标示根音位置（如6弦空弦、1弦5品等），空心圆点为音阶内其他音符。该指型设计包含开放弦与重复音，旨在提供丰富的旋律选择，适用于Math Rock风格的主奏、点弦Riff及过渡乐句创作。 |

### style_facgce_am_add11 - PASS

- Query: FACGCE 特殊调弦下 Am add11 开放弦 voicing 指型
- Expected any: mr_style_001_am_add11, FACGCE_Am_add11_chord_shape
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.153s = embed 0.142s + chroma 0.011s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1213 | 0.0317 | `FACGCE_Am_add11_chord_shape` | 33 | chord_diagram | add11, am, facgce, voicing, 开放弦, 指型, 特殊调弦下, 调弦 | FACGCE特殊调弦下的Am(add11)和弦指型图。图示为开放把位按法，利用调弦特性在低把位构建包含根音、小三度、五度及十一度延伸音的和声结构。高音弦（1、2弦）标记为“xx”表示制音或不发声，强调低音区开放弦的共鸣与数学摇滚特有的清冷色彩。 |
| 2 | 2 |  | 0.1244 | 0.0026 | `FACGCE_tuning_Am_chord_shape` | 33 | chord_diagram | am, facgce, voicing, 开放弦, 指型, 调弦 | FACGCE调弦下的Am和弦指型图。图示显示6弦与1弦标记为闷音（X），根音A位于6弦3品，其余按弦点分布在5、4、3弦的低把位区域。该指型利用开放弦共鸣，构成完整的A小三和弦结构，是Math Rock风格中基于特殊调弦的基础和声素材。 |
| 3 | 3 |  | 0.1464 | -0.0104 | `FACGCE_tuning_G7_chord_shape` | 33 | chord_diagram | am, facgce, voicing, 开放弦, 指型, 特殊调弦下, 调弦 | FACGCE特殊调弦下的G7和弦指型图。利用该调弦特性，通过6弦3品按弦配合多根开放弦构成属七和弦 voicing。1、2弦标注闷音（xx），保留中低频开放弦共鸣，呈现Math Rock风格特有的开放、清脆且具张力的和声色彩。 |
| 4 | 4 |  | 0.1579 | -0.0249 | `FACGCE_tuning_Fmaj9_open_chord` | 33 | chord_diagram | am, facgce, voicing, 开放弦, 指型, 特殊调弦下, 调弦 | FACGCE特殊调弦下的Fmaj9和弦指型图。图示显示该和弦在开放把位演奏，六根弦均为空弦音（oooooo），无需左手按品。利用FACGCE调弦特性，空弦音直接构成F大九和弦（根音F、三音A、五音C、九音G、七音E），是Math Rock风格中典型的开放和声Voicing。 |
| 5 | 5 |  | 0.1647 | -0.0347 | `FACGCE_Bm7b5_chord_shape` | 33 | chord_diagram | am, facgce, voicing, 开放弦, 指型, 特殊调弦下, 调弦 | FACGCE特殊调弦下的Bm7b5（半减七）和弦指型图。图示标记起始品位为5品，展示该调弦体系中Bm7b5的特定按法与把位分布，包含根音B及降五度音F的排列结构，适用于Math Rock风格编配。 |

### style_facgce_bm7b5 - PASS

- Query: FACGCE 调弦 Bm7b5 半减七 可移动和弦指型
- Expected any: mr_style_001_bm7b5, FACGCE_Bm7b5_chord_shape
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 11.511s = embed 11.500s + chroma 0.010s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0970 | 0.0330 | `FACGCE_Bm7b5_chord_shape` | 33 | chord_diagram | bm7b5, facgce, 半减七, 和弦, 指型, 调弦 | FACGCE特殊调弦下的Bm7b5（半减七）和弦指型图。图示标记起始品位为5品，展示该调弦体系中Bm7b5的特定按法与把位分布，包含根音B及降五度音F的排列结构，适用于Math Rock风格编配。 |
| 2 | 2 |  | 0.1465 | -0.0525 | `FACGCE_tuning_Am_chord_shape` | 33 | chord_diagram | facgce, 和弦, 指型, 调弦 | FACGCE调弦下的Am和弦指型图。图示显示6弦与1弦标记为闷音（X），根音A位于6弦3品，其余按弦点分布在5、4、3弦的低把位区域。该指型利用开放弦共鸣，构成完整的A小三和弦结构，是Math Rock风格中基于特殊调弦的基础和声素材。 |
| 3 | 3 |  | 0.1504 | -0.0564 | `FACGCE_tuning_G7_chord_shape` | 33 | chord_diagram | facgce, 和弦, 指型, 调弦 | FACGCE特殊调弦下的G7和弦指型图。利用该调弦特性，通过6弦3品按弦配合多根开放弦构成属七和弦 voicing。1、2弦标注闷音（xx），保留中低频开放弦共鸣，呈现Math Rock风格特有的开放、清脆且具张力的和声色彩。 |
| 4 | 4 |  | 0.1524 | -0.0584 | `FACGCE_tuning_Fmaj9_open_chord` | 33 | chord_diagram | facgce, 和弦, 指型, 调弦 | FACGCE特殊调弦下的Fmaj9和弦指型图。图示显示该和弦在开放把位演奏，六根弦均为空弦音（oooooo），无需左手按品。利用FACGCE调弦特性，空弦音直接构成F大九和弦（根音F、三音A、五音C、九音G、七音E），是Math Rock风格中典型的开放和声Voicing。 |
| 5 | 5 |  | 0.1534 | -0.0694 | `FACGCE_Am_add11_chord_shape` | 33 | chord_diagram | facgce, 和弦, 指型, 调弦 | FACGCE特殊调弦下的Am(add11)和弦指型图。图示为开放把位按法，利用调弦特性在低把位构建包含根音、小三度、五度及十一度延伸音的和声结构。高音弦（1、2弦）标记为“xx”表示制音或不发声，强调低音区开放弦的共鸣与数学摇滚特有的清冷色彩。 |

### style_facgce_major_map - PASS

- Query: FACGCE 大调指板音阶图，适合开放弦点弦和旋律 riff
- Expected any: mr_style_002, FACGCE_tuning_major_scale_fingerboard_map
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.823s = embed 0.811s + chroma 0.012s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1000 | 0.0260 | `FACGCE_tuning_major_scale_fingerboard_map` | 34 | fretboard_diagram | facgce, riff, 大调, 开放弦, 点弦, 音阶 | FACGCE调弦下的大调实用音符指板图，覆盖0-7品。图中黑色圆点标示根音位置（如6弦空弦、1弦5品等），空心圆点为音阶内其他音符。该指型设计包含开放弦与重复音，旨在提供丰富的旋律选择，适用于Math Rock风格的主奏、点弦Riff及过渡乐句创作。 |
| 2 | 5 |  | 0.1460 | -0.0740 | `D 自然大调音阶 (单弦指板图)` | data/练习解答（图片）/练习6-练习9.png | scale_pattern | 大调, 音阶 | 吉他第4弦（D弦）自然大调音阶指板图。展示了从空弦D开始的自然音阶音符排列：空弦D、1品E、2品F、3品G，并延伸至更高把位的A、B、C、D、E、F。用于记忆单弦上的全全半全全全半音程关系。 |
| 3 | 12 |  | 0.1497 | -0.0777 | `F 大调五声音阶 指型5` | data/练习解答（图片）/练习16-练习19.png | scale_pattern | 大调, 音阶 | F大调五声音阶指型5图示（II把位）。图中展示了基于F根音的五声音阶按法，通过叉号划去大调音阶中的4级和7级音，保留1、2、3、5、6级音构成五声结构。 |
| 4 | 8 |  | 0.1470 | -0.0780 | `C大调自然音阶（单弦指板图）` | data/练习解答（图片）/练习6-练习9.png | scale_pattern | 大调, 音阶 | 吉他单弦指板图解，展示从空弦到第12品的自然音阶音符排列。可见音符序列：空弦B、1品C、3品D、5品E、6品F、8品G、10品A、12品B。图示强调全音/半音关系及八度循环概念。 |
| 5 | 19 |  | 0.1514 | -0.0794 | `C大调音阶（或A小调自然音阶）指板全貌图示` | data/练习解答（图片）/练习1-练习5.png | scale_pattern | 大调, 音阶 | 吉他指板C大调音阶全颈分布图。横向展示0-12品，空心圆圈标记所有C音（根音）位置，覆盖开放把位至高把位。图上方标注数字1-5及1-3，对应不同的指型分区或把位划分，用于演示全指板根音型式。 |

### style_g7_shell - PASS

- Query: Math Rock 高增益编配的 G7 shell voicing，省略五音减少频段冲突
- Expected any: mr_style_008, G7_shell_voicings
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.088s = embed 0.078s + chroma 0.010s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1442 | -0.0212 | `G7_shell_voicings` | 61 | chord_diagram | g7, math, rock, shell, voicing, 省略五音减少频段冲突 | 展示G7属七和弦的三种Shell Voicing（壳式按法）指型图。包含开放把位、第4把位及第9把位三种形态。图示明确标记了 mute (x) 位置，强调仅保留根音、三音与七音的稀疏结构，省略五音，适用于Math Rock风格的高增益编配。 |
| 2 | 3 |  | 0.1858 | -0.0918 | `FACGCE_tuning_G7_chord_shape` | 33 | chord_diagram | g7, math, rock, voicing | FACGCE特殊调弦下的G7和弦指型图。利用该调弦特性，通过6弦3品按弦配合多根开放弦构成属七和弦 voicing。1、2弦标注闷音（xx），保留中低频开放弦共鸣，呈现Math Rock风格特有的开放、清脆且具张力的和声色彩。 |
| 3 | 2 |  | 0.1850 | -0.1130 | `math_rock_I_IV_riff_irregular_meters` | 78 | tab_excerpt | math, rock, voicing | Math Rock风格I-IV和弦进行Riff谱例。包含C大七与F大七和弦的快速转换，采用6/8与9/8非常规节拍混合。谱面展示了开放把位与高把位封闭和弦的交替，体现了数学摇滚中复杂的节奏分组（3+4拍与3组3拍）及编配特征。 |
| 4 | 5 |  | 0.2087 | -0.1387 | `FACGCE_tuning_Am_chord_shape` | 33 | chord_diagram | math, rock, voicing | FACGCE调弦下的Am和弦指型图。图示显示6弦与1弦标记为闷音（X），根音A位于6弦3品，其余按弦点分布在5、4、3弦的低把位区域。该指型利用开放弦共鸣，构成完整的A小三和弦结构，是Math Rock风格中基于特殊调弦的基础和声素材。 |
| 5 | 4 |  | 0.1972 | -0.1432 | `FACGCE_Am_add11_chord_shape` | 33 | chord_diagram | math, rock, voicing | FACGCE特殊调弦下的Am(add11)和弦指型图。图示为开放把位按法，利用调弦特性在低把位构建包含根音、小三度、五度及十一度延伸音的和声结构。高音弦（1、2弦）标记为“xx”表示制音或不发声，强调低音区开放弦的共鸣与数学摇滚特有的清冷色彩。 |

### style_cmaj7_tapping - PASS

- Query: Math Rock Cmaj7 两手点弦琶音，开放弦持续音和 let ring 谱例
- Expected any: mr_style_010, Cmaj7_tapping_arpeggio
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.082s = embed 0.076s + chroma 0.007s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0874 | 0.0896 | `Cmaj7_tapping_arpeggio` | 73 | tab_excerpt | cmaj7, let, math, ring, rock, 开放弦, 点弦, 琶音, 谱例 | C大七和弦（Cmaj7）点弦琶音谱例。展示标准调弦下结合开放弦持续音与高把位点弦（T/P）的演奏技法。乐谱包含明确的“持续音”与“let ring”标记，强调声部延留与数学摇滚风格的复调听感，涵盖根音、三音、五音及七音的分解排列。 |
| 2 | 2 |  | 0.1249 | -0.0139 | `math_rock_I_IV_riff_irregular_meters` | 78 | tab_excerpt | cmaj7, math, ring, rock, 开放弦, 谱例 | Math Rock风格I-IV和弦进行Riff谱例。包含C大七与F大七和弦的快速转换，采用6/8与9/8非常规节拍混合。谱面展示了开放把位与高把位封闭和弦的交替，体现了数学摇滚中复杂的节奏分组（3+4拍与3组3拍）及编配特征。 |
| 3 | 3 |  | 0.1320 | -0.0480 | `FACGCE_tuning_Fmaj9_open_chord` | 33 | chord_diagram | math, ring, rock, 开放弦, 点弦 | FACGCE特殊调弦下的Fmaj9和弦指型图。图示显示该和弦在开放把位演奏，六根弦均为空弦音（oooooo），无需左手按品。利用FACGCE调弦特性，空弦音直接构成F大九和弦（根音F、三音A、五音C、九音G、七音E），是Math Rock风格中典型的开放和声Voicing。 |
| 4 | 7 |  | 0.1562 | -0.0662 | `FACGCE_tuning_major_scale_fingerboard_map` | 34 | fretboard_diagram | math, ring, rock, 开放弦, 点弦 | FACGCE调弦下的大调实用音符指板图，覆盖0-7品。图中黑色圆点标示根音位置（如6弦空弦、1弦5品等），空心圆点为音阶内其他音符。该指型设计包含开放弦与重复音，旨在提供丰富的旋律选择，适用于Math Rock风格的主奏、点弦Riff及过渡乐句创作。 |
| 5 | 4 |  | 0.1336 | -0.0686 | `FACGCE_tuning_G7_chord_shape` | 33 | chord_diagram | math, ring, rock, 开放弦 | FACGCE特殊调弦下的G7和弦指型图。利用该调弦特性，通过6弦3品按弦配合多根开放弦构成属七和弦 voicing。1、2弦标注闷音（xx），保留中低频开放弦共鸣，呈现Math Rock风格特有的开放、清脆且具张力的和声色彩。 |

### style_odd_meter_riff - PASS

- Query: Math Rock I-IV 大七和弦快速转换，6/8 到 9/8 变拍 riff
- Expected any: mr_style_015, math_rock_I_IV_riff_irregular_meters
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.084s = embed 0.077s + chroma 0.007s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1147 | 0.0413 | `math_rock_I_IV_riff_irregular_meters` | 78 | tab_excerpt | 6, 8, 9, i-iv, math, riff, rock, 和弦 | Math Rock风格I-IV和弦进行Riff谱例。包含C大七与F大七和弦的快速转换，采用6/8与9/8非常规节拍混合。谱面展示了开放把位与高把位封闭和弦的交替，体现了数学摇滚中复杂的节奏分组（3+4拍与3组3拍）及编配特征。 |
| 2 | 3 |  | 0.2054 | -0.0914 | `FACGCE_tuning_G7_chord_shape` | 33 | chord_diagram | 6, 8, 9, math, riff, rock, 和弦 | FACGCE特殊调弦下的G7和弦指型图。利用该调弦特性，通过6弦3品按弦配合多根开放弦构成属七和弦 voicing。1、2弦标注闷音（xx），保留中低频开放弦共鸣，呈现Math Rock风格特有的开放、清脆且具张力的和声色彩。 |
| 3 | 2 |  | 0.2015 | -0.0995 | `G7_shell_voicings` | 61 | chord_diagram | 6, 8, 9, math, rock, 和弦 | 展示G7属七和弦的三种Shell Voicing（壳式按法）指型图。包含开放把位、第4把位及第9把位三种形态。图示明确标记了 mute (x) 位置，强调仅保留根音、三音与七音的稀疏结构，省略五音，适用于Math Rock风格的高增益编配。 |
| 4 | 8 |  | 0.2249 | -0.1049 | `FACGCE_tuning_Fmaj9_open_chord` | 33 | chord_diagram | 6, 8, 9, math, riff, rock, 和弦 | FACGCE特殊调弦下的Fmaj9和弦指型图。图示显示该和弦在开放把位演奏，六根弦均为空弦音（oooooo），无需左手按品。利用FACGCE调弦特性，空弦音直接构成F大九和弦（根音F、三音A、五音C、九音G、七音E），是Math Rock风格中典型的开放和声Voicing。 |
| 5 | 7 |  | 0.2156 | -0.1136 | `FACGCE_tuning_Am_chord_shape` | 33 | chord_diagram | 6, 9, math, riff, rock, 和弦 | FACGCE调弦下的Am和弦指型图。图示显示6弦与1弦标记为闷音（X），根音A位于6弦3品，其余按弦点分布在5、4、3弦的低把位区域。该指型利用开放弦共鸣，构成完整的A小三和弦结构，是Math Rock风格中基于特殊调弦的基础和声素材。 |

### foundation_b6 - PASS

- Query: B6 六和弦指法，不包含七度音，根音在九品附近
- Expected any: B6_chord_shape, B6
- First hit rank: 1
- Rerank: `True`, candidates: 30
- Latency: total 0.085s = embed 0.076s + chroma 0.009s

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
- Latency: total 0.079s = embed 0.069s + chroma 0.010s

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
- Latency: total 0.090s = embed 0.077s + chroma 0.012s

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
- Latency: total 0.089s = embed 0.080s + chroma 0.008s

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
- Latency: total 0.057s = embed 0.049s + chroma 0.008s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1414 | -0.0064 | `Gsus2` | data/练习解答（图片）/练习58-59.png | chord_diagram | 1, 2, 5, gsus2, 和弦, 指法, 构成音 | Gsus2和弦指法图，位于第II把位。图示包含根音标记及声部编号1、2、5，展示了该挂留和弦在指板上的具体按点位置与构成音分布。 |
| 2 | 2 |  | 0.2054 | -0.0904 | `C/G (C major triad over G bass)` | data/练习解答（图片）/练习58-59.png | chord_diagram | 1, 2, 5, 和弦, 指法, 构成音 | 吉他指板图示展示 C/G 和弦指型。位于第 V 把位（约第5品），指法标记为 5-1-3。构成音为低音 G 加上 C 大三和弦（C-E-G），属于 Slash 和弦 voicing。 |
| 3 | 20 |  | 0.2292 | -0.1052 | `G13` | data/练习解答（图片）/练习49-51.png | chord_diagram | 1, 2, 5, 和弦, 指法, 构成音 | G13和弦指法图，位于第3把位（III）。图示标注了声部构成音程：b7、3、13、1。按点分布在6弦3品、5弦5品、4弦4品及2弦3品（双圈强调）。 |
| 4 | 24 |  | 0.2306 | -0.1096 | `G7(#5)` | data/练习解答（图片）/练习49-51.png | chord_diagram | 1, 2, 5, 和弦, 指法, 构成音 | 练习51第8题答案：G7(#5)和弦指法图。根音位于III把位（3品6弦），构成音标注为b7、3、#5，分别位于4品5弦、5品4弦和5品3弦。 |
| 5 | 7 |  | 0.2188 | -0.1098 | `Gbma13` | data/练习解答（图片）/练习49-51.png | chord_diagram | 1, 2, 5, 和弦, 指法 | Gbma13和弦指法图，位于第II把位。图示标注了声部构成：1(根音)、7、3、13。6弦2品为根音Gb，配合5、4、3弦的延伸音构成大十三和弦。 |

### foundation_plain_g7 - PASS

- Query: 标准调弦 G7 属七和弦普通指型图
- Expected any: G7
- First hit rank: 4
- Rerank: `True`, candidates: 30
- Latency: total 0.137s = embed 0.129s + chroma 0.008s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 |  | 0.1210 | -0.0270 | `FACGCE_tuning_G7_chord_shape` | 33 | chord_diagram | g7, 和弦, 指型, 调弦 | FACGCE特殊调弦下的G7和弦指型图。利用该调弦特性，通过6弦3品按弦配合多根开放弦构成属七和弦 voicing。1、2弦标注闷音（xx），保留中低频开放弦共鸣，呈现Math Rock风格特有的开放、清脆且具张力的和声色彩。 |
| 2 | 2 |  | 0.1394 | -0.0584 | `G7_shell_voicings` | 61 | chord_diagram | g7, 和弦, 指型, 调弦 | 展示G7属七和弦的三种Shell Voicing（壳式按法）指型图。包含开放把位、第4把位及第9把位三种形态。图示明确标记了 mute (x) 位置，强调仅保留根音、三音与七音的稀疏结构，省略五音，适用于Math Rock风格的高增益编配。 |
| 3 | 5 |  | 0.1670 | -0.0820 | `FACGCE_tuning_Am_chord_shape` | 33 | chord_diagram | 和弦, 指型, 标准调弦, 调弦 | FACGCE调弦下的Am和弦指型图。图示显示6弦与1弦标记为闷音（X），根音A位于6弦3品，其余按弦点分布在5、4、3弦的低把位区域。该指型利用开放弦共鸣，构成完整的A小三和弦结构，是Math Rock风格中基于特殊调弦的基础和声素材。 |
| 4 | 4 | Y | 0.1604 | -0.0844 | `G7(#5)` | data/练习解答（图片）/练习49-51.png | chord_diagram | g7, 和弦, 指型 | 练习51第8题答案：G7(#5)和弦指法图。根音位于III把位（3品6弦），构成音标注为b7、3、#5，分别位于4品5弦、5品4弦和5品3弦。 |
| 5 | 7 | Y | 0.1701 | -0.0941 | `G7(b9)` | data/练习解答（图片）/练习49-51.png | chord_diagram | g7, 和弦, 指型 | 垂直指板图展示 G7(b9) 和弦，位于第 IX 把位（9品）。上方标注声部构成：1、3、b7、b9。按点分布：6弦9品为根音（双圈强调），4弦9品，3弦10品，2弦10品。 |

### foundation_plain_cmaj7 - MISS

- Query: 标准调弦 Cmaj7 大七和弦基础指型，不需要点弦谱例
- Expected any: Cmaj7, Cma7, C major seventh, MA7
- First hit rank: None
- Rerank: `True`, candidates: 30
- Latency: total 0.085s = embed 0.076s + chroma 0.009s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 |  | 0.1126 | 0.0134 | `Cmaj7_tapping_arpeggio` | 73 | tab_excerpt | cmaj7, 和弦, 指型, 标准调弦, 点弦, 调弦, 谱例 | C大七和弦（Cmaj7）点弦琶音谱例。展示标准调弦下结合开放弦持续音与高把位点弦（T/P）的演奏技法。乐谱包含明确的“持续音”与“let ring”标记，强调声部延留与数学摇滚风格的复调听感，涵盖根音、三音、五音及七音的分解排列。 |
| 2 | 2 |  | 0.1401 | -0.0551 | `FACGCE_tuning_Fmaj9_open_chord` | 33 | chord_diagram | 和弦, 指型, 点弦, 调弦 | FACGCE特殊调弦下的Fmaj9和弦指型图。图示显示该和弦在开放把位演奏，六根弦均为空弦音（oooooo），无需左手按品。利用FACGCE调弦特性，空弦音直接构成F大九和弦（根音F、三音A、五音C、九音G、七音E），是Math Rock风格中典型的开放和声Voicing。 |
| 3 | 8 |  | 0.1485 | -0.0635 | `FACGCE_tuning_Am_chord_shape` | 33 | chord_diagram | 和弦, 指型, 标准调弦, 调弦 | FACGCE调弦下的Am和弦指型图。图示显示6弦与1弦标记为闷音（X），根音A位于6弦3品，其余按弦点分布在5、4、3弦的低把位区域。该指型利用开放弦共鸣，构成完整的A小三和弦结构，是Math Rock风格中基于特殊调弦的基础和声素材。 |
| 4 | 3 |  | 0.1402 | -0.0672 | `FACGCE_tuning_G7_chord_shape` | 33 | chord_diagram | 和弦, 指型, 调弦 | FACGCE特殊调弦下的G7和弦指型图。利用该调弦特性，通过6弦3品按弦配合多根开放弦构成属七和弦 voicing。1、2弦标注闷音（xx），保留中低频开放弦共鸣，呈现Math Rock风格特有的开放、清脆且具张力的和声色彩。 |
| 5 | 25 |  | 0.1653 | -0.0683 | `FACGCE_tuning_major_scale_fingerboard_map` | 34 | fretboard_diagram | 和弦, 指型, 标准调弦, 点弦, 调弦 | FACGCE调弦下的大调实用音符指板图，覆盖0-7品。图中黑色圆点标示根音位置（如6弦空弦、1弦5品等），空心圆点为音阶内其他音符。该指型设计包含开放弦与重复音，旨在提供丰富的旋律选择，适用于Math Rock风格的主奏、点弦Riff及过渡乐句创作。 |
