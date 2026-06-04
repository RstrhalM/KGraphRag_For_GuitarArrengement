# Retrieval Bundle 小规模评测

- 生成时间：2026-06-02 01:52:10
- 测试数：3
- Bundle 通过率：2/3 (66.7%)
- 文本 Top1 准确率：33.3%
- 文本 Recall@5：66.7%
- 文本 Precision@5 平均：0.27
- 视觉 Top1 准确率：100.0%
- 视觉 Recall@5：100.0%
- 视觉 Precision@5 平均：1.00
- Neo4j 预期节点命中率：100.0%
- 总耗时：256.32s
- 单条平均耗时：85.44s
- 文本平均耗时：42.53s
- 视觉平均耗时：42.50s
- Neo4j 平均耗时：0.41s
- Embedding 缓存：303 条，路径 `D:\Guitar Arrangement Inspiration Agent\KGraphRag2\data\cache\embeddings.sqlite`

## 总览

| 用例 | 文本Top1 | 文本R@5 | 视觉Top1 | 视觉R@5 | KG | Bundle | 耗时 |
|---|---:|---:|---:|---:|---:|---:|---:|
| pdf_tapping_simultaneous_rhythm_lead | MISS | OK | OK | OK | OK | OK | 86.29s |
| pdf_facgce_open_string_voicing | OK | OK | OK | OK | OK | OK | 85.02s |
| pdf_clean_maj9_ambient_texture | MISS | MISS | OK | OK | OK | MISS | 85.01s |

## 明细

### pdf_tapping_simultaneous_rhythm_lead

- 查询：`math rock two hand tapping simultaneous rhythm and lead clean solo guitar arrangement`
- 期望文本源：mathrock_pdf_steve_h
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=86.29s，text=42.59s，visual=42.52s，kg=1.18s
- 缓存：text_embedding=MISS，visual_embedding=MISS

文本 Top5：
1. `mathrock_text_course` / `chunk_0002` / dist=0.4146 /   
   all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered ar
2. `mathrock_text_course` / `chunk_0003` / dist=0.4264 /   
   math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shoo
3. `mathrock_text_course` / `chunk_0001` / dist=0.4428 /   
   so what are the basics of math rock or midwest emo we're going to take a look at this little progression right here which is in the key of dd major,and i have it in a very common a
4. `mathrock_text_course` / `chunk_0006` / dist=0.4656 /   
   what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique
5. `mathrock_pdf_steve_h` / `md_chunk_0003` / dist=0.4682 /   
   ## 双⼿点弦与交替⼿指点弦 双⼿点弦主要包括交替点弦（双⼿轮流击弦），这可能是数学摇滚吉他⼿最常⽤的点弦技法。但有时你也会需要双⼿同步点奏音符，或⽤按弦⼿凭空锤音并保持音符以构建功能性和声（如⻉斯线）。以下范例（练习1.d）节选⾃我改编的《圣诞⽼人进城》曲谱。为清晰起⻅我将两个声部分开记谱，但实际需同步点奏。我发现让⼤脑同时处理两个点弦音符要困难得多。亲⾃

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
- 期望文本源：mathrock_pdf_steve_h
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=85.02s，text=42.47s，visual=42.53s，kg=0.03s
- 缓存：text_embedding=MISS，visual_embedding=MISS

文本 Top5：
1. `mathrock_pdf_steve_h` / `md_chunk_0010` / dist=0.2947 /   
   41cd24f5b6f41b5b7538cdc609862439798fcbc01c6d8d548d9d4c21e6.jpg] 更多FACGCE和弦与进⾏3： [IMAGE_BLOCK:images/9c7b977e0ff2ccf9e6a705e4351ab4f298c674e9bb006a4fceb98145a441aa4b.jpg] FACGCE调弦的⼤
2. `mathrock_text_course` / `chunk_0002` / dist=0.3863 /   
   all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered ar
3. `mathrock_pdf_steve_h` / `md_chunk_0007` / dist=0.3865 /   
   ## 1.D - 非标准调弦法 （乐理新⼿？本节涉及专业术语与知识，建议先完成第2章学习再继续本段内容） 在数学摇滚⻛格中，非标准调弦极为常⻅。这指的是我们采⽤除标准调弦EADGCE之外的任何调弦方式。本节将重点探讨其中两种主流调弦法：它们音色出众、激发灵感，最重要的是充满演奏乐趣！但挑战在于，你会失去对指板位置的熟悉感原有的和弦指型、琶音、音阶等知识在不同
4. `mathrock_text_course` / `chunk_0001` / dist=0.3870 /   
   so what are the basics of math rock or midwest emo we're going to take a look at this little progression right here which is in the key of dd major,and i have it in a very common a
5. `mathrock_pdf_steve_h` / `md_chunk_0009` / dist=0.3943 /   
   ## 特殊调弦技巧指南： 琴弦规格 - 我们许多人都有⼀个疑问："不同调弦方式是否需要更换单根琴弦的规格？" 以下是我的建议： 若只是短期调整或仅将某些琴弦升降⼀个全音（例如标准调弦时E弦升到F，D弦降到C，B弦升到E，像FACGCE调弦法那样），建议直接使⽤标准调弦时的琴弦规格。这种情况不会对琴颈造成损害，也不会影响演奏。 若计划⻓期或永久改⽤某种特殊调弦

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
- 期望文本源：mathrock_pdf_steve_h
- 期望视觉：n/a
- 结果：文本R@5=MISS，视觉R@5=OK，KG=OK，Bundle=MISS
- 耗时：total=85.01s，text=42.54s，visual=42.45s，kg=0.03s
- 缓存：text_embedding=MISS，visual_embedding=MISS

文本 Top5：
1. `mathrock_text_course` / `chunk_0006` / dist=0.3879 /   
   what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique
2. `mathrock_text_course` / `chunk_0001` / dist=0.3896 /   
   so what are the basics of math rock or midwest emo we're going to take a look at this little progression right here which is in the key of dd major,and i have it in a very common a
3. `mathrock_text_course` / `chunk_0002` / dist=0.3931 /   
   all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered ar
4. `mathrock_text_course` / `chunk_0004` / dist=0.4608 /   
   hey hey hey,let's do it. let's do another math Rock progression. shall we so this one kind of call we have another minor shape gone on AH be min,or we have?bf shocks of one five,we
5. `mathrock_text_course` / `chunk_0005` / dist=0.4673 /   
   we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have A

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
