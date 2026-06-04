# Text RAG Retrieval Evaluation

## Summary

- Collection: `guitar_text_chunks_qwen3_06b` (68 docs)
- Model: `models\embedding\qwen3-embedding-0.6b` on `cuda`, dim=1024
- Tests: 40, TopK: 5
- Rerank: `False`, candidates: 5
- Pass all: 33/40
- Source Hit@1: 19/40
- Source Hit@K: 34/40
- Keyword Hit@1: 21/40
- Keyword Hit@K: 37/40
- Avg latency/query: 0.047s
- Median latency/query: 0.036s

## Misses

`funk_note_location_prereq`, `mathrock_pdf_tapping_evenness`, `mathrock_pdf_shell_voicing`, `mathrock_pdf_jazz_voicing_progressions`, `fretboard_six_nine_add9`, `cross_gp5_funk_16th_muting`, `cross_rhythm_plus_harmony`

## Cases

### funk_note_location_prereq - MISS

- Query: Cory Wong funk 课程里为什么要求先掌握指板音名和 circle of fourths
- Expected sources: cory_wong_funk_core
- Expected keywords any: note location, circle of fourths, circle of fifths
- Rerank: `False`, candidates: 5
- Source first rank: None
- Keyword first rank: None
- Latency: total 0.390s = embed 0.327s + chroma 0.063s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  |  | 0.2442 | -0.2442 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 2 | 2 |  |  | 0.2445 | -0.2445 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 3 | 3 |  |  | 0.2480 | -0.2480 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 4 | 4 |  |  | 0.2646 | -0.2646 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 5 | 5 |  |  | 0.2671 | -0.2671 | `mathrock_text_course` | `chunk_0007` |  | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |

### funk_muted_chuck_density - PASS

- Query: funk rhythm guitar 里 muted chuck ghost note 作为十六分律动怎么安排
- Expected sources: cory_wong_funk_core
- Expected keywords any: muted, chuck, sixteenth, ghost
- Rerank: `False`, candidates: 5
- Source first rank: 4
- Keyword first rank: 3
- Latency: total 0.042s = embed 0.040s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  |  | 0.2326 | -0.2326 | `mathrock_text_course` | `chunk_0002` |  | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 2 | 2 |  |  | 0.2415 | -0.2415 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 3 | 3 |  | Y | 0.2543 | -0.2543 | `mathrock_text_course` | `chunk_0006` |  | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |
| 4 | 4 | Y | Y | 0.2561 | -0.2561 | `cory_wong_funk_core` | `chunk_0011` |  | one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accomplish some of my signature moves,both in ... |
| 5 | 5 |  | Y | 0.2572 | -0.2572 | `mathrock_text_course` | `chunk_0005` |  | we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have AC sharp right there and e. ,so we have ... |

### funk_leave_space_for_band - PASS

- Query: funk 吉他伴奏为什么要给 bass 和 drums 留空间
- Expected sources: cory_wong_funk_core
- Expected keywords any: space, bass, drums, band
- Rerank: `False`, candidates: 5
- Source first rank: 3
- Keyword first rank: 3
- Latency: total 0.044s = embed 0.042s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  |  | 0.3036 | -0.3036 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 2 | 2 |  |  | 0.3134 | -0.3134 | `mathrock_text_course` | `chunk_0002` |  | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 3 | 3 | Y | Y | 0.3154 | -0.3154 | `cory_wong_funk_core` | `chunk_0010` |  | now those are a couple of my main approaches to ribbon guitar,but some other things just to consider are ribbon IC density.range on the instrument.tone.and space.OK so.sometimes a song is going to call for a ribbon guit... |
| 4 | 4 |  |  | 0.3179 | -0.3179 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 5 | 5 |  |  | 0.3181 | -0.3181 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |

### funk_right_hand_pocket - PASS

- Query: Cory Wong funk 右手节奏 pocket 和 groove 的训练重点
- Expected sources: cory_wong_funk_core
- Expected keywords any: right hand, pocket, groove, rhythm
- Rerank: `False`, candidates: 5
- Source first rank: 2
- Keyword first rank: 2
- Latency: total 0.083s = embed 0.081s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  |  | 0.2898 | -0.2898 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 2 | 2 | Y | Y | 0.2970 | -0.2970 | `cory_wong_funk_core` | `chunk_0011` |  | one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accomplish some of my signature moves,both in ... |
| 3 | 3 |  | Y | 0.3017 | -0.3017 | `mathrock_text_course` | `chunk_0002` |  | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 4 | 4 |  | Y | 0.3028 | -0.3028 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 5 | 5 | Y | Y | 0.3031 | -0.3031 | `cory_wong_funk_core` | `chunk_0009` |  | now something to really note is.there's a difference between timing.patterns.and groove.they all kind of make up this thing that we call ribbon.那timing is。where you're placing something.right? the timing is a hundred an... |

### funk_syncopation_comping - PASS

- Query: funk comping 如何用 syncopation 和短促和弦切分
- Expected sources: cory_wong_funk_core
- Expected keywords any: syncopation, comping, rhythm, chord
- Rerank: `False`, candidates: 5
- Source first rank: 2
- Keyword first rank: 1
- Latency: total 0.041s = embed 0.039s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  | Y | 0.2886 | -0.2886 | `mathrock_text_course` | `chunk_0007` |  | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 2 | 2 | Y | Y | 0.2977 | -0.2977 | `cory_wong_funk_core` | `chunk_0004` |  | that's just actually articulating and playing a different type of phrasing on it,but it's one way to use that voicing.嗯。minor seven chords are super common in funk music and especially in a lot of the music that i play,... |
| 3 | 3 |  | Y | 0.3076 | -0.3076 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 4 | 4 | Y | Y | 0.3097 | -0.3097 | `cory_wong_funk_core` | `chunk_0011` |  | one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accomplish some of my signature moves,both in ... |
| 5 | 5 |  | Y | 0.3178 | -0.3178 | `mathrock_text_course` | `chunk_0002` |  | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |

### funk_percussive_guitar_role - PASS

- Query: funk guitar 在乐队中更像打击乐还是和声乐器，如何处理 percussive attack
- Expected sources: cory_wong_funk_core
- Expected keywords any: percussive, attack, rhythm, guitar
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.041s = embed 0.039s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2861 | -0.2861 | `cory_wong_funk_core` | `chunk_0007` |  | today I want to give you a little ribbon guitar primer now I am.what I would consider a consummate ribbon guitar player I love,the ribbon guitar I love,the role and I think it's often actually a neglected role.lot of gu... |
| 2 | 2 | Y | Y | 0.2984 | -0.2984 | `cory_wong_funk_core` | `chunk_0010` |  | now those are a couple of my main approaches to ribbon guitar,but some other things just to consider are ribbon IC density.range on the instrument.tone.and space.OK so.sometimes a song is going to call for a ribbon guit... |
| 3 | 3 | Y | Y | 0.2985 | -0.2985 | `cory_wong_funk_core` | `chunk_0006` |  | now that you've gone through all these,different chord voicings and hopefully you've paused and put in the practice and really started to understand how the voicings work with the corresponding scale.and pentatonic scal... |
| 4 | 4 |  | Y | 0.3086 | -0.3086 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 5 | 5 |  | Y | 0.3148 | -0.3148 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |

### funk_triads_relative_minor - PASS

- Query: funk 课程中 major minor triads 和 relative minor 为什么是前置知识
- Expected sources: cory_wong_funk_core
- Expected keywords any: major, minor, triads, relative minor
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.042s = embed 0.040s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2447 | -0.2447 | `cory_wong_funk_core` | `chunk_0005` |  | the last type of chord voicings I want to talk to you about is triads.and the way that I'm going to think about triads,I'm going to talk about triads today,is in groupings of three strings. I'm going to go in depth on t... |
| 2 | 2 | Y | Y | 0.2498 | -0.2498 | `cory_wong_funk_core` | `chunk_0002` |  | so if you have canda minor.next to it,you're going to have f and d minor,and you're going to have g and e minor. those six chords are all the major and minor triads in the key of c.and if you shift it over,you're going ... |
| 3 | 3 |  |  | 0.2637 | -0.2637 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 4 | 4 | Y | Y | 0.2797 | -0.2797 | `cory_wong_funk_core` | `chunk_0003` |  | this next series of lessons is about cord voicings and cord moves that I use in my playing.especially,in the context of funk,music now most of these voice o icings start from the caged system if you're not familiar with... |
| 5 | 5 | Y | Y | 0.2847 | -0.2847 | `cory_wong_funk_core` | `chunk_0004` |  | that's just actually articulating and playing a different type of phrasing on it,but it's one way to use that voicing.嗯。minor seven chords are super common in funk music and especially in a lot of the music that i play,... |

### funk_caged_system - PASS

- Query: CAGED system 在 Cory Wong 课程里如何组织 chord shape 和 scale shape
- Expected sources: cory_wong_funk_core
- Expected keywords any: caged, chord shapes, scale shapes
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.046s = embed 0.044s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2556 | -0.2556 | `cory_wong_funk_core` | `chunk_0002` |  | so if you have canda minor.next to it,you're going to have f and d minor,and you're going to have g and e minor. those six chords are all the major and minor triads in the key of c.and if you shift it over,you're going ... |
| 2 | 2 |  |  | 0.2652 | -0.2652 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 3 | 3 | Y | Y | 0.2670 | -0.2670 | `cory_wong_funk_core` | `chunk_0003` |  | this next series of lessons is about cord voicings and cord moves that I use in my playing.especially,in the context of funk,music now most of these voice o icings start from the caged system if you're not familiar with... |
| 4 | 4 |  |  | 0.2727 | -0.2727 | `mathrock_text_course` | `chunk_0007` |  | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 5 | 5 |  |  | 0.2733 | -0.2733 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |

### mathrock_text_dadgad_open_drone - PASS

- Query: math rock 文本课 DADGAD 调弦如何产生 open string drone 和 common tone
- Expected sources: mathrock_text_course
- Expected keywords any: dadgad, open, common tone, drone
- Rerank: `False`, candidates: 5
- Source first rank: 4
- Keyword first rank: 2
- Latency: total 0.040s = embed 0.038s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  |  | 0.2743 | -0.2743 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 2 | 2 |  | Y | 0.2950 | -0.2950 | `mathrock_pdf_steve_h` | `chunk_0004` |  | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 3 | 3 |  |  | 0.2972 | -0.2972 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 4 | 4 | Y | Y | 0.3017 | -0.3017 | `mathrock_text_course` | `chunk_0002` |  | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 5 | 5 | Y | Y | 0.3030 | -0.3030 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |

### mathrock_text_tapped_power_chords - PASS

- Query: math rock 文本课里 tapped power chords 如何在旋律中使用
- Expected sources: mathrock_text_course
- Expected keywords any: tap, power chord, tapped, melody
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.038s = embed 0.036s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2780 | -0.2780 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 2 | 2 |  |  | 0.2800 | -0.2800 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 3 | 3 | Y | Y | 0.2988 | -0.2988 | `mathrock_text_course` | `chunk_0002` |  | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 4 | 4 | Y | Y | 0.3002 | -0.3002 | `mathrock_text_course` | `chunk_0006` |  | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |
| 5 | 5 | Y | Y | 0.3094 | -0.3094 | `mathrock_text_course` | `chunk_0007` |  | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |

### mathrock_text_hammer_pull_slide - PASS

- Query: math rock riff 用 hammer on pull off slide 制造高密度连奏
- Expected sources: mathrock_text_course
- Expected keywords any: hammer, pull, slide, legato
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.040s = embed 0.039s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2358 | -0.2358 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 2 | 2 | Y | Y | 0.2442 | -0.2442 | `mathrock_text_course` | `chunk_0002` |  | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 3 | 3 | Y | Y | 0.2703 | -0.2703 | `mathrock_text_course` | `chunk_0005` |  | we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have AC sharp right there and e. ,so we have ... |
| 4 | 4 |  |  | 0.2705 | -0.2705 | `cory_wong_funk_core` | `chunk_0011` |  | one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accomplish some of my signature moves,both in ... |
| 5 | 5 | Y | Y | 0.2779 | -0.2779 | `mathrock_text_course` | `chunk_0006` |  | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |

### mathrock_text_percussive_slap - PASS

- Query: math rock midwest emo 编配里 percussive slap 和 dead note 的作用
- Expected sources: mathrock_text_course
- Expected keywords any: percussive, slap, dead, rhythm
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.039s = embed 0.037s + chroma 0.001s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2657 | -0.2657 | `mathrock_text_course` | `chunk_0002` |  | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 2 | 2 | Y |  | 0.2743 | -0.2743 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 3 | 3 | Y | Y | 0.2973 | -0.2973 | `mathrock_text_course` | `chunk_0005` |  | we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have AC sharp right there and e. ,so we have ... |
| 4 | 4 | Y | Y | 0.2979 | -0.2979 | `mathrock_text_course` | `chunk_0007` |  | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 5 | 5 | Y | Y | 0.2994 | -0.2994 | `mathrock_text_course` | `chunk_0006` |  | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |

### mathrock_text_theme_variation - PASS

- Query: math rock progression 如何从简单主题逐步加复杂 theme variation
- Expected sources: mathrock_text_course
- Expected keywords any: theme, variation, progression, complex
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.036s = embed 0.034s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.3376 | -0.3376 | `mathrock_text_course` | `chunk_0007` |  | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 2 | 2 |  |  | 0.3428 | -0.3428 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 3 | 3 | Y | Y | 0.3479 | -0.3479 | `mathrock_text_course` | `chunk_0006` |  | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |
| 4 | 4 |  |  | 0.3486 | -0.3486 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 5 | 5 |  |  | 0.3552 | -0.3552 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |

### mathrock_text_open_string_pull_off - PASS

- Query: midwest emo 乐句里 slide 后 pull off 到 open string 的色彩
- Expected sources: mathrock_text_course
- Expected keywords any: slide, pull off, open string
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.035s = embed 0.034s + chroma 0.001s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2427 | -0.2427 | `mathrock_text_course` | `chunk_0002` |  | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 2 | 2 | Y | Y | 0.2446 | -0.2446 | `mathrock_text_course` | `chunk_0006` |  | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |
| 3 | 3 | Y | Y | 0.2449 | -0.2449 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 4 | 4 | Y | Y | 0.2490 | -0.2490 | `mathrock_text_course` | `chunk_0005` |  | we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have AC sharp right there and e. ,so we have ... |
| 5 | 5 | Y |  | 0.2587 | -0.2587 | `mathrock_text_course` | `chunk_0007` |  | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |

### mathrock_text_harp_harmonics - PASS

- Query: math rock 教学课里 harp harmonics 可以怎样启发 riff writing
- Expected sources: mathrock_text_course
- Expected keywords any: harp, harmonics, riff
- Rerank: `False`, candidates: 5
- Source first rank: 2
- Keyword first rank: 2
- Latency: total 0.035s = embed 0.034s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  |  | 0.2506 | -0.2506 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 2 | 2 | Y | Y | 0.2818 | -0.2818 | `mathrock_text_course` | `chunk_0007` |  | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 3 | 3 |  | Y | 0.2878 | -0.2878 | `cory_wong_funk_core` | `chunk_0011` |  | one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accomplish some of my signature moves,both in ... |
| 4 | 4 | Y | Y | 0.2902 | -0.2902 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 5 | 5 |  |  | 0.2934 | -0.2934 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |

### mathrock_text_alternate_tuning_dependency - PASS

- Query: 为什么 math rock 的指型常常依赖 alternate tuning，不能直接搬到标准调弦
- Expected sources: mathrock_text_course
- Expected keywords any: alternate tuning, tuning, shape, dependency
- Rerank: `False`, candidates: 5
- Source first rank: 3
- Keyword first rank: 3
- Latency: total 0.035s = embed 0.034s + chroma 0.001s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  |  | 0.2774 | -0.2774 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 2 | 2 |  |  | 0.2820 | -0.2820 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 3 | 3 | Y | Y | 0.2835 | -0.2835 | `mathrock_text_course` | `chunk_0002` |  | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 4 | 4 | Y | Y | 0.2966 | -0.2966 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 5 | 5 |  |  | 0.2979 | -0.2979 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |

### mathrock_pdf_finger_tapping_types - PASS

- Query: Math Rock PDF 中点弦技巧包括哪些类型，双手点弦和持续音点弦怎么练
- Expected sources: mathrock_pdf_steve_h
- Expected keywords any: 点弦, 双手点弦, 持续音, tapping
- Rerank: `False`, candidates: 5
- Source first rank: 3
- Keyword first rank: 3
- Latency: total 0.035s = embed 0.033s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  |  | 0.2381 | -0.2381 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 2 | 2 |  |  | 0.2549 | -0.2549 | `cory_wong_funk_core` | `chunk_0011` |  | one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accomplish some of my signature moves,both in ... |
| 3 | 3 | Y | Y | 0.2737 | -0.2737 | `mathrock_pdf_steve_h` | `chunk_0002` |  | ## 双⼿点弦与交替⼿指点弦 双⼿点弦主要包括交替点弦（双⼿轮流击弦），这可能是数学摇滚吉他⼿最常⽤的点弦技法。但有时你也会需要双⼿同步点奏音符，或⽤按弦⼿凭空锤音并保持音符以构建功能性和声（如⻉斯线）。以下范例（练习1.d）节选⾃我改编的《圣诞⽼人进城》曲谱。为清晰起⻅我将两个声部分开记谱，但实际需同步点奏。我发现让⼤脑同时处理两个点弦音符要困难得多。亲⾃试试感觉如何？有个简化技巧：先分别练习每个声部，再合并演奏。 [IMAGE_B... |
| 4 | 4 |  | Y | 0.2868 | -0.2868 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 5 | 5 | Y | Y | 0.2931 | -0.2931 | `mathrock_pdf_steve_h` | `chunk_0003` |  | ## ⼿指控制+拨弦和弦 现在我们来学习同时拨弦的技巧。这能为你的和弦带来截然不同的质感——因为所有琴弦是被同时拨响，⽽非拨⽚扫弦的连续发声方式。它能提供更精准的动态控制、更高的演奏准确度，以及整体音色的变化。 入⻔练习2.g将不同⼿指组合（注意符头标注的使⽤⼿指）与拇指练习相结合。 [IMAGE_BLOCK:images/82b3d390df1caea14de87e86fde9d5cf5344c06334726ac7921b7f38... |

### mathrock_pdf_tapping_evenness - MISS

- Query: Math Rock PDF 里点弦练习为什么强调音量均匀和手指力量平衡
- Expected sources: mathrock_pdf_steve_h
- Expected keywords any: 均匀, 手指力量, 点弦, 音量
- Rerank: `False`, candidates: 5
- Source first rank: None
- Keyword first rank: None
- Latency: total 0.035s = embed 0.033s + chroma 0.001s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  |  | 0.2250 | -0.2250 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 2 | 2 |  |  | 0.2623 | -0.2623 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 3 | 3 |  |  | 0.2627 | -0.2627 | `cory_wong_funk_core` | `chunk_0011` |  | one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accomplish some of my signature moves,both in ... |
| 4 | 4 |  |  | 0.2774 | -0.2774 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 5 | 5 |  |  | 0.2807 | -0.2807 | `mathrock_text_course` | `chunk_0002` |  | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |

### mathrock_pdf_muting_tapping_noise - PASS

- Query: 点弦时如何用食指内侧和拨弦手掌消音避免杂音
- Expected sources: mathrock_pdf_steve_h
- Expected keywords any: 消音, 杂音, 食指, 手掌
- Rerank: `False`, candidates: 5
- Source first rank: 2
- Keyword first rank: 1
- Latency: total 0.036s = embed 0.034s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  | Y | 0.2686 | -0.2686 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 2 | 2 | Y | Y | 0.3154 | -0.3154 | `mathrock_pdf_steve_h` | `chunk_0003` |  | ## ⼿指控制+拨弦和弦 现在我们来学习同时拨弦的技巧。这能为你的和弦带来截然不同的质感——因为所有琴弦是被同时拨响，⽽非拨⽚扫弦的连续发声方式。它能提供更精准的动态控制、更高的演奏准确度，以及整体音色的变化。 入⻔练习2.g将不同⼿指组合（注意符头标注的使⽤⼿指）与拇指练习相结合。 [IMAGE_BLOCK:images/82b3d390df1caea14de87e86fde9d5cf5344c06334726ac7921b7f38... |
| 3 | 3 | Y | Y | 0.3172 | -0.3172 | `mathrock_pdf_steve_h` | `chunk_0002` |  | ## 双⼿点弦与交替⼿指点弦 双⼿点弦主要包括交替点弦（双⼿轮流击弦），这可能是数学摇滚吉他⼿最常⽤的点弦技法。但有时你也会需要双⼿同步点奏音符，或⽤按弦⼿凭空锤音并保持音符以构建功能性和声（如⻉斯线）。以下范例（练习1.d）节选⾃我改编的《圣诞⽼人进城》曲谱。为清晰起⻅我将两个声部分开记谱，但实际需同步点奏。我发现让⼤脑同时处理两个点弦音符要困难得多。亲⾃试试感觉如何？有个简化技巧：先分别练习每个声部，再合并演奏。 [IMAGE_B... |
| 4 | 4 | Y |  | 0.3498 | -0.3498 | `mathrock_pdf_steve_h` | `chunk_0004` |  | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 5 | 5 | Y |  | 0.3510 | -0.3510 | `mathrock_pdf_steve_h` | `chunk_0010` |  | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |

### mathrock_pdf_facgce_theory - PASS

- Query: FACGCE 调弦在 Math Rock PDF 中如何用开放弦和和弦指型构建声音
- Expected sources: mathrock_pdf_steve_h
- Expected keywords any: FACGCE, 开放弦, 和弦, 调弦
- Rerank: `False`, candidates: 5
- Source first rank: 3
- Keyword first rank: 1
- Latency: total 0.038s = embed 0.036s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  | Y | 0.2230 | -0.2230 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 2 |  | Y | 0.2414 | -0.2414 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 3 | 3 | Y | Y | 0.2481 | -0.2481 | `mathrock_pdf_steve_h` | `chunk_0004` |  | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 4 | 4 |  | Y | 0.2648 | -0.2648 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 5 | 5 | Y | Y | 0.2786 | -0.2786 | `mathrock_pdf_steve_h` | `chunk_0009` |  | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |

### mathrock_pdf_daeacse_scales - PASS

- Query: DAEAC#E 调弦的大调与小调音阶为什么有重复音和开放弦选择
- Expected sources: mathrock_pdf_steve_h
- Expected keywords any: DAEAC#E, 大调, 小调, 音阶
- Rerank: `False`, candidates: 5
- Source first rank: 2
- Keyword first rank: 1
- Latency: total 0.036s = embed 0.034s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  | Y | 0.1562 | -0.1562 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 2 | Y | Y | 0.2210 | -0.2210 | `mathrock_pdf_steve_h` | `chunk_0004` |  | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 3 | 3 | Y | Y | 0.2560 | -0.2560 | `mathrock_pdf_steve_h` | `chunk_0010` |  | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 4 | 4 | Y | Y | 0.2628 | -0.2628 | `mathrock_pdf_steve_h` | `chunk_0009` |  | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |
| 5 | 5 |  | Y | 0.2633 | -0.2633 | `fretboard_handbook_mineru` | `md_chunk_0008` |  | ## 第8章 自然小调音阶 学习目标：构建自然小调音阶的五种指型。理解关系小调和关系大调。 大调音阶只有一种构建公式，但对于小调音阶来说却有许多种构建方式，每一种都有它自己的公式。当人们提到“小调音阶”时，首先想到的应该是自然小调音阶。下面是它的构建公式（大声地读出来）： ## “全、半、全、全、半、全、全” 2级音和3级音之间、5级音和6级音之间是半音关系。可以写成：12^345^678。 [IMAGE_BLOCK:images/3... |

### mathrock_pdf_shell_voicing - MISS

- Query: Math Rock PDF 中 shell voicing 如何用于 m7 G7 maj7 进行
- Expected sources: mathrock_pdf_steve_h
- Expected keywords any: shell, voicing, G7, maj7
- Rerank: `False`, candidates: 5
- Source first rank: None
- Keyword first rank: 1
- Latency: total 0.037s = embed 0.035s + chroma 0.001s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  | Y | 0.2902 | -0.2902 | `mathrock_text_course` | `chunk_0007` |  | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 2 | 2 |  |  | 0.3017 | -0.3017 | `mathrock_text_course` | `chunk_0002` |  | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 3 | 3 |  |  | 0.3050 | -0.3050 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 4 | 4 |  | Y | 0.3119 | -0.3119 | `mathrock_text_course` | `chunk_0004` |  | hey hey hey,let's do it. let's do another math Rock progression. shall we so this one kind of call we have another minor shape gone on AH be min,or we have?bf shocks of one five,we have the three,which is the d.and then... |
| 5 | 5 |  |  | 0.3160 | -0.3160 | `mathrock_text_course` | `chunk_0006` |  | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |

### mathrock_pdf_extended_chords - PASS

- Query: CM9 Dsus4 Em9 Gsus2 C6/9 这类扩展和弦在 PDF 里如何组织
- Expected sources: mathrock_pdf_steve_h
- Expected keywords any: 扩展壳式和弦, 延伸和弦, 壳式按法, extended
- Rerank: `False`, candidates: 5
- Source first rank: 2
- Keyword first rank: 5
- Latency: total 0.036s = embed 0.034s + chroma 0.001s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  |  | 0.2453 | -0.2453 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 2 | Y |  | 0.2724 | -0.2724 | `mathrock_pdf_steve_h` | `chunk_0004` |  | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 3 | 3 |  |  | 0.2881 | -0.2881 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 4 | 4 |  |  | 0.2894 | -0.2894 | `mathrock_text_course` | `chunk_0007` |  | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 5 | 5 | Y | Y | 0.2945 | -0.2945 | `mathrock_pdf_steve_h` | `chunk_0009` |  | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |

### mathrock_pdf_jazz_voicing_progressions - MISS

- Query: Math Rock PDF 后半部分的 jazz voicing progression 如何连接 C6 G6/9 Bm7
- Expected sources: mathrock_pdf_steve_h
- Expected keywords any: C6, G6/9, Bm7, jazz
- Rerank: `False`, candidates: 5
- Source first rank: None
- Keyword first rank: 1
- Latency: total 0.035s = embed 0.033s + chroma 0.001s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  | Y | 0.2514 | -0.2514 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 2 |  |  | 0.2577 | -0.2577 | `mathrock_text_course` | `chunk_0007` |  | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 3 | 3 |  | Y | 0.2580 | -0.2580 | `mathrock_text_course` | `chunk_0006` |  | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |
| 4 | 4 |  |  | 0.2607 | -0.2607 | `mathrock_text_course` | `chunk_0002` |  | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 5 | 5 |  |  | 0.2709 | -0.2709 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |

### fretboard_note_location - PASS

- Query: 吉他指板手册如何训练在每根弦上找到音名和根音
- Expected sources: fretboard_handbook_mineru
- Expected keywords any: 根音, 指板, 音名, 六根弦
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.035s = embed 0.033s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.1767 | -0.1767 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 2 | 2 | Y | Y | 0.2521 | -0.2521 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 3 | 3 |  | Y | 0.2892 | -0.2892 | `mathrock_pdf_steve_h` | `chunk_0010` |  | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 4 | 4 | Y | Y | 0.2945 | -0.2945 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 5 | 5 | Y | Y | 0.3062 | -0.3062 | `fretboard_handbook_mineru` | `md_chunk_0001` |  | [IMAGE_BLOCK:images/8b7ba2f10bcaab55ce9201207558dc26f0f3bd7d10ba53803cf9777452bbd505.jpg] [IMAGE_BLOCK:images/02959d5afc23bcd298aba62bc77aa210b94bfadeb6686e3d159117940e4cf8e5.jpg] [IMAGE_BLOCK:images/bf740813094108cf43a... |

### fretboard_intervals_octave - PASS

- Query: 指板手册里八度音和不同弦组之间的品位关系怎么记忆
- Expected sources: fretboard_handbook_mineru
- Expected keywords any: 八度, 品, 弦, 指板
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.035s = embed 0.033s + chroma 0.001s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2146 | -0.2146 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 2 | 2 | Y | Y | 0.2348 | -0.2348 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 3 | 3 |  | Y | 0.2590 | -0.2590 | `mathrock_pdf_steve_h` | `chunk_0010` |  | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 4 | 4 | Y | Y | 0.2724 | -0.2724 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 5 | 5 |  | Y | 0.2860 | -0.2860 | `mathrock_pdf_steve_h` | `chunk_0004` |  | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |

### fretboard_major_triad_arpeggio - PASS

- Query: 大三和弦琶音由根音大三度纯五度构成，如何在六根弦上练指型
- Expected sources: fretboard_handbook_mineru
- Expected keywords any: 大三和弦, 琶音, 根音, 纯五度
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.036s = embed 0.034s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2052 | -0.2052 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 2 |  | Y | 0.2400 | -0.2400 | `mathrock_pdf_steve_h` | `chunk_0010` |  | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 3 | 3 | Y | Y | 0.2566 | -0.2566 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 4 | 4 |  | Y | 0.2702 | -0.2702 | `mathrock_pdf_steve_h` | `chunk_0004` |  | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 5 | 5 |  | Y | 0.2765 | -0.2765 | `mathrock_pdf_steve_h` | `chunk_0009` |  | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |

### fretboard_minor_diminished_augmented - PASS

- Query: 小三和弦 减三和弦 增三和弦的琶音指型有什么音程差异
- Expected sources: fretboard_handbook_mineru
- Expected keywords any: 小三和弦, 减三和弦, 增三和弦, 琶音
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: 2
- Latency: total 0.036s = embed 0.034s + chroma 0.001s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y |  | 0.2452 | -0.2452 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 2 |  | Y | 0.2825 | -0.2825 | `mathrock_pdf_steve_h` | `chunk_0009` |  | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |
| 3 | 3 |  | Y | 0.2834 | -0.2834 | `mathrock_pdf_steve_h` | `chunk_0010` |  | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 4 | 4 |  | Y | 0.2916 | -0.2916 | `mathrock_pdf_steve_h` | `chunk_0004` |  | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 5 | 5 |  |  | 0.3009 | -0.3009 | `cory_wong_funk_core` | `chunk_0005` |  | the last type of chord voicings I want to talk to you about is triads.and the way that I'm going to think about triads,I'm going to talk about triads today,is in groupings of three strings. I'm going to go in depth on t... |

### fretboard_seventh_arpeggios - PASS

- Query: 大七 小七 属七 小七减五 减七和弦琶音在指板手册中怎么练
- Expected sources: fretboard_handbook_mineru
- Expected keywords any: 大七, 小七, 属七, 减七
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: 4
- Latency: total 0.036s = embed 0.034s + chroma 0.001s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y |  | 0.3017 | -0.3017 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 2 | Y |  | 0.3221 | -0.3221 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 3 | 3 | Y |  | 0.3284 | -0.3284 | `fretboard_handbook_mineru` | `md_chunk_0001` |  | [IMAGE_BLOCK:images/8b7ba2f10bcaab55ce9201207558dc26f0f3bd7d10ba53803cf9777452bbd505.jpg] [IMAGE_BLOCK:images/02959d5afc23bcd298aba62bc77aa210b94bfadeb6686e3d159117940e4cf8e5.jpg] [IMAGE_BLOCK:images/bf740813094108cf43a... |
| 4 | 4 |  | Y | 0.3389 | -0.3389 | `mathrock_pdf_steve_h` | `chunk_0009` |  | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |
| 5 | 5 | Y |  | 0.3430 | -0.3430 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |

### fretboard_open_major_triad_voicing - PASS

- Query: 开放大三和弦声部和牛仔和弦为什么先学琶音再学和弦
- Expected sources: fretboard_handbook_mineru
- Expected keywords any: 开放大三和弦, 牛仔和弦, 琶音, 声部
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: 2
- Latency: total 0.036s = embed 0.034s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y |  | 0.2341 | -0.2341 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 2 | Y | Y | 0.2846 | -0.2846 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 3 | 3 |  | Y | 0.2866 | -0.2866 | `mathrock_pdf_steve_h` | `chunk_0009` |  | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |
| 4 | 4 |  | Y | 0.2916 | -0.2916 | `mathrock_pdf_steve_h` | `chunk_0010` |  | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 5 | 5 |  | Y | 0.3012 | -0.3012 | `mathrock_pdf_steve_h` | `chunk_0004` |  | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |

### fretboard_closed_triad_voicing - PASS

- Query: 密集三和弦和闭合排列在指板上如何构建转位
- Expected sources: fretboard_handbook_mineru
- Expected keywords any: 密集三和弦, 转位, 声部, 指板
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.035s = embed 0.034s + chroma 0.001s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2337 | -0.2337 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 2 | Y | Y | 0.2560 | -0.2560 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 3 | 3 |  | Y | 0.2730 | -0.2730 | `mathrock_pdf_steve_h` | `chunk_0009` |  | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |
| 4 | 4 |  | Y | 0.2761 | -0.2761 | `mathrock_pdf_steve_h` | `chunk_0010` |  | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 5 | 5 |  | Y | 0.2797 | -0.2797 | `mathrock_pdf_steve_h` | `chunk_0004` |  | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |

### fretboard_six_nine_add9 - MISS

- Query: 加九和弦 六九和弦 和属九大九有什么区别
- Expected sources: fretboard_handbook_mineru
- Expected keywords any: 加九, 六九, 属九, 大九
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: None
- Latency: total 0.032s = embed 0.031s + chroma 0.001s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y |  | 0.2693 | -0.2693 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 2 |  |  | 0.3164 | -0.3164 | `mathrock_pdf_steve_h` | `chunk_0004` |  | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 3 | 3 | Y |  | 0.3202 | -0.3202 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 4 | 4 |  |  | 0.3217 | -0.3217 | `mathrock_pdf_steve_h` | `chunk_0009` |  | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |
| 5 | 5 |  |  | 0.3248 | -0.3248 | `mathrock_pdf_steve_h` | `chunk_0010` |  | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |

### cross_open_string_texture - PASS

- Query: 开放弦持续音在 math rock 和指板和弦声部里分别有什么作用
- Expected sources: mathrock_text_course, mathrock_pdf_steve_h, fretboard_handbook_mineru
- Expected keywords any: open string, 开放弦, common tone, 声部
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: 5
- Latency: total 0.035s = embed 0.034s + chroma 0.001s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y |  | 0.2526 | -0.2526 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 2 | Y |  | 0.2588 | -0.2588 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 3 | 3 | Y |  | 0.2659 | -0.2659 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 4 | 4 | Y |  | 0.2675 | -0.2675 | `mathrock_text_course` | `chunk_0007` |  | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 5 | 5 | Y | Y | 0.2768 | -0.2768 | `mathrock_text_course` | `chunk_0006` |  | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |

### cross_sparse_vs_dense_arrangement - PASS

- Query: 编配太密时，funk 的留白和 math rock 的开放弦密集织体有什么不同
- Expected sources: cory_wong_funk_core, mathrock_text_course, mathrock_pdf_steve_h
- Expected keywords any: space, open string, dense, rhythm
- Rerank: `False`, candidates: 5
- Source first rank: 2
- Keyword first rank: 5
- Latency: total 0.036s = embed 0.035s + chroma 0.001s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  |  | 0.2767 | -0.2767 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 2 | 2 | Y |  | 0.2824 | -0.2824 | `mathrock_text_course` | `chunk_0007` |  | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 3 | 3 |  |  | 0.2928 | -0.2928 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 4 | 4 |  |  | 0.2996 | -0.2996 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 5 | 5 | Y | Y | 0.3146 | -0.3146 | `mathrock_pdf_steve_h` | `chunk_0009` |  | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |

### cross_gp5_tapping_features - PASS

- Query: 如果 GP5 检测到大量 tapping hammer pull off open string，应匹配哪些教材证据
- Expected sources: mathrock_text_course, mathrock_pdf_steve_h
- Expected keywords any: tapping, hammer, pull, open string
- Rerank: `False`, candidates: 5
- Source first rank: 2
- Keyword first rank: 2
- Latency: total 0.036s = embed 0.035s + chroma 0.001s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  |  | 0.2887 | -0.2887 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 2 | 2 | Y | Y | 0.3007 | -0.3007 | `mathrock_text_course` | `chunk_0002` |  | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 3 | 3 | Y | Y | 0.3028 | -0.3028 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 4 | 4 |  |  | 0.3065 | -0.3065 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 5 | 5 |  |  | 0.3195 | -0.3195 | `cory_wong_funk_core` | `chunk_0011` |  | one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accomplish some of my signature moves,both in ... |

### cross_gp5_funk_16th_muting - MISS

- Query: 如果 GP5 里十六分音符很多且有 muted strum，应该检索 funk 哪些证据
- Expected sources: cory_wong_funk_core
- Expected keywords any: sixteenth, muted, strum, rhythm
- Rerank: `False`, candidates: 5
- Source first rank: None
- Keyword first rank: 2
- Latency: total 0.036s = embed 0.035s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  |  | 0.2577 | -0.2577 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 2 | 2 |  | Y | 0.2612 | -0.2612 | `mathrock_text_course` | `chunk_0002` |  | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 3 | 3 |  |  | 0.2647 | -0.2647 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 4 | 4 |  |  | 0.2749 | -0.2749 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 5 | 5 |  |  | 0.2796 | -0.2796 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |

### cross_voicing_advice - PASS

- Query: 想把普通和弦进行改成更有风格的 guitar voicing，可以参考 funk sparse voicing 还是 math rock maj9 shell voicing
- Expected sources: cory_wong_funk_core, mathrock_pdf_steve_h
- Expected keywords any: voicing, maj9, shell, sparse
- Rerank: `False`, candidates: 5
- Source first rank: 2
- Keyword first rank: 1
- Latency: total 0.037s = embed 0.035s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  | Y | 0.2085 | -0.2085 | `mathrock_text_course` | `chunk_0007` |  | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 2 | 2 | Y | Y | 0.2319 | -0.2319 | `cory_wong_funk_core` | `chunk_0004` |  | that's just actually articulating and playing a different type of phrasing on it,but it's one way to use that voicing.嗯。minor seven chords are super common in funk music and especially in a lot of the music that i play,... |
| 3 | 3 | Y | Y | 0.2363 | -0.2363 | `cory_wong_funk_core` | `chunk_0003` |  | this next series of lessons is about cord voicings and cord moves that I use in my playing.especially,in the context of funk,music now most of these voice o icings start from the caged system if you're not familiar with... |
| 4 | 4 |  | Y | 0.2434 | -0.2434 | `mathrock_text_course` | `chunk_0003` |  | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 5 | 5 |  |  | 0.2482 | -0.2482 | `mathrock_text_course` | `chunk_0002` |  | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |

### cross_arpeggio_to_riff - PASS

- Query: 如何把指板手册里的琶音指型转化成 math rock riff 或填充句
- Expected sources: fretboard_handbook_mineru, mathrock_text_course
- Expected keywords any: 琶音, arpeggio, riff, 指型
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.036s = embed 0.034s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2232 | -0.2232 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 2 | 2 | Y |  | 0.2518 | -0.2518 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 3 | 3 |  | Y | 0.2907 | -0.2907 | `mathrock_pdf_steve_h` | `chunk_0010` |  | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 4 | 4 |  | Y | 0.2942 | -0.2942 | `cory_wong_funk_core` | `chunk_0011` |  | one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accomplish some of my signature moves,both in ... |
| 5 | 5 | Y | Y | 0.2979 | -0.2979 | `fretboard_handbook_mineru` | `md_chunk_0001` |  | [IMAGE_BLOCK:images/8b7ba2f10bcaab55ce9201207558dc26f0f3bd7d10ba53803cf9777452bbd505.jpg] [IMAGE_BLOCK:images/02959d5afc23bcd298aba62bc77aa210b94bfadeb6686e3d159117940e4cf8e5.jpg] [IMAGE_BLOCK:images/bf740813094108cf43a... |

### cross_alternate_tuning_limit - PASS

- Query: 为什么特殊调弦下的和弦指型不能直接套用到标准调弦指板知识
- Expected sources: mathrock_text_course, mathrock_pdf_steve_h, fretboard_handbook_mineru
- Expected keywords any: tuning, 调弦, 指型, standard
- Rerank: `False`, candidates: 5
- Source first rank: 1
- Keyword first rank: 2
- Latency: total 0.039s = embed 0.037s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y |  | 0.2395 | -0.2395 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 2 | 2 | Y | Y | 0.2417 | -0.2417 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 3 | 3 | Y | Y | 0.2719 | -0.2719 | `mathrock_pdf_steve_h` | `chunk_0004` |  | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 4 | 4 | Y | Y | 0.2729 | -0.2729 | `mathrock_pdf_steve_h` | `chunk_0010` |  | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 5 | 5 | Y |  | 0.2954 | -0.2954 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |

### cross_rhythm_plus_harmony - MISS

- Query: 如何同时考虑 funk 节奏律动和 math rock 扩展和弦色彩来做吉他编配
- Expected sources: cory_wong_funk_core, mathrock_pdf_steve_h
- Expected keywords any: rhythm, groove, extended, 和弦
- Rerank: `False`, candidates: 5
- Source first rank: None
- Keyword first rank: 1
- Latency: total 0.038s = embed 0.037s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 |  | Y | 0.2877 | -0.2877 | `fretboard_handbook_mineru` | `md_chunk_0037` |  | ## 关于作 巴雷特·塔利亚里诺自1987年起在MI执教，并且在1994年成为奥地利维也纳霍纳音乐学校摇滚系主任。他通过乘坐轮船、火车、公共汽车、飞机、卡车或者汽车去往各地进行无数次的公演和巡回演出。同时他还开展了许多教学研讨班、进修班以及私人课程。 巴雷特参加过许多CD、电视节目、广播商业节目和卡拉OK伴奏的吉他演奏录制。他的教学被著名的杂志《经典摇滚吉他独奏》（ClassicRockGuitarSoloing）中的星级教学视频收录... |
| 2 | 2 |  | Y | 0.2969 | -0.2969 | `fretboard_handbook_mineru` | `md_chunk_0021` |  | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 3 | 3 |  |  | 0.2974 | -0.2974 | `mathrock_text_course` | `chunk_0007` |  | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 4 | 4 |  | Y | 0.2985 | -0.2985 | `mathrock_text_course` | `chunk_0002` |  | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 5 | 5 |  | Y | 0.3013 | -0.3013 | `fretboard_handbook_mineru` | `md_chunk_0002` |  | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
