# Query RAG Bundle Report

- Query: 标准调弦的普通 G7 和弦指型，不要点弦
- Intent: `mixed_lookup`
- Sufficient: `True`
- Confidence: 0.71
- Total latency: 6.797s

## Query Analysis

```json
{
  "query": "标准调弦的普通 G7 和弦指型，不要点弦",
  "intent": "mixed_lookup",
  "style_hints": [],
  "theory_terms": [
    "G7",
    "和弦",
    "指型"
  ],
  "technique_terms": [
    "点弦"
  ],
  "needs_fretboard_text": true,
  "needs_visual": true,
  "needs_style_text": true,
  "needs_kg": false,
  "confidence": 0.75,
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
| `fretboard_text` | `chroma` | `guitar_fretboard_handbook_text_qwen3_06b` | 5 | 指板/理论/练习题干证据 | 标准调弦的普通 G7 和弦指型，不要点弦 |
| `visual_caption` | `chroma` | `guitar_visual_mixed_mathrock_trial_qwen3_06b` | 5 | 具体图形/指法/voicing/答案图证据 | 标准调弦的普通 G7 和弦指型，不要点弦 指型图 和弦图 voicing |
| `style_text` | `chroma` | `guitar_text_chunks_qwen3_06b` | 5 | 风格/riff/节奏/技法文本证据 | 标准调弦的普通 G7 和弦指型，不要点弦 |

## Text Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `text:fretboard_text_0118` | `fretboard_handbook_clean_text` | 1.1194 | 吉他指板手册正文清洗层 | ## 10） Bb13 指型 11)Fmi11(b5) XI 12)Cma13(#11) 三 13) G9 VlI 14)D11 15)Ami13 XI 弹奏以上练习中的琶音，演奏时大声说出和弦名称、指型序号和声部构成。 “G大九和弦，指型4，‘1、3、5、7、9... D小九和弦，指型” 在指板上构建延伸和弦时，采用与七和弦一样的方法：升高八度或者降低八度，以使每根琴弦上仅有一个和弦音。通常，让延伸音在和弦的最高处比较好。 之前也曾提到过，在指板上弹奏延伸和弦时，可以根据演奏者的需要，忽略部分音符，从而获得更好... |
| 2 | `text:fretboard_text_0037` | `fretboard_handbook_clean_text` | 1.0819 | 吉他指板手册正文清洗层 | ## 练习12 利用大调音阶公式并根据下图中给出的根音画出各大调音阶指型中的其他音符。画音符时，不要按照品位标记进行，要尽可能使用最小的把位移动。圈出指型中的所有根音，并且用指型的序号标记出来。 2 G大调指型\_ 3)C大调指型一 = 51 Bb大调指型\_ = G大调指型 IV A大调指型\_ 8 Gb大调指型 I三I 101 Eb大调指型 三 弹奏每种指型。先大声说出每种音阶的名称和指型的序号。弹奏的时候也可以同时说出音符在音阶中的级数（第1一7级）。从每种指型中最低的根音开始弹奏，然后弹至最高的音符，接着... |
| 3 | `text:fretboard_text_0028` | `fretboard_handbook_clean_text` | 1.0786 | 吉他指板手册正文清洗层 | ## 练习10 在正确的弦上，画出指板图上方所写的音符。可以运用自然音阶推算的方法，也可以采用五种根音指型的方法。有时可能需要运用各种不同的方法： ·从每根弦的空弦音向上推算 ·从每根弦的第12品向下推算 ·从另外一个熟悉的音符（比如，第7品的D音）向上或者向下推算 ·选择一个临近的音符（比如E音)，首先找到它所在的位置 F VI 2) F# IV II G V A V Eb VII B 三 Db XI 10) C xV [图示引用 10 张，详见 image_refs] |
| 4 | `text:fretboard_text_0108` | `fretboard_handbook_clean_text` | 1.0739 | 吉他指板手册正文清洗层 | 学习目标：构建七和弦的常备声部。 前面我们已学习了密集和弦，实际上对于三和弦和七和弦而言，开放和弦有时更加悦耳好听并且更加容易弹奏。 对于七和弦来说，密集和弦有时在吉他上是很难弹奏的。按弦的手指有时够不到并按住全部的音符。例如，像Amaj7这样的密集和弦。 和弦中的音符在指板上的跨度太大，以致很难全部按住。同时，这样的和弦中也含有较多相近的低音，使得音色也会变得暗淡浑浊。 为了找到和弦中更有用的和弦音，常常需要将其中的某些音符升高或降低一个八度，这样就可以得到更加宽广的和弦声音。下面来尝试一下。密集大七和弦Ama... |
| 5 | `text:fretboard_text_0061` | `fretboard_handbook_clean_text` | 1.0731 | 吉他指板手册正文清洗层 | ## 纯四度 吉他的调弦应用的便是纯四度。每根弦都比其下方的弦高四度，除了第2弦的B音比第3弦的G音高一个大三度音程外。 [图示引用 3 张，详见 image_refs] |
| 6 | `text:fretboard_text_0044` | `fretboard_handbook_clean_text` | 1.0690 | 吉他指板手册正文清洗层 | ## 练习14 回到练习13。在每种指型上方用圆括号写出它的关系大调。在指型图中用方形画出其关系大调的根音。下面是第一个指型的例子。 E小调指型5(G大调指型4） 再次弹奏练习13中的各种指型。首先从小调音阶的根音弹奏这个指型，然后从其关系大调音阶的根音开始弹奏。弹奏之前先大声说出每种指型的序号。 [图示引用 1 张，详见 image_refs] |
| 7 | `text:fretboard_text_0021` | `fretboard_handbook_clean_text` | 1.0497 | 吉他指板手册正文清洗层 | ## 练习8 指板上第12品位置的音符和空弦的音符是相同的。用一张含有6根弦的指板图，在每根弦的第12品处标出音符的名称。然后再次在每根弦上写出每个自然音阶音符，不同的是这次从第12品开始，向前写出来。记住F和E之间是半音，C和B之间也是半音。 ←A 除了以上这些练习之外，你还可以这样练习。先弹奏每根弦空弦上的自然音阶音符。然后从空弦位置向上一直弹奏到手可以容易按得到的位置。在弹奏的同时大声地说出每个音符的名称（以及所在品格的位置）： “第6弦：、空·F、第品G、第3品…A、第5品…B、第品…C、第8…” 说出品... |
| 8 | `text:fretboard_text_0010` | `fretboard_handbook_clean_text` | 1.0415 | 吉他指板手册正文清洗层 | ## 琴弦 琴弦一般按从第6弦到第1弦的顺序命名。第6弦指的是最粗的那根琴弦，而第1弦指的是最细的那根。同时第1弦也是音高最高的琴弦。 向上到下一根琴弦的意思就是说到音高更高的琴弦上。除非你是倒立着弹吉他（见第19章)，否则这里所说的移动到更高的弦时，指的是将手指向地面的方向移动。这样说来，标示弦的数字与我们通常理解的意义是相反的。要想改变这个规则是比较难的，目前所有 的吉他书籍都是这样标示的。 从第6弦开始，每根弦用字母标示的名称是：E、A、D、G、B、E。在开始下面的学习之前，先记熟这些弦的名称。记住了这些内... |
| 9 | `text:fretboard_text_0018` | `fretboard_handbook_clean_text` | 1.0386 | 吉他指板手册正文清洗层 | 学习目标：学习音乐的字母表；认识全音和半音；记住B和C之间、E和F之间的自然半音。 音乐中一共有12个音。但是，通常仅用字母表中的7个字母来表示它们：A、B、C、D、E、F和G。是不是有些糊涂了？ 之所以用7个字母来表示，是因为大多数的音乐都是用7个音符构成的音阶来创作的。使用7个音符可以很快地组合成一个音阶。如果要用到12个音符中的其他音符时，可以在这7个音符的末尾加上一个临时记号（#、b或者)。临时记号是非常重要的，所以请反复大声朗读下面这句话： “升号（#）升高音符，降号（b）降低音符，还原记号（）将它们变... |
| 10 | `text:md_chunk_0021` | `fretboard_handbook_mineru` | 1.0263 | 吉他指板手册 | ## 第19章调式 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边构建C小调的两个和弦若干次： [IMAGE_BLOCK:images/82991... |

## Visual Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `visual_caption:fretboard_answer_E50_6` | `fretboard_handbook_question_answer` | 1.2258 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 50 小题: 6 证据类型: fretboard_diagram 视觉类型: chord_diagram 对象: Gmi9 指型4 根音: G 性质/调式: minor ninth 位置/指型: 指型4 / III把位 音程: 1, b3, b7, 9 方向: vertical 把位: III 可见标签: 6) 和弦 Gmi9, 指型 4, 1 b3 b7 9 按点概述: 垂直指板图，左侧标注罗马数字III。根音（双圈）位于推断的6弦3品(G)，其余按点分布在5弦、4弦及2弦，构成G... |
| 2 | `visual_caption:fretboard_answer_E48_13` | `fretboard_handbook_question_answer` | 1.2249 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 48 小题: 13 证据类型: fretboard_diagram 视觉类型: chord_diagram 对象: G9 指型 1 根音: G 性质/调式: dominant ninth 位置/指型: 指型 1 / VII把位 方向: horizontal 把位: VII 可见标签: 3) G9, 指型 1, VII 按点概述: 横向指板图，显示5个按点。根音位于第6弦（推断）VII品（双圈标记），其余音符分布在相邻弦的高把位区域，构成G9和弦指型。 caption: G9和弦指板图... |
| 3 | `visual_caption:fretboard_answer_E51_8` | `fretboard_handbook_question_answer` | 1.1999 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 51 小题: 8 证据类型: fretboard_diagram 视觉类型: chord_diagram 对象: G7(#5) 根音: G 性质/调式: dominant seventh sharp five 位置/指型: III (3rd fret root on E string) 音程: b7, 3, #5 方向: vertical 把位: III 品位范围: 1-5 可见标签: 8), G7(#5), b7, 3, #5 按点概述: Root at 3rd fret low ... |
| 4 | `visual_caption:fretboard_answer_E48_1` | `fretboard_handbook_question_answer` | 1.1956 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 48 小题: 1 证据类型: fretboard_diagram 视觉类型: chord_diagram 对象: Gma9 指型 4 根音: G 性质/调式: major ninth 位置/指型: 指型 4 方向: horizontal 可见标签: 1) Gma9, 指型 4 按点概述: 横向指板图，显示5个按点。根据Gma9和弦构成及指型分布推断，根音G位于第6弦3品（带圈标记），其余音符分布在相邻品格，符合G大调九和弦指法特征。 caption: 练习48第1题答案：Gma9和弦... |
| 5 | `visual_caption:fretboard_answer_E07_4` | `fretboard_handbook_question_answer` | 1.1772 | 吉他指板手册：题目级练习答案图 | 来源: 吉他指板手册 练习: 7 小题: 4 证据类型: fretboard_diagram 视觉类型: scale_pattern 对象: 吉他指板半音阶（Chromatic Scale）全音符名称对照表 根音: G 性质/调式: Chromatic / 半音阶 位置/指型: 3弦开放把位至12品八度 答案项: 1: G#/Ab; 2: A#/Bb; 3: C#/Db; 4: D#/Eb; 5: F#/Gb 方向: horizontal 品位范围: Open-12 可见标签: G, G# Ab, A, A# B... |

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
  "text_count": 43,
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
    "text:fretboard_text_0118",
    "text:fretboard_text_0037",
    "text:fretboard_text_0028"
  ],
  "top_visual_ids": [
    "visual_caption:fretboard_answer_E50_6",
    "visual_caption:fretboard_answer_E48_13",
    "visual_caption:fretboard_answer_E51_8"
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
  "model_load_seconds": 5.210897200013278,
  "fretboard_text_seconds": 0.3516161000006832,
  "visual_caption_seconds": 0.22294710000278428,
  "style_text_seconds": 0.07544620000408031,
  "model_rerank_seconds": 3.480000304989517e-05,
  "total_seconds": 6.797014399984619
}
```
