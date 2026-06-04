# Retrieval Bundle 小规模评测

- 生成时间：2026-06-02 19:33:05
- 检索模式：`global`
- CLI primary sources：n/a
- 测试数：4
- Bundle 通过率：4/4 (100.0%)
- 文本 Top1 准确率：100.0%
- 文本 Recall@5：100.0%
- 文本 Precision@5 平均：0.90
- 视觉 Top1 准确率：100.0%
- 视觉 Recall@5：100.0%
- 视觉 Precision@5 平均：1.00
- Neo4j 预期节点命中率：100.0%
- 总耗时：5.77s
- 单条平均耗时：1.44s
- 文本平均耗时：1.29s
- 视觉平均耗时：0.06s
- Neo4j 平均耗时：0.12s
- Embedding 缓存：316 条，路径 `D:\Guitar Arrangement Inspiration Agent\KGraphRag2\data\cache\embeddings.sqlite`

## 总览

| 用例 | 文本Top1 | 文本R@5 | 视觉Top1 | 视觉R@5 | KG | Bundle | 耗时 |
|---|---:|---:|---:|---:|---:|---:|---:|
| whole_funk_muted_chuck_space | OK | OK | n/a | n/a | OK | OK | 5.36s |
| whole_mathrock_open_string_tapping | OK | OK | OK | OK | OK | OK | 0.20s |
| whole_fretboard_triad_arpeggio | OK | OK | OK | OK | OK | OK | 0.13s |
| whole_arrangement_diagnosis_muddy_dense | OK | OK | n/a | n/a | OK | OK | 0.08s |

## 明细

### whole_funk_muted_chuck_space

- 查询：`funk rhythm guitar sixteenth muted chuck ghost note leave space for bass drums`
- 检索模式：`global`
- Primary sources：n/a
- 期望文本源：cory_wong_funk_core
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=n/a，KG=OK，Bundle=OK
- 耗时：total=5.36s，text=4.98s，visual=n/a，kg=0.38s
- 缓存：text_embedding=MISS，visual_embedding=n/a

文本 Top5：
1. `cory_wong_funk_core` / `chunk_0012` / dist=0.2233 /   
   another one of my signature guitar moves is this sort of thing.that sort of thing you hear me do that all the time now part of how I get that sound obviously it's double strokes it
2. `cory_wong_funk_core` / `chunk_0008` / dist=0.2247 /   
   let's dive deeper into that bongo conga style to me,that world of ribbon guitar playing is the bubble. now you hear this sort of thing on a lot of songs,it's classic.billy IE,Jean,
3. `cory_wong_funk_core` / `chunk_0010` / dist=0.2340 /   
   now those are a couple of my main approaches to ribbon guitar,but some other things just to consider are ribbon IC density.range on the instrument.tone.and space.OK so.sometimes a 
4. `cory_wong_funk_core` / `chunk_0011` / dist=0.2396 /   
   one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accompl
5. `cory_wong_funk_core` / `chunk_0009` / dist=0.2486 /   
   now something to really note is.there's a difference between timing.patterns.and groove.they all kind of make up this thing that we call ribbon.那timing is。where you're placing some

Neo4j：
- 命中节点：heuristic:leave_space_for_band, feature:muted_chuck_density, feature:sixteenth_note_undercurrent
- 关系样例：`voicing:sparse_funk_voicing` -[ENABLES]- `heuristic:leave_space_for_band`
- 关系样例：`heuristic:leave_space_for_band` -[ENABLES]- `voicing:sparse_funk_voicing`
- 关系样例：`voicing:sparse_funk_voicing` -[ENABLES]- `heuristic:leave_space_for_band`

### whole_mathrock_open_string_tapping

- 查询：`math rock open string drone tapping riff clean wide interval texture`
- 检索模式：`global`
- Primary sources：n/a
- 期望文本源：mathrock_pdf_steve_h, mathrock_text_course
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=0.20s，text=0.06s，visual=0.11s，kg=0.03s
- 缓存：text_embedding=MISS，visual_embedding=OK

文本 Top5：
1. `mathrock_text_course` / `chunk_0003` / dist=0.2286 /   
   math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shoo
2. `mathrock_text_course` / `chunk_0002` / dist=0.2397 /   
   all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered ar
3. `mathrock_text_course` / `chunk_0007` / dist=0.2456 /   
   we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can 
4. `mathrock_text_course` / `chunk_0006` / dist=0.2510 /   
   what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique
5. `mathrock_text_course` / `chunk_0005` / dist=0.2545 /   
   we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have A

视觉 Top5：
- 推断 priority：P1_scales_intervals
1. `None` / page=77 / dist=0.4381 / rerank=0.7500 /   
   `data\processed\mathrock\pdf_mineru\Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans\auto\images\7e00ec5ecaeefdeb5c6ddb2c2b1754892f7829606b7ae1bfbee5092cc460c008.jpg`
2. `None` / page=77 / dist=0.4674 / rerank=0.7500 /   
   `data\processed\mathrock\pdf_mineru\Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans\auto\images\f9c4d79826ed121574f604ea4b24497e5f6ef828400975d1ba24056ae77f235a.jpg`
3. `None` / page=33 / dist=0.4755 / rerank=0.7500 /   
   `data\processed\mathrock\pdf_mineru\Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans\auto\images\9c7b977e0ff2ccf9e6a705e4351ab4f298c674e9bb006a4fceb98145a441aa4b.jpg`
4. `None` / page=20 / dist=0.4170 / rerank=0.5000 / ⼿指控制+拨弦和弦 | 情境化指弹练习  
   `data\processed\mathrock\pdf_mineru\Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans\auto\images\b7797b8676eef652b7d4e802d3176ad5c5ef7d0019046c882d9a95fb00c39877.jpg`
5. `None` / page=25 / dist=0.4368 / rerank=0.5000 / 练习3.f在先前练习基础上扩展，结合拨⽚与双指拨弦技巧，并在最后⼩节加入全部三根备⽤⼿指的运⽤ | 练习3.g演⽰如何仅⽤混合拨弦技术组合两个音符，创造新颖乐思 | 混合拨弦技巧与⼒量发展的情境化练习  
   `data\processed\mathrock\pdf_mineru\Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans\auto\images\67b2ebfdbc78a35c746c708a30dba26a18c2568b2811afbcc146b28062334eee.jpg`

Neo4j：
- 命中节点：feature:open_string_drone, technique:two_hand_tapping, pattern:wide_interval_leap_utilization
- 关系样例：`tuning:DADGAD` -[ENABLES]- `feature:open_string_drone`
- 关系样例：`feature:open_string_drone` -[ENABLES]- `tuning:DADGAD`
- 关系样例：`feature:open_string_drone` -[SUGGESTS]- `heuristic:common_tone_anchor`

### whole_fretboard_triad_arpeggio

- 查询：`大三和弦 琶音 指型 根音 major triad arpeggio fretboard`
- 检索模式：`global`
- Primary sources：n/a
- 期望文本源：fretboard_handbook_mineru
- 期望视觉：P2_arpeggios_chords
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=0.13s，text=0.06s，visual=0.02s，kg=0.05s
- 缓存：text_embedding=MISS，visual_embedding=OK

文本 Top5：
1. `fretboard_handbook_mineru` / `md_chunk_0021` / dist=0.2181 /   
   ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个
2. `fretboard_handbook_mineru` / `md_chunk_0037` / dist=0.2987 /   
   ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他
3. `fretboard_handbook_mineru` / `md_chunk_0002` / dist=0.3003 /   
   ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果
4. `fretboard_handbook_mineru` / `md_chunk_0008` / dist=0.3165 /   
   ## 第8章 自然小调音阶 学习目标：构建自然小调音阶的五种指型。理解关系小调和关系大调。 大调音阶只有一种构建公式，但对于小调音阶来说却有许多种构建方式，每一种都有它自己的公式。当人们提到“小调音阶”时，首先想到的应该是自然小调音阶。下面是它的构建公式（大声地读出来）： ## “全、半、全、全、半、全、全” 2级音和3级音之间、5级音和6级音之间是半音关系
5. `fretboard_handbook_mineru` / `md_chunk_0001` / dist=0.3205 /   
   [IMAGE_BLOCK:images/8b7ba2f10bcaab55ce9201207558dc26f0f3bd7d10ba53803cf9777452bbd505.jpg] [IMAGE_BLOCK:images/02959d5afc23bcd298aba62bc77aa210b94bfadeb6686e3d159117940e4cf8e5.jpg] 

视觉 Top5：
- 推断 priority：P2_arpeggios_chords, P0_root_fingering_forms
1. `P2_arpeggios_chords` / page=48 / dist=0.4982 / rerank=17.7500 / 大三和弦 | 练习34 | 小三和弦 | 练习35  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\3473ccf4b0ddca16337f75a8662133621b1216ba3dfbf85b814b6a8b5475be1c.jpg`
2. `P2_arpeggios_chords` / page=48 / dist=0.5005 / rerank=17.7500 / 大三和弦 | 练习34 | 小三和弦 | 练习35  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\009e1d43b54dfbb636e9b9a7cc6e2b351320257ed9a587bf454dde2c17df36c7.jpg`
3. `P2_arpeggios_chords` / page=49 / dist=0.4973 / rerank=17.5000 / 减三和弦 | 练习36 | 增三和弦 | 练习37  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\cca58c83e81e9167c7a622a30b0e81bc3f4613f91394affc899c46d81d9e69ea.jpg`
4. `P2_arpeggios_chords` / page=50 / dist=0.4815 / rerank=17.0000 / 转位 | 练习  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\524e93470084f0cfb5adfd9a350701f856930f7a00d296466de4f938038c33af.jpg`
5. `P2_arpeggios_chords` / page=47 / dist=0.5047 / rerank=17.0000 / 第14章 三和弦  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\3f5d0bc1badfed39b798af4bec9ca590df3e86cbdbddcbb96c5cc904f2e803a7.jpg`

Neo4j：
- 命中节点：chord:aug_triad, chord:major_triad, chord:triad_inversions, pattern:caged_system_shapes
- Alias 扩展：chord:major_triad, chord:triad_inversions, pattern:caged_system_shapes, chord:aug_triad
- 关系样例：`chord:aug_triad` -[ENABLES]- `pattern:symmetric_fingering`
- 关系样例：`pattern:symmetric_fingering` -[ENABLES]- `chord:aug_triad`
- 关系样例：`chord:triad_inversions` -[SUGGESTS]- `heuristic:caged_system_mobility`

### whole_arrangement_diagnosis_muddy_dense

- 查询：`guitar arrangement too dense muddy low strings need sparse voicing and muting advice`
- 检索模式：`global`
- Primary sources：n/a
- 期望文本源：cory_wong_funk_core, mathrock_pdf_steve_h
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=n/a，KG=OK，Bundle=OK
- 耗时：total=0.08s，text=0.05s，visual=n/a，kg=0.03s
- 缓存：text_embedding=MISS，visual_embedding=n/a

文本 Top5：
1. `cory_wong_funk_core` / `chunk_0010` / dist=0.1747 /   
   now those are a couple of my main approaches to ribbon guitar,but some other things just to consider are ribbon IC density.range on the instrument.tone.and space.OK so.sometimes a 
2. `mathrock_text_course` / `chunk_0007` / dist=0.2113 /   
   we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can 
3. `mathrock_text_course` / `chunk_0003` / dist=0.2138 /   
   math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shoo
4. `cory_wong_funk_core` / `chunk_0008` / dist=0.2168 /   
   let's dive deeper into that bongo conga style to me,that world of ribbon guitar playing is the bubble. now you hear this sort of thing on a lot of songs,it's classic.billy IE,Jean,
5. `cory_wong_funk_core` / `chunk_0012` / dist=0.2216 /   
   another one of my signature guitar moves is this sort of thing.that sort of thing you hear me do that all the time now part of how I get that sound obviously it's double strokes it

Neo4j：
- 命中节点：heuristic:leave_space_for_band, voicing:sparse_funk_voicing, caution:low_string_sympathetic_resonance
- 关系样例：`voicing:sparse_funk_voicing` -[ENABLES]- `heuristic:leave_space_for_band`
- 关系样例：`heuristic:leave_space_for_band` -[ENABLES]- `voicing:sparse_funk_voicing`
- 关系样例：`voicing:sparse_funk_voicing` -[ENABLES]- `heuristic:leave_space_for_band`
