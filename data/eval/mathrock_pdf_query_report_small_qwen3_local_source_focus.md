# Retrieval Bundle 小规模评测

- 生成时间：2026-06-02 19:32:30
- 检索模式：`source_focus`
- CLI primary sources：mathrock_pdf_steve_h
- 测试数：3
- Bundle 通过率：3/3 (100.0%)
- 文本 Top1 准确率：100.0%
- 文本 Recall@5：100.0%
- 文本 Precision@5 平均：1.00
- 视觉 Top1 准确率：100.0%
- 视觉 Recall@5：100.0%
- 视觉 Precision@5 平均：1.00
- Neo4j 预期节点命中率：100.0%
- 总耗时：8.72s
- 单条平均耗时：2.91s
- 文本平均耗时：1.71s
- 视觉平均耗时：0.04s
- Neo4j 平均耗时：1.15s
- Embedding 缓存：312 条，路径 `D:\Guitar Arrangement Inspiration Agent\KGraphRag2\data\cache\embeddings.sqlite`

## 总览

| 用例 | 文本Top1 | 文本R@5 | 视觉Top1 | 视觉R@5 | KG | Bundle | 耗时 |
|---|---:|---:|---:|---:|---:|---:|---:|
| pdf_tapping_simultaneous_rhythm_lead | OK | OK | OK | OK | OK | OK | 8.52s |
| pdf_facgce_open_string_voicing | OK | OK | OK | OK | OK | OK | 0.11s |
| pdf_clean_maj9_ambient_texture | OK | OK | OK | OK | OK | OK | 0.08s |

## 明细

### pdf_tapping_simultaneous_rhythm_lead

- 查询：`math rock two hand tapping simultaneous rhythm and lead clean solo guitar arrangement`
- 检索模式：`source_focus`
- Primary sources：mathrock_pdf_steve_h
- 期望文本源：mathrock_pdf_steve_h
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=8.52s，text=5.02s，visual=0.10s，kg=3.41s
- 缓存：text_embedding=MISS，visual_embedding=OK

文本 Top5：
1. `mathrock_pdf_steve_h` / `chunk_0002` / dist=0.3835 /   
   ## 双⼿点弦与交替⼿指点弦 双⼿点弦主要包括交替点弦（双⼿轮流击弦），这可能是数学摇滚吉他⼿最常⽤的点弦技法。但有时你也会需要双⼿同步点奏音符，或⽤按弦⼿凭空锤音并保持音符以构建功能性和声（如⻉斯线）。以下范例（练习1.d）节选⾃我改编的《圣诞⽼人进城》曲谱。为清晰起⻅我将两个声部分开记谱，但实际需同步点奏。我发现让⼤脑同时处理两个点弦音符要困难得多。亲⾃
2. `mathrock_pdf_steve_h` / `chunk_0003` / dist=0.3983 /   
   ## ⼿指控制+拨弦和弦 现在我们来学习同时拨弦的技巧。这能为你的和弦带来截然不同的质感——因为所有琴弦是被同时拨响，⽽非拨⽚扫弦的连续发声方式。它能提供更精准的动态控制、更高的演奏准确度，以及整体音色的变化。 入⻔练习2.g将不同⼿指组合（注意符头标注的使⽤⼿指）与拇指练习相结合。 [IMAGE_BLOCK:images/82b3d390df1caea14
3. `mathrock_pdf_steve_h` / `chunk_0004` / dist=0.4095 /   
   ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音
4. `mathrock_pdf_steve_h` / `chunk_0009` / dist=0.4174 /   
   ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益
5. `mathrock_pdf_steve_h` / `chunk_0010` / dist=0.4396 /   
   ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩

Support 文本 Top：
1. `mathrock_text_course` / `chunk_0003` / dist=0.2284 /   
   math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shoo
2. `mathrock_text_course` / `chunk_0002` / dist=0.2290 /   
   all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered ar
3. `mathrock_text_course` / `chunk_0005` / dist=0.2569 /   
   we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have A

视觉 Top5：
1. `None` / page=25 / dist=0.4862 / rerank=0.7500 / 练习3.f在先前练习基础上扩展，结合拨⽚与双指拨弦技巧，并在最后⼩节加入全部三根备⽤⼿指的运⽤ | 练习3.g演⽰如何仅⽤混合拨弦技术组合两个音符，创造新颖乐思 | 混合拨弦技巧与⼒量发展的情境化练习  
   `data\processed\mathrock\pdf_mineru\Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans\auto\images\67b2ebfdbc78a35c746c708a30dba26a18c2568b2811afbcc146b28062334eee.jpg`
2. `None` / page=20 / dist=0.4903 / rerank=0.7500 / ⼿指控制+拨弦和弦 | 情境化指弹练习  
   `data\processed\mathrock\pdf_mineru\Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans\auto\images\b7797b8676eef652b7d4e802d3176ad5c5ef7d0019046c882d9a95fb00c39877.jpg`
3. `None` / page=77 / dist=0.5011 / rerank=0.7500 / 琶音/riff/节拍谱例密集页，整页适合作视觉证据。  
   `data\processed\mathrock\pdf_page_images\mathrock_pdf_page_078.jpg`
4. `None` / page=18 / dist=0.5158 / rerank=0.7500 /   
   `data\processed\mathrock\pdf_mineru\Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans\auto\images\bb371f205382904cfc3b0ca70af0e42ef2b4a409f05fa8428532a223ea0296ce.jpg`
5. `None` / page=36 / dist=0.5192 / rerank=0.7500 / DAEAC#E调弦法和弦指法  
   `data\processed\mathrock\pdf_mineru\Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans\auto\images\0f7e0b37016fdef91e7b35f84ebb9504a38ade78bdb19614f17414dfddef355a.jpg`

Neo4j：
- 命中节点：technique:two_hand_tapping, guitar_idiom:simultaneous_rhythm_lead, guitar_idiom:solo_guitar_arrangement
- 关系样例：`technique:two_hand_tapping` -[ENABLES]- `feature:tapped_power_chords`
- 关系样例：`feature:tapped_power_chords` -[ENABLES]- `technique:two_hand_tapping`
- 关系样例：`technique:two_hand_tapping` -[ENABLES]- `guitar_idiom:simultaneous_rhythm_lead`

### pdf_facgce_open_string_voicing

- 查询：`FACGCE tuning open strings Fmaj9 movable barre shapes math rock voicing`
- 检索模式：`source_focus`
- Primary sources：mathrock_pdf_steve_h
- 期望文本源：mathrock_pdf_steve_h
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=0.11s，text=0.07s，visual=0.01s，kg=0.03s
- 缓存：text_embedding=MISS，visual_embedding=OK

文本 Top5：
1. `mathrock_pdf_steve_h` / `chunk_0004` / dist=0.3202 /   
   ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音
2. `mathrock_pdf_steve_h` / `chunk_0009` / dist=0.3539 /   
   ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益
3. `mathrock_pdf_steve_h` / `chunk_0002` / dist=0.3621 /   
   ## 双⼿点弦与交替⼿指点弦 双⼿点弦主要包括交替点弦（双⼿轮流击弦），这可能是数学摇滚吉他⼿最常⽤的点弦技法。但有时你也会需要双⼿同步点奏音符，或⽤按弦⼿凭空锤音并保持音符以构建功能性和声（如⻉斯线）。以下范例（练习1.d）节选⾃我改编的《圣诞⽼人进城》曲谱。为清晰起⻅我将两个声部分开记谱，但实际需同步点奏。我发现让⼤脑同时处理两个点弦音符要困难得多。亲⾃
4. `mathrock_pdf_steve_h` / `chunk_0006` / dist=0.3831 /   
   ## 为何掌握调号至关重要？ 明确调性对创作和演奏歌曲⼤有裨益。⾸先，它能精准定位可⽤的和弦、音符及音阶/琶音体系。 以C⼤调为例，其音阶包含以下音符： <table><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>3</td><t
5. `mathrock_pdf_steve_h` / `chunk_0010` / dist=0.3838 /   
   ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩

Support 文本 Top：
1. `mathrock_text_course` / `chunk_0007` / dist=0.2376 /   
   we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can 
2. `mathrock_text_course` / `chunk_0003` / dist=0.2530 /   
   math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shoo
3. `mathrock_text_course` / `chunk_0002` / dist=0.2638 /   
   all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered ar

视觉 Top5：
- 推断 priority：P2_arpeggios_chords
1. `None` / page=32 / dist=0.4601 / rerank=1.0000 / 特殊调弦/指型/音阶密集页，整页保留上下文。  
   `data\processed\mathrock\pdf_page_images\mathrock_pdf_page_033.jpg`
2. `None` / page=33 / dist=0.3995 / rerank=0.7500 / 特殊调弦/指型/音阶密集页，整页保留上下文。  
   `data\processed\mathrock\pdf_page_images\mathrock_pdf_page_034.jpg`
3. `None` / page=66 / dist=0.4159 / rerank=0.7500 /   
   `data\processed\mathrock\pdf_mineru\Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans\auto\images\453abdc92272702f3f1d53ed0110eef727bb4d495ba1d760a7015fc672b62500.jpg`
4. `None` / page=36 / dist=0.4230 / rerank=0.7500 / 特殊调弦/指型/音阶密集页，整页保留上下文。  
   `data\processed\mathrock\pdf_page_images\mathrock_pdf_page_037.jpg`
5. `None` / page=34 / dist=0.4264 / rerank=0.7500 / 特殊调弦/指型/音阶密集页，整页保留上下文。  
   `data\processed\mathrock\pdf_page_images\mathrock_pdf_page_035.jpg`

Neo4j：
- 命中节点：tuning:FACGCE, chord:open_Fmaj9, pattern:movable_barre_shapes_root_6
- 关系样例：`tuning:FACGCE` -[ENABLES]- `chord:open_Fmaj9`
- 关系样例：`chord:open_Fmaj9` -[ENABLES]- `tuning:FACGCE`
- 关系样例：`tuning:FACGCE` -[SUGGESTS]- `pattern:movable_barre_shapes_root_6`

### pdf_clean_maj9_ambient_texture

- 查询：`math rock clean open string maj9 lush ambient texture arpeggio intro bridge`
- 检索模式：`source_focus`
- Primary sources：mathrock_pdf_steve_h
- 期望文本源：mathrock_pdf_steve_h
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=0.08s，text=0.05s，visual=0.01s，kg=0.03s
- 缓存：text_embedding=MISS，visual_embedding=OK

文本 Top5：
1. `mathrock_pdf_steve_h` / `chunk_0004` / dist=0.3572 /   
   ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音
2. `mathrock_pdf_steve_h` / `chunk_0009` / dist=0.3705 /   
   ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益
3. `mathrock_pdf_steve_h` / `chunk_0002` / dist=0.3834 /   
   ## 双⼿点弦与交替⼿指点弦 双⼿点弦主要包括交替点弦（双⼿轮流击弦），这可能是数学摇滚吉他⼿最常⽤的点弦技法。但有时你也会需要双⼿同步点奏音符，或⽤按弦⼿凭空锤音并保持音符以构建功能性和声（如⻉斯线）。以下范例（练习1.d）节选⾃我改编的《圣诞⽼人进城》曲谱。为清晰起⻅我将两个声部分开记谱，但实际需同步点奏。我发现让⼤脑同时处理两个点弦音符要困难得多。亲⾃
4. `mathrock_pdf_steve_h` / `chunk_0003` / dist=0.4068 /   
   ## ⼿指控制+拨弦和弦 现在我们来学习同时拨弦的技巧。这能为你的和弦带来截然不同的质感——因为所有琴弦是被同时拨响，⽽非拨⽚扫弦的连续发声方式。它能提供更精准的动态控制、更高的演奏准确度，以及整体音色的变化。 入⻔练习2.g将不同⼿指组合（注意符头标注的使⽤⼿指）与拇指练习相结合。 [IMAGE_BLOCK:images/82b3d390df1caea14
5. `mathrock_pdf_steve_h` / `chunk_0010` / dist=0.4092 /   
   ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩

Support 文本 Top：
1. `mathrock_text_course` / `chunk_0007` / dist=0.2420 /   
   we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can 
2. `mathrock_text_course` / `chunk_0003` / dist=0.2470 /   
   math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shoo
3. `mathrock_text_course` / `chunk_0002` / dist=0.2484 /   
   all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered ar

视觉 Top5：
- 推断 priority：P2_arpeggios_chords
1. `None` / page=66 / dist=0.5573 / rerank=0.7500 /   
   `data\processed\mathrock\pdf_mineru\Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans\auto\images\453abdc92272702f3f1d53ed0110eef727bb4d495ba1d760a7015fc672b62500.jpg`
2. `None` / page=77 / dist=0.5406 / rerank=0.5000 /   
   `data\processed\mathrock\pdf_mineru\Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans\auto\images\f9c4d79826ed121574f604ea4b24497e5f6ef828400975d1ba24056ae77f235a.jpg`
3. `None` / page=61 / dist=0.5409 / rerank=0.5000 / 和弦进⾏  
   `data\processed\mathrock\pdf_mineru\Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans\auto\images\3d5f88929db9c3662b0dea0792712ba5f772087cb6874ccd41216c0bf26577d7.jpg`
4. `None` / page=50 / dist=0.5493 / rerank=0.5000 /   
   `data\processed\mathrock\pdf_mineru\Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans\auto\images\f5a1231ab0bab8751141282b772f559088fb8d34bc06a6be58bd14b007b8e763.jpg`
5. `None` / page=32 / dist=0.5506 / rerank=0.5000 /   
   `data\processed\mathrock\pdf_mineru\Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans\auto\images\9ed53806fff183b09cbaf3e2567910c6331f48ab28f5cd80392ef44ed53a2a88.jpg`

Neo4j：
- 命中节点：chord:maj9, color:lush_ambient_texture, voicing:open_string_maj9_cluster
- 关系样例：`tuning:DAEAC#E` -[ENABLES]- `voicing:open_string_maj9_cluster`
- 关系样例：`voicing:open_string_maj9_cluster` -[ENABLES]- `tuning:DAEAC#E`
- 关系样例：`chord:maj9` -[EVOKES]- `color:lush_ambient_texture`
