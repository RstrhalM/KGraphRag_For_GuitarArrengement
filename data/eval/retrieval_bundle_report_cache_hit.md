# Retrieval Bundle 小规模评测

- 生成时间：2026-06-01 12:32:16
- 测试数：22
- Bundle 通过率：22/22 (100.0%)
- 文本 Top1 准确率：100.0%
- 文本 Recall@5：100.0%
- 文本 Precision@5 平均：1.00
- 视觉 Top1 准确率：100.0%
- 视觉 Recall@5：100.0%
- 视觉 Precision@5 平均：1.00
- Neo4j 预期节点命中率：100.0%
- 总耗时：1.31s
- 单条平均耗时：0.06s
- 文本平均耗时：0.01s
- 视觉平均耗时：0.01s
- Neo4j 平均耗时：0.05s
- Embedding 缓存：32 条，路径 `D:\Guitar Arrangement Inspiration Agent\KGraphRag2\data\cache\embeddings.sqlite`

## 总览

| 用例 | 文本Top1 | 文本R@5 | 视觉Top1 | 视觉R@5 | KG | Bundle | 耗时 |
|---|---:|---:|---:|---:|---:|---:|---:|
| funk_muted_chuck | OK | OK | n/a | n/a | OK | OK | 0.41s |
| funk_upstroke_downstroke | OK | OK | n/a | n/a | OK | OK | 0.05s |
| funk_sparse_voicing_space | OK | OK | n/a | n/a | OK | OK | 0.03s |
| funk_section_energy | OK | OK | n/a | n/a | OK | OK | 0.04s |
| mathrock_dadgad_open_strings | OK | OK | n/a | n/a | OK | OK | 0.04s |
| mathrock_alternate_tuning | OK | OK | n/a | n/a | OK | OK | 0.03s |
| mathrock_tapping_power_chord | OK | OK | n/a | n/a | OK | OK | 0.04s |
| mathrock_non_diatonic_passing | OK | OK | n/a | n/a | OK | OK | 0.04s |
| fretboard_root_fingering_forms | OK | OK | OK | OK | OK | OK | 0.07s |
| fretboard_intervals_octave | OK | OK | OK | OK | OK | OK | 0.05s |
| fretboard_triad_arpeggio | OK | OK | OK | OK | OK | OK | 0.04s |
| fretboard_common_chords_6_9 | OK | OK | OK | OK | OK | OK | 0.05s |
| funk_ghost_note_left_hand_muting | OK | OK | n/a | n/a | OK | OK | 0.03s |
| funk_timing_groove_density | OK | OK | n/a | n/a | OK | OK | 0.03s |
| mathrock_open_string_drone_odd_meter | OK | OK | n/a | n/a | OK | OK | 0.03s |
| mathrock_dyad_pull_off_open_string | OK | OK | n/a | n/a | OK | OK | 0.03s |
| fretboard_root_octave_ambiguous | OK | OK | OK | OK | OK | OK | 0.10s |
| fretboard_perfect_fifth_power_chord_interval | OK | OK | OK | OK | OK | OK | 0.03s |
| fretboard_caged_major_triad_shapes | OK | OK | OK | OK | OK | OK | 0.05s |
| fretboard_add9_not_dom9 | OK | OK | OK | OK | OK | OK | 0.04s |
| fretboard_pentatonic_two_notes_per_string | OK | OK | OK | OK | OK | OK | 0.05s |
| fretboard_root_pattern_cycle_overlap | OK | OK | OK | OK | OK | OK | 0.03s |

## 明细

### funk_muted_chuck

- 查询：`funk rhythm guitar sixteenth note muted chuck bubble groove`
- 期望文本源：cory_wong_funk_core
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=n/a，KG=OK，Bundle=OK
- 耗时：total=0.41s，text=0.05s，visual=n/a，kg=0.36s
- 缓存：text_embedding=OK，visual_embedding=n/a

文本 Top5：
1. `cory_wong_funk_core` / `chunk_0008` / dist=0.3708 /   
   let's dive deeper into that bongo conga style to me,that world of ribbon guitar playing is the bubble. now you hear this sort of thing on a lot of songs,it's classic.billy IE,Jean,
2. `cory_wong_funk_core` / `chunk_0011` / dist=0.5006 /   
   one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accompl
3. `cory_wong_funk_core` / `chunk_0009` / dist=0.5016 /   
   now something to really note is.there's a difference between timing.patterns.and groove.they all kind of make up this thing that we call ribbon.那timing is。where you're placing some
4. `cory_wong_funk_core` / `chunk_0012` / dist=0.5185 /   
   another one of my signature guitar moves is this sort of thing.that sort of thing you hear me do that all the time now part of how I get that sound obviously it's double strokes it
5. `cory_wong_funk_core` / `chunk_0004` / dist=0.5432 /   
   that's just actually articulating and playing a different type of phrasing on it,but it's one way to use that voicing.嗯。minor seven chords are super common in funk music and especi

Neo4j：
- 命中节点：feature:muted_chuck_density, feature:sixteenth_note_undercurrent, feature:staccato_bubble
- 关系样例：`technique:caged_system_fragmentation` -[ENABLES]- `feature:staccato_bubble`
- 关系样例：`feature:staccato_bubble` -[ENABLES]- `technique:caged_system_fragmentation`
- 关系样例：`feature:staccato_bubble` -[ENABLES]- `heuristic:make_rhythm_part_a_hook`

### funk_upstroke_downstroke

- 查询：`upstroke hit downstroke muted strings funk rhythm guitar`
- 期望文本源：cory_wong_funk_core
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=n/a，KG=OK，Bundle=OK
- 耗时：total=0.05s，text=0.01s，visual=n/a，kg=0.04s
- 缓存：text_embedding=OK，visual_embedding=n/a

文本 Top5：
1. `cory_wong_funk_core` / `chunk_0011` / dist=0.3066 /   
   one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accompl
2. `cory_wong_funk_core` / `chunk_0012` / dist=0.4038 /   
   another one of my signature guitar moves is this sort of thing.that sort of thing you hear me do that all the time now part of how I get that sound obviously it's double strokes it
3. `cory_wong_funk_core` / `chunk_0008` / dist=0.5289 /   
   let's dive deeper into that bongo conga style to me,that world of ribbon guitar playing is the bubble. now you hear this sort of thing on a lot of songs,it's classic.billy IE,Jean,
4. `cory_wong_funk_core` / `chunk_0009` / dist=0.5458 /   
   now something to really note is.there's a difference between timing.patterns.and groove.they all kind of make up this thing that we call ribbon.那timing is。where you're placing some
5. `cory_wong_funk_core` / `chunk_0004` / dist=0.5569 /   
   that's just actually articulating and playing a different type of phrasing on it,but it's one way to use that voicing.嗯。minor seven chords are super common in funk music and especi

Neo4j：
- 命中节点：technique:upstroke_hit_downstroke, technique:left_hand_muting
- 关系样例：`technique:upstroke_hit_downstroke` -[ENABLES]- `feature:percussive_ghost_note`
- 关系样例：`feature:percussive_ghost_note` -[ENABLES]- `technique:upstroke_hit_downstroke`
- 关系样例：`technique:upstroke_hit_downstroke` -[SUGGESTS]- `feature:sixteenth_note_undercurrent`

### funk_sparse_voicing_space

- 查询：`funk rhythm guitar sparse voicing leave space for bass drums keys horns`
- 期望文本源：cory_wong_funk_core
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=n/a，KG=OK，Bundle=OK
- 耗时：total=0.03s，text=0.01s，visual=n/a，kg=0.02s
- 缓存：text_embedding=OK，visual_embedding=n/a

文本 Top5：
1. `cory_wong_funk_core` / `chunk_0003` / dist=0.4664 /   
   this next series of lessons is about cord voicings and cord moves that I use in my playing.especially,in the context of funk,music now most of these voice o icings start from the c
2. `cory_wong_funk_core` / `chunk_0004` / dist=0.4765 /   
   that's just actually articulating and playing a different type of phrasing on it,but it's one way to use that voicing.嗯。minor seven chords are super common in funk music and especi
3. `cory_wong_funk_core` / `chunk_0010` / dist=0.4788 /   
   now those are a couple of my main approaches to ribbon guitar,but some other things just to consider are ribbon IC density.range on the instrument.tone.and space.OK so.sometimes a 
4. `cory_wong_funk_core` / `chunk_0008` / dist=0.5169 /   
   let's dive deeper into that bongo conga style to me,that world of ribbon guitar playing is the bubble. now you hear this sort of thing on a lot of songs,it's classic.billy IE,Jean,
5. `cory_wong_funk_core` / `chunk_0009` / dist=0.5176 /   
   now something to really note is.there's a difference between timing.patterns.and groove.they all kind of make up this thing that we call ribbon.那timing is。where you're placing some

Neo4j：
- 命中节点：heuristic:leave_space_for_band, voicing:sparse_funk_voicing
- 关系样例：`voicing:sparse_funk_voicing` -[ENABLES]- `heuristic:leave_space_for_band`
- 关系样例：`heuristic:leave_space_for_band` -[ENABLES]- `voicing:sparse_funk_voicing`
- 关系样例：`voicing:sparse_funk_voicing` -[ENABLES]- `heuristic:leave_space_for_band`

### funk_section_energy

- 查询：`section build rhythm guitar verse chorus wider strum more velocity`
- 期望文本源：cory_wong_funk_core
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=n/a，KG=OK，Bundle=OK
- 耗时：total=0.04s，text=0.00s，visual=n/a，kg=0.04s
- 缓存：text_embedding=OK，visual_embedding=n/a

文本 Top5：
1. `cory_wong_funk_core` / `chunk_0011` / dist=0.4492 /   
   one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accompl
2. `cory_wong_funk_core` / `chunk_0009` / dist=0.4840 /   
   now something to really note is.there's a difference between timing.patterns.and groove.they all kind of make up this thing that we call ribbon.那timing is。where you're placing some
3. `cory_wong_funk_core` / `chunk_0010` / dist=0.5034 /   
   now those are a couple of my main approaches to ribbon guitar,but some other things just to consider are ribbon IC density.range on the instrument.tone.and space.OK so.sometimes a 
4. `cory_wong_funk_core` / `chunk_0008` / dist=0.5126 /   
   let's dive deeper into that bongo conga style to me,that world of ribbon guitar playing is the bubble. now you hear this sort of thing on a lot of songs,it's classic.billy IE,Jean,
5. `cory_wong_funk_core` / `chunk_0012` / dist=0.5288 /   
   another one of my signature guitar moves is this sort of thing.that sort of thing you hear me do that all the time now part of how I get that sound obviously it's double strokes it

Neo4j：
- 命中节点：heuristic:section_energy_stair_step
- 关系样例：`voicing:sparse_to_dense_layering` -[ENABLES]- `heuristic:section_energy_stair_step`
- 关系样例：`heuristic:section_energy_stair_step` -[ENABLES]- `voicing:sparse_to_dense_layering`
- 关系样例：`heuristic:section_energy_stair_step` -[SUGGESTS]- `task:rhythm_guitar_arrangement`

### mathrock_dadgad_open_strings

- 查询：`DADGAD open strings common tones tapping power chords math rock`
- 期望文本源：mathrock_text_course
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=n/a，KG=OK，Bundle=OK
- 耗时：total=0.04s，text=0.01s，visual=n/a，kg=0.03s
- 缓存：text_embedding=OK，visual_embedding=n/a

文本 Top5：
1. `mathrock_text_course` / `chunk_0001` / dist=0.2916 /   
   so what are the basics of math rock or midwest emo we're going to take a look at this little progression right here which is in the key of dd major,and i have it in a very common a
2. `mathrock_text_course` / `chunk_0002` / dist=0.3108 /   
   all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered ar
3. `mathrock_text_course` / `chunk_0003` / dist=0.3646 /   
   math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shoo
4. `mathrock_text_course` / `chunk_0006` / dist=0.4091 /   
   what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique
5. `mathrock_text_course` / `chunk_0005` / dist=0.4605 /   
   we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have A

Neo4j：
- 命中节点：feature:open_string_drone, technique:tapped_power_chord, tuning:DADGAD, feature:tapped_power_chords, feature:tapped_power_chords_melodic
- Alias 扩展：technique:tapped_power_chord, feature:tapped_power_chords, feature:tapped_power_chords_melodic
- 关系样例：`tuning:DADGAD` -[ENABLES]- `feature:movable_power_chord_shapes_top_strings`
- 关系样例：`feature:movable_power_chord_shapes_top_strings` -[ENABLES]- `tuning:DADGAD`
- 关系样例：`tuning:DADGAD` -[ENABLES]- `feature:open_string_drone`

### mathrock_alternate_tuning

- 查询：`alternate tuning movable chord shapes open string drone midwest emo`
- 期望文本源：mathrock_text_course
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=n/a，KG=OK，Bundle=OK
- 耗时：total=0.03s，text=0.01s，visual=n/a，kg=0.02s
- 缓存：text_embedding=OK，visual_embedding=n/a

文本 Top5：
1. `mathrock_text_course` / `chunk_0001` / dist=0.2657 /   
   so what are the basics of math rock or midwest emo we're going to take a look at this little progression right here which is in the key of dd major,and i have it in a very common a
2. `mathrock_text_course` / `chunk_0006` / dist=0.2979 /   
   what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique
3. `mathrock_text_course` / `chunk_0002` / dist=0.3462 /   
   all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered ar
4. `mathrock_text_course` / `chunk_0005` / dist=0.3476 /   
   we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have A
5. `mathrock_text_course` / `chunk_0003` / dist=0.3507 /   
   math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shoo

Neo4j：
- 命中节点：feature:open_string_drone
- 关系样例：`tuning:DADGAD` -[ENABLES]- `feature:open_string_drone`
- 关系样例：`feature:open_string_drone` -[ENABLES]- `tuning:DADGAD`
- 关系样例：`feature:open_string_drone` -[SUGGESTS]- `heuristic:common_tone_anchor`

### mathrock_tapping_power_chord

- 查询：`tapping power chord suspended chord math rock riff`
- 期望文本源：mathrock_text_course
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=n/a，KG=OK，Bundle=OK
- 耗时：total=0.04s，text=0.01s，visual=n/a，kg=0.03s
- 缓存：text_embedding=OK，visual_embedding=n/a

文本 Top5：
1. `mathrock_text_course` / `chunk_0003` / dist=0.3644 /   
   math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shoo
2. `mathrock_text_course` / `chunk_0002` / dist=0.3724 /   
   all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered ar
3. `mathrock_text_course` / `chunk_0001` / dist=0.4079 /   
   so what are the basics of math rock or midwest emo we're going to take a look at this little progression right here which is in the key of dd major,and i have it in a very common a
4. `mathrock_text_course` / `chunk_0006` / dist=0.4175 /   
   what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique
5. `mathrock_text_course` / `chunk_0005` / dist=0.4902 /   
   we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have A

Neo4j：
- 命中节点：technique:tapped_power_chord, feature:tapped_dyads, technique:two_hand_tapping, feature:tapped_power_chords, feature:tapped_power_chords_melodic
- Alias 扩展：technique:tapped_power_chord, feature:tapped_power_chords, feature:tapped_power_chords_melodic, technique:two_hand_tapping, feature:tapped_dyads
- 关系样例：`technique:two_hand_tapping` -[ENABLES]- `feature:tapped_power_chords`
- 关系样例：`feature:tapped_power_chords` -[ENABLES]- `technique:two_hand_tapping`
- 关系样例：`technique:two_hand_tapping` -[CAN_INSPIRE]- `feature:tapped_power_chords_melodic`

### mathrock_non_diatonic_passing

- 查询：`midwest emo chromatic passing chord jazzy non diatonic triad slide`
- 期望文本源：mathrock_text_course
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=n/a，KG=OK，Bundle=OK
- 耗时：total=0.04s，text=0.01s，visual=n/a，kg=0.04s
- 缓存：text_embedding=OK，visual_embedding=n/a

文本 Top5：
1. `mathrock_text_course` / `chunk_0001` / dist=0.3728 /   
   so what are the basics of math rock or midwest emo we're going to take a look at this little progression right here which is in the key of dd major,and i have it in a very common a
2. `mathrock_text_course` / `chunk_0002` / dist=0.3972 /   
   all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered ar
3. `mathrock_text_course` / `chunk_0006` / dist=0.3974 /   
   what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique
4. `mathrock_text_course` / `chunk_0005` / dist=0.3995 /   
   we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have A
5. `mathrock_text_course` / `chunk_0003` / dist=0.4383 /   
   math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shoo

Neo4j：
- 命中节点：color:jazzy_midwest_emo, heuristic:non_diatonic_passing_chords
- 关系样例：`heuristic:non_diatonic_passing_chords` -[SUGGESTS]- `color:jazzy_midwest_emo`
- 关系样例：`color:jazzy_midwest_emo` -[SUGGESTS]- `heuristic:non_diatonic_passing_chords`

### fretboard_root_fingering_forms

- 查询：`根音 指型 五种 root fingering form`
- 期望文本源：fretboard_handbook_mineru
- 期望视觉：P0_root_fingering_forms
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=0.07s，text=0.00s，visual=0.04s，kg=0.02s
- 缓存：text_embedding=OK，visual_embedding=OK

文本 Top5：
1. `fretboard_handbook_mineru` / `chunk_0002` / dist=0.3423 /   
   ## 练习1 在下面图示空白处用字母填上对应的琴弦名称。做题时可以不看前面的内容，凭记忆进行填写。第6弦的名称已经给出。 ⑥6④③②① [IMAGE_BLOCK:images/fe57c06be60349e91861ff8b1d5ca2233520a6df3dc06711a0d746eaa348de7e.jpg] ## 练习2 当图中包含多个品格时，需要将上
2. `fretboard_handbook_mineru` / `chunk_0012` / dist=0.3682 /   
   ## 练习52 用以上所学习的三步寻找Ionian的方法，填写下面的空格。 1.BMixolydian=Ionian从B到B 6.GLocrian Ionian从G到G 2. CLydian = Ionian从C到C 7. A Phrygian Ionian从A到A 3.EDorian Ionian从E到E 8.FDorian Ionian从F到F 4.A 
3. `fretboard_handbook_mineru` / `chunk_0005` / dist=0.3834 /   
   ## 第8章 自然小调音阶 学习目标：构建自然小调音阶的五种指型。理解关系小调和关系大调。 大调音阶只有一种构建公式，但对于小调音阶来说却有许多种构建方式，每一种都有它自己的公式。当人们提到“小调音阶”时，首先想到的应该是自然小调音阶。下面是它的构建公式（大声地读出来）： ## “全、半、全、全、半、全、全” 2级音和3级音之间、5级音和6级音之间是半音关系
4. `fretboard_handbook_mineru` / `chunk_0013` / dist=0.3897 /   
   ## 分割（Slash）和弦 分割和弦就是将三和弦或七和弦叠加在一个非和弦根音的低音上。这种和弦可以用这种方式来表达：C/D。当这个低音也是和弦中的音时，分割和弦就变成了一种和弦转位。否则，分割和弦就是延伸和弦或者变化和弦的一种声部构成。 ## 练习59 在下面的图示中画出 Slash 和弦。 [IMAGE_BLOCK:images/323a85babce1
5. `fretboard_handbook_mineru` / `chunk_0004` / dist=0.3941 /   
   ## 练习 1.每天花5分钟时间大声地念出指板上音符的名称。最好的方法是给那些你已经学过的歌曲或者乐句中的音符命名，但是也可以采用随机的音符来练习命名。所以，不要再做那种“这个手指按住这里”之类的练习了，大声地说出：“我在演奏第2弦第9品上的音符Ab音！”这个练习至少要坚持做一个星期。 2.接下来的7周时间里，每周都要着重练习一个自然音阶音符。从A音开始，每

视觉 Top5：
- 推断 priority：P0_root_fingering_forms
1. `P0_root_fingering_forms` / page=13 / dist=0.5091 / rerank=6.7500 / 练习4 | 练习5  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\af1f5dfaafd4bc331b51424c9497e14435fd6bfae20d720cef1b5b032136240b.jpg`
2. `P0_root_fingering_forms` / page=13 / dist=0.5100 / rerank=6.7500 / 练习4 | 练习5  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\27cc76634908dd1aa263d40b028c2df067a9b7cd0086cb49716815d05f9739a6.jpg`
3. `P0_root_fingering_forms` / page=13 / dist=0.5276 / rerank=6.7500 / 练习4 | 练习5  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\d502da690fe431965bb7cfbb25884f52fa71e3449b72b8a0a2c5a5d3b6a74232.jpg`
4. `P0_root_fingering_forms` / page=13 / dist=0.5282 / rerank=6.7500 / 练习4 | 练习5  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\390c9ca9c8c33fa97fafaffddd65050f4049a92d839a07cb279caac3c5049a13.jpg`
5. `P0_root_fingering_forms` / page=13 / dist=0.5364 / rerank=6.7500 / 练习4 | 练习5  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\f5458035580ef6687c4357684818cd39f2d499329404121c4b8b6e8eeef51a3b.jpg`

Neo4j：
- 命中节点：concept:five_major_scale_patterns, concept:root_pattern_cycle, concept:root_pattern_system, guitar_idiom:position_based_melodic_design, heuristic:minimize_position_shift, heuristic:power_chord_root_finding, pattern:caged_system_navigation, pattern:caged_system_shapes, pattern:interval_geometry_shift, pattern:interval_shape_shift, pattern:root_shape_1, pattern:root_shape_4
- Alias 扩展：concept:root_pattern_cycle, concept:root_pattern_system, pattern:root_shape_1, pattern:root_shape_4, heuristic:power_chord_root_finding, concept:five_major_scale_patterns, pattern:caged_system_shapes, pattern:caged_system_navigation
- 关系样例：`concept:guitar_tuning` -[CONSTRAINS]- `pattern:interval_shape_shift`
- 关系样例：`pattern:interval_shape_shift` -[CONSTRAINS]- `concept:guitar_tuning`
- 关系样例：`interval:perfect_5th` -[ENABLES]- `heuristic:power_chord_root_finding`

### fretboard_intervals_octave

- 查询：`八度 音程 指板 interval octave`
- 期望文本源：fretboard_handbook_mineru
- 期望视觉：P1_scales_intervals
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=0.05s，text=0.01s，visual=0.01s，kg=0.03s
- 缓存：text_embedding=OK，visual_embedding=OK

文本 Top5：
1. `fretboard_handbook_mineru` / `chunk_0006` / dist=0.3244 /   
   ## 练习22 回到前面的两个练习（练习20和练习21)，写出每一图形中对应的关系小调五声音阶或关系大调五声音阶，并且用方形画出关系调中的根音。 弹奏以上这些练习。对于练习20，先弹大调五声音阶，然后再弹它的关系小调五声音阶。对于练习21，先弹小调五声音阶，然后再弹其关系大调五声音阶。在弹奏之前请说出音阶名称和指型序号。 ## 第10章 大调和纯音程 学习目
2. `fretboard_handbook_mineru` / `chunk_0007` / dist=0.3777 /   
   ## 练习26 按照图示中给出的音程和音符画出另外的音符。可先找到大音程或者纯音程，然后在需要的时候利用增、减的方法确定音符的位置。当同一个音程可以找到不同的音符时，把这些音符都标出来。第一个图示已经给出答案作为参考。 [IMAGE_BLOCK:images/25b8493f9159d471045a9c3bb03270a1c97732433c3b1bb0cb
3. `fretboard_handbook_mineru` / `chunk_0002` / dist=0.4341 /   
   ## 练习1 在下面图示空白处用字母填上对应的琴弦名称。做题时可以不看前面的内容，凭记忆进行填写。第6弦的名称已经给出。 ⑥6④③②① [IMAGE_BLOCK:images/fe57c06be60349e91861ff8b1d5ca2233520a6df3dc06711a0d746eaa348de7e.jpg] ## 练习2 当图中包含多个品格时，需要将上
4. `fretboard_handbook_mineru` / `chunk_0012` / dist=0.4461 /   
   ## 练习52 用以上所学习的三步寻找Ionian的方法，填写下面的空格。 1.BMixolydian=Ionian从B到B 6.GLocrian Ionian从G到G 2. CLydian = Ionian从C到C 7. A Phrygian Ionian从A到A 3.EDorian Ionian从E到E 8.FDorian Ionian从F到F 4.A 
5. `fretboard_handbook_mineru` / `chunk_0005` / dist=0.4534 /   
   ## 第8章 自然小调音阶 学习目标：构建自然小调音阶的五种指型。理解关系小调和关系大调。 大调音阶只有一种构建公式，但对于小调音阶来说却有许多种构建方式，每一种都有它自己的公式。当人们提到“小调音阶”时，首先想到的应该是自然小调音阶。下面是它的构建公式（大声地读出来）： ## “全、半、全、全、半、全、全” 2级音和3级音之间、5级音和6级音之间是半音关系

视觉 Top5：
- 推断 priority：P1_scales_intervals
1. `P1_scales_intervals` / page=37 / dist=0.5439 / rerank=13.0000 / 纯一度 | 大二度 | 大三度 | 纯四度  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\a9aeebcb3ca3013ba8215cbd266747b7b6dc087d3e8521b1039f8898dc388e0c.jpg`
2. `P1_scales_intervals` / page=37 / dist=0.5506 / rerank=13.0000 / 纯一度 | 大二度 | 大三度 | 纯四度  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\c22f406257b38763731cc17b6a0564e099a2a5d59cb811c44777be49d02905eb.jpg`
3. `P1_scales_intervals` / page=34 / dist=0.5458 / rerank=12.2500 / 练习18 | 练习19 | 练习20  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\d189bc7ade098216ca2646aaa05d19aa749d6b282ad2b365e744bfd6fe77268d.jpg`
4. `P1_scales_intervals` / page=35 / dist=0.5528 / rerank=12.2500 / 练习21 | 练习22  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\ed691e747eb5e90158e4503d87ce95254b472f07495e5d13d4fb9c95eb00e9ad.jpg`
5. `P1_scales_intervals` / page=39 / dist=0.5625 / rerank=12.2500 / 练习24 | 练习25  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\fda2c29d65a27e594532d5907dc5c2a8b93b067fc73d189cc193602ebd5da08f.jpg`

Neo4j：
- 命中节点：interval:major_6th, interval:perfect_5th, concept:compound_interval, concept:fretboard_geometry, heuristic:fretboard_navigation_logic, heuristic:octave_symmetry_at_12th_fret, interval:octave, pattern:interval_geometry_shift, pattern:interval_shape_shift, pattern:octave_minus_one_fret, technique:octave_displacement_rule
- Alias 扩展：interval:octave, heuristic:octave_symmetry_at_12th_fret, technique:octave_displacement_rule, pattern:octave_minus_one_fret, concept:compound_interval, pattern:interval_geometry_shift, pattern:interval_shape_shift, interval:perfect_5th
- 关系样例：`concept:guitar_tuning` -[CONSTRAINS]- `pattern:interval_shape_shift`
- 关系样例：`pattern:interval_shape_shift` -[CONSTRAINS]- `concept:guitar_tuning`
- 关系样例：`interval:major_seventh` -[ENABLES]- `pattern:octave_minus_one_fret`

### fretboard_triad_arpeggio

- 查询：`大三和弦 琶音 指型 根音 major triad arpeggio`
- 期望文本源：fretboard_handbook_mineru
- 期望视觉：P2_arpeggios_chords
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=0.04s，text=0.01s，visual=0.01s，kg=0.03s
- 缓存：text_embedding=OK，visual_embedding=OK

文本 Top5：
1. `fretboard_handbook_mineru` / `chunk_0008` / dist=0.2514 /   
   ## 小三和弦琵音 小三和弦是由根音、根音上方的小三度音和纯五度音组成的：1、b3、5。 ## 练习31 构建D小三和弦琶音的五种指型。注意不要用品位标记以下的音符，并且在画出音符时，保证所有的音符都在左手所在的把位以内，最多不要超出1品以外。 1)D小三和弦琶音 V [IMAGE_BLOCK:images/f09a862e2cade2cfda3e9353a
2. `fretboard_handbook_mineru` / `chunk_0009` / dist=0.3205 /   
   ## 第15章 七和弦琶音 学习目标：在指板上构建七和弦的琶音。 七和弦是学习三和弦之后的进阶，每个七和弦包含四个音。首先，还是先来学习七和弦的琶音，之后再来学习七和弦。七和弦琶音之间的音程关系和三和弦是相似的。 ## 大七和弦 在大三和弦的基础上增加一个大七度音就形成了大七和弦，其音符为：1、3、5和7。表示大七和弦的标记有以下几种：Cmaj7，Cma7，
3. `fretboard_handbook_mineru` / `chunk_0007` / dist=0.3447 /   
   ## 练习26 按照图示中给出的音程和音符画出另外的音符。可先找到大音程或者纯音程，然后在需要的时候利用增、减的方法确定音符的位置。当同一个音程可以找到不同的音符时，把这些音符都标出来。第一个图示已经给出答案作为参考。 [IMAGE_BLOCK:images/25b8493f9159d471045a9c3bb03270a1c97732433c3b1bb0cb
4. `fretboard_handbook_mineru` / `chunk_0012` / dist=0.3687 /   
   ## 练习52 用以上所学习的三步寻找Ionian的方法，填写下面的空格。 1.BMixolydian=Ionian从B到B 6.GLocrian Ionian从G到G 2. CLydian = Ionian从C到C 7. A Phrygian Ionian从A到A 3.EDorian Ionian从E到E 8.FDorian Ionian从F到F 4.A 
5. `fretboard_handbook_mineru` / `chunk_0013` / dist=0.3727 /   
   ## 分割（Slash）和弦 分割和弦就是将三和弦或七和弦叠加在一个非和弦根音的低音上。这种和弦可以用这种方式来表达：C/D。当这个低音也是和弦中的音时，分割和弦就变成了一种和弦转位。否则，分割和弦就是延伸和弦或者变化和弦的一种声部构成。 ## 练习59 在下面的图示中画出 Slash 和弦。 [IMAGE_BLOCK:images/323a85babce1

视觉 Top5：
- 推断 priority：P2_arpeggios_chords, P0_root_fingering_forms
1. `P2_arpeggios_chords` / page=48 / dist=0.5181 / rerank=17.7500 / 大三和弦 | 练习34 | 小三和弦 | 练习35  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\3473ccf4b0ddca16337f75a8662133621b1216ba3dfbf85b814b6a8b5475be1c.jpg`
2. `P2_arpeggios_chords` / page=48 / dist=0.5196 / rerank=17.7500 / 大三和弦 | 练习34 | 小三和弦 | 练习35  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\009e1d43b54dfbb636e9b9a7cc6e2b351320257ed9a587bf454dde2c17df36c7.jpg`
3. `P2_arpeggios_chords` / page=49 / dist=0.5183 / rerank=17.5000 / 减三和弦 | 练习36 | 增三和弦 | 练习37  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\cca58c83e81e9167c7a622a30b0e81bc3f4613f91394affc899c46d81d9e69ea.jpg`
4. `P2_arpeggios_chords` / page=50 / dist=0.5160 / rerank=17.0000 / 转位 | 练习  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\524e93470084f0cfb5adfd9a350701f856930f7a00d296466de4f938038c33af.jpg`
5. `P2_arpeggios_chords` / page=47 / dist=0.5204 / rerank=17.0000 / 第14章 三和弦  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\3f5d0bc1badfed39b798af4bec9ca590df3e86cbdbddcbb96c5cc904f2e803a7.jpg`

Neo4j：
- 命中节点：chord:aug_triad, chord:major_triad, chord:triad_inversions, pattern:caged_system_shapes
- Alias 扩展：chord:major_triad, chord:triad_inversions, pattern:caged_system_shapes, chord:aug_triad
- 关系样例：`chord:aug_triad` -[ENABLES]- `pattern:symmetric_fingering`
- 关系样例：`pattern:symmetric_fingering` -[ENABLES]- `chord:aug_triad`
- 关系样例：`chord:triad_inversions` -[SUGGESTS]- `heuristic:caged_system_mobility`

### fretboard_common_chords_6_9

- 查询：`其他常用和弦 指型 六和弦 九和弦 add9 6/9`
- 期望文本源：fretboard_handbook_mineru
- 期望视觉：P3_common_scales_chords
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=0.05s，text=0.01s，visual=0.01s，kg=0.04s
- 缓存：text_embedding=OK，visual_embedding=OK

文本 Top5：
1. `fretboard_handbook_mineru` / `chunk_0010` / dist=0.3416 /   
   ## 练习44 运用指型2和指型5画出七和弦“1、5、7、3”常用声部构成。 [IMAGE_BLOCK:images/6e05e11e982d36687c5df5564b6bf1ef6efb314c6143bb7c6ebfe3a865bdf034.jpg] [IMAGE_BLOCK:images/c1b81c203b4a0affa11063cfd87b862
2. `fretboard_handbook_mineru` / `chunk_0013` / dist=0.3432 /   
   ## 分割（Slash）和弦 分割和弦就是将三和弦或七和弦叠加在一个非和弦根音的低音上。这种和弦可以用这种方式来表达：C/D。当这个低音也是和弦中的音时，分割和弦就变成了一种和弦转位。否则，分割和弦就是延伸和弦或者变化和弦的一种声部构成。 ## 练习59 在下面的图示中画出 Slash 和弦。 [IMAGE_BLOCK:images/323a85babce1
3. `fretboard_handbook_mineru` / `chunk_0012` / dist=0.3461 /   
   ## 练习52 用以上所学习的三步寻找Ionian的方法，填写下面的空格。 1.BMixolydian=Ionian从B到B 6.GLocrian Ionian从G到G 2. CLydian = Ionian从C到C 7. A Phrygian Ionian从A到A 3.EDorian Ionian从E到E 8.FDorian Ionian从F到F 4.A 
4. `fretboard_handbook_mineru` / `chunk_0009` / dist=0.3578 /   
   ## 第15章 七和弦琶音 学习目标：在指板上构建七和弦的琶音。 七和弦是学习三和弦之后的进阶，每个七和弦包含四个音。首先，还是先来学习七和弦的琶音，之后再来学习七和弦。七和弦琶音之间的音程关系和三和弦是相似的。 ## 大七和弦 在大三和弦的基础上增加一个大七度音就形成了大七和弦，其音符为：1、3、5和7。表示大七和弦的标记有以下几种：Cmaj7，Cma7，
5. `fretboard_handbook_mineru` / `chunk_0016` / dist=0.3688 /   
   ## 练习33 1)D增三和弦指型1 [IMAGE_BLOCK:images/e9b5e7ec9bc7597cbae8189f9771e6614100c452a02734945206b25d0ccc594d.jpg] 2）D增三和弦 指型2 [IMAGE_BLOCK:images/5a68f6f59f98ac3fc684152d7c958b740d02565

视觉 Top5：
- 推断 priority：P3_common_scales_chords
1. `P3_common_scales_chords` / page=68 / dist=0.4501 / rerank=20.5000 / 第21章 其他常用和弦 | 练习58  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\6adcb92bcf27554cc5f9bdb7c39dbcae6d5385f77864bee4163f9d3ccbb788e3.jpg`
2. `P3_common_scales_chords` / page=68 / dist=0.4594 / rerank=20.5000 / 第21章 其他常用和弦 | 练习58  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\7915644f58172e192a14dbf16a653d9b27d31c9210b2d7fe4ad37199f9085bce.jpg`
3. `P3_common_scales_chords` / page=68 / dist=0.5341 / rerank=20.5000 / 第21章 其他常用和弦 | 练习58  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\ee5c10ed920b19c453b2962073feb887d3e33c867763614b3808c08fac91d5eb.jpg`
4. `P3_common_scales_chords` / page=68 / dist=0.4650 / rerank=19.5000 / 第21章 其他常用和弦 | 练习58  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\19c70069724de5b61cb416d5281ab07e0823e87d4ec934b7dac90aef049b1ab7.jpg`
5. `P3_common_scales_chords` / page=68 / dist=0.4918 / rerank=19.5000 / 第21章 其他常用和弦 | 练习58  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\48b8d933c0ef36d4e4bc329917be9ca10970107f7f0196ba8b6b12afc610a178.jpg`

Neo4j：
- 命中节点：interval:major_6th, chord:add9, chord:6/9, chord:6_9, chord:extended_chords
- Alias 扩展：chord:6/9, chord:6_9, interval:major_6th, chord:add9, chord:extended_chords
- 关系样例：`chord:add9` -[CONFLICTS_WITH]- `chord:dom9`
- 关系样例：`chord:dom9` -[CONFLICTS_WITH]- `chord:add9`
- 关系样例：`chord:add9` -[CONFLICTS_WITH]- `chord:dominant_9th`

### funk_ghost_note_left_hand_muting

- 查询：`funk ghost note left hand muting sixteenth rhythm guitar tight groove`
- 期望文本源：cory_wong_funk_core
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=n/a，KG=OK，Bundle=OK
- 耗时：total=0.03s，text=0.01s，visual=n/a，kg=0.02s
- 缓存：text_embedding=OK，visual_embedding=n/a

文本 Top5：
1. `cory_wong_funk_core` / `chunk_0012` / dist=0.4443 /   
   another one of my signature guitar moves is this sort of thing.that sort of thing you hear me do that all the time now part of how I get that sound obviously it's double strokes it
2. `cory_wong_funk_core` / `chunk_0011` / dist=0.4742 /   
   one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accompl
3. `cory_wong_funk_core` / `chunk_0009` / dist=0.5086 /   
   now something to really note is.there's a difference between timing.patterns.and groove.they all kind of make up this thing that we call ribbon.那timing is。where you're placing some
4. `cory_wong_funk_core` / `chunk_0008` / dist=0.5445 /   
   let's dive deeper into that bongo conga style to me,that world of ribbon guitar playing is the bubble. now you hear this sort of thing on a lot of songs,it's classic.billy IE,Jean,
5. `cory_wong_funk_core` / `chunk_0004` / dist=0.5576 /   
   that's just actually articulating and playing a different type of phrasing on it,but it's one way to use that voicing.嗯。minor seven chords are super common in funk music and especi

Neo4j：
- 命中节点：feature:sixteenth_note_undercurrent, technique:left_hand_muting
- 关系样例：`technique:right_hand_constant_motion` -[ENABLES]- `feature:sixteenth_note_undercurrent`
- 关系样例：`feature:sixteenth_note_undercurrent` -[ENABLES]- `technique:right_hand_constant_motion`
- 关系样例：`technique:upstroke_hit_downstroke` -[SUGGESTS]- `feature:sixteenth_note_undercurrent`

### funk_timing_groove_density

- 查询：`funk timing groove density range tone space rhythm guitar`
- 期望文本源：cory_wong_funk_core
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=n/a，KG=OK，Bundle=OK
- 耗时：total=0.03s，text=0.00s，visual=n/a，kg=0.03s
- 缓存：text_embedding=OK，visual_embedding=n/a

文本 Top5：
1. `cory_wong_funk_core` / `chunk_0010` / dist=0.3425 /   
   now those are a couple of my main approaches to ribbon guitar,but some other things just to consider are ribbon IC density.range on the instrument.tone.and space.OK so.sometimes a 
2. `cory_wong_funk_core` / `chunk_0009` / dist=0.3590 /   
   now something to really note is.there's a difference between timing.patterns.and groove.they all kind of make up this thing that we call ribbon.那timing is。where you're placing some
3. `cory_wong_funk_core` / `chunk_0011` / dist=0.5690 /   
   one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accompl
4. `cory_wong_funk_core` / `chunk_0007` / dist=0.5714 /   
   today I want to give you a little ribbon guitar primer now I am.what I would consider a consummate ribbon guitar player I love,the ribbon guitar I love,the role and I think it's of
5. `cory_wong_funk_core` / `chunk_0008` / dist=0.5729 /   
   let's dive deeper into that bongo conga style to me,that world of ribbon guitar playing is the bubble. now you hear this sort of thing on a lot of songs,it's classic.billy IE,Jean,

Neo4j：
- 命中节点：heuristic:leave_space_for_band, feature:staccato_bubble
- 关系样例：`voicing:sparse_funk_voicing` -[ENABLES]- `heuristic:leave_space_for_band`
- 关系样例：`heuristic:leave_space_for_band` -[ENABLES]- `voicing:sparse_funk_voicing`
- 关系样例：`voicing:sparse_funk_voicing` -[ENABLES]- `heuristic:leave_space_for_band`

### mathrock_open_string_drone_odd_meter

- 查询：`math rock open string drone odd meter clean tapping riff`
- 期望文本源：mathrock_text_course
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=n/a，KG=OK，Bundle=OK
- 耗时：total=0.03s，text=0.01s，visual=n/a，kg=0.02s
- 缓存：text_embedding=OK，visual_embedding=n/a

文本 Top5：
1. `mathrock_text_course` / `chunk_0001` / dist=0.3691 /   
   so what are the basics of math rock or midwest emo we're going to take a look at this little progression right here which is in the key of dd major,and i have it in a very common a
2. `mathrock_text_course` / `chunk_0002` / dist=0.3890 /   
   all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered ar
3. `mathrock_text_course` / `chunk_0006` / dist=0.3999 /   
   what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique
4. `mathrock_text_course` / `chunk_0003` / dist=0.4233 /   
   math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shoo
5. `mathrock_text_course` / `chunk_0005` / dist=0.4517 /   
   we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have A

Neo4j：
- 命中节点：feature:open_string_drone, technique:two_hand_tapping
- 关系样例：`tuning:DADGAD` -[ENABLES]- `feature:open_string_drone`
- 关系样例：`feature:open_string_drone` -[ENABLES]- `tuning:DADGAD`
- 关系样例：`feature:open_string_drone` -[SUGGESTS]- `heuristic:common_tone_anchor`

### mathrock_dyad_pull_off_open_string

- 查询：`tapped dyads pull off to open string math rock melodic power chord`
- 期望文本源：mathrock_text_course
- 期望视觉：n/a
- 结果：文本R@5=OK，视觉R@5=n/a，KG=OK，Bundle=OK
- 耗时：total=0.03s，text=0.01s，visual=n/a，kg=0.03s
- 缓存：text_embedding=OK，visual_embedding=n/a

文本 Top5：
1. `mathrock_text_course` / `chunk_0001` / dist=0.3056 /   
   so what are the basics of math rock or midwest emo we're going to take a look at this little progression right here which is in the key of dd major,and i have it in a very common a
2. `mathrock_text_course` / `chunk_0002` / dist=0.3427 /   
   all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered ar
3. `mathrock_text_course` / `chunk_0003` / dist=0.3494 /   
   math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shoo
4. `mathrock_text_course` / `chunk_0006` / dist=0.3598 /   
   what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique
5. `mathrock_text_course` / `chunk_0004` / dist=0.4026 /   
   hey hey hey,let's do it. let's do another math Rock progression. shall we so this one kind of call we have another minor shape gone on AH be min,or we have?bf shocks of one five,we

Neo4j：
- 命中节点：technique:tapped_power_chord, feature:tapped_dyads, technique:pull-off_to_open_string
- 关系样例：`technique:tapped_power_chord` -[SUGGESTS]- `heuristic:theme_variation_layering`
- 关系样例：`heuristic:theme_variation_layering` -[SUGGESTS]- `technique:tapped_power_chord`
- 关系样例：`technique:tapped_power_chord` -[SUGGESTS]- `feature:tapped_dyads`

### fretboard_root_octave_ambiguous

- 查询：`根音 八度 指型 octave root pattern`
- 期望文本源：fretboard_handbook_mineru
- 期望视觉：P1_scales_intervals
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=0.10s，text=0.01s，visual=0.01s，kg=0.09s
- 缓存：text_embedding=OK，visual_embedding=OK

文本 Top5：
1. `fretboard_handbook_mineru` / `chunk_0002` / dist=0.3327 /   
   ## 练习1 在下面图示空白处用字母填上对应的琴弦名称。做题时可以不看前面的内容，凭记忆进行填写。第6弦的名称已经给出。 ⑥6④③②① [IMAGE_BLOCK:images/fe57c06be60349e91861ff8b1d5ca2233520a6df3dc06711a0d746eaa348de7e.jpg] ## 练习2 当图中包含多个品格时，需要将上
2. `fretboard_handbook_mineru` / `chunk_0005` / dist=0.3390 /   
   ## 第8章 自然小调音阶 学习目标：构建自然小调音阶的五种指型。理解关系小调和关系大调。 大调音阶只有一种构建公式，但对于小调音阶来说却有许多种构建方式，每一种都有它自己的公式。当人们提到“小调音阶”时，首先想到的应该是自然小调音阶。下面是它的构建公式（大声地读出来）： ## “全、半、全、全、半、全、全” 2级音和3级音之间、5级音和6级音之间是半音关系
3. `fretboard_handbook_mineru` / `chunk_0012` / dist=0.3471 /   
   ## 练习52 用以上所学习的三步寻找Ionian的方法，填写下面的空格。 1.BMixolydian=Ionian从B到B 6.GLocrian Ionian从G到G 2. CLydian = Ionian从C到C 7. A Phrygian Ionian从A到A 3.EDorian Ionian从E到E 8.FDorian Ionian从F到F 4.A 
4. `fretboard_handbook_mineru` / `chunk_0006` / dist=0.3618 /   
   ## 练习22 回到前面的两个练习（练习20和练习21)，写出每一图形中对应的关系小调五声音阶或关系大调五声音阶，并且用方形画出关系调中的根音。 弹奏以上这些练习。对于练习20，先弹大调五声音阶，然后再弹它的关系小调五声音阶。对于练习21，先弹小调五声音阶，然后再弹其关系大调五声音阶。在弹奏之前请说出音阶名称和指型序号。 ## 第10章 大调和纯音程 学习目
5. `fretboard_handbook_mineru` / `chunk_0004` / dist=0.3693 /   
   ## 练习 1.每天花5分钟时间大声地念出指板上音符的名称。最好的方法是给那些你已经学过的歌曲或者乐句中的音符命名，但是也可以采用随机的音符来练习命名。所以，不要再做那种“这个手指按住这里”之类的练习了，大声地说出：“我在演奏第2弦第9品上的音符Ab音！”这个练习至少要坚持做一个星期。 2.接下来的7周时间里，每周都要着重练习一个自然音阶音符。从A音开始，每

视觉 Top5：
- 推断 priority：P1_scales_intervals, P0_root_fingering_forms
1. `P1_scales_intervals` / page=34 / dist=0.4869 / rerank=9.0000 / 练习18 | 练习19 | 练习20  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\d189bc7ade098216ca2646aaa05d19aa749d6b282ad2b365e744bfd6fe77268d.jpg`
2. `P1_scales_intervals` / page=34 / dist=0.5121 / rerank=9.0000 / 练习18 | 练习19 | 练习20  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\220c776cc6654768ae42b830284921efab5f11ce9d1ddf94cf4e101eb5b6376f.jpg`
3. `P1_scales_intervals` / page=37 / dist=0.5210 / rerank=7.5000 / 纯一度 | 大二度 | 大三度 | 纯四度  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\a9aeebcb3ca3013ba8215cbd266747b7b6dc087d3e8521b1039f8898dc388e0c.jpg`
4. `P1_scales_intervals` / page=34 / dist=0.5212 / rerank=7.5000 / 练习18 | 练习19 | 练习20  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\8922df0cd14551b3413fc931ac576bf37822609a953dd8365e4dcfefc04867a4.jpg`
5. `P1_scales_intervals` / page=37 / dist=0.5214 / rerank=7.5000 / 纯一度 | 大二度 | 大三度 | 纯四度  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\c22f406257b38763731cc17b6a0564e099a2a5d59cb811c44777be49d02905eb.jpg`

Neo4j：
- 命中节点：concept:five_major_scale_patterns, concept:root_pattern_cycle, concept:root_pattern_system, heuristic:octave_symmetry_at_12th_fret, heuristic:power_chord_root_finding, interval:octave, pattern:caged_system_navigation, pattern:caged_system_shapes, pattern:interval_geometry_shift, pattern:interval_shape_shift, pattern:octave_minus_one_fret, pattern:root_shape_1, pattern:root_shape_4, technique:octave_displacement_rule
- Alias 扩展：interval:octave, heuristic:octave_symmetry_at_12th_fret, technique:octave_displacement_rule, pattern:octave_minus_one_fret, concept:root_pattern_cycle, concept:root_pattern_system, pattern:root_shape_1, pattern:root_shape_4
- 关系样例：`concept:guitar_tuning` -[CONSTRAINS]- `pattern:interval_shape_shift`
- 关系样例：`pattern:interval_shape_shift` -[CONSTRAINS]- `concept:guitar_tuning`
- 关系样例：`interval:major_seventh` -[ENABLES]- `pattern:octave_minus_one_fret`

### fretboard_perfect_fifth_power_chord_interval

- 查询：`纯五度 音程 power chord root finding 指板`
- 期望文本源：fretboard_handbook_mineru
- 期望视觉：P1_scales_intervals
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=0.03s，text=0.01s，visual=0.01s，kg=0.01s
- 缓存：text_embedding=OK，visual_embedding=OK

文本 Top5：
1. `fretboard_handbook_mineru` / `chunk_0006` / dist=0.2916 /   
   ## 练习22 回到前面的两个练习（练习20和练习21)，写出每一图形中对应的关系小调五声音阶或关系大调五声音阶，并且用方形画出关系调中的根音。 弹奏以上这些练习。对于练习20，先弹大调五声音阶，然后再弹它的关系小调五声音阶。对于练习21，先弹小调五声音阶，然后再弹其关系大调五声音阶。在弹奏之前请说出音阶名称和指型序号。 ## 第10章 大调和纯音程 学习目
2. `fretboard_handbook_mineru` / `chunk_0012` / dist=0.3611 /   
   ## 练习52 用以上所学习的三步寻找Ionian的方法，填写下面的空格。 1.BMixolydian=Ionian从B到B 6.GLocrian Ionian从G到G 2. CLydian = Ionian从C到C 7. A Phrygian Ionian从A到A 3.EDorian Ionian从E到E 8.FDorian Ionian从F到F 4.A 
3. `fretboard_handbook_mineru` / `chunk_0007` / dist=0.3701 /   
   ## 练习26 按照图示中给出的音程和音符画出另外的音符。可先找到大音程或者纯音程，然后在需要的时候利用增、减的方法确定音符的位置。当同一个音程可以找到不同的音符时，把这些音符都标出来。第一个图示已经给出答案作为参考。 [IMAGE_BLOCK:images/25b8493f9159d471045a9c3bb03270a1c97732433c3b1bb0cb
4. `fretboard_handbook_mineru` / `chunk_0002` / dist=0.3902 /   
   ## 练习1 在下面图示空白处用字母填上对应的琴弦名称。做题时可以不看前面的内容，凭记忆进行填写。第6弦的名称已经给出。 ⑥6④③②① [IMAGE_BLOCK:images/fe57c06be60349e91861ff8b1d5ca2233520a6df3dc06711a0d746eaa348de7e.jpg] ## 练习2 当图中包含多个品格时，需要将上
5. `fretboard_handbook_mineru` / `chunk_0005` / dist=0.4014 /   
   ## 第8章 自然小调音阶 学习目标：构建自然小调音阶的五种指型。理解关系小调和关系大调。 大调音阶只有一种构建公式，但对于小调音阶来说却有许多种构建方式，每一种都有它自己的公式。当人们提到“小调音阶”时，首先想到的应该是自然小调音阶。下面是它的构建公式（大声地读出来）： ## “全、半、全、全、半、全、全” 2级音和3级音之间、5级音和6级音之间是半音关系

视觉 Top5：
- 推断 priority：P1_scales_intervals
1. `P1_scales_intervals` / page=37 / dist=0.5130 / rerank=6.7500 / 纯一度 | 大二度 | 大三度 | 纯四度  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\a9aeebcb3ca3013ba8215cbd266747b7b6dc087d3e8521b1039f8898dc388e0c.jpg`
2. `P1_scales_intervals` / page=37 / dist=0.5387 / rerank=6.7500 / 纯一度 | 大二度 | 大三度 | 纯四度  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\c22f406257b38763731cc17b6a0564e099a2a5d59cb811c44777be49d02905eb.jpg`
3. `P1_scales_intervals` / page=34 / dist=0.4804 / rerank=6.0000 / 练习18 | 练习19 | 练习20  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\d189bc7ade098216ca2646aaa05d19aa749d6b282ad2b365e744bfd6fe77268d.jpg`
4. `P1_scales_intervals` / page=39 / dist=0.5179 / rerank=6.0000 / 练习24 | 练习25  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\07f72703ce0a15cbaff2ec023bcd3e4d3cebb00d2c5efef55993c0c3233f7054.jpg`
5. `P1_scales_intervals` / page=39 / dist=0.5235 / rerank=6.0000 / 练习24 | 练习25  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\fda2c29d65a27e594532d5907dc5c2a8b93b067fc73d189cc193602ebd5da08f.jpg`

Neo4j：
- 命中节点：interval:major_6th, interval:perfect_5th, concept:compound_interval, heuristic:power_chord_root_finding, pattern:interval_geometry_shift, pattern:interval_shape_shift
- Alias 扩展：concept:compound_interval, pattern:interval_geometry_shift, pattern:interval_shape_shift, interval:perfect_5th, interval:major_6th
- 关系样例：`concept:guitar_tuning` -[CONSTRAINS]- `pattern:interval_shape_shift`
- 关系样例：`pattern:interval_shape_shift` -[CONSTRAINS]- `concept:guitar_tuning`
- 关系样例：`interval:perfect_5th` -[ENABLES]- `pattern:power_chord_shape`

### fretboard_caged_major_triad_shapes

- 查询：`CAGED 大三和弦 五种指型 major triad shapes`
- 期望文本源：fretboard_handbook_mineru
- 期望视觉：P2_arpeggios_chords
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=0.05s，text=0.01s，visual=0.01s，kg=0.03s
- 缓存：text_embedding=OK，visual_embedding=OK

文本 Top5：
1. `fretboard_handbook_mineru` / `chunk_0008` / dist=0.3273 /   
   ## 小三和弦琵音 小三和弦是由根音、根音上方的小三度音和纯五度音组成的：1、b3、5。 ## 练习31 构建D小三和弦琶音的五种指型。注意不要用品位标记以下的音符，并且在画出音符时，保证所有的音符都在左手所在的把位以内，最多不要超出1品以外。 1)D小三和弦琶音 V [IMAGE_BLOCK:images/f09a862e2cade2cfda3e9353a
2. `fretboard_handbook_mineru` / `chunk_0009` / dist=0.3485 /   
   ## 第15章 七和弦琶音 学习目标：在指板上构建七和弦的琶音。 七和弦是学习三和弦之后的进阶，每个七和弦包含四个音。首先，还是先来学习七和弦的琶音，之后再来学习七和弦。七和弦琶音之间的音程关系和三和弦是相似的。 ## 大七和弦 在大三和弦的基础上增加一个大七度音就形成了大七和弦，其音符为：1、3、5和7。表示大七和弦的标记有以下几种：Cmaj7，Cma7，
3. `fretboard_handbook_mineru` / `chunk_0015` / dist=0.3595 /   
   ## 练习23 1.同度音在指板上为两根相邻弦相差5品位置的音。对于第3弦上的音，其在第2弦上的同度音为向下4品的位置。 1.b5 2.#4 3.4 2.大二度在同一根弦上的距离为2品。从一根弦到另一根弦上的大二度为向下3品的距离。而第3弦和第2弦之间的大二度为2品的距离。 4.b3 5.b3 3.大三度在同一根弦上的距离为4品。从一根弦到另一根弦上的大三度
4. `fretboard_handbook_mineru` / `chunk_0013` / dist=0.3651 /   
   ## 分割（Slash）和弦 分割和弦就是将三和弦或七和弦叠加在一个非和弦根音的低音上。这种和弦可以用这种方式来表达：C/D。当这个低音也是和弦中的音时，分割和弦就变成了一种和弦转位。否则，分割和弦就是延伸和弦或者变化和弦的一种声部构成。 ## 练习59 在下面的图示中画出 Slash 和弦。 [IMAGE_BLOCK:images/323a85babce1
5. `fretboard_handbook_mineru` / `chunk_0012` / dist=0.3765 /   
   ## 练习52 用以上所学习的三步寻找Ionian的方法，填写下面的空格。 1.BMixolydian=Ionian从B到B 6.GLocrian Ionian从G到G 2. CLydian = Ionian从C到C 7. A Phrygian Ionian从A到A 3.EDorian Ionian从E到E 8.FDorian Ionian从F到F 4.A 

视觉 Top5：
- 推断 priority：P2_arpeggios_chords
1. `P2_arpeggios_chords` / page=47 / dist=0.4872 / rerank=15.2500 / 第14章 三和弦  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\0a2a6f601b344ae09fe6e977704f1260fa55caf22a3f1f1cc9643aa2af5bde12.jpg`
2. `P2_arpeggios_chords` / page=50 / dist=0.5616 / rerank=15.2500 / 转位 | 练习  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\4f88f53cedc0999c8cf7ae26e45330bb18f910bee111d5f3945410b902371eab.jpg`
3. `P2_arpeggios_chords` / page=48 / dist=0.5650 / rerank=15.2500 / 大三和弦 | 练习34 | 小三和弦 | 练习35  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\3473ccf4b0ddca16337f75a8662133621b1216ba3dfbf85b814b6a8b5475be1c.jpg`
4. `P2_arpeggios_chords` / page=49 / dist=0.5663 / rerank=15.0000 / 减三和弦 | 练习36 | 增三和弦 | 练习37  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\cca58c83e81e9167c7a622a30b0e81bc3f4613f91394affc899c46d81d9e69ea.jpg`
5. `P2_arpeggios_chords` / page=50 / dist=0.5264 / rerank=14.5000 / 转位 | 练习  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\524e93470084f0cfb5adfd9a350701f856930f7a00d296466de4f938038c33af.jpg`

Neo4j：
- 命中节点：chord:major_triad, concept:five_major_scale_patterns, pattern:caged_system_navigation, pattern:caged_system_shapes, pattern:interval_geometry_shift, pattern:interval_shape_shift
- Alias 扩展：chord:major_triad, concept:five_major_scale_patterns, pattern:caged_system_shapes, pattern:caged_system_navigation, pattern:interval_geometry_shift, pattern:interval_shape_shift
- 关系样例：`concept:guitar_tuning` -[CONSTRAINS]- `pattern:interval_shape_shift`
- 关系样例：`pattern:interval_shape_shift` -[CONSTRAINS]- `concept:guitar_tuning`
- 关系样例：`concept:root_pattern_system` -[CONSTRAINS]- `pattern:caged_system_navigation`

### fretboard_add9_not_dom9

- 查询：`add9 加九和弦 不含七音 不要混淆 dominant 9`
- 期望文本源：fretboard_handbook_mineru
- 期望视觉：P3_common_scales_chords
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=0.04s，text=0.01s，visual=0.01s，kg=0.03s
- 缓存：text_embedding=OK，visual_embedding=OK

文本 Top5：
1. `fretboard_handbook_mineru` / `chunk_0010` / dist=0.4789 /   
   ## 练习44 运用指型2和指型5画出七和弦“1、5、7、3”常用声部构成。 [IMAGE_BLOCK:images/6e05e11e982d36687c5df5564b6bf1ef6efb314c6143bb7c6ebfe3a865bdf034.jpg] [IMAGE_BLOCK:images/c1b81c203b4a0affa11063cfd87b862
2. `fretboard_handbook_mineru` / `chunk_0009` / dist=0.4994 /   
   ## 第15章 七和弦琶音 学习目标：在指板上构建七和弦的琶音。 七和弦是学习三和弦之后的进阶，每个七和弦包含四个音。首先，还是先来学习七和弦的琶音，之后再来学习七和弦。七和弦琶音之间的音程关系和三和弦是相似的。 ## 大七和弦 在大三和弦的基础上增加一个大七度音就形成了大七和弦，其音符为：1、3、5和7。表示大七和弦的标记有以下几种：Cmaj7，Cma7，
3. `fretboard_handbook_mineru` / `chunk_0011` / dist=0.5093 /   
   ## 练习49 根据给出的声部构成，在下面的图示中构建延伸和弦。 [IMAGE_BLOCK:images/8b4316202b722a59012caf14d81fafb2e864d6437437f7193aa92f4485ecec90.jpg] [IMAGE_BLOCK:images/a5cad2ac1a60193c9315db6052c0675e341d9
4. `fretboard_handbook_mineru` / `chunk_0013` / dist=0.5172 /   
   ## 分割（Slash）和弦 分割和弦就是将三和弦或七和弦叠加在一个非和弦根音的低音上。这种和弦可以用这种方式来表达：C/D。当这个低音也是和弦中的音时，分割和弦就变成了一种和弦转位。否则，分割和弦就是延伸和弦或者变化和弦的一种声部构成。 ## 练习59 在下面的图示中画出 Slash 和弦。 [IMAGE_BLOCK:images/323a85babce1
5. `fretboard_handbook_mineru` / `chunk_0015` / dist=0.5323 /   
   ## 练习23 1.同度音在指板上为两根相邻弦相差5品位置的音。对于第3弦上的音，其在第2弦上的同度音为向下4品的位置。 1.b5 2.#4 3.4 2.大二度在同一根弦上的距离为2品。从一根弦到另一根弦上的大二度为向下3品的距离。而第3弦和第2弦之间的大二度为2品的距离。 4.b3 5.b3 3.大三度在同一根弦上的距离为4品。从一根弦到另一根弦上的大三度

视觉 Top5：
- 推断 priority：P3_common_scales_chords
1. `P3_common_scales_chords` / page=68 / dist=0.4792 / rerank=12.7500 / 第21章 其他常用和弦 | 练习58  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\48b8d933c0ef36d4e4bc329917be9ca10970107f7f0196ba8b6b12afc610a178.jpg`
2. `P3_common_scales_chords` / page=68 / dist=0.5053 / rerank=12.7500 / 第21章 其他常用和弦 | 练习58  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\19c70069724de5b61cb416d5281ab07e0823e87d4ec934b7dac90aef049b1ab7.jpg`
3. `P3_common_scales_chords` / page=68 / dist=0.5568 / rerank=12.7500 / 第21章 其他常用和弦 | 练习58  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\7915644f58172e192a14dbf16a653d9b27d31c9210b2d7fe4ad37199f9085bce.jpg`
4. `P3_common_scales_chords` / page=68 / dist=0.5574 / rerank=12.7500 / 第21章 其他常用和弦 | 练习58  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\ee5c10ed920b19c453b2962073feb887d3e33c867763614b3808c08fac91d5eb.jpg`
5. `P3_common_scales_chords` / page=68 / dist=0.5620 / rerank=12.7500 / 第21章 其他常用和弦 | 练习58  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\6adcb92bcf27554cc5f9bdb7c39dbcae6d5385f77864bee4163f9d3ccbb788e3.jpg`

Neo4j：
- 命中节点：chord:add9, chord:6/9, chord:6_9, chord:extended_chords
- Alias 扩展：chord:add9, chord:6/9, chord:6_9, chord:extended_chords
- 关系样例：`chord:add9` -[CONFLICTS_WITH]- `chord:dom9`
- 关系样例：`chord:dom9` -[CONFLICTS_WITH]- `chord:add9`
- 关系样例：`chord:add9` -[CONFLICTS_WITH]- `chord:dominant_9th`

### fretboard_pentatonic_two_notes_per_string

- 查询：`五声音阶 每根弦两个音 pentatonic two notes per string`
- 期望文本源：fretboard_handbook_mineru
- 期望视觉：P1_scales_intervals
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=0.05s，text=0.01s，visual=0.01s，kg=0.03s
- 缓存：text_embedding=OK，visual_embedding=OK

文本 Top5：
1. `fretboard_handbook_mineru` / `chunk_0005` / dist=0.3355 /   
   ## 第8章 自然小调音阶 学习目标：构建自然小调音阶的五种指型。理解关系小调和关系大调。 大调音阶只有一种构建公式，但对于小调音阶来说却有许多种构建方式，每一种都有它自己的公式。当人们提到“小调音阶”时，首先想到的应该是自然小调音阶。下面是它的构建公式（大声地读出来）： ## “全、半、全、全、半、全、全” 2级音和3级音之间、5级音和6级音之间是半音关系
2. `fretboard_handbook_mineru` / `chunk_0002` / dist=0.3399 /   
   ## 练习1 在下面图示空白处用字母填上对应的琴弦名称。做题时可以不看前面的内容，凭记忆进行填写。第6弦的名称已经给出。 ⑥6④③②① [IMAGE_BLOCK:images/fe57c06be60349e91861ff8b1d5ca2233520a6df3dc06711a0d746eaa348de7e.jpg] ## 练习2 当图中包含多个品格时，需要将上
3. `fretboard_handbook_mineru` / `chunk_0006` / dist=0.3582 /   
   ## 练习22 回到前面的两个练习（练习20和练习21)，写出每一图形中对应的关系小调五声音阶或关系大调五声音阶，并且用方形画出关系调中的根音。 弹奏以上这些练习。对于练习20，先弹大调五声音阶，然后再弹它的关系小调五声音阶。对于练习21，先弹小调五声音阶，然后再弹其关系大调五声音阶。在弹奏之前请说出音阶名称和指型序号。 ## 第10章 大调和纯音程 学习目
4. `fretboard_handbook_mineru` / `chunk_0004` / dist=0.3660 /   
   ## 练习 1.每天花5分钟时间大声地念出指板上音符的名称。最好的方法是给那些你已经学过的歌曲或者乐句中的音符命名，但是也可以采用随机的音符来练习命名。所以，不要再做那种“这个手指按住这里”之类的练习了，大声地说出：“我在演奏第2弦第9品上的音符Ab音！”这个练习至少要坚持做一个星期。 2.接下来的7周时间里，每周都要着重练习一个自然音阶音符。从A音开始，每
5. `fretboard_handbook_mineru` / `chunk_0012` / dist=0.3786 /   
   ## 练习52 用以上所学习的三步寻找Ionian的方法，填写下面的空格。 1.BMixolydian=Ionian从B到B 6.GLocrian Ionian从G到G 2. CLydian = Ionian从C到C 7. A Phrygian Ionian从A到A 3.EDorian Ionian从E到E 8.FDorian Ionian从F到F 4.A 

视觉 Top5：
- 推断 priority：P1_scales_intervals
1. `P1_scales_intervals` / page=34 / dist=0.4528 / rerank=6.0000 / 练习18 | 练习19 | 练习20  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\d189bc7ade098216ca2646aaa05d19aa749d6b282ad2b365e744bfd6fe77268d.jpg`
2. `P1_scales_intervals` / page=34 / dist=0.4965 / rerank=6.0000 / 练习18 | 练习19 | 练习20  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\220c776cc6654768ae42b830284921efab5f11ce9d1ddf94cf4e101eb5b6376f.jpg`
3. `P1_scales_intervals` / page=37 / dist=0.4716 / rerank=5.0000 / 纯一度 | 大二度 | 大三度 | 纯四度  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\a9aeebcb3ca3013ba8215cbd266747b7b6dc087d3e8521b1039f8898dc388e0c.jpg`
4. `P1_scales_intervals` / page=39 / dist=0.4908 / rerank=5.0000 / 练习24 | 练习25  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\07f72703ce0a15cbaff2ec023bcd3e4d3cebb00d2c5efef55993c0c3233f7054.jpg`
5. `P1_scales_intervals` / page=37 / dist=0.4924 / rerank=5.0000 / 纯一度 | 大二度 | 大三度 | 纯四度  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\c06a5ebd8a8adaf77734d7afb6a66faa80a7505bc9115091785d5e808b81f41d.jpg`

Neo4j：
- 命中节点：scale:pentatonic_major, heuristic:two_notes_per_string_geometry
- 关系样例：`scale:pentatonic_major` -[ENABLES]- `idiom:two_notes_per_string_pattern`
- 关系样例：`idiom:two_notes_per_string_pattern` -[ENABLES]- `scale:pentatonic_major`
- 关系样例：`scale:pentatonic_major` -[ENABLES]- `guitar_idiom:open_string_resonance_in_key_of_g_d_a_e`

### fretboard_root_pattern_cycle_overlap

- 查询：`五种根音型式 循环 重叠 root pattern cycle overlap`
- 期望文本源：fretboard_handbook_mineru
- 期望视觉：P0_root_fingering_forms
- 结果：文本R@5=OK，视觉R@5=OK，KG=OK，Bundle=OK
- 耗时：total=0.03s，text=0.01s，visual=0.01s，kg=0.02s
- 缓存：text_embedding=OK，visual_embedding=OK

文本 Top5：
1. `fretboard_handbook_mineru` / `chunk_0002` / dist=0.3720 /   
   ## 练习1 在下面图示空白处用字母填上对应的琴弦名称。做题时可以不看前面的内容，凭记忆进行填写。第6弦的名称已经给出。 ⑥6④③②① [IMAGE_BLOCK:images/fe57c06be60349e91861ff8b1d5ca2233520a6df3dc06711a0d746eaa348de7e.jpg] ## 练习2 当图中包含多个品格时，需要将上
2. `fretboard_handbook_mineru` / `chunk_0012` / dist=0.3890 /   
   ## 练习52 用以上所学习的三步寻找Ionian的方法，填写下面的空格。 1.BMixolydian=Ionian从B到B 6.GLocrian Ionian从G到G 2. CLydian = Ionian从C到C 7. A Phrygian Ionian从A到A 3.EDorian Ionian从E到E 8.FDorian Ionian从F到F 4.A 
3. `fretboard_handbook_mineru` / `chunk_0005` / dist=0.3918 /   
   ## 第8章 自然小调音阶 学习目标：构建自然小调音阶的五种指型。理解关系小调和关系大调。 大调音阶只有一种构建公式，但对于小调音阶来说却有许多种构建方式，每一种都有它自己的公式。当人们提到“小调音阶”时，首先想到的应该是自然小调音阶。下面是它的构建公式（大声地读出来）： ## “全、半、全、全、半、全、全” 2级音和3级音之间、5级音和6级音之间是半音关系
4. `fretboard_handbook_mineru` / `chunk_0004` / dist=0.4015 /   
   ## 练习 1.每天花5分钟时间大声地念出指板上音符的名称。最好的方法是给那些你已经学过的歌曲或者乐句中的音符命名，但是也可以采用随机的音符来练习命名。所以，不要再做那种“这个手指按住这里”之类的练习了，大声地说出：“我在演奏第2弦第9品上的音符Ab音！”这个练习至少要坚持做一个星期。 2.接下来的7周时间里，每周都要着重练习一个自然音阶音符。从A音开始，每
5. `fretboard_handbook_mineru` / `chunk_0013` / dist=0.4047 /   
   ## 分割（Slash）和弦 分割和弦就是将三和弦或七和弦叠加在一个非和弦根音的低音上。这种和弦可以用这种方式来表达：C/D。当这个低音也是和弦中的音时，分割和弦就变成了一种和弦转位。否则，分割和弦就是延伸和弦或者变化和弦的一种声部构成。 ## 练习59 在下面的图示中画出 Slash 和弦。 [IMAGE_BLOCK:images/323a85babce1

视觉 Top5：
- 推断 priority：P0_root_fingering_forms
1. `P0_root_fingering_forms` / page=13 / dist=0.5677 / rerank=14.0000 / 练习4 | 练习5  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\af1f5dfaafd4bc331b51424c9497e14435fd6bfae20d720cef1b5b032136240b.jpg`
2. `P0_root_fingering_forms` / page=13 / dist=0.5689 / rerank=14.0000 / 练习4 | 练习5  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\27cc76634908dd1aa263d40b028c2df067a9b7cd0086cb49716815d05f9739a6.jpg`
3. `P0_root_fingering_forms` / page=13 / dist=0.5747 / rerank=14.0000 / 练习4 | 练习5  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\d502da690fe431965bb7cfbb25884f52fa71e3449b72b8a0a2c5a5d3b6a74232.jpg`
4. `P0_root_fingering_forms` / page=13 / dist=0.5765 / rerank=14.0000 / 练习4 | 练习5  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\f5458035580ef6687c4357684818cd39f2d499329404121c4b8b6e8eeef51a3b.jpg`
5. `P0_root_fingering_forms` / page=13 / dist=0.5779 / rerank=14.0000 / 练习4 | 练习5  
   `data\processed\mineru_full_gpu\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\images\e6cdbd16559a30dcaacfc5049d15927fe64e005083abf4195dca1af9eefe36e3.jpg`

Neo4j：
- 命中节点：concept:five_major_scale_patterns, concept:root_pattern_cycle, concept:root_pattern_system, heuristic:power_chord_root_finding, pattern:caged_system_navigation, pattern:caged_system_shapes, pattern:interval_geometry_shift, pattern:interval_shape_shift, pattern:root_shape_1, pattern:root_shape_4
- Alias 扩展：concept:root_pattern_cycle, concept:root_pattern_system, pattern:root_shape_1, pattern:root_shape_4, heuristic:power_chord_root_finding, concept:five_major_scale_patterns, pattern:caged_system_shapes, pattern:caged_system_navigation
- 关系样例：`concept:guitar_tuning` -[CONSTRAINS]- `pattern:interval_shape_shift`
- 关系样例：`pattern:interval_shape_shift` -[CONSTRAINS]- `concept:guitar_tuning`
- 关系样例：`interval:perfect_5th` -[ENABLES]- `heuristic:power_chord_root_finding`
