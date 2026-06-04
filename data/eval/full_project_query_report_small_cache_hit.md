# Retrieval Bundle 小规模评测

- 生成时间：2026-06-02 01:57:44
- 测试数：4
- Bundle 通过率：4/4 (100.0%)
- 文本 Top1 准确率：75.0%
- 文本 Recall@5：100.0%
- 文本 Precision@5 平均：0.85
- 视觉 Top1 准确率：100.0%
- 视觉 Recall@5：100.0%
- 视觉 Precision@5 平均：1.00
- Neo4j 预期节点命中率：100.0%
- 总耗时：0.62s
- 单条平均耗时：0.16s
- 文本平均耗时：0.02s
- 视觉平均耗时：0.05s
- Neo4j 平均耗时：0.11s
- Embedding 缓存：309 条，路径 `D:\Guitar Arrangement Inspiration Agent\KGraphRag2\data\cache\embeddings.sqlite`

## 总览

| 用例 | 文本Top1 | 文本R@5 | 视觉Top1 | 视觉R@5 | KG | Bundle | 耗时 |
|---|---:|---:|---:|---:|---:|---:|---:|
| whole_funk_muted_chuck_space | OK | OK | n/a | n/a | OK | OK | 0.36s |
| whole_mathrock_open_string_tapping | OK | OK | OK | OK | OK | OK | 0.13s |
| whole_fretboard_triad_arpeggio | OK | OK | OK | OK | OK | OK | 0.05s |
| whole_arrangement_diagnosis_muddy_dense | MISS | OK | n/a | n/a | OK | OK | 0.08s |

## 明细

### whole_funk_muted_chuck_space

- 查询：`funk rhythm guitar sixteenth muted chuck ghost note leave space for bass drums`
- 期望文本源：cory_wong_funk_core
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=n/a，KG=OK，Bundle=OK
- 耗时：total=0.36s，text=0.06s，visual=n/a，kg=0.30s
- 缓存：text_embedding=OK，visual_embedding=n/a

文本 Top5：
1. `cory_wong_funk_core` / `chunk_0008` / dist=0.4691 /   
   let's dive deeper into that bongo conga style to me,that world of ribbon guitar playing is the bubble. now you hear this sort of thing on a lot of songs,it's classic.billy IE,Jean,
2. `cory_wong_funk_core` / `chunk_0012` / dist=0.4693 /   
   another one of my signature guitar moves is this sort of thing.that sort of thing you hear me do that all the time now part of how I get that sound obviously it's double strokes it
3. `cory_wong_funk_core` / `chunk_0011` / dist=0.4842 /   
   one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accompl
4. `cory_wong_funk_core` / `chunk_0004` / dist=0.5146 /   
   that's just actually articulating and playing a different type of phrasing on it,but it's one way to use that voicing.嗯。minor seven chords are super common in funk music and especi
5. `cory_wong_funk_core` / `chunk_0009` / dist=0.5297 /   
   now something to really note is.there's a difference between timing.patterns.and groove.they all kind of make up this thing that we call ribbon.那timing is。where you're placing some

Neo4j：
- 命中节点：heuristic:leave_space_for_band, feature:muted_chuck_density, feature:sixteenth_note_undercurrent
- 关系样例：`voicing:sparse_funk_voicing` -[ENABLES]- `heuristic:leave_space_for_band`
- 关系样例：`heuristic:leave_space_for_band` -[ENABLES]- `voicing:sparse_funk_voicing`
- 关系样例：`voicing:sparse_funk_voicing` -[ENABLES]- `heuristic:leave_space_for_band`

### whole_mathrock_open_string_tapping

- 查询：`math rock open string drone tapping riff clean wide interval texture`
- 期望文本源：mathrock_pdf_steve_h, mathrock_text_course
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=0.13s，text=0.01s，visual=0.09s，kg=0.03s
- 缓存：text_embedding=OK，visual_embedding=OK

文本 Top5：
1. `mathrock_text_course` / `chunk_0001` / dist=0.3588 /   
   so what are the basics of math rock or midwest emo we're going to take a look at this little progression right here which is in the key of dd major,and i have it in a very common a
2. `mathrock_text_course` / `chunk_0002` / dist=0.3757 /   
   all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered ar
3. `mathrock_text_course` / `chunk_0006` / dist=0.3999 /   
   what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique
4. `mathrock_text_course` / `chunk_0003` / dist=0.4051 /   
   math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shoo
5. `mathrock_text_course` / `chunk_0005` / dist=0.4362 /   
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
- 期望文本源：fretboard_handbook_mineru
- 期望视觉：P2_arpeggios_chords
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=0.05s，text=0.01s，visual=0.01s，kg=0.03s
- 缓存：text_embedding=OK，visual_embedding=OK

文本 Top5：
1. `fretboard_handbook_mineru` / `chunk_0008` / dist=0.2443 /   
   ## 小三和弦琵音 小三和弦是由根音、根音上方的小三度音和纯五度音组成的：1、b3、5。 ## 练习31 构建D小三和弦琶音的五种指型。注意不要用品位标记以下的音符，并且在画出音符时，保证所有的音符都在左手所在的把位以内，最多不要超出1品以外。 1)D小三和弦琶音 V [IMAGE_BLOCK:images/f09a862e2cade2cfda3e9353a
2. `fretboard_handbook_mineru` / `chunk_0009` / dist=0.2998 /   
   ## 第15章 七和弦琶音 学习目标：在指板上构建七和弦的琶音。 七和弦是学习三和弦之后的进阶，每个七和弦包含四个音。首先，还是先来学习七和弦的琶音，之后再来学习七和弦。七和弦琶音之间的音程关系和三和弦是相似的。 ## 大七和弦 在大三和弦的基础上增加一个大七度音就形成了大七和弦，其音符为：1、3、5和7。表示大七和弦的标记有以下几种：Cmaj7，Cma7，
3. `fretboard_handbook_mineru` / `chunk_0007` / dist=0.3328 /   
   ## 练习26 按照图示中给出的音程和音符画出另外的音符。可先找到大音程或者纯音程，然后在需要的时候利用增、减的方法确定音符的位置。当同一个音程可以找到不同的音符时，把这些音符都标出来。第一个图示已经给出答案作为参考。 [IMAGE_BLOCK:images/25b8493f9159d471045a9c3bb03270a1c97732433c3b1bb0cb
4. `fretboard_handbook_mineru` / `chunk_0013` / dist=0.3461 /   
   ## 分割（Slash）和弦 分割和弦就是将三和弦或七和弦叠加在一个非和弦根音的低音上。这种和弦可以用这种方式来表达：C/D。当这个低音也是和弦中的音时，分割和弦就变成了一种和弦转位。否则，分割和弦就是延伸和弦或者变化和弦的一种声部构成。 ## 练习59 在下面的图示中画出 Slash 和弦。 [IMAGE_BLOCK:images/323a85babce1
5. `fretboard_handbook_mineru` / `chunk_0012` / dist=0.3524 /   
   ## 练习52 用以上所学习的三步寻找Ionian的方法，填写下面的空格。 1.BMixolydian=Ionian从B到B 6.GLocrian Ionian从G到G 2. CLydian = Ionian从C到C 7. A Phrygian Ionian从A到A 3.EDorian Ionian从E到E 8.FDorian Ionian从F到F 4.A 

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
- 期望文本源：cory_wong_funk_core, mathrock_pdf_steve_h
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=n/a，KG=OK，Bundle=OK
- 耗时：total=0.08s，text=0.01s，visual=n/a，kg=0.07s
- 缓存：text_embedding=OK，visual_embedding=n/a

文本 Top5：
1. `mathrock_text_course` / `chunk_0005` / dist=0.4650 /   
   we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have A
2. `mathrock_text_course` / `chunk_0007` / dist=0.4751 /   
   we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can 
3. `cory_wong_funk_core` / `chunk_0012` / dist=0.4811 /   
   another one of my signature guitar moves is this sort of thing.that sort of thing you hear me do that all the time now part of how I get that sound obviously it's double strokes it
4. `mathrock_text_course` / `chunk_0002` / dist=0.4856 /   
   all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered ar
5. `cory_wong_funk_core` / `chunk_0010` / dist=0.4879 /   
   now those are a couple of my main approaches to ribbon guitar,but some other things just to consider are ribbon IC density.range on the instrument.tone.and space.OK so.sometimes a 

Neo4j：
- 命中节点：heuristic:leave_space_for_band, voicing:sparse_funk_voicing, caution:low_string_sympathetic_resonance
- 关系样例：`voicing:sparse_funk_voicing` -[ENABLES]- `heuristic:leave_space_for_band`
- 关系样例：`heuristic:leave_space_for_band` -[ENABLES]- `voicing:sparse_funk_voicing`
- 关系样例：`voicing:sparse_funk_voicing` -[ENABLES]- `heuristic:leave_space_for_band`
