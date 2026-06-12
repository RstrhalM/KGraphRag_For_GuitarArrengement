# Visual Caption Retrieval Trial

## Summary

- Collection: `guitar_mathrock_style_visual_trial_qwen3_06b` (9 docs)
- Model: `D:\Guitar Arrangement Inspiration Agent\KGraphRag2\models\embedding\qwen3-embedding-0.6b` on `cuda`, dim=1024
- Tests: 7, TopK: 5
- Rerank: `True`, candidates: 9
- Hit@1: 7/7
- Hit@K: 7/7
- Avg total latency/query: 0.143s
- Median total latency/query: 0.058s

## Cases

### facgce_fmaj9 - PASS

- Query: FACGCE 调弦的 Fmaj9 全开放弦和弦指型
- Expected any: mr_style_001_fmaj9, FACGCE_tuning_Fmaj9_open_chord
- First hit rank: 1
- Rerank: `True`, candidates: 9
- Latency: total 0.665s = embed 0.486s + chroma 0.179s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0893 | 0.0377 | `FACGCE_tuning_Fmaj9_open_chord` | 33 | chord_diagram | facgce, fmaj9, 和弦, 开放弦, 指型, 调弦 | FACGCE特殊调弦下的Fmaj9和弦指型图。图示显示该和弦在开放把位演奏，六根弦均为空弦音（oooooo），无需左手按品。利用FACGCE调弦特性，空弦音直接构成F大九和弦（根音F、三音A、五音C、九音G、七音E），是Math Rock风格中典型的开放和声Voicing。 |
| 2 | 2 |  | 0.1166 | 0.0074 | `FACGCE_tuning_Am_chord_shape` | 33 | chord_diagram | facgce, 和弦, 开放弦, 指型, 调弦, 调弦的 | FACGCE调弦下的Am和弦指型图。图示显示6弦与1弦标记为闷音（X），根音A位于6弦3品，其余按弦点分布在5、4、3弦的低把位区域。该指型利用开放弦共鸣，构成完整的A小三和弦结构，是Math Rock风格中基于特殊调弦的基础和声素材。 |
| 3 | 3 |  | 0.1204 | 0.0006 | `FACGCE_tuning_G7_chord_shape` | 33 | chord_diagram | facgce, 和弦, 开放弦, 指型, 调弦, 调弦的 | FACGCE特殊调弦下的G7和弦指型图。利用该调弦特性，通过6弦3品按弦配合多根开放弦构成属七和弦 voicing。1、2弦标注闷音（xx），保留中低频开放弦共鸣，呈现Math Rock风格特有的开放、清脆且具张力的和声色彩。 |
| 4 | 5 |  | 0.1405 | -0.0225 | `FACGCE_tuning_major_scale_fingerboard_map` | 34 | fretboard_diagram | facgce, 和弦, 开放弦, 指型, 调弦, 调弦的 | FACGCE调弦下的大调实用音符指板图，覆盖0-7品。图中黑色圆点标示根音位置（如6弦空弦、1弦5品等），空心圆点为音阶内其他音符。该指型设计包含开放弦与重复音，旨在提供丰富的旋律选择，适用于Math Rock风格的主奏、点弦Riff及过渡乐句创作。 |
| 5 | 6 |  | 0.1441 | -0.0381 | `FACGCE_Bm7b5_chord_shape` | 33 | chord_diagram | facgce, 和弦, 开放弦, 指型, 调弦 | FACGCE特殊调弦下的Bm7b5（半减七）和弦指型图。图示标记起始品位为5品，展示该调弦体系中Bm7b5的特定按法与把位分布，包含根音B及降五度音F的排列结构，适用于Math Rock风格编配。 |

### facgce_am_add11 - PASS

- Query: FACGCE 特殊调弦下 Am add11 开放弦 voicing 指型
- Expected any: mr_style_001_am_add11, FACGCE_Am_add11_chord_shape
- First hit rank: 1
- Rerank: `True`, candidates: 9
- Latency: total 0.067s = embed 0.064s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1213 | 0.0317 | `FACGCE_Am_add11_chord_shape` | 33 | chord_diagram | add11, am, facgce, voicing, 开放弦, 指型, 特殊调弦下, 调弦 | FACGCE特殊调弦下的Am(add11)和弦指型图。图示为开放把位按法，利用调弦特性在低把位构建包含根音、小三度、五度及十一度延伸音的和声结构。高音弦（1、2弦）标记为“xx”表示制音或不发声，强调低音区开放弦的共鸣与数学摇滚特有的清冷色彩。 |
| 2 | 2 |  | 0.1244 | 0.0026 | `FACGCE_tuning_Am_chord_shape` | 33 | chord_diagram | am, facgce, voicing, 开放弦, 指型, 调弦 | FACGCE调弦下的Am和弦指型图。图示显示6弦与1弦标记为闷音（X），根音A位于6弦3品，其余按弦点分布在5、4、3弦的低把位区域。该指型利用开放弦共鸣，构成完整的A小三和弦结构，是Math Rock风格中基于特殊调弦的基础和声素材。 |
| 3 | 3 |  | 0.1464 | -0.0104 | `FACGCE_tuning_G7_chord_shape` | 33 | chord_diagram | am, facgce, voicing, 开放弦, 指型, 特殊调弦下, 调弦 | FACGCE特殊调弦下的G7和弦指型图。利用该调弦特性，通过6弦3品按弦配合多根开放弦构成属七和弦 voicing。1、2弦标注闷音（xx），保留中低频开放弦共鸣，呈现Math Rock风格特有的开放、清脆且具张力的和声色彩。 |
| 4 | 4 |  | 0.1579 | -0.0249 | `FACGCE_tuning_Fmaj9_open_chord` | 33 | chord_diagram | am, facgce, voicing, 开放弦, 指型, 特殊调弦下, 调弦 | FACGCE特殊调弦下的Fmaj9和弦指型图。图示显示该和弦在开放把位演奏，六根弦均为空弦音（oooooo），无需左手按品。利用FACGCE调弦特性，空弦音直接构成F大九和弦（根音F、三音A、五音C、九音G、七音E），是Math Rock风格中典型的开放和声Voicing。 |
| 5 | 5 |  | 0.1647 | -0.0347 | `FACGCE_Bm7b5_chord_shape` | 33 | chord_diagram | am, facgce, voicing, 开放弦, 指型, 特殊调弦下, 调弦 | FACGCE特殊调弦下的Bm7b5（半减七）和弦指型图。图示标记起始品位为5品，展示该调弦体系中Bm7b5的特定按法与把位分布，包含根音B及降五度音F的排列结构，适用于Math Rock风格编配。 |

### facgce_bm7b5 - PASS

- Query: FACGCE 调弦 Bm7b5 半减七 可移动和弦指型
- Expected any: mr_style_001_bm7b5, FACGCE_Bm7b5_chord_shape
- First hit rank: 1
- Rerank: `True`, candidates: 9
- Latency: total 0.063s = embed 0.060s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0970 | 0.0330 | `FACGCE_Bm7b5_chord_shape` | 33 | chord_diagram | bm7b5, facgce, 半减七, 和弦, 指型, 调弦 | FACGCE特殊调弦下的Bm7b5（半减七）和弦指型图。图示标记起始品位为5品，展示该调弦体系中Bm7b5的特定按法与把位分布，包含根音B及降五度音F的排列结构，适用于Math Rock风格编配。 |
| 2 | 2 |  | 0.1465 | -0.0525 | `FACGCE_tuning_Am_chord_shape` | 33 | chord_diagram | facgce, 和弦, 指型, 调弦 | FACGCE调弦下的Am和弦指型图。图示显示6弦与1弦标记为闷音（X），根音A位于6弦3品，其余按弦点分布在5、4、3弦的低把位区域。该指型利用开放弦共鸣，构成完整的A小三和弦结构，是Math Rock风格中基于特殊调弦的基础和声素材。 |
| 3 | 3 |  | 0.1504 | -0.0564 | `FACGCE_tuning_G7_chord_shape` | 33 | chord_diagram | facgce, 和弦, 指型, 调弦 | FACGCE特殊调弦下的G7和弦指型图。利用该调弦特性，通过6弦3品按弦配合多根开放弦构成属七和弦 voicing。1、2弦标注闷音（xx），保留中低频开放弦共鸣，呈现Math Rock风格特有的开放、清脆且具张力的和声色彩。 |
| 4 | 4 |  | 0.1524 | -0.0584 | `FACGCE_tuning_Fmaj9_open_chord` | 33 | chord_diagram | facgce, 和弦, 指型, 调弦 | FACGCE特殊调弦下的Fmaj9和弦指型图。图示显示该和弦在开放把位演奏，六根弦均为空弦音（oooooo），无需左手按品。利用FACGCE调弦特性，空弦音直接构成F大九和弦（根音F、三音A、五音C、九音G、七音E），是Math Rock风格中典型的开放和声Voicing。 |
| 5 | 5 |  | 0.1534 | -0.0694 | `FACGCE_Am_add11_chord_shape` | 33 | chord_diagram | facgce, 和弦, 指型, 调弦 | FACGCE特殊调弦下的Am(add11)和弦指型图。图示为开放把位按法，利用调弦特性在低把位构建包含根音、小三度、五度及十一度延伸音的和声结构。高音弦（1、2弦）标记为“xx”表示制音或不发声，强调低音区开放弦的共鸣与数学摇滚特有的清冷色彩。 |

### facgce_major_tapping_map - PASS

- Query: FACGCE 大调指板音阶图，适合开放弦点弦和旋律 riff
- Expected any: mr_style_002, FACGCE_tuning_major_scale_fingerboard_map
- First hit rank: 1
- Rerank: `True`, candidates: 9
- Latency: total 0.049s = embed 0.046s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1000 | 0.0260 | `FACGCE_tuning_major_scale_fingerboard_map` | 34 | fretboard_diagram | facgce, riff, 大调, 开放弦, 点弦, 音阶 | FACGCE调弦下的大调实用音符指板图，覆盖0-7品。图中黑色圆点标示根音位置（如6弦空弦、1弦5品等），空心圆点为音阶内其他音符。该指型设计包含开放弦与重复音，旨在提供丰富的旋律选择，适用于Math Rock风格的主奏、点弦Riff及过渡乐句创作。 |
| 2 | 3 |  | 0.1279 | -0.0989 | `FACGCE_tuning_Fmaj9_open_chord` | 33 | chord_diagram | facgce, riff, 开放弦, 点弦 | FACGCE特殊调弦下的Fmaj9和弦指型图。图示显示该和弦在开放把位演奏，六根弦均为空弦音（oooooo），无需左手按品。利用FACGCE调弦特性，空弦音直接构成F大九和弦（根音F、三音A、五音C、九音G、七音E），是Math Rock风格中典型的开放和声Voicing。 |
| 3 | 2 |  | 0.1268 | -0.1068 | `FACGCE_tuning_Am_chord_shape` | 33 | chord_diagram | facgce, riff, 开放弦 | FACGCE调弦下的Am和弦指型图。图示显示6弦与1弦标记为闷音（X），根音A位于6弦3品，其余按弦点分布在5、4、3弦的低把位区域。该指型利用开放弦共鸣，构成完整的A小三和弦结构，是Math Rock风格中基于特殊调弦的基础和声素材。 |
| 4 | 4 |  | 0.1347 | -0.1147 | `FACGCE_tuning_G7_chord_shape` | 33 | chord_diagram | facgce, riff, 开放弦 | FACGCE特殊调弦下的G7和弦指型图。利用该调弦特性，通过6弦3品按弦配合多根开放弦构成属七和弦 voicing。1、2弦标注闷音（xx），保留中低频开放弦共鸣，呈现Math Rock风格特有的开放、清脆且具张力的和声色彩。 |
| 5 | 7 |  | 0.1619 | -0.1319 | `Cmaj7_tapping_arpeggio` | 73 | tab_excerpt | 开放弦, 点弦 | C大七和弦（Cmaj7）点弦琶音谱例。展示标准调弦下结合开放弦持续音与高把位点弦（T/P）的演奏技法。乐谱包含明确的“持续音”与“let ring”标记，强调声部延留与数学摇滚风格的复调听感，涵盖根音、三音、五音及七音的分解排列。 |

### g7_shell_voicing - PASS

- Query: G7 shell voicing 壳式和弦，省略五音并减少高增益频段冲突
- Expected any: mr_style_008, G7_shell_voicings
- First hit rank: 1
- Rerank: `True`, candidates: 9
- Latency: total 0.058s = embed 0.056s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1137 | -0.0177 | `G7_shell_voicings` | 61 | chord_diagram | g7, shell, voicing, 和弦 | 展示G7属七和弦的三种Shell Voicing（壳式按法）指型图。包含开放把位、第4把位及第9把位三种形态。图示明确标记了 mute (x) 位置，强调仅保留根音、三音与七音的稀疏结构，省略五音，适用于Math Rock风格的高增益编配。 |
| 2 | 2 |  | 0.1767 | -0.0977 | `FACGCE_tuning_G7_chord_shape` | 33 | chord_diagram | g7, voicing, 和弦 | FACGCE特殊调弦下的G7和弦指型图。利用该调弦特性，通过6弦3品按弦配合多根开放弦构成属七和弦 voicing。1、2弦标注闷音（xx），保留中低频开放弦共鸣，呈现Math Rock风格特有的开放、清脆且具张力的和声色彩。 |
| 3 | 4 |  | 0.2101 | -0.1551 | `FACGCE_tuning_Am_chord_shape` | 33 | chord_diagram | voicing, 和弦 | FACGCE调弦下的Am和弦指型图。图示显示6弦与1弦标记为闷音（X），根音A位于6弦3品，其余按弦点分布在5、4、3弦的低把位区域。该指型利用开放弦共鸣，构成完整的A小三和弦结构，是Math Rock风格中基于特殊调弦的基础和声素材。 |
| 4 | 5 |  | 0.2136 | -0.1586 | `FACGCE_Bm7b5_chord_shape` | 33 | chord_diagram | voicing, 和弦 | FACGCE特殊调弦下的Bm7b5（半减七）和弦指型图。图示标记起始品位为5品，展示该调弦体系中Bm7b5的特定按法与把位分布，包含根音B及降五度音F的排列结构，适用于Math Rock风格编配。 |
| 5 | 3 |  | 0.2072 | -0.1622 | `FACGCE_Am_add11_chord_shape` | 33 | chord_diagram | voicing, 和弦 | FACGCE特殊调弦下的Am(add11)和弦指型图。图示为开放把位按法，利用调弦特性在低把位构建包含根音、小三度、五度及十一度延伸音的和声结构。高音弦（1、2弦）标记为“xx”表示制音或不发声，强调低音区开放弦的共鸣与数学摇滚特有的清冷色彩。 |

### cmaj7_tapping - PASS

- Query: Cmaj7 两手点弦琶音，开放弦持续音和 let ring 谱例
- Expected any: mr_style_010, Cmaj7_tapping_arpeggio
- First hit rank: 1
- Rerank: `True`, candidates: 9
- Latency: total 0.046s = embed 0.043s + chroma 0.002s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.0921 | 0.0609 | `Cmaj7_tapping_arpeggio` | 73 | tab_excerpt | cmaj7, let, ring, 开放弦, 点弦, 琶音, 谱例 | C大七和弦（Cmaj7）点弦琶音谱例。展示标准调弦下结合开放弦持续音与高把位点弦（T/P）的演奏技法。乐谱包含明确的“持续音”与“let ring”标记，强调声部延留与数学摇滚风格的复调听感，涵盖根音、三音、五音及七音的分解排列。 |
| 2 | 2 |  | 0.1343 | -0.0803 | `FACGCE_tuning_Fmaj9_open_chord` | 33 | chord_diagram | ring, 开放弦, 点弦 | FACGCE特殊调弦下的Fmaj9和弦指型图。图示显示该和弦在开放把位演奏，六根弦均为空弦音（oooooo），无需左手按品。利用FACGCE调弦特性，空弦音直接构成F大九和弦（根音F、三音A、五音C、九音G、七音E），是Math Rock风格中典型的开放和声Voicing。 |
| 3 | 4 |  | 0.1514 | -0.0824 | `math_rock_I_IV_riff_irregular_meters` | 78 | tab_excerpt | cmaj7, ring, 开放弦, 谱例 | Math Rock风格I-IV和弦进行Riff谱例。包含C大七与F大七和弦的快速转换，采用6/8与9/8非常规节拍混合。谱面展示了开放把位与高把位封闭和弦的交替，体现了数学摇滚中复杂的节奏分组（3+4拍与3组3拍）及编配特征。 |
| 4 | 6 |  | 0.1597 | -0.0997 | `FACGCE_tuning_major_scale_fingerboard_map` | 34 | fretboard_diagram | ring, 开放弦, 点弦 | FACGCE调弦下的大调实用音符指板图，覆盖0-7品。图中黑色圆点标示根音位置（如6弦空弦、1弦5品等），空心圆点为音阶内其他音符。该指型设计包含开放弦与重复音，旨在提供丰富的旋律选择，适用于Math Rock风格的主奏、点弦Riff及过渡乐句创作。 |
| 5 | 3 |  | 0.1473 | -0.1123 | `FACGCE_tuning_G7_chord_shape` | 33 | chord_diagram | ring, 开放弦 | FACGCE特殊调弦下的G7和弦指型图。利用该调弦特性，通过6弦3品按弦配合多根开放弦构成属七和弦 voicing。1、2弦标注闷音（xx），保留中低频开放弦共鸣，呈现Math Rock风格特有的开放、清脆且具张力的和声色彩。 |

### mathrock_odd_meter_riff - PASS

- Query: Math Rock I-IV 大七和弦快速转换，6/8 到 9/8 变拍 riff
- Expected any: mr_style_015, math_rock_I_IV_riff_irregular_meters
- First hit rank: 1
- Rerank: `True`, candidates: 9
- Latency: total 0.050s = embed 0.047s + chroma 0.003s

| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |
|---:|---:|:---:|---:|---:|---|---:|---|---|---|
| 1 | 1 | Y | 0.1147 | 0.0413 | `math_rock_I_IV_riff_irregular_meters` | 78 | tab_excerpt | 6, 8, 9, i-iv, math, riff, rock, 和弦 | Math Rock风格I-IV和弦进行Riff谱例。包含C大七与F大七和弦的快速转换，采用6/8与9/8非常规节拍混合。谱面展示了开放把位与高把位封闭和弦的交替，体现了数学摇滚中复杂的节奏分组（3+4拍与3组3拍）及编配特征。 |
| 2 | 3 |  | 0.2054 | -0.0914 | `FACGCE_tuning_G7_chord_shape` | 33 | chord_diagram | 6, 8, 9, math, riff, rock, 和弦 | FACGCE特殊调弦下的G7和弦指型图。利用该调弦特性，通过6弦3品按弦配合多根开放弦构成属七和弦 voicing。1、2弦标注闷音（xx），保留中低频开放弦共鸣，呈现Math Rock风格特有的开放、清脆且具张力的和声色彩。 |
| 3 | 2 |  | 0.2015 | -0.0995 | `G7_shell_voicings` | 61 | chord_diagram | 6, 8, 9, math, rock, 和弦 | 展示G7属七和弦的三种Shell Voicing（壳式按法）指型图。包含开放把位、第4把位及第9把位三种形态。图示明确标记了 mute (x) 位置，强调仅保留根音、三音与七音的稀疏结构，省略五音，适用于Math Rock风格的高增益编配。 |
| 4 | 8 |  | 0.2249 | -0.1049 | `FACGCE_tuning_Fmaj9_open_chord` | 33 | chord_diagram | 6, 8, 9, math, riff, rock, 和弦 | FACGCE特殊调弦下的Fmaj9和弦指型图。图示显示该和弦在开放把位演奏，六根弦均为空弦音（oooooo），无需左手按品。利用FACGCE调弦特性，空弦音直接构成F大九和弦（根音F、三音A、五音C、九音G、七音E），是Math Rock风格中典型的开放和声Voicing。 |
| 5 | 7 |  | 0.2156 | -0.1136 | `FACGCE_tuning_Am_chord_shape` | 33 | chord_diagram | 6, 9, math, riff, rock, 和弦 | FACGCE调弦下的Am和弦指型图。图示显示6弦与1弦标记为闷音（X），根音A位于6弦3品，其余按弦点分布在5、4、3弦的低把位区域。该指型利用开放弦共鸣，构成完整的A小三和弦结构，是Math Rock风格中基于特殊调弦的基础和声素材。 |
