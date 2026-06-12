# Query RAG Bundle Report

- Query: FACGCE 调弦下的 math rock G7 和弦指型图
- Intent: `mixed_lookup`
- Sufficient: `True`
- Confidence: 0.71
- Total latency: 5.897s

## Query Analysis

```json
{
  "query": "FACGCE 调弦下的 math rock G7 和弦指型图",
  "intent": "mixed_lookup",
  "style_hints": [
    "mathrock"
  ],
  "theory_terms": [
    "G7",
    "和弦",
    "指型"
  ],
  "technique_terms": [],
  "needs_fretboard_text": true,
  "needs_visual": true,
  "needs_style_text": true,
  "needs_kg": false,
  "confidence": 0.8,
  "matched_rules": [
    "fretboard_terms",
    "visual_terms",
    "style_or_technique_terms"
  ]
}
```

## Retrieval Plan

| Name | Backend | Collection | TopK | Reason | Query |
|---|---|---|---:|---|---|
| `fretboard_text` | `chroma` | `guitar_fretboard_handbook_text_qwen3_06b` | 5 | 指板/理论/练习题干证据 | FACGCE 调弦下的 math rock G7 和弦指型图 |
| `visual_caption` | `chroma` | `guitar_visual_mixed_mathrock_trial_qwen3_06b` | 5 | 具体图形/指法/voicing/答案图证据 | FACGCE 调弦下的 math rock G7 和弦指型图 |
| `style_text` | `chroma` | `guitar_text_chunks_qwen3_06b` | 5 | 风格/riff/节奏/技法文本证据 | FACGCE 调弦下的 math rock G7 和弦指型图 mathrock |

## Text Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `text:chunk_0004` | `mathrock_pdf_steve_h` | 1.6420 | Math Rock Guitar E-book | ## 为何某些特殊调弦如此动听 你可能在想"为什么有些特殊调弦听起来如此美妙？" 关键在于音符的选择与各音之间的音程关系。借助基础乐理知识，我可以解释其原理（若您对下文探讨的理论概念理解尚不清晰，建议先学习本指南乐理章节中关于和弦构成的部分后再回看）。 观察标准调弦E A D G B E各弦的音程关系，可⻅主要由四度音程构成，唯有⼀处三度音程（即相邻两弦的音高距离）。具体解析如下： E 1E FF G G A A B B C C D D 22 33 44 5 5 66 77 BB CC DD EE F F GG ... |
| 2 | `text:chunk_0002` | `mathrock_pdf_steve_h` | 1.5186 | Math Rock Guitar E-book | ## 双⼿点弦与交替⼿指点弦 双⼿点弦主要包括交替点弦（双⼿轮流击弦），这可能是数学摇滚吉他⼿最常⽤的点弦技法。但有时你也会需要双⼿同步点奏音符，或⽤按弦⼿凭空锤音并保持音符以构建功能性和声（如⻉斯线）。以下范例（练习1.d）节选⾃我改编的《圣诞⽼人进城》曲谱。为清晰起⻅我将两个声部分开记谱，但实际需同步点奏。我发现让⼤脑同时处理两个点弦音符要困难得多。亲⾃试试感觉如何？有个简化技巧：先分别练习每个声部，再合并演奏。 [IMAGE_BLOCK:images/d2c33157c8b04974314c5e85514c... |
| 3 | `text:chunk_0003` | `mathrock_pdf_steve_h` | 1.5124 | Math Rock Guitar E-book | ## ⼿指控制+拨弦和弦 现在我们来学习同时拨弦的技巧。这能为你的和弦带来截然不同的质感——因为所有琴弦是被同时拨响，⽽非拨⽚扫弦的连续发声方式。它能提供更精准的动态控制、更高的演奏准确度，以及整体音色的变化。 入⻔练习2.g将不同⼿指组合（注意符头标注的使⽤⼿指）与拇指练习相结合。 [IMAGE_BLOCK:images/82b3d390df1caea14de87e86fde9d5cf5344c06334726ac7921b7f3884d7b340.jpg] 练习2.h在前⼀练习基础上增加了⼀根⼿指。熟练后，可... |
| 4 | `text:chunk_0005` | `mathrock_text_course` | 1.4470 | mathrock教学课 | we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have AC sharp right there and e. ,so we have the fifth right here in AB,and then we h... |
| 5 | `text:chunk_0001` | `mathrock_text_course` | 1.4175 | mathrock教学课 | so what are the basics of math rock or midwest emo we're going to take a look at this little progression right here which is in the key of dd major,and i have it in a very common alternate tuning of dad gad it's going to be an acronym for dad side from the to... |
| 6 | `text:chunk_0007` | `mathrock_text_course` | 1.3749 | mathrock教学课 | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movable core shapes,all right? thinking about ... |
| 7 | `text:chunk_0009` | `mathrock_pdf_steve_h` | 1.3743 | Math Rock Guitar E-book | ## 扩展壳式和弦排列 扩展壳式和弦按法是⼀种特殊的和弦排列方式。它包含定义延伸和弦所需的核心音符（三度音与七度音），并与根音结合形成⼀、三、七音结构。这种按法能保留延伸和弦的整体调性（⼤调、⼩调等），同时进⾏精简处理。这类和弦具有实⽤价值，例如在合奏场景中，当其他乐⼿已演奏密集和声时，使⽤壳式和弦（或仅⽤三度/七度音）更为适宜。相比完整和弦，它们更适配增益音色，同时也适合构建基于和弦的连复段，因其能勾勒出特定和弦的主⼲音符。 以下是我常⽤的七和弦壳式按法指型，许多数学摇滚⻛格的乐队也广泛使⽤这些指型。 ⼤七和弦... |
| 8 | `text:chunk_0010` | `mathrock_pdf_steve_h` | 1.3438 | Math Rock Guitar E-book | ## 习题答案 调性练习 1. E⼤调 - A⼤调 - G#⼩调 - F#⼩调 - E⼤调 = E⼤调：I - IV - iii - ii - I 2. D⼩调 - G属 - C⼤调 = C⼤调：ii - V - I 3. D⼤调 - E⼩调 - F#减 - G⼤调 = G⼤调：V - vi - vii - I 4. C⼤调 - G⼤调 - A⼩调 - E⼩调 = 可能是C⼤调：I - V - vi -iii 或 G⼤调：IV - V - ii - vi 5. G⼤调 - B⼩调 - C⼤调 - C⼩调 = G⼤... |
| 9 | `text:chunk_0006` | `mathrock_pdf_steve_h` | 1.3070 | Math Rock Guitar E-book | ## 为何掌握调号至关重要？ 明确调性对创作和演奏歌曲⼤有裨益。⾸先，它能精准定位可⽤的和弦、音符及音阶/琶音体系。 以C⼤调为例，其音阶包含以下音符： <table><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan... |
| 10 | `text:fretboard_text_0119` | `fretboard_handbook_clean_text` | 1.0731 | 吉他指板手册正文清洗层 | ## 练习49 根据给出的声部构成，在下面的图示中构建延伸和弦。 5）F#7(#11) 6Db13 7）A13(#11) 8 E13 10）F9（#11) 弹奏上页练习中的延伸和弦，弹奏时大声说出和弦名称、指型序号和声部构成。 “C九和弦，指型1，‘1、3、b7、. G大十三和弦，指型4，‘1、3、7、13..” [图示引用 10 张，详见 image_refs] |

## Visual Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `visual_caption:mr_style_001_g7` | `mathrock_pdf` | 1.9996 | Math Rock 吉他教材 | 来源: Math Rock 吉他教材 / mathrock_pdf 视觉角色: style_visual_evidence 页码: 33 图像类型: chord_diagram 主题: FACGCE_tuning_G7_chord_shape 调弦: FACGCE 调性: C major 根音: G 和弦: G7 技法: mute, open_strings 弦组: 6 strings 品位范围: open-3 开放弦: 5th string, 4th string, 3rd string, 2nd string... |
| 2 | `visual_caption:mr_style_001_bm7b5` | `mathrock_pdf` | 1.8791 | Math Rock 吉他教材 | 来源: Math Rock 吉他教材 / mathrock_pdf 视觉角色: style_visual_evidence 页码: 33 图像类型: chord_diagram 主题: FACGCE_Bm7b5_chord_shape 调弦: FACGCE 调性: unknown 根音: B 和弦: Bm7b5 弦组: 6 strings 品位范围: 4-7 (based on 5fr marker) 包含音: B, D, F, A caption: FACGCE特殊调弦下的Bm7b5（半减七）和弦指型图。图示标... |
| 3 | `visual_caption:mr_style_002` | `mathrock_pdf` | 1.8145 | Math Rock 吉他教材 | 来源: Math Rock 吉他教材 / mathrock_pdf 视觉角色: style_visual_evidence 页码: 34 图像类型: fretboard_diagram 主题: FACGCE_tuning_major_scale_fingerboard_map 调弦: FACGCE 调性: unknown 根音: unknown 音阶: major scale 技法: tapping, riff construction, melodic phrasing 指型: movable patterns... |
| 4 | `visual_caption:mr_style_001_am` | `mathrock_pdf` | 1.6852 | Math Rock 吉他教材 | 来源: Math Rock 吉他教材 / mathrock_pdf 视觉角色: style_visual_evidence 页码: 33 图像类型: chord_diagram 主题: FACGCE_tuning_Am_chord_shape 调弦: FACGCE 调性: A minor 根音: A 和弦: Am 技法: muted_strings 弦组: 6 strings 品位范围: open-3 开放弦: 5th string (C), 4th string (G), 3rd string (C), 2nd... |
| 5 | `visual_caption:mr_style_008` | `mathrock_pdf` | 1.6851 | Math Rock 吉他教材 | 来源: Math Rock 吉他教材 / mathrock_pdf 视觉角色: style_visual_evidence 页码: 61 图像类型: chord_diagram 主题: G7_shell_voicings 调弦: standard 调性: G major 根音: G 和弦: G7 音程: major_third, minor_seventh 技法: shell_voicing, mute 弦组: 6 strings (with mutes) 品位范围: open / 4fr / 9fr 省略音: ... |

## KG Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| - | - | - | - | - | - |

## Bundle Judgement

```json
{
  "sufficient": true,
  "confidence": 0.71,
  "missing": [],
  "warnings": [],
  "evidence_type_count": 2,
  "text_count": 42,
  "visual_count": 25,
  "kg_count": 0,
  "next_queries": []
}
```

## Answer Seed

```json
{
  "recommended_structure": [
    "结论",
    "相关教材证据",
    "视觉/指法证据",
    "KG/风格关系",
    "可操作编配建议",
    "不确定点"
  ],
  "top_text_ids": [
    "text:chunk_0004",
    "text:chunk_0002",
    "text:chunk_0003"
  ],
  "top_visual_ids": [
    "visual_caption:mr_style_001_g7",
    "visual_caption:mr_style_001_bm7b5",
    "visual_caption:mr_style_002"
  ],
  "top_kg_ids": [],
  "composer_instruction": "只能基于 evidence_id 引用证据；区分教材明确内容与系统推断；如果 judgement.missing 非空，需要先说明证据不足。",
  "visual_collection": "guitar_visual_mixed_mathrock_trial_qwen3_06b",
  "model_rerank": {
    "text": {
      "enabled": false,
      "provider": "none",
      "reason": "disabled"
    },
    "visual": {
      "enabled": false,
      "provider": "none",
      "reason": "disabled"
    },
    "kg": {
      "enabled": false,
      "provider": "none",
      "reason": "disabled"
    }
  }
}
```

## Timings

```json
{
  "model_load_seconds": 4.5216301000036765,
  "fretboard_text_seconds": 0.3108060999948066,
  "visual_caption_seconds": 0.21865559997968376,
  "style_text_seconds": 0.09011009999085218,
  "model_rerank_seconds": 3.7299992982298136e-05,
  "total_seconds": 5.896607200003928
}
```
