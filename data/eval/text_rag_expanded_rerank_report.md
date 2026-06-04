# Text RAG Retrieval Evaluation

## Summary

- Collection: `guitar_text_chunks_qwen3_06b` (68 docs)
- Model: `models\embedding\qwen3-embedding-0.6b` on `cuda`, dim=1024
- Tests: 40, TopK: 5
- Rerank: `True`, candidates: 25
- Pass all: 40/40
- Source Hit@1: 39/40
- Source Hit@K: 40/40
- Keyword Hit@1: 33/40
- Keyword Hit@K: 40/40
- Avg latency/query: 0.048s
- Median latency/query: 0.038s

## Cases

### funk_note_location_prereq - PASS

- Query: Cory Wong funk 课程里为什么要求先掌握指板音名和 circle of fourths
- Expected sources: cory_wong_funk_core
- Expected keywords any: note location, circle of fourths, circle of fifths
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.314s = embed 0.248s + chroma 0.066s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 7 | Y | Y | 0.2763 | -0.1613 | `cory_wong_funk_core` | `chunk_0001` | circle, cory, fourths, funk, of, wong | hey,what's up? this is cory wong.welcome to my lesson package,I'm super excited about this this is kind of an all inclusive masterclass I'm going to talk a lot about music,a lot about guitar,a lot about studio versus li... |
| 2 | 10 | Y | Y | 0.2918 | -0.1868 | `cory_wong_funk_core` | `chunk_0002` | circle, cory, funk, of, wong | so if you have canda minor.next to it,you're going to have f and d minor,and you're going to have g and e minor. those six chords are all the major and minor triads in the key of c.and if you shift it over,you're going ... |
| 3 | 3 |  |  | 0.2480 | -0.1880 | `fretboard_handbook_mineru` | `md_chunk_0021` | 指板 | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 4 | 11 | Y |  | 0.2926 | -0.1976 | `cory_wong_funk_core` | `chunk_0011` | cory, funk, of, wong | one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accomplish some of my signature moves,both in ... |
| 5 | 12 | Y |  | 0.2938 | -0.1988 | `cory_wong_funk_core` | `chunk_0004` | cory, funk, of, wong | that's just actually articulating and playing a different type of phrasing on it,but it's one way to use that voicing.嗯。minor seven chords are super common in funk music and especially in a lot of the music that i play,... |

### funk_muted_chuck_density - PASS

- Query: funk rhythm guitar 里 muted chuck ghost note 作为十六分律动怎么安排
- Expected sources: cory_wong_funk_core
- Expected keywords any: muted, chuck, sixteenth, ghost
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.050s = embed 0.047s + chroma 0.004s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 4 | Y | Y | 0.2561 | -0.1411 | `cory_wong_funk_core` | `chunk_0011` | funk, ghost, guitar, muted, note, rhythm | one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accomplish some of my signature moves,both in ... |
| 2 | 6 | Y | Y | 0.2651 | -0.1501 | `cory_wong_funk_core` | `chunk_0008` | chuck, funk, guitar, muted, note, rhythm | let's dive deeper into that bongo conga style to me,that world of ribbon guitar playing is the bubble. now you hear this sort of thing on a lot of songs,it's classic.billy IE,Jean,you hear it on?a lot of other songs tha... |
| 3 | 8 | Y | Y | 0.2654 | -0.1504 | `cory_wong_funk_core` | `chunk_0012` | chuck, funk, guitar, muted, note, rhythm | another one of my signature guitar moves is this sort of thing.that sort of thing you hear me do that all the time now part of how I get that sound obviously it's double strokes it's two notes at the same time.now,in or... |
| 4 | 9 | Y | Y | 0.2666 | -0.1516 | `cory_wong_funk_core` | `chunk_0009` | funk, guitar, muted, note, rhythm, 律动 | now something to really note is.there's a difference between timing.patterns.and groove.they all kind of make up this thing that we call ribbon.那timing is。where you're placing something.right? the timing is a hundred an... |
| 5 | 14 | Y | Y | 0.2882 | -0.1632 | `cory_wong_funk_core` | `chunk_0007` | chuck, funk, ghost, guitar, muted, note, rhythm | today I want to give you a little ribbon guitar primer now I am.what I would consider a consummate ribbon guitar player I love,the ribbon guitar I love,the role and I think it's often actually a neglected role.lot of gu... |

### funk_leave_space_for_band - PASS

- Query: funk 吉他伴奏为什么要给 bass 和 drums 留空间
- Expected sources: cory_wong_funk_core
- Expected keywords any: space, bass, drums, band
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.051s = embed 0.047s + chroma 0.004s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 7 | Y | Y | 0.3248 | -0.2498 | `cory_wong_funk_core` | `chunk_0007` | drums, funk | today I want to give you a little ribbon guitar primer now I am.what I would consider a consummate ribbon guitar player I love,the ribbon guitar I love,the role and I think it's often actually a neglected role.lot of gu... |
| 2 | 3 | Y | Y | 0.3154 | -0.2504 | `cory_wong_funk_core` | `chunk_0010` | funk | now those are a couple of my main approaches to ribbon guitar,but some other things just to consider are ribbon IC density.range on the instrument.tone.and space.OK so.sometimes a song is going to call for a ribbon guit... |
| 3 | 6 | Y | Y | 0.3199 | -0.2549 | `cory_wong_funk_core` | `chunk_0006` | funk | now that you've gone through all these,different chord voicings and hopefully you've paused and put in the practice and really started to understand how the voicings work with the corresponding scale.and pentatonic scal... |
| 4 | 8 | Y | Y | 0.3356 | -0.2706 | `cory_wong_funk_core` | `chunk_0008` | funk | let's dive deeper into that bongo conga style to me,that world of ribbon guitar playing is the bubble. now you hear this sort of thing on a lot of songs,it's classic.billy IE,Jean,you hear it on?a lot of other songs tha... |
| 5 | 11 | Y |  | 0.3373 | -0.2723 | `cory_wong_funk_core` | `chunk_0011` | funk | one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accomplish some of my signature moves,both in ... |

### funk_right_hand_pocket - PASS

- Query: Cory Wong funk 右手节奏 pocket 和 groove 的训练重点
- Expected sources: cory_wong_funk_core
- Expected keywords any: right hand, pocket, groove, rhythm
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.100s = embed 0.096s + chroma 0.004s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 2 | Y | Y | 0.2970 | -0.1920 | `cory_wong_funk_core` | `chunk_0011` | cory, funk, groove, pocket, wong | one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accomplish some of my signature moves,both in ... |
| 2 | 5 | Y | Y | 0.3031 | -0.2081 | `cory_wong_funk_core` | `chunk_0009` | cory, funk, groove, wong | now something to really note is.there's a difference between timing.patterns.and groove.they all kind of make up this thing that we call ribbon.那timing is。where you're placing something.right? the timing is a hundred an... |
| 3 | 7 | Y | Y | 0.3151 | -0.2201 | `cory_wong_funk_core` | `chunk_0012` | cory, funk, groove, wong | another one of my signature guitar moves is this sort of thing.that sort of thing you hear me do that all the time now part of how I get that sound obviously it's double strokes it's two notes at the same time.now,in or... |
| 4 | 9 | Y | Y | 0.3206 | -0.2256 | `cory_wong_funk_core` | `chunk_0008` | cory, funk, groove, wong | let's dive deeper into that bongo conga style to me,that world of ribbon guitar playing is the bubble. now you hear this sort of thing on a lot of songs,it's classic.billy IE,Jean,you hear it on?a lot of other songs tha... |
| 5 | 11 | Y | Y | 0.3327 | -0.2477 | `cory_wong_funk_core` | `chunk_0004` | cory, funk, wong | that's just actually articulating and playing a different type of phrasing on it,but it's one way to use that voicing.嗯。minor seven chords are super common in funk music and especially in a lot of the music that i play,... |

### funk_syncopation_comping - PASS

- Query: funk comping 如何用 syncopation 和短促和弦切分
- Expected sources: cory_wong_funk_core
- Expected keywords any: syncopation, comping, rhythm, chord
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.053s = embed 0.050s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 2 | Y | Y | 0.2977 | -0.2227 | `cory_wong_funk_core` | `chunk_0004` | comping, funk | that's just actually articulating and playing a different type of phrasing on it,but it's one way to use that voicing.嗯。minor seven chords are super common in funk music and especially in a lot of the music that i play,... |
| 2 | 4 | Y | Y | 0.3097 | -0.2347 | `cory_wong_funk_core` | `chunk_0011` | comping, funk | one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accomplish some of my signature moves,both in ... |
| 3 | 7 | Y | Y | 0.3240 | -0.2490 | `cory_wong_funk_core` | `chunk_0008` | comping, funk | let's dive deeper into that bongo conga style to me,that world of ribbon guitar playing is the bubble. now you hear this sort of thing on a lot of songs,it's classic.billy IE,Jean,you hear it on?a lot of other songs tha... |
| 4 | 10 | Y | Y | 0.3355 | -0.2605 | `cory_wong_funk_core` | `chunk_0003` | comping, funk | this next series of lessons is about cord voicings and cord moves that I use in my playing.especially,in the context of funk,music now most of these voice o icings start from the caged system if you're not familiar with... |
| 5 | 12 | Y | Y | 0.3370 | -0.2620 | `cory_wong_funk_core` | `chunk_0010` | comping, funk | now those are a couple of my main approaches to ribbon guitar,but some other things just to consider are ribbon IC density.range on the instrument.tone.and space.OK so.sometimes a song is going to call for a ribbon guit... |

### funk_percussive_guitar_role - PASS

- Query: funk guitar 在乐队中更像打击乐还是和声乐器，如何处理 percussive attack
- Expected sources: cory_wong_funk_core
- Expected keywords any: percussive, attack, rhythm, guitar
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.046s = embed 0.043s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2861 | -0.2011 | `cory_wong_funk_core` | `chunk_0007` | funk, guitar, percussive | today I want to give you a little ribbon guitar primer now I am.what I would consider a consummate ribbon guitar player I love,the ribbon guitar I love,the role and I think it's often actually a neglected role.lot of gu... |
| 2 | 2 | Y | Y | 0.2984 | -0.2134 | `cory_wong_funk_core` | `chunk_0010` | attack, funk, guitar | now those are a couple of my main approaches to ribbon guitar,but some other things just to consider are ribbon IC density.range on the instrument.tone.and space.OK so.sometimes a song is going to call for a ribbon guit... |
| 3 | 3 | Y | Y | 0.2985 | -0.2235 | `cory_wong_funk_core` | `chunk_0006` | funk, guitar | now that you've gone through all these,different chord voicings and hopefully you've paused and put in the practice and really started to understand how the voicings work with the corresponding scale.and pentatonic scal... |
| 4 | 6 | Y | Y | 0.3203 | -0.2353 | `cory_wong_funk_core` | `chunk_0011` | funk, guitar, percussive | one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accomplish some of my signature moves,both in ... |
| 5 | 12 | Y | Y | 0.3402 | -0.2452 | `cory_wong_funk_core` | `chunk_0012` | attack, funk, guitar, percussive | another one of my signature guitar moves is this sort of thing.that sort of thing you hear me do that all the time now part of how I get that sound obviously it's double strokes it's two notes at the same time.now,in or... |

### funk_triads_relative_minor - PASS

- Query: funk 课程中 major minor triads 和 relative minor 为什么是前置知识
- Expected sources: cory_wong_funk_core
- Expected keywords any: major, minor, triads, relative minor
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.051s = embed 0.048s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 2 | Y | Y | 0.2498 | -0.1448 | `cory_wong_funk_core` | `chunk_0002` | funk, major, minor, relative, triads | so if you have canda minor.next to it,you're going to have f and d minor,and you're going to have g and e minor. those six chords are all the major and minor triads in the key of c.and if you shift it over,you're going ... |
| 2 | 1 | Y | Y | 0.2447 | -0.1497 | `cory_wong_funk_core` | `chunk_0005` | funk, major, minor, triads | the last type of chord voicings I want to talk to you about is triads.and the way that I'm going to think about triads,I'm going to talk about triads today,is in groupings of three strings. I'm going to go in depth on t... |
| 3 | 4 | Y | Y | 0.2797 | -0.1747 | `cory_wong_funk_core` | `chunk_0003` | funk, major, minor, relative, triads | this next series of lessons is about cord voicings and cord moves that I use in my playing.especially,in the context of funk,music now most of these voice o icings start from the caged system if you're not familiar with... |
| 4 | 5 | Y | Y | 0.2847 | -0.1997 | `cory_wong_funk_core` | `chunk_0004` | funk, major, minor | that's just actually articulating and playing a different type of phrasing on it,but it's one way to use that voicing.嗯。minor seven chords are super common in funk music and especially in a lot of the music that i play,... |
| 5 | 9 | Y | Y | 0.3265 | -0.2215 | `cory_wong_funk_core` | `chunk_0001` | funk, major, minor, relative, triads | hey,what's up? this is cory wong.welcome to my lesson package,I'm super excited about this this is kind of an all inclusive masterclass I'm going to talk a lot about music,a lot about guitar,a lot about studio versus li... |

### funk_caged_system - PASS

- Query: CAGED system 在 Cory Wong 课程里如何组织 chord shape 和 scale shape
- Expected sources: cory_wong_funk_core
- Expected keywords any: caged, chord shapes, scale shapes
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.041s = embed 0.038s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2556 | -0.1306 | `cory_wong_funk_core` | `chunk_0002` | caged, chord, cory, scale, shape, system, wong | so if you have canda minor.next to it,you're going to have f and d minor,and you're going to have g and e minor. those six chords are all the major and minor triads in the key of c.and if you shift it over,you're going ... |
| 2 | 3 | Y | Y | 0.2670 | -0.1420 | `cory_wong_funk_core` | `chunk_0003` | caged, chord, cory, scale, shape, system, wong | this next series of lessons is about cord voicings and cord moves that I use in my playing.especially,in the context of funk,music now most of these voice o icings start from the caged system if you're not familiar with... |
| 3 | 6 | Y |  | 0.2833 | -0.1783 | `cory_wong_funk_core` | `chunk_0004` | chord, cory, scale, shape, wong | that's just actually articulating and playing a different type of phrasing on it,but it's one way to use that voicing.嗯。minor seven chords are super common in funk music and especially in a lot of the music that i play,... |
| 4 | 11 | Y | Y | 0.3090 | -0.1940 | `cory_wong_funk_core` | `chunk_0001` | caged, cory, scale, shape, system, wong | hey,what's up? this is cory wong.welcome to my lesson package,I'm super excited about this this is kind of an all inclusive masterclass I'm going to talk a lot about music,a lot about guitar,a lot about studio versus li... |
| 5 | 10 | Y |  | 0.3053 | -0.2003 | `cory_wong_funk_core` | `chunk_0005` | chord, cory, scale, shape, wong | the last type of chord voicings I want to talk to you about is triads.and the way that I'm going to think about triads,I'm going to talk about triads today,is in groupings of three strings. I'm going to go in depth on t... |

### mathrock_text_dadgad_open_drone - PASS

- Query: math rock 文本课 DADGAD 调弦如何产生 open string drone 和 common tone
- Expected sources: mathrock_text_course
- Expected keywords any: dadgad, open, common tone, drone
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.041s = embed 0.038s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 4 | Y | Y | 0.3017 | -0.1867 | `mathrock_text_course` | `chunk_0002` | common, dadgad, drone, math, open, rock, string, tone | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 2 | 6 | Y | Y | 0.3031 | -0.1981 | `mathrock_text_course` | `chunk_0007` | common, drone, math, open, rock, string, tone | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 3 | 7 | Y | Y | 0.3106 | -0.2056 | `mathrock_text_course` | `chunk_0006` | common, drone, math, open, rock, string, tone | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |
| 4 | 5 | Y | Y | 0.3030 | -0.2080 | `mathrock_text_course` | `chunk_0003` | dadgad, drone, math, open, rock, string | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 5 | 2 |  | Y | 0.2950 | -0.2200 | `mathrock_pdf_steve_h` | `chunk_0004` | math, open, rock, string, 调弦 | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |

### mathrock_text_tapped_power_chords - PASS

- Query: math rock 文本课里 tapped power chords 如何在旋律中使用
- Expected sources: mathrock_text_course
- Expected keywords any: tap, power chord, tapped, melody
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.035s = embed 0.033s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2780 | -0.2030 | `mathrock_text_course` | `chunk_0003` | math, power, rock, tapped | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 2 | 3 | Y | Y | 0.2988 | -0.2138 | `mathrock_text_course` | `chunk_0002` | chords, math, power, rock, tapped | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 3 | 4 | Y | Y | 0.3002 | -0.2152 | `mathrock_text_course` | `chunk_0006` | chords, math, power, rock, tapped | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |
| 4 | 5 | Y | Y | 0.3094 | -0.2344 | `mathrock_text_course` | `chunk_0007` | math, power, rock, tapped | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 5 | 14 | Y | Y | 0.3324 | -0.2474 | `mathrock_text_course` | `chunk_0004` | chords, math, power, rock, tapped | hey hey hey,let's do it. let's do another math Rock progression. shall we so this one kind of call we have another minor shape gone on AH be min,or we have?bf shocks of one five,we have the three,which is the d.and then... |

### mathrock_text_hammer_pull_slide - PASS

- Query: math rock riff 用 hammer on pull off slide 制造高密度连奏
- Expected sources: mathrock_text_course
- Expected keywords any: hammer, pull, slide, legato
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.037s = embed 0.035s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2358 | -0.1208 | `mathrock_text_course` | `chunk_0003` | hammer, math, off, on, pull, riff, rock, slide | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 2 | 2 | Y | Y | 0.2442 | -0.1292 | `mathrock_text_course` | `chunk_0002` | hammer, math, off, on, pull, riff, rock, slide | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 3 | 5 | Y | Y | 0.2779 | -0.1629 | `mathrock_text_course` | `chunk_0006` | hammer, math, off, on, pull, riff, rock, slide | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |
| 4 | 3 | Y | Y | 0.2703 | -0.1653 | `mathrock_text_course` | `chunk_0005` | hammer, math, off, on, pull, riff, rock | we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have AC sharp right there and e. ,so we have ... |
| 5 | 6 | Y | Y | 0.2848 | -0.1798 | `mathrock_text_course` | `chunk_0001` | hammer, math, off, on, pull, rock, slide | so what are the basics of math rock or midwest emo we're going to take a look at this little progression right here which is in the key of dd major,and i have it in a very common alternate tuning of dad gad it's going t... |

### mathrock_text_percussive_slap - PASS

- Query: math rock midwest emo 编配里 percussive slap 和 dead note 的作用
- Expected sources: mathrock_text_course
- Expected keywords any: percussive, slap, dead, rhythm
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.038s = embed 0.035s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2657 | -0.1607 | `mathrock_text_course` | `chunk_0002` | emo, math, midwest, note, percussive, rock, slap | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 2 | 3 | Y | Y | 0.2973 | -0.1823 | `mathrock_text_course` | `chunk_0005` | dead, emo, math, midwest, note, percussive, rock, slap | we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have AC sharp right there and e. ,so we have ... |
| 3 | 4 | Y | Y | 0.2979 | -0.1829 | `mathrock_text_course` | `chunk_0007` | dead, emo, math, midwest, note, percussive, rock, slap | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 4 | 5 | Y | Y | 0.2994 | -0.1844 | `mathrock_text_course` | `chunk_0006` | dead, emo, math, midwest, note, percussive, rock, slap | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |
| 5 | 2 | Y |  | 0.2743 | -0.1893 | `mathrock_text_course` | `chunk_0003` | emo, math, midwest, note, rock | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |

### mathrock_text_theme_variation - PASS

- Query: math rock progression 如何从简单主题逐步加复杂 theme variation
- Expected sources: mathrock_text_course
- Expected keywords any: theme, variation, progression, complex
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.035s = embed 0.033s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.3376 | -0.2526 | `mathrock_text_course` | `chunk_0007` | math, progression, rock, theme, variation | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 2 | 3 | Y | Y | 0.3479 | -0.2629 | `mathrock_text_course` | `chunk_0006` | math, progression, rock, theme, variation | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |
| 3 | 8 | Y | Y | 0.3632 | -0.2782 | `mathrock_text_course` | `chunk_0002` | math, progression, rock, theme, variation | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 4 | 10 | Y | Y | 0.3655 | -0.2805 | `mathrock_text_course` | `chunk_0001` | math, progression, rock, theme, variation | so what are the basics of math rock or midwest emo we're going to take a look at this little progression right here which is in the key of dd major,and i have it in a very common alternate tuning of dad gad it's going t... |
| 5 | 6 | Y | Y | 0.3585 | -0.2835 | `mathrock_text_course` | `chunk_0003` | math, rock, theme, variation | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |

### mathrock_text_open_string_pull_off - PASS

- Query: midwest emo 乐句里 slide 后 pull off 到 open string 的色彩
- Expected sources: mathrock_text_course
- Expected keywords any: slide, pull off, open string
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.038s = embed 0.035s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2427 | -0.1377 | `mathrock_text_course` | `chunk_0002` | emo, midwest, off, open, pull, slide, string | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 2 | 2 | Y | Y | 0.2446 | -0.1396 | `mathrock_text_course` | `chunk_0006` | emo, midwest, off, open, pull, slide, string | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |
| 3 | 3 | Y | Y | 0.2449 | -0.1399 | `mathrock_text_course` | `chunk_0003` | emo, midwest, off, open, pull, slide, string | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 4 | 4 | Y | Y | 0.2490 | -0.1540 | `mathrock_text_course` | `chunk_0005` | emo, midwest, off, open, pull, string | we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have AC sharp right there and e. ,so we have ... |
| 5 | 7 | Y | Y | 0.2648 | -0.1598 | `mathrock_text_course` | `chunk_0001` | emo, midwest, off, open, pull, slide, string | so what are the basics of math rock or midwest emo we're going to take a look at this little progression right here which is in the key of dd major,and i have it in a very common alternate tuning of dad gad it's going t... |

### mathrock_text_harp_harmonics - PASS

- Query: math rock 教学课里 harp harmonics 可以怎样启发 riff writing
- Expected sources: mathrock_text_course
- Expected keywords any: harp, harmonics, riff
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.039s = embed 0.036s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 6 | Y | Y | 0.2969 | -0.2019 | `mathrock_text_course` | `chunk_0006` | harmonics, harp, math, riff, rock, writing | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |
| 2 | 2 | Y | Y | 0.2818 | -0.2068 | `mathrock_text_course` | `chunk_0007` | math, riff, rock, writing | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 3 | 7 | Y | Y | 0.2997 | -0.2147 | `mathrock_text_course` | `chunk_0002` | harp, math, riff, rock, writing | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 4 | 4 | Y | Y | 0.2902 | -0.2152 | `mathrock_text_course` | `chunk_0003` | math, riff, rock, writing | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 5 | 10 | Y | Y | 0.3117 | -0.2167 | `mathrock_text_course` | `chunk_0005` | harmonics, harp, math, riff, rock, writing | we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have AC sharp right there and e. ,so we have ... |

### mathrock_text_alternate_tuning_dependency - PASS

- Query: 为什么 math rock 的指型常常依赖 alternate tuning，不能直接搬到标准调弦
- Expected sources: mathrock_text_course
- Expected keywords any: alternate tuning, tuning, shape, dependency
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.038s = embed 0.035s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 3 | Y | Y | 0.2835 | -0.2085 | `mathrock_text_course` | `chunk_0002` | alternate, math, rock, tuning | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 2 | 4 | Y | Y | 0.2966 | -0.2216 | `mathrock_text_course` | `chunk_0003` | alternate, math, rock, tuning | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 3 | 6 | Y | Y | 0.2987 | -0.2237 | `mathrock_text_course` | `chunk_0006` | alternate, math, rock, tuning | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |
| 4 | 7 | Y | Y | 0.3104 | -0.2354 | `mathrock_text_course` | `chunk_0007` | alternate, math, rock, tuning | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 5 | 11 |  | Y | 0.3239 | -0.2389 | `mathrock_pdf_steve_h` | `chunk_0004` | alternate, math, rock, tuning, 为什么, 调弦 | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |

### mathrock_pdf_finger_tapping_types - PASS

- Query: Math Rock PDF 中点弦技巧包括哪些类型，双手点弦和持续音点弦怎么练
- Expected sources: mathrock_pdf_steve_h
- Expected keywords any: 点弦, 双手点弦, 持续音, tapping
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.038s = embed 0.035s + chroma 0.004s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 3 | Y | Y | 0.2737 | -0.1487 | `mathrock_pdf_steve_h` | `chunk_0002` | math, pdf, rock, 点弦 | ## 双⼿点弦与交替⼿指点弦 双⼿点弦主要包括交替点弦（双⼿轮流击弦），这可能是数学摇滚吉他⼿最常⽤的点弦技法。但有时你也会需要双⼿同步点奏音符，或⽤按弦⼿凭空锤音并保持音符以构建功能性和声（如⻉斯线）。以下范例（练习1.d）节选⾃我改编的《圣诞⽼人进城》曲谱。为清晰起⻅我将两个声部分开记谱，但实际需同步点奏。我发现让⼤脑同时处理两个点弦音符要困难得多。亲⾃试试感觉如何？有个简化技巧：先分别练习每个声部，再合并演奏。 [IMAGE_B... |
| 2 | 5 | Y | Y | 0.2931 | -0.1781 | `mathrock_pdf_steve_h` | `chunk_0003` | math, pdf, rock | ## ⼿指控制+拨弦和弦 现在我们来学习同时拨弦的技巧。这能为你的和弦带来截然不同的质感——因为所有琴弦是被同时拨响，⽽非拨⽚扫弦的连续发声方式。它能提供更精准的动态控制、更高的演奏准确度，以及整体音色的变化。 入⻔练习2.g将不同⼿指组合（注意符头标注的使⽤⼿指）与拇指练习相结合。 [IMAGE_BLOCK:images/82b3d390df1caea14de87e86fde9d5cf5344c06334726ac7921b7f38... |
| 3 | 11 | Y | Y | 0.3200 | -0.1950 | `mathrock_pdf_steve_h` | `chunk_0004` | math, pdf, rock, 点弦 | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 4 | 12 | Y | Y | 0.3233 | -0.1983 | `mathrock_pdf_steve_h` | `chunk_0010` | math, pdf, rock, 点弦 | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 5 | 19 | Y | Y | 0.3466 | -0.2316 | `mathrock_pdf_steve_h` | `chunk_0009` | math, pdf, rock | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |

### mathrock_pdf_tapping_evenness - PASS

- Query: Math Rock PDF 里点弦练习为什么强调音量均匀和手指力量平衡
- Expected sources: mathrock_pdf_steve_h
- Expected keywords any: 均匀, 手指力量, 点弦, 音量
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.036s = embed 0.034s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 6 | Y | Y | 0.2830 | -0.1580 | `mathrock_pdf_steve_h` | `chunk_0002` | math, pdf, rock, 点弦 | ## 双⼿点弦与交替⼿指点弦 双⼿点弦主要包括交替点弦（双⼿轮流击弦），这可能是数学摇滚吉他⼿最常⽤的点弦技法。但有时你也会需要双⼿同步点奏音符，或⽤按弦⼿凭空锤音并保持音符以构建功能性和声（如⻉斯线）。以下范例（练习1.d）节选⾃我改编的《圣诞⽼人进城》曲谱。为清晰起⻅我将两个声部分开记谱，但实际需同步点奏。我发现让⼤脑同时处理两个点弦音符要困难得多。亲⾃试试感觉如何？有个简化技巧：先分别练习每个声部，再合并演奏。 [IMAGE_B... |
| 2 | 14 | Y | Y | 0.3017 | -0.1767 | `mathrock_pdf_steve_h` | `chunk_0004` | math, pdf, rock, 点弦 | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 3 | 13 | Y |  | 0.3013 | -0.1863 | `mathrock_pdf_steve_h` | `chunk_0003` | math, pdf, rock | ## ⼿指控制+拨弦和弦 现在我们来学习同时拨弦的技巧。这能为你的和弦带来截然不同的质感——因为所有琴弦是被同时拨响，⽽非拨⽚扫弦的连续发声方式。它能提供更精准的动态控制、更高的演奏准确度，以及整体音色的变化。 入⻔练习2.g将不同⼿指组合（注意符头标注的使⽤⼿指）与拇指练习相结合。 [IMAGE_BLOCK:images/82b3d390df1caea14de87e86fde9d5cf5344c06334726ac7921b7f38... |
| 4 | 18 | Y | Y | 0.3206 | -0.1956 | `mathrock_pdf_steve_h` | `chunk_0010` | math, pdf, rock, 点弦 | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 5 | 2 |  |  | 0.2623 | -0.2073 | `mathrock_text_course` | `chunk_0003` | math, rock | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |

### mathrock_pdf_muting_tapping_noise - PASS

- Query: 点弦时如何用食指内侧和拨弦手掌消音避免杂音
- Expected sources: mathrock_pdf_steve_h
- Expected keywords any: 消音, 杂音, 食指, 手掌
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.037s = embed 0.034s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 3 | Y | Y | 0.3172 | -0.3072 | `mathrock_pdf_steve_h` | `chunk_0002` | 点弦 | ## 双⼿点弦与交替⼿指点弦 双⼿点弦主要包括交替点弦（双⼿轮流击弦），这可能是数学摇滚吉他⼿最常⽤的点弦技法。但有时你也会需要双⼿同步点奏音符，或⽤按弦⼿凭空锤音并保持音符以构建功能性和声（如⻉斯线）。以下范例（练习1.d）节选⾃我改编的《圣诞⽼人进城》曲谱。为清晰起⻅我将两个声部分开记谱，但实际需同步点奏。我发现让⼤脑同时处理两个点弦音符要困难得多。亲⾃试试感觉如何？有个简化技巧：先分别练习每个声部，再合并演奏。 [IMAGE_B... |
| 2 | 2 | Y | Y | 0.3154 | -0.3154 | `mathrock_pdf_steve_h` | `chunk_0003` |  | ## ⼿指控制+拨弦和弦 现在我们来学习同时拨弦的技巧。这能为你的和弦带来截然不同的质感——因为所有琴弦是被同时拨响，⽽非拨⽚扫弦的连续发声方式。它能提供更精准的动态控制、更高的演奏准确度，以及整体音色的变化。 入⻔练习2.g将不同⼿指组合（注意符头标注的使⽤⼿指）与拇指练习相结合。 [IMAGE_BLOCK:images/82b3d390df1caea14de87e86fde9d5cf5344c06334726ac7921b7f38... |
| 3 | 4 | Y |  | 0.3498 | -0.3398 | `mathrock_pdf_steve_h` | `chunk_0004` | 点弦 | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 4 | 5 | Y |  | 0.3510 | -0.3410 | `mathrock_pdf_steve_h` | `chunk_0010` | 点弦 | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 5 | 8 |  |  | 0.3677 | -0.3677 | `cory_wong_funk_core` | `chunk_0011` |  | one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accomplish some of my signature moves,both in ... |

### mathrock_pdf_facgce_theory - PASS

- Query: FACGCE 调弦在 Math Rock PDF 中如何用开放弦和和弦指型构建声音
- Expected sources: mathrock_pdf_steve_h
- Expected keywords any: FACGCE, 开放弦, 和弦, 调弦
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.036s = embed 0.034s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 3 | Y | Y | 0.2481 | -0.1031 | `mathrock_pdf_steve_h` | `chunk_0004` | facgce, math, pdf, rock, 和弦, 调弦 | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 2 | 6 | Y | Y | 0.2826 | -0.1476 | `mathrock_pdf_steve_h` | `chunk_0010` | math, pdf, rock, 和弦, 调弦 | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 3 | 5 | Y | Y | 0.2786 | -0.1536 | `mathrock_pdf_steve_h` | `chunk_0009` | math, pdf, rock, 和弦 | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |
| 4 | 11 | Y | Y | 0.2956 | -0.1606 | `mathrock_pdf_steve_h` | `chunk_0002` | math, pdf, rock, 和弦, 调弦 | ## 双⼿点弦与交替⼿指点弦 双⼿点弦主要包括交替点弦（双⼿轮流击弦），这可能是数学摇滚吉他⼿最常⽤的点弦技法。但有时你也会需要双⼿同步点奏音符，或⽤按弦⼿凭空锤音并保持音符以构建功能性和声（如⻉斯线）。以下范例（练习1.d）节选⾃我改编的《圣诞⽼人进城》曲谱。为清晰起⻅我将两个声部分开记谱，但实际需同步点奏。我发现让⼤脑同时处理两个点弦音符要困难得多。亲⾃试试感觉如何？有个简化技巧：先分别练习每个声部，再合并演奏。 [IMAGE_B... |
| 5 | 16 | Y | Y | 0.3180 | -0.1730 | `mathrock_pdf_steve_h` | `chunk_0003` | facgce, math, pdf, rock, 和弦, 调弦 | ## ⼿指控制+拨弦和弦 现在我们来学习同时拨弦的技巧。这能为你的和弦带来截然不同的质感——因为所有琴弦是被同时拨响，⽽非拨⽚扫弦的连续发声方式。它能提供更精准的动态控制、更高的演奏准确度，以及整体音色的变化。 入⻔练习2.g将不同⼿指组合（注意符头标注的使⽤⼿指）与拇指练习相结合。 [IMAGE_BLOCK:images/82b3d390df1caea14de87e86fde9d5cf5344c06334726ac7921b7f38... |

### mathrock_pdf_daeacse_scales - PASS

- Query: DAEAC#E 调弦的大调与小调音阶为什么有重复音和开放弦选择
- Expected sources: mathrock_pdf_steve_h
- Expected keywords any: DAEAC#E, 大调, 小调, 音阶
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.037s = embed 0.034s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 2 | Y | Y | 0.2210 | -0.1410 | `mathrock_pdf_steve_h` | `chunk_0004` | 调弦, 音阶 | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 2 | 1 |  | Y | 0.1562 | -0.1462 | `fretboard_handbook_mineru` | `md_chunk_0021` | 音阶 | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 3 | 3 | Y | Y | 0.2560 | -0.1760 | `mathrock_pdf_steve_h` | `chunk_0010` | 调弦, 音阶 | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 4 | 4 | Y | Y | 0.2628 | -0.1928 | `mathrock_pdf_steve_h` | `chunk_0009` | 音阶 | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |
| 5 | 7 | Y | Y | 0.2756 | -0.1956 | `mathrock_pdf_steve_h` | `chunk_0006` | 调弦, 音阶 | ## 为何掌握调号至关重要？ 明确调性对创作和演奏歌曲⼤有裨益。⾸先，它能精准定位可⽤的和弦、音符及音阶/琶音体系。 以C⼤调为例，其音阶包含以下音符： <table><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>4</td><td rowspan... |

### mathrock_pdf_shell_voicing - PASS

- Query: Math Rock PDF 中 shell voicing 如何用于 m7 G7 maj7 进行
- Expected sources: mathrock_pdf_steve_h
- Expected keywords any: shell, voicing, G7, maj7
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.037s = embed 0.035s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 11 | Y | Y | 0.3274 | -0.1724 | `mathrock_pdf_steve_h` | `chunk_0009` | g7, m7, math, pdf, rock, shell, voicing | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |
| 2 | 12 | Y | Y | 0.3301 | -0.1851 | `mathrock_pdf_steve_h` | `chunk_0004` | g7, m7, math, pdf, rock, voicing | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 3 | 1 |  | Y | 0.2902 | -0.2252 | `mathrock_text_course` | `chunk_0007` | math, rock, voicing | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 4 | 4 |  | Y | 0.3119 | -0.2369 | `mathrock_text_course` | `chunk_0004` | math, rock, shell, voicing | hey hey hey,let's do it. let's do another math Rock progression. shall we so this one kind of call we have another minor shape gone on AH be min,or we have?bf shocks of one five,we have the three,which is the d.and then... |
| 5 | 24 | Y | Y | 0.3791 | -0.2441 | `mathrock_pdf_steve_h` | `chunk_0010` | maj7, math, pdf, rock, voicing | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |

### mathrock_pdf_extended_chords - PASS

- Query: CM9 Dsus4 Em9 Gsus2 C6/9 这类扩展和弦在 PDF 里如何组织
- Expected sources: mathrock_pdf_steve_h
- Expected keywords any: 扩展壳式和弦, 延伸和弦, 壳式按法, extended
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 2
- Latency: total 0.038s = embed 0.035s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 2 | Y |  | 0.2724 | -0.1924 | `mathrock_pdf_steve_h` | `chunk_0004` | pdf, 和弦 | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 2 | 5 | Y | Y | 0.2945 | -0.2145 | `mathrock_pdf_steve_h` | `chunk_0009` | pdf, 和弦 | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |
| 3 | 1 |  |  | 0.2453 | -0.2353 | `fretboard_handbook_mineru` | `md_chunk_0021` | 和弦 | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 4 | 14 | Y | Y | 0.3210 | -0.2410 | `mathrock_pdf_steve_h` | `chunk_0006` | pdf, 和弦 | ## 为何掌握调号至关重要？ 明确调性对创作和演奏歌曲⼤有裨益。⾸先，它能精准定位可⽤的和弦、音符及音阶/琶音体系。 以C⼤调为例，其音阶包含以下音符： <table><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>4</td><td rowspan... |
| 5 | 18 | Y |  | 0.3288 | -0.2488 | `mathrock_pdf_steve_h` | `chunk_0010` | pdf, 和弦 | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |

### mathrock_pdf_jazz_voicing_progressions - PASS

- Query: Math Rock PDF 后半部分的 jazz voicing progression 如何连接 C6 G6/9 Bm7
- Expected sources: mathrock_pdf_steve_h
- Expected keywords any: C6, G6/9, Bm7, jazz
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.038s = embed 0.035s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 10 | Y | Y | 0.2854 | -0.1404 | `mathrock_pdf_steve_h` | `chunk_0004` | bm7, c6, math, pdf, rock, voicing | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 2 | 18 | Y | Y | 0.3109 | -0.1559 | `mathrock_pdf_steve_h` | `chunk_0009` | bm7, c6, math, pdf, progression, rock, voicing | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |
| 3 | 24 | Y | Y | 0.3340 | -0.1790 | `mathrock_pdf_steve_h` | `chunk_0006` | c6, jazz, math, pdf, progression, rock, voicing | ## 为何掌握调号至关重要？ 明确调性对创作和演奏歌曲⼤有裨益。⾸先，它能精准定位可⽤的和弦、音符及音阶/琶音体系。 以C⼤调为例，其音阶包含以下音符： <table><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>4</td><td rowspan... |
| 4 | 2 |  |  | 0.2577 | -0.1827 | `mathrock_text_course` | `chunk_0007` | math, progression, rock, voicing | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 5 | 3 |  | Y | 0.2580 | -0.1830 | `mathrock_text_course` | `chunk_0006` | jazz, math, progression, rock | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |

### fretboard_note_location - PASS

- Query: 吉他指板手册如何训练在每根弦上找到音名和根音
- Expected sources: fretboard_handbook_mineru
- Expected keywords any: 根音, 指板, 音名, 六根弦
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.038s = embed 0.035s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.1767 | -0.2167 | `fretboard_handbook_mineru` | `md_chunk_0002` | 指板 | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |
| 2 | 4 | Y | Y | 0.2945 | -0.2245 | `fretboard_handbook_mineru` | `md_chunk_0021` | 指板, 根音 | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 3 | 6 | Y | Y | 0.3079 | -0.2379 | `fretboard_handbook_mineru` | `md_chunk_0005` | 指板, 根音 | ## 练习8 指板上第12品位置的音符和空弦的音符是相同的。用一张含有6根弦的指板图，在每根弦的第12品处标出音符的名称。然后再次在每根弦上写出每个自然音阶音符，不同的是这次从第12品开始，向前写出来。记住F和E之间是半音，C和B之间也是半音。 [IMAGE_BLOCK:images/24126a6e73ef4ac122e855eb06967856951e6a0e507f4cf585e28f1a9bef4e21.jpg] [IMAGE... |
| 4 | 12 | Y | Y | 0.3324 | -0.2624 | `fretboard_handbook_mineru` | `md_chunk_0008` | 指板, 根音 | ## 第8章 自然小调音阶 学习目标：构建自然小调音阶的五种指型。理解关系小调和关系大调。 大调音阶只有一种构建公式，但对于小调音阶来说却有许多种构建方式，每一种都有它自己的公式。当人们提到“小调音阶”时，首先想到的应该是自然小调音阶。下面是它的构建公式（大声地读出来）： ## “全、半、全、全、半、全、全” 2级音和3级音之间、5级音和6级音之间是半音关系。可以写成：12^345^678。 [IMAGE_BLOCK:images/3... |
| 5 | 3 |  | Y | 0.2892 | -0.2692 | `mathrock_pdf_steve_h` | `chunk_0010` | 指板, 根音 | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |

### fretboard_intervals_octave - PASS

- Query: 指板手册里八度音和不同弦组之间的品位关系怎么记忆
- Expected sources: fretboard_handbook_mineru
- Expected keywords any: 八度, 品, 弦, 指板
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.039s = embed 0.036s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 2 | Y | Y | 0.2348 | -0.1748 | `fretboard_handbook_mineru` | `md_chunk_0021` | 指板 | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 3 |  | Y | 0.2590 | -0.2490 | `mathrock_pdf_steve_h` | `chunk_0010` | 指板 | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 3 | 7 | Y | Y | 0.3091 | -0.2491 | `fretboard_handbook_mineru` | `md_chunk_0008` | 指板 | ## 第8章 自然小调音阶 学习目标：构建自然小调音阶的五种指型。理解关系小调和关系大调。 大调音阶只有一种构建公式，但对于小调音阶来说却有许多种构建方式，每一种都有它自己的公式。当人们提到“小调音阶”时，首先想到的应该是自然小调音阶。下面是它的构建公式（大声地读出来）： ## “全、半、全、全、半、全、全” 2级音和3级音之间、5级音和6级音之间是半音关系。可以写成：12^345^678。 [IMAGE_BLOCK:images/3... |
| 4 | 8 | Y | Y | 0.3127 | -0.2527 | `fretboard_handbook_mineru` | `md_chunk_0005` | 指板 | ## 练习8 指板上第12品位置的音符和空弦的音符是相同的。用一张含有6根弦的指板图，在每根弦的第12品处标出音符的名称。然后再次在每根弦上写出每个自然音阶音符，不同的是这次从第12品开始，向前写出来。记住F和E之间是半音，C和B之间也是半音。 [IMAGE_BLOCK:images/24126a6e73ef4ac122e855eb06967856951e6a0e507f4cf585e28f1a9bef4e21.jpg] [IMAGE... |
| 5 | 1 | Y | Y | 0.2146 | -0.2546 | `fretboard_handbook_mineru` | `md_chunk_0002` | 指板 | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |

### fretboard_major_triad_arpeggio - PASS

- Query: 大三和弦琶音由根音大三度纯五度构成，如何在六根弦上练指型
- Expected sources: fretboard_handbook_mineru
- Expected keywords any: 大三和弦, 琶音, 根音, 纯五度
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.039s = embed 0.036s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2052 | -0.1352 | `fretboard_handbook_mineru` | `md_chunk_0021` | 和弦, 根音 | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 2 |  | Y | 0.2400 | -0.2100 | `mathrock_pdf_steve_h` | `chunk_0010` | 和弦, 根音, 琶音 | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 3 | 8 | Y | Y | 0.3078 | -0.2278 | `fretboard_handbook_mineru` | `md_chunk_0015` | 和弦, 根音, 琶音 | ## 练习33 在五种根音指型中，构建D增三和弦琶音型式。不用圈出每个音符。其中有些指型需要越弦演奏。在构建增三和弦时会发现，有时同一指型中的一个音符有两种弹法，这两种都是正确的。 1)D增三和弦琶音 指型1 [IMAGE_BLOCK:images/be4322276df242e12f2f42306cd9dabc71a5b02294fbc770696af4fffc83f279.jpg] = 2)D增三和弦琶音 指型2 [IMAGE_B... |
| 4 | 9 | Y | Y | 0.3117 | -0.2317 | `fretboard_handbook_mineru` | `md_chunk_0017` | 和弦, 根音, 琶音 | ## 练习41 在F减三和弦琶音的基础上增加小七度音，并画出六根弦上F小七减五和弦的五种琶音指型。圈出根音，和弦的全称和指型序号已经标出。 1）Fmi7(b5)琶音 [IMAGE_BLOCK:images/e59bd9b18318b42b3e72c06ff8169b2030ebf567755dc252440f41380f8a7fa3.jpg] 2)Fmi7(b5)琶音 指型2 [IMAGE_BLOCK:images/6b087a425... |
| 5 | 4 |  | Y | 0.2702 | -0.2402 | `mathrock_pdf_steve_h` | `chunk_0004` | 和弦, 根音, 琶音 | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |

### fretboard_minor_diminished_augmented - PASS

- Query: 小三和弦 减三和弦 增三和弦的琶音指型有什么音程差异
- Expected sources: fretboard_handbook_mineru
- Expected keywords any: 小三和弦, 减三和弦, 增三和弦, 琶音
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 2
- Latency: total 0.038s = embed 0.035s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y |  | 0.2452 | -0.1852 | `fretboard_handbook_mineru` | `md_chunk_0021` | 和弦 | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 8 | Y | Y | 0.3144 | -0.2244 | `fretboard_handbook_mineru` | `md_chunk_0015` | 减三和弦, 和弦, 小三和弦, 琶音 | ## 练习33 在五种根音指型中，构建D增三和弦琶音型式。不用圈出每个音符。其中有些指型需要越弦演奏。在构建增三和弦时会发现，有时同一指型中的一个音符有两种弹法，这两种都是正确的。 1)D增三和弦琶音 指型1 [IMAGE_BLOCK:images/be4322276df242e12f2f42306cd9dabc71a5b02294fbc770696af4fffc83f279.jpg] = 2)D增三和弦琶音 指型2 [IMAGE_B... |
| 3 | 9 | Y | Y | 0.3186 | -0.2386 | `fretboard_handbook_mineru` | `md_chunk_0017` | 减三和弦, 和弦, 琶音 | ## 练习41 在F减三和弦琶音的基础上增加小七度音，并画出六根弦上F小七减五和弦的五种琶音指型。圈出根音，和弦的全称和指型序号已经标出。 1）Fmi7(b5)琶音 [IMAGE_BLOCK:images/e59bd9b18318b42b3e72c06ff8169b2030ebf567755dc252440f41380f8a7fa3.jpg] 2)Fmi7(b5)琶音 指型2 [IMAGE_BLOCK:images/6b087a425... |
| 4 | 2 |  | Y | 0.2825 | -0.2625 | `mathrock_pdf_steve_h` | `chunk_0009` | 和弦, 琶音 | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |
| 5 | 3 |  | Y | 0.2834 | -0.2634 | `mathrock_pdf_steve_h` | `chunk_0010` | 和弦, 琶音 | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |

### fretboard_seventh_arpeggios - PASS

- Query: 大七 小七 属七 小七减五 减七和弦琶音在指板手册中怎么练
- Expected sources: fretboard_handbook_mineru
- Expected keywords any: 大七, 小七, 属七, 减七
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 2
- Latency: total 0.037s = embed 0.034s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y |  | 0.3017 | -0.2317 | `fretboard_handbook_mineru` | `md_chunk_0021` | 和弦, 指板 | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 7 | Y | Y | 0.3541 | -0.2441 | `fretboard_handbook_mineru` | `md_chunk_0017` | 和弦, 大七, 小七, 小七减五, 指板, 琶音 | ## 练习41 在F减三和弦琶音的基础上增加小七度音，并画出六根弦上F小七减五和弦的五种琶音指型。圈出根音，和弦的全称和指型序号已经标出。 1）Fmi7(b5)琶音 [IMAGE_BLOCK:images/e59bd9b18318b42b3e72c06ff8169b2030ebf567755dc252440f41380f8a7fa3.jpg] 2)Fmi7(b5)琶音 指型2 [IMAGE_BLOCK:images/6b087a425... |
| 3 | 3 | Y |  | 0.3284 | -0.2884 | `fretboard_handbook_mineru` | `md_chunk_0001` | 和弦, 指板, 琶音 | [IMAGE_BLOCK:images/8b7ba2f10bcaab55ce9201207558dc26f0f3bd7d10ba53803cf9777452bbd505.jpg] [IMAGE_BLOCK:images/02959d5afc23bcd298aba62bc77aa210b94bfadeb6686e3d159117940e4cf8e5.jpg] [IMAGE_BLOCK:images/bf740813094108cf43a... |
| 4 | 19 | Y | Y | 0.4172 | -0.2972 | `fretboard_handbook_mineru` | `md_chunk_0023` | 和弦, 大七, 小七, 小七减五, 属七, 指板, 琶音 | ## 练习57 在下面的图示中画出Ab旋律小调音阶的五种指型。 1 Ab旋律小调指型1 [IMAGE_BLOCK:images/cecd89101935fffb98b884118e87c5f229633b7e7a28bd1c8435ec8dea6ceac4.jpg] 2) Ab旋律小调 指型2 [IMAGE_BLOCK:images/36a5f7d5040a085dac44fba6fc437800d25de615e36e42b6bc6... |
| 5 | 4 |  | Y | 0.3389 | -0.2989 | `mathrock_pdf_steve_h` | `chunk_0009` | 和弦, 属七, 指板, 琶音 | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |

### fretboard_open_major_triad_voicing - PASS

- Query: 开放大三和弦声部和牛仔和弦为什么先学琶音再学和弦
- Expected sources: fretboard_handbook_mineru
- Expected keywords any: 开放大三和弦, 牛仔和弦, 琶音, 声部
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 2
- Latency: total 0.039s = embed 0.036s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y |  | 0.2341 | -0.1741 | `fretboard_handbook_mineru` | `md_chunk_0021` | 和弦 | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 3 |  | Y | 0.2866 | -0.2666 | `mathrock_pdf_steve_h` | `chunk_0009` | 和弦, 琶音 | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |
| 3 | 20 | Y | Y | 0.3509 | -0.2709 | `fretboard_handbook_mineru` | `md_chunk_0015` | 和弦, 声部, 琶音 | ## 练习33 在五种根音指型中，构建D增三和弦琶音型式。不用圈出每个音符。其中有些指型需要越弦演奏。在构建增三和弦时会发现，有时同一指型中的一个音符有两种弹法，这两种都是正确的。 1)D增三和弦琶音 指型1 [IMAGE_BLOCK:images/be4322276df242e12f2f42306cd9dabc71a5b02294fbc770696af4fffc83f279.jpg] = 2)D增三和弦琶音 指型2 [IMAGE_B... |
| 4 | 4 |  | Y | 0.2916 | -0.2716 | `mathrock_pdf_steve_h` | `chunk_0010` | 和弦, 琶音 | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 5 | 22 | Y | Y | 0.3527 | -0.2727 | `fretboard_handbook_mineru` | `md_chunk_0017` | 和弦, 声部, 琶音 | ## 练习41 在F减三和弦琶音的基础上增加小七度音，并画出六根弦上F小七减五和弦的五种琶音指型。圈出根音，和弦的全称和指型序号已经标出。 1）Fmi7(b5)琶音 [IMAGE_BLOCK:images/e59bd9b18318b42b3e72c06ff8169b2030ebf567755dc252440f41380f8a7fa3.jpg] 2)Fmi7(b5)琶音 指型2 [IMAGE_BLOCK:images/6b087a425... |

### fretboard_closed_triad_voicing - PASS

- Query: 密集三和弦和闭合排列在指板上如何构建转位
- Expected sources: fretboard_handbook_mineru
- Expected keywords any: 密集三和弦, 转位, 声部, 指板
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.037s = embed 0.034s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.2337 | -0.1637 | `fretboard_handbook_mineru` | `md_chunk_0021` | 和弦, 指板 | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 3 |  | Y | 0.2730 | -0.2330 | `mathrock_pdf_steve_h` | `chunk_0009` | 和弦, 密集, 指板, 转位 | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |
| 3 | 21 | Y | Y | 0.3308 | -0.2408 | `fretboard_handbook_mineru` | `md_chunk_0015` | 和弦, 密集, 指板, 转位 | ## 练习33 在五种根音指型中，构建D增三和弦琶音型式。不用圈出每个音符。其中有些指型需要越弦演奏。在构建增三和弦时会发现，有时同一指型中的一个音符有两种弹法，这两种都是正确的。 1)D增三和弦琶音 指型1 [IMAGE_BLOCK:images/be4322276df242e12f2f42306cd9dabc71a5b02294fbc770696af4fffc83f279.jpg] = 2)D增三和弦琶音 指型2 [IMAGE_B... |
| 4 | 4 |  | Y | 0.2761 | -0.2561 | `mathrock_pdf_steve_h` | `chunk_0010` | 和弦, 指板 | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 5 | 5 |  | Y | 0.2797 | -0.2597 | `mathrock_pdf_steve_h` | `chunk_0004` | 和弦, 指板 | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |

### fretboard_six_nine_add9 - PASS

- Query: 加九和弦 六九和弦 和属九大九有什么区别
- Expected sources: fretboard_handbook_mineru
- Expected keywords any: 加九, 六九, 属九, 大九
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 3
- Latency: total 0.035s = embed 0.032s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y |  | 0.2693 | -0.2093 | `fretboard_handbook_mineru` | `md_chunk_0021` | 和弦 | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 2 |  |  | 0.3164 | -0.3064 | `mathrock_pdf_steve_h` | `chunk_0004` | 和弦 | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 3 | 22 | Y | Y | 0.3889 | -0.3089 | `fretboard_handbook_mineru` | `md_chunk_0023` | 六九和弦, 加九和弦, 和弦 | ## 练习57 在下面的图示中画出Ab旋律小调音阶的五种指型。 1 Ab旋律小调指型1 [IMAGE_BLOCK:images/cecd89101935fffb98b884118e87c5f229633b7e7a28bd1c8435ec8dea6ceac4.jpg] 2) Ab旋律小调 指型2 [IMAGE_BLOCK:images/36a5f7d5040a085dac44fba6fc437800d25de615e36e42b6bc6... |
| 4 | 15 | Y |  | 0.3704 | -0.3104 | `fretboard_handbook_mineru` | `md_chunk_0017` | 和弦 | ## 练习41 在F减三和弦琶音的基础上增加小七度音，并画出六根弦上F小七减五和弦的五种琶音指型。圈出根音，和弦的全称和指型序号已经标出。 1）Fmi7(b5)琶音 [IMAGE_BLOCK:images/e59bd9b18318b42b3e72c06ff8169b2030ebf567755dc252440f41380f8a7fa3.jpg] 2)Fmi7(b5)琶音 指型2 [IMAGE_BLOCK:images/6b087a425... |
| 5 | 4 |  |  | 0.3217 | -0.3117 | `mathrock_pdf_steve_h` | `chunk_0009` | 和弦 | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |

### cross_open_string_texture - PASS

- Query: 开放弦持续音在 math rock 和指板和弦声部里分别有什么作用
- Expected sources: mathrock_text_course, mathrock_pdf_steve_h, fretboard_handbook_mineru
- Expected keywords any: open string, 开放弦, common tone, 声部
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 4
- Latency: total 0.038s = embed 0.035s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y |  | 0.2526 | -0.1826 | `fretboard_handbook_mineru` | `md_chunk_0021` | 和弦, 指板 | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 4 | Y |  | 0.2675 | -0.2125 | `mathrock_text_course` | `chunk_0007` | math, rock | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 3 | 8 | Y |  | 0.2838 | -0.2188 | `mathrock_pdf_steve_h` | `chunk_0009` | math, rock, 和弦, 指板 | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |
| 4 | 5 | Y | Y | 0.2768 | -0.2218 | `mathrock_text_course` | `chunk_0006` | math, rock | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |
| 5 | 6 | Y |  | 0.2781 | -0.2231 | `mathrock_text_course` | `chunk_0002` | math, rock | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |

### cross_sparse_vs_dense_arrangement - PASS

- Query: 编配太密时，funk 的留白和 math rock 的开放弦密集织体有什么不同
- Expected sources: cory_wong_funk_core, mathrock_text_course, mathrock_pdf_steve_h
- Expected keywords any: space, open string, dense, rhythm
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 2
- Latency: total 0.037s = embed 0.034s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 2 | Y |  | 0.2824 | -0.2274 | `mathrock_text_course` | `chunk_0007` | math, rock | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 2 | 10 | Y | Y | 0.3194 | -0.2444 | `cory_wong_funk_core` | `chunk_0010` | funk, rock | now those are a couple of my main approaches to ribbon guitar,but some other things just to consider are ribbon IC density.range on the instrument.tone.and space.OK so.sometimes a song is going to call for a ribbon guit... |
| 3 | 6 | Y | Y | 0.3148 | -0.2498 | `cory_wong_funk_core` | `chunk_0009` | funk | now something to really note is.there's a difference between timing.patterns.and groove.they all kind of make up this thing that we call ribbon.那timing is。where you're placing something.right? the timing is a hundred an... |
| 4 | 5 | Y | Y | 0.3146 | -0.2596 | `mathrock_pdf_steve_h` | `chunk_0009` | math, rock, 密集 | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是... |
| 5 | 8 | Y | Y | 0.3167 | -0.2617 | `mathrock_text_course` | `chunk_0003` | math, rock | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |

### cross_gp5_tapping_features - PASS

- Query: 如果 GP5 检测到大量 tapping hammer pull off open string，应匹配哪些教材证据
- Expected sources: mathrock_text_course, mathrock_pdf_steve_h
- Expected keywords any: tapping, hammer, pull, open string
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.037s = embed 0.034s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 2 | Y | Y | 0.3007 | -0.1957 | `mathrock_text_course` | `chunk_0002` | gp5, hammer, off, open, pull, string, tapping | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 2 | 3 | Y | Y | 0.3028 | -0.1978 | `mathrock_text_course` | `chunk_0003` | gp5, hammer, off, open, pull, string, tapping | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |
| 3 | 6 | Y | Y | 0.3329 | -0.2279 | `mathrock_text_course` | `chunk_0005` | gp5, hammer, off, open, pull, string, tapping | we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have AC sharp right there and e. ,so we have ... |
| 4 | 7 | Y | Y | 0.3342 | -0.2292 | `mathrock_text_course` | `chunk_0006` | gp5, hammer, off, open, pull, string, tapping | what is up guys we're back with another crazy midwest emerin math Rock progression? this one is gonna be.I'm going to keep a beamon on the tuning one. I'm using is something unique it's bfs hop de a.d and dokay so i did... |
| 5 | 11 | Y | Y | 0.3505 | -0.2555 | `mathrock_text_course` | `chunk_0004` | gp5, hammer, off, open, pull, string | hey hey hey,let's do it. let's do another math Rock progression. shall we so this one kind of call we have another minor shape gone on AH be min,or we have?bf shocks of one five,we have the three,which is the d.and then... |

### cross_gp5_funk_16th_muting - PASS

- Query: 如果 GP5 里十六分音符很多且有 muted strum，应该检索 funk 哪些证据
- Expected sources: cory_wong_funk_core
- Expected keywords any: sixteenth, muted, strum, rhythm
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.037s = embed 0.033s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 7 | Y | Y | 0.2847 | -0.1897 | `cory_wong_funk_core` | `chunk_0011` | funk, gp5, muted, strum | one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accomplish some of my signature moves,both in ... |
| 2 | 14 | Y | Y | 0.3074 | -0.2124 | `cory_wong_funk_core` | `chunk_0012` | funk, gp5, muted, strum | another one of my signature guitar moves is this sort of thing.that sort of thing you hear me do that all the time now part of how I get that sound obviously it's double strokes it's two notes at the same time.now,in or... |
| 3 | 15 | Y | Y | 0.3082 | -0.2132 | `cory_wong_funk_core` | `chunk_0008` | funk, gp5, muted, strum | let's dive deeper into that bongo conga style to me,that world of ribbon guitar playing is the bubble. now you hear this sort of thing on a lot of songs,it's classic.billy IE,Jean,you hear it on?a lot of other songs tha... |
| 4 | 11 | Y | Y | 0.3023 | -0.2173 | `cory_wong_funk_core` | `chunk_0009` | funk, gp5, muted | now something to really note is.there's a difference between timing.patterns.and groove.they all kind of make up this thing that we call ribbon.那timing is。where you're placing something.right? the timing is a hundred an... |
| 5 | 12 | Y | Y | 0.3051 | -0.2201 | `cory_wong_funk_core` | `chunk_0004` | funk, gp5, strum | that's just actually articulating and playing a different type of phrasing on it,but it's one way to use that voicing.嗯。minor seven chords are super common in funk music and especially in a lot of the music that i play,... |

### cross_voicing_advice - PASS

- Query: 想把普通和弦进行改成更有风格的 guitar voicing，可以参考 funk sparse voicing 还是 math rock maj9 shell voicing
- Expected sources: cory_wong_funk_core, mathrock_pdf_steve_h
- Expected keywords any: voicing, maj9, shell, sparse
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.044s = embed 0.041s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 3 | Y | Y | 0.2363 | -0.1313 | `cory_wong_funk_core` | `chunk_0003` | funk, guitar, rock, sparse, voicing | this next series of lessons is about cord voicings and cord moves that I use in my playing.especially,in the context of funk,music now most of these voice o icings start from the caged system if you're not familiar with... |
| 2 | 2 | Y | Y | 0.2319 | -0.1369 | `cory_wong_funk_core` | `chunk_0004` | funk, guitar, sparse, voicing | that's just actually articulating and playing a different type of phrasing on it,but it's one way to use that voicing.嗯。minor seven chords are super common in funk music and especially in a lot of the music that i play,... |
| 3 | 1 |  | Y | 0.2085 | -0.1435 | `mathrock_text_course` | `chunk_0007` | math, rock, voicing | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 4 | 9 | Y | Y | 0.2555 | -0.1505 | `cory_wong_funk_core` | `chunk_0010` | funk, guitar, rock, sparse, voicing | now those are a couple of my main approaches to ribbon guitar,but some other things just to consider are ribbon IC density.range on the instrument.tone.and space.OK so.sometimes a song is going to call for a ribbon guit... |
| 5 | 7 | Y | Y | 0.2530 | -0.1580 | `cory_wong_funk_core` | `chunk_0008` | funk, guitar, sparse, voicing | let's dive deeper into that bongo conga style to me,that world of ribbon guitar playing is the bubble. now you hear this sort of thing on a lot of songs,it's classic.billy IE,Jean,you hear it on?a lot of other songs tha... |

### cross_arpeggio_to_riff - PASS

- Query: 如何把指板手册里的琶音指型转化成 math rock riff 或填充句
- Expected sources: fretboard_handbook_mineru, mathrock_text_course
- Expected keywords any: 琶音, arpeggio, riff, 指型
- Rerank: `True`, candidates: 25
- Source first rank: 3
- Keyword first rank: 1
- Latency: total 0.038s = embed 0.035s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 3 |  | Y | 0.2907 | -0.2157 | `mathrock_pdf_steve_h` | `chunk_0010` | math, riff, rock, 指板, 琶音 | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 2 | 6 |  | Y | 0.2992 | -0.2242 | `mathrock_pdf_steve_h` | `chunk_0002` | math, riff, rock, 指板, 琶音 | ## 双⼿点弦与交替⼿指点弦 双⼿点弦主要包括交替点弦（双⼿轮流击弦），这可能是数学摇滚吉他⼿最常⽤的点弦技法。但有时你也会需要双⼿同步点奏音符，或⽤按弦⼿凭空锤音并保持音符以构建功能性和声（如⻉斯线）。以下范例（练习1.d）节选⾃我改编的《圣诞⽼人进城》曲谱。为清晰起⻅我将两个声部分开记谱，但实际需同步点奏。我发现让⼤脑同时处理两个点弦音符要困难得多。亲⾃试试感觉如何？有个简化技巧：先分别练习每个声部，再合并演奏。 [IMAGE_B... |
| 3 | 7 | Y | Y | 0.3002 | -0.2402 | `fretboard_handbook_mineru` | `md_chunk_0021` | 指板 | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 4 | 8 | Y | Y | 0.3066 | -0.2416 | `mathrock_text_course` | `chunk_0002` | math, riff, rock | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
| 5 | 9 | Y | Y | 0.3172 | -0.2522 | `mathrock_text_course` | `chunk_0003` | math, riff, rock | math Rock and midwest emo it looks pretty tricky right,is it yes sort of well if you play like this it is but what if we break it down a little bit we go to a lot of alternate shootings for this kind of music?why is tha... |

### cross_alternate_tuning_limit - PASS

- Query: 为什么特殊调弦下的和弦指型不能直接套用到标准调弦指板知识
- Expected sources: mathrock_text_course, mathrock_pdf_steve_h, fretboard_handbook_mineru
- Expected keywords any: tuning, 调弦, 指型, standard
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.040s = embed 0.037s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 2 | Y | Y | 0.2417 | -0.1717 | `fretboard_handbook_mineru` | `md_chunk_0021` | 和弦, 指板 | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边... |
| 2 | 3 | Y | Y | 0.2719 | -0.2419 | `mathrock_pdf_steve_h` | `chunk_0004` | 和弦, 指板, 调弦 | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D ... |
| 3 | 4 | Y | Y | 0.2729 | -0.2429 | `mathrock_pdf_steve_h` | `chunk_0010` | 和弦, 指板, 调弦 | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V... |
| 4 | 11 | Y | Y | 0.3244 | -0.2644 | `fretboard_handbook_mineru` | `md_chunk_0008` | 指板 | ## 第8章 自然小调音阶 学习目标：构建自然小调音阶的五种指型。理解关系小调和关系大调。 大调音阶只有一种构建公式，但对于小调音阶来说却有许多种构建方式，每一种都有它自己的公式。当人们提到“小调音阶”时，首先想到的应该是自然小调音阶。下面是它的构建公式（大声地读出来）： ## “全、半、全、全、半、全、全” 2级音和3级音之间、5级音和6级音之间是半音关系。可以写成：12^345^678。 [IMAGE_BLOCK:images/3... |
| 5 | 1 | Y |  | 0.2395 | -0.2695 | `fretboard_handbook_mineru` | `md_chunk_0002` | 和弦, 指板 | ## 如何应用本书 本书前后章节之间的关联性很强，后续的章节经常会追述到前面的章节，所以希望你能循序渐进地学习。如果你处于认真学习吉他的初始阶段，我建议在学习本书的内容一年后，再重新温习一遍，至少花一周的时间，每天抽出几分钟，把每个章节仔细回顾一遍。 在学习每章之前，先仔细想一想这一章的学习目标。如果觉得已经掌握了学习的目标，那么就可以去做后面的练习了。如果你能完整无误并且很快地完成这些练习，那么就可以去学习下一章了。如果不能，那么就... |

### cross_rhythm_plus_harmony - PASS

- Query: 如何同时考虑 funk 节奏律动和 math rock 扩展和弦色彩来做吉他编配
- Expected sources: cory_wong_funk_core, mathrock_pdf_steve_h
- Expected keywords any: rhythm, groove, extended, 和弦
- Rerank: `True`, candidates: 25
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.037s = embed 0.034s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 11 | Y | Y | 0.3122 | -0.2272 | `cory_wong_funk_core` | `chunk_0010` | funk, rock, 节奏 | now those are a couple of my main approaches to ribbon guitar,but some other things just to consider are ribbon IC density.range on the instrument.tone.and space.OK so.sometimes a song is going to call for a ribbon guit... |
| 2 | 8 | Y | Y | 0.3068 | -0.2318 | `cory_wong_funk_core` | `chunk_0009` | funk, 律动 | now something to really note is.there's a difference between timing.patterns.and groove.they all kind of make up this thing that we call ribbon.那timing is。where you're placing something.right? the timing is a hundred an... |
| 3 | 7 | Y | Y | 0.3066 | -0.2416 | `cory_wong_funk_core` | `chunk_0008` | funk | let's dive deeper into that bongo conga style to me,that world of ribbon guitar playing is the bubble. now you hear this sort of thing on a lot of songs,it's classic.billy IE,Jean,you hear it on?a lot of other songs tha... |
| 4 | 3 |  |  | 0.2974 | -0.2424 | `mathrock_text_course` | `chunk_0007` | math, rock | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movabl... |
| 5 | 4 |  | Y | 0.2985 | -0.2435 | `mathrock_text_course` | `chunk_0002` | math, rock | all right,guys,so for this math Rock midwest emo progression,we're looking at a tune in dad gatt.gad gad what are the codes we're looking at here the key is going to be centered around de maja. I have this bmi NOR in th... |
