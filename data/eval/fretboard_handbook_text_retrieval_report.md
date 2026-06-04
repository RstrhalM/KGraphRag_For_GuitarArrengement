# Text RAG Retrieval Evaluation

## Summary

- Collection: `guitar_fretboard_handbook_text_qwen3_06b` (174 docs)
- Model: `Qwen/Qwen3-Embedding-0.6B` on `cuda`, dim=1024
- Tests: 10, TopK: 5
- Rerank: `True`, candidates: 20
- Pass all: 10/10
- Source Hit@1: 10/10
- Source Hit@K: 10/10
- Keyword Hit@1: 10/10
- Keyword Hit@K: 10/10
- Avg latency/query: 0.077s
- Median latency/query: 0.040s

## Cases

### fretboard_strings_names - PASS

- Query: 标准调弦下吉他第6弦到第1弦的名称是什么
- Expected sources: fretboard_handbook_clean_text
- Expected keywords any: E、A、D、G、B、E, 第6弦, 第1弦
- Rerank: `True`, candidates: 20
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.385s = embed 0.315s + chroma 0.070s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.1211 | -0.1111 | `fretboard_handbook_clean_text` | `fretboard_text_0010` | 弦到第 | ## 琴弦 琴弦一般按从第6弦到第1弦的顺序命名。第6弦指的是最粗的那根琴弦，而第1弦指的是最细的那根。同时第1弦也是音高最高的琴弦。 向上到下一根琴弦的意思就是说到音高更高的琴弦上。除非你是倒立着弹吉他（见第19章)，否则这里所说的移动到更高的弦时，指的是将手指向地面的方向移动。这样说来，标示弦的数字与我们通常理解的意义是相反的。要想改变这个规则是比较难的，目前所有 的吉他书籍都是这样标示的。 从第6弦开始，每根弦用字母标示的名称是... |
| 2 | 2 | Y |  | 0.1341 | -0.1241 | `fretboard_handbook_clean_text` | `fretboard_text_0061` | 调弦 | ## 纯四度 吉他的调弦应用的便是纯四度。每根弦都比其下方的弦高四度，除了第2弦的B音比第3弦的G音高一个大三度音程外。 [图示引用 3 张，详见 image_refs] |
| 3 | 3 | Y | Y | 0.1556 | -0.1556 | `fretboard_handbook_clean_text` | `fretboard_text_0013` |  | ## 练习3 大声回答下面的问题，并且填空。 1.第3弦的字母名称是什么？ 2.B弦是第几弦？ 3.第4弦的字母名称是什么？ 4.G弦是第几弦？ 5.第6弦的字母名称是什么？ 6.A弦是第几弦？ 7.第2弦的字母名称是什么？ 8.E弦是第几弦？ 9.第1弦的字母名称是什么？ 10.D弦是第几弦？ |
| 4 | 4 | Y | Y | 0.1762 | -0.1762 | `fretboard_handbook_clean_text` | `fretboard_text_0021` |  | ## 练习8 指板上第12品位置的音符和空弦的音符是相同的。用一张含有6根弦的指板图，在每根弦的第12品处标出音符的名称。然后再次在每根弦上写出每个自然音阶音符，不同的是这次从第12品开始，向前写出来。记住F和E之间是半音，C和B之间也是半音。 ←A 除了以上这些练习之外，你还可以这样练习。先弹奏每根弦空弦上的自然音阶音符。然后从空弦位置向上一直弹奏到手可以容易按得到的位置。在弹奏的同时大声地说出每个音符的名称（以及所在品格的位置）：... |
| 5 | 5 | Y | Y | 0.1816 | -0.1816 | `fretboard_handbook_clean_text` | `fretboard_text_0019` |  | ## 练习6 画出每根弦上的自然音阶音符。在下面写出音符的名称。其中第6弦的音符已经作为例子写出来了。 [图示引用 6 张，详见 image_refs] |

### fretboard_root_form_3 - PASS

- Query: 指型3的根音在第几弦，相差几品
- Expected sources: fretboard_handbook_clean_text
- Expected keywords any: 指型3, 第3弦, 第5弦, 第6弦
- Rerank: `True`, candidates: 20
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.040s = embed 0.038s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.1161 | -0.0961 | `fretboard_handbook_clean_text` | `fretboard_text_0024` | 指型, 根音 | ## 方法2：根音型式 我们也可以通过使用根音型式来命名音符。比如前面我们找到了第2弦第7品上的音符，它属于根音指型5，这个指型的根音在第2弦和第4弦上，距离为3品。这样就可以知道第4弦的第4品和我们已经知道的音符具有相同的名称。 指型5 VlI 根音指型4的根音在第1弦、第6弦和第4弦上，距离2品。按照前面的方法推算，在第6弦第2品处也和之前找到的音符是相同的。这个音比E弦的空弦音高2品，那么它就是F#或者Gb(我们要找的音)。 指... |
| 2 | 2 | Y |  | 0.1278 | -0.1078 | `fretboard_handbook_clean_text` | `fretboard_text_0028` | 指型, 根音 | ## 练习10 在正确的弦上，画出指板图上方所写的音符。可以运用自然音阶推算的方法，也可以采用五种根音指型的方法。有时可能需要运用各种不同的方法： ·从每根弦的空弦音向上推算 ·从每根弦的第12品向下推算 ·从另外一个熟悉的音符（比如，第7品的D音）向上或者向下推算 ·选择一个临近的音符（比如E音)，首先找到它所在的位置 F VI 2) F# IV II G V A V Eb VII B 三 Db XI 10) C xV [图示引用 ... |
| 3 | 3 | Y | Y | 0.1304 | -0.1104 | `fretboard_handbook_clean_text` | `fretboard_text_0025` | 指型, 根音 | ## 新音符：第7品的D音 如果你已经记住了除空弦音以外的很少几个其他音符，那么采用根音型式的方法找到别的音符也是非常方便的。比如我们己经记住一个新的音符，第3弦第7品的D音。 VlI 现在你已经可以更快地说出3弦在这个音附近的音符名称了。并且根据根音指型的知识，第3弦上的任意一个音符都可以作为根音型式2和根音型式3中的音符，因此可以直接由此得出组成这些根音型式的其他音符的位置。 VII [图示引用 2 张，详见 image_refs] |
| 4 | 6 | Y | Y | 0.1516 | -0.1316 | `fretboard_handbook_clean_text` | `fretboard_text_0014` | 指型, 根音 | 学习目标：学习五种根音型式。 每种音阶、和弦或者旋律都是由一组音符构成的，这组音符中有一个主要的音被称为根音。根音可以作为我们的向导，如果没有根音，就会迷失方向。 当我们找到一个根音的位置时，就可以根据它的位置找出相邻的另外一个根音。这两个相邻的根音就构成了一种根音型式。在指板上共有五种根音型式，所以用1到5这五个数字进行标识。以C调为例，下面是C调中的五种根音型式。 C调 随着本书的学习，你会逐渐体会出这些根音型式是相当重要的。演奏... |
| 5 | 7 | Y |  | 0.1534 | -0.1334 | `fretboard_handbook_clean_text` | `fretboard_text_0037` | 指型, 根音 | ## 练习12 利用大调音阶公式并根据下图中给出的根音画出各大调音阶指型中的其他音符。画音符时，不要按照品位标记进行，要尽可能使用最小的把位移动。圈出指型中的所有根音，并且用指型的序号标记出来。 2 G大调指型\_ 3)C大调指型一 = 51 Bb大调指型\_ = G大调指型 IV A大调指型\_ 8 Gb大调指型 I三I 101 Eb大调指型 三 弹奏每种指型。先大声说出每种音阶的名称和指型的序号。弹奏的时候也可以同时说出音符在音阶... |

### fretboard_major_scale_formula - PASS

- Query: 大调音阶的全音半音结构是什么
- Expected sources: fretboard_handbook_clean_text
- Expected keywords any: 大调音阶, 全音, 半音
- Rerank: `True`, candidates: 20
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.040s = embed 0.037s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.1255 | -0.1155 | `fretboard_handbook_clean_text` | `fretboard_text_0031` | 音阶 | ## 大调音阶公式 音阶中的音符通常用“音阶的级数”来表示，或者简称“音级”。想要搞清楚音级的位置，就先要牢记大调音阶的公式。反复大声说出下面这句话： “全、全、半、全、全、全、半。” 任何一个大调音阶中，3级音和4级音之间都是半音，7级音和8级音之间也是半音。除此之外，其他相邻两音之间都是全音。在纸上写出一个完整的音阶，然后在半音关系的两个音符之间写上一个（^）符号，就像这样：1234567^8。 在不是从C音开始的其他大调中，要保... |
| 2 | 2 | Y | Y | 0.1299 | -0.1199 | `fretboard_handbook_clean_text` | `fretboard_text_0124` | 音阶 | 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边构建C小调的两个和弦... |
| 3 | 3 | Y | Y | 0.1315 | -0.1215 | `fretboard_handbook_clean_text` | `fretboard_text_0048` | 音阶 | ## 练习16 依据给出的根音在下面的图示中画出大调音阶。可以应用前面学到的大调音阶公式：全一全一半一全一全一全—半（123^4567^8)。这些音符中包含了4级音和7级音，用叉号将这些音符划出，剩下的音符便组成了大调五声音阶。用圆圈圈出根音，在图示上方写出音阶的名称和指型的序号。第一个图示作为例子已经给出。 弹奏上面每个图示中的练习，先弹大调音阶，再弹大调五声音阶。在弹奏的同时要大声地说出音阶的名称和指型的序号。 [图示引用 1 张... |
| 4 | 4 | Y | Y | 0.1332 | -0.1232 | `fretboard_handbook_clean_text` | `fretboard_text_0039` | 音阶 | 学习目标：构建自然小调音阶的五种指型。理解关系小调和关系大调。 大调音阶只有一种构建公式，但对于小调音阶来说却有许多种构建方式，每一种都有它自己的公式。当人们提到“小调音阶”时，首先想到的应该是自然小调音阶。下面是它的构建公式（大声地读出来）： |
| 5 | 5 | Y | Y | 0.1363 | -0.1263 | `fretboard_handbook_clean_text` | `fretboard_text_0129` | 音阶 | ## 练习54 写出各种调式的音阶，其中Ionian（大调）音阶和Aeolian（自然小调）音阶已经给出。可以参考以上练习中的指板指型，也可以参考之前学过的C大调（Ionian）音阶的全音和半音关系。 [图示引用 1 张，详见 image_refs] |

### fretboard_relative_minor - PASS

- Query: 自然小调音阶和关系大调有什么关系
- Expected sources: fretboard_handbook_clean_text
- Expected keywords any: 自然小调, 关系大调, 小调音阶
- Rerank: `True`, candidates: 20
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.039s = embed 0.037s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.1065 | -0.0965 | `fretboard_handbook_clean_text` | `fretboard_text_0039` | 音阶 | 学习目标：构建自然小调音阶的五种指型。理解关系小调和关系大调。 大调音阶只有一种构建公式，但对于小调音阶来说却有许多种构建方式，每一种都有它自己的公式。当人们提到“小调音阶”时，首先想到的应该是自然小调音阶。下面是它的构建公式（大声地读出来）： |
| 2 | 2 | Y | Y | 0.1235 | -0.1135 | `fretboard_handbook_clean_text` | `fretboard_text_0124` | 音阶 | 学习目标：记住各种调式的顺序，学习伊奥尼亚（Ionian）调式。 当我们学习小调音阶的时候，已经知道小调音阶和大调音阶是相关的。先来复习一下关系大小调：“大调音阶的6级音是其关系小调的根音。” 当练习大调音阶和小调音阶的时候，你会发现如果不采用特殊的方法强调根音的话，比如从根音开始并以根音结束，很难去找出哪个音是音阶的根音。但是，当在一个和弦进行中弹奏某一大调或者小调音阶，就很容易找出哪个音是根音。 例如，弹奏右边构建C小调的两个和弦... |
| 3 | 3 | Y | Y | 0.1331 | -0.1231 | `fretboard_handbook_clean_text` | `fretboard_text_0043` | 音阶 | ## 关系小调和关系大调 在进行前面的练习时，你也许会注意到，这些音阶指型和之前我们学过的大调音阶指型是基本相同的。唯一不同的地方就是指型中的根音不同。例如，在写出E小调音阶时，就用到了G大调音阶中的音符。这是因为，E小调是G大调的关系小调。 这种关系十分重要，所以请大声地复述下面的话： “大调音阶的6级音是其关系小调的根音。” 反过来说也是对的，G大调也是E小调的关系大调。下面再大声地复述下面这句话： “小调音阶的3级音是其关系大调... |
| 4 | 4 | Y | Y | 0.1367 | -0.1267 | `fretboard_handbook_clean_text` | `fretboard_text_0051` | 音阶 | ## 关系五声音阶 五声音阶中也存在关系大小调的概念。我们可以通过大声说出下面的方法来获得关系小调五声音阶： “大调音阶的6级音是其关系小调五声音阶的根音。” 得到关系大调五声音阶的规则如下： “小调音阶的3级音是其关系大调五声音阶的根音。” (F大调五声音阶指型1） |
| 5 | 5 | Y | Y | 0.1501 | -0.1401 | `fretboard_handbook_clean_text` | `fretboard_text_0129` | 音阶 | ## 练习54 写出各种调式的音阶，其中Ionian（大调）音阶和Aeolian（自然小调）音阶已经给出。可以参考以上练习中的指板指型，也可以参考之前学过的C大调（Ionian）音阶的全音和半音关系。 [图示引用 1 张，详见 image_refs] |

### fretboard_pentatonic_scale - PASS

- Query: 五声音阶为什么少了两个音
- Expected sources: fretboard_handbook_clean_text
- Expected keywords any: 五声音阶, 大调音阶, 七个音
- Rerank: `True`, candidates: 20
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.057s = embed 0.055s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.1525 | -0.1425 | `fretboard_handbook_clean_text` | `fretboard_text_0049` | 音阶 | ## 小调五声音阶 小调五声音阶的构建方式是，从自然小调音阶中，去除2级音和6级音。为了记忆小调五声音阶的构成方式，请大声朗读下面这句话： “小调五声音阶没有2级音和6级音。” |
| 2 | 2 | Y | Y | 0.1690 | -0.1590 | `fretboard_handbook_clean_text` | `fretboard_text_0055` | 音阶 | ## 练习21 依据下面每一图示中给出的根音，用小调音阶公式构建小调五声音阶，注意去除2级音和6级音。写出每一图示中对应的音阶名称和指型序号。 1） D小调五声音阶 2) 4) 5) [图示引用 10 张，详见 image_refs] |
| 3 | 3 | Y | Y | 0.1763 | -0.1663 | `fretboard_handbook_clean_text` | `fretboard_text_0046` | 音阶 | 学习目标：构建五种大调五声音阶指型和五种小调音阶指型。 五声音阶只包含五个音符。五声音阶的英文“pentatonic”来自希腊语“penta”（五）和“tonos”（音）。在五声音阶的每种指型中，每根琴弦上都只有2个音符，这让五声音阶演奏起来非常容易并且很有趣。五声音阶是许多摇滚乐、布鲁斯音乐和乡村音乐独奏的基础。 |
| 4 | 4 | Y | Y | 0.1778 | -0.1678 | `fretboard_handbook_clean_text` | `fretboard_text_0056` | 音阶 | ## 练习22 回到前面的两个练习（练习20和练习21)，写出每一图形中对应的关系小调五声音阶或关系大调五声音阶，并且用方形画出关系调中的根音。 弹奏以上这些练习。对于练习20，先弹大调五声音阶，然后再弹它的关系小调五声音阶。对于练习21，先弹小调五声音阶，然后再弹其关系大调五声音阶。在弹奏之前请说出音阶名称和指型序号。 |
| 5 | 5 | Y | Y | 0.1779 | -0.1679 | `fretboard_handbook_clean_text` | `fretboard_text_0050` | 音阶 | ## 练习17 依据给出的根音在下面的图示中画出自然小调音阶。可以应用前面学到的自然小调音阶公式：全一半一全一全一半一全一全（12^345^678)。从这些音符中用叉号划出2级音和6级音，便可得到小调五声音阶。在每一图示的上方写出音阶的名称和指型的序号。 弹奏上面每个图示中的练习，先弹自然小调音阶，再弹小调五声音阶。要能够识别每一图示中的音阶名称和指型序号，并且要在弹奏之前大声地说出来。 [图示引用 1 张，详见 image_refs] |

### fretboard_major_triad_arpeggio - PASS

- Query: 大三和弦琶音由哪些音构成
- Expected sources: fretboard_handbook_clean_text
- Expected keywords any: 大三和弦, 1、3、5, 根音
- Rerank: `True`, candidates: 20
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.040s = embed 0.038s + chroma 0.003s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.1056 | -0.0856 | `fretboard_handbook_clean_text` | `fretboard_text_0078` | 和弦, 琶音 | ## 大三和弦琵音 大三和弦的组成包括根音和根音上的大三度和纯五度音，也就是：1、3、5。也可以将其看成是大调音阶的1级、3级和5级音。通过重复这些音符（在不同的八度中）可以组建C大三和弦琶音的两种型式。 C大三和弦 XI C大三和弦，指型2 [图示引用 2 张，详见 image_refs] |
| 2 | 4 | Y | Y | 0.1249 | -0.1049 | `fretboard_handbook_clean_text` | `fretboard_text_0077` | 和弦, 琶音 | 学习目标：在指板上构建三和弦的琶音。 两个或者更多的音同时发声称为和弦。而琶音是指将和弦中的音符依次弹出，而不是同时弹奏。在指板上找出琶音比和弦更加容易，所以我们先来学习琶音。下一章，将用这章学习到的同样的音符来组成和弦。 最基础的琶音（或和弦）是三和弦。三和弦由三个音构成：根音、三度音和五度音。这些音可以在不同的八度中重复，以此方式来构成指型1到指型5这五种琶音指型。 不要试图在一天中记住所有的指型。在开始学习时，用大声朗读的方法，... |
| 3 | 5 | Y | Y | 0.1296 | -0.1096 | `fretboard_handbook_clean_text` | `fretboard_text_0086` | 和弦, 琶音 | 学习目标：在指板上构建密集三和弦。弹奏密集三和弦的所有转位。 相对于琶音是依次弹奏每一个音，和弦是同时扫奏或拨奏所有的音。琶音存在同一根弦上有2个音符的情况，但是在和弦中不会，因为一根弦一次只能发出一个音。这也是我们先学习琶音，再学习和弦的原因。相对于琶音而言，和弦会稍难一些。 在指板上找到琶音在不同弦上的音，然后同时扫奏或拨奏，这样就产生了和弦。和弦中音符不同的排列方式称为声部。一个完整的三和弦声部仅需要3个音符，但吉他手在演奏三和... |
| 4 | 2 | Y | Y | 0.1219 | -0.1119 | `fretboard_handbook_clean_text` | `fretboard_text_0087` | 和弦 | ## 大三和弦 大三和弦是由根音、根音的大三度音和纯五度音组成的：1、3、5。大三和弦可用下面任意一种和弦标记来表达：Abmai，Abma，AbMa，Ab。 |
| 5 | 3 | Y | Y | 0.1231 | -0.1131 | `fretboard_handbook_clean_text` | `fretboard_text_0080` | 和弦 | ## 小三和弦琵音 小三和弦是由根音、根音上方的小三度音和纯五度音组成的：1、b3、5。 |

### fretboard_chord_voicing_definition - PASS

- Query: 和弦声部是什么意思，为什么吉他三和弦会重复八度音
- Expected sources: fretboard_handbook_clean_text
- Expected keywords any: 声部, 三和弦, 不同的八度
- Rerank: `True`, candidates: 20
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.049s = embed 0.047s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.1168 | -0.0968 | `fretboard_handbook_clean_text` | `fretboard_text_0086` | 和弦, 声部 | 学习目标：在指板上构建密集三和弦。弹奏密集三和弦的所有转位。 相对于琶音是依次弹奏每一个音，和弦是同时扫奏或拨奏所有的音。琶音存在同一根弦上有2个音符的情况，但是在和弦中不会，因为一根弦一次只能发出一个音。这也是我们先学习琶音，再学习和弦的原因。相对于琶音而言，和弦会稍难一些。 在指板上找到琶音在不同弦上的音，然后同时扫奏或拨奏，这样就产生了和弦。和弦中音符不同的排列方式称为声部。一个完整的三和弦声部仅需要3个音符，但吉他手在演奏三和... |
| 2 | 2 | Y | Y | 0.1538 | -0.1338 | `fretboard_handbook_clean_text` | `fretboard_text_0108` | 和弦, 声部 | 学习目标：构建七和弦的常备声部。 前面我们已学习了密集和弦，实际上对于三和弦和七和弦而言，开放和弦有时更加悦耳好听并且更加容易弹奏。 对于七和弦来说，密集和弦有时在吉他上是很难弹奏的。按弦的手指有时够不到并按住全部的音符。例如，像Amaj7这样的密集和弦。 和弦中的音符在指板上的跨度太大，以致很难全部按住。同时，这样的和弦中也含有较多相近的低音，使得音色也会变得暗淡浑浊。 为了找到和弦中更有用的和弦音，常常需要将其中的某些音符升高或降... |
| 3 | 4 | Y | Y | 0.1616 | -0.1416 | `fretboard_handbook_clean_text` | `fretboard_text_0137` | 和弦, 声部 | ## 分割（Slash）和弦 分割和弦就是将三和弦或七和弦叠加在一个非和弦根音的低音上。这种和弦可以用这种方式来表达：C/D。当这个低音也是和弦中的音时，分割和弦就变成了一种和弦转位。否则，分割和弦就是延伸和弦或者变化和弦的一种声部构成。 |
| 4 | 3 | Y | Y | 0.1540 | -0.1440 | `fretboard_handbook_clean_text` | `fretboard_text_0077` | 和弦 | 学习目标：在指板上构建三和弦的琶音。 两个或者更多的音同时发声称为和弦。而琶音是指将和弦中的音符依次弹出，而不是同时弹奏。在指板上找出琶音比和弦更加容易，所以我们先来学习琶音。下一章，将用这章学习到的同样的音符来组成和弦。 最基础的琶音（或和弦）是三和弦。三和弦由三个音构成：根音、三度音和五度音。这些音可以在不同的八度中重复，以此方式来构成指型1到指型5这五种琶音指型。 不要试图在一天中记住所有的指型。在开始学习时，用大声朗读的方法，... |
| 5 | 5 | Y | Y | 0.1665 | -0.1465 | `fretboard_handbook_clean_text` | `fretboard_text_0118` | 和弦, 声部 | ## 10） Bb13 指型 11)Fmi11(b5) XI 12)Cma13(#11) 三 13) G9 VlI 14)D11 15)Ami13 XI 弹奏以上练习中的琶音，演奏时大声说出和弦名称、指型序号和声部构成。 “G大九和弦，指型4，‘1、3、5、7、9... D小九和弦，指型” 在指板上构建延伸和弦时，采用与七和弦一样的方法：升高八度或者降低八度，以使每根琴弦上仅有一个和弦音。通常，让延伸音在和弦的最高处比较好。 之前也曾... |

### fretboard_extended_chord_11th - PASS

- Query: 延伸和弦里九度十一度十三度是什么概念
- Expected sources: fretboard_handbook_clean_text
- Expected keywords any: 延伸和弦, 九度, 十一度, 十三度
- Rerank: `True`, candidates: 20
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.038s = embed 0.036s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.1482 | -0.1382 | `fretboard_handbook_clean_text` | `fretboard_text_0115` | 和弦 | 学习目标：学习构建延伸和弦及其琶音，并在指板上进行应用。 延伸和弦指的是在七和弦的基础上再增加根音上方其他音程的一个或者几个音：如九度、十一度或者十三度音。在有些地区，这些增加的音符被称为“延伸音”。延伸和弦常被运用在一些特定的音乐风格中，或者有的乐手喜欢用它来替代七和弦，从而起到特殊的效果。 这里仅用“和弦”来进行讲解，但是下面的规则既适用于和弦也适用于琶音。 ·当对七和弦进行和弦延伸时，和弦本身的性质不变； ·任何的ma7，dom... |
| 2 | 2 | Y | Y | 0.1530 | -0.1430 | `fretboard_handbook_clean_text` | `fretboard_text_0118` | 和弦 | ## 10） Bb13 指型 11)Fmi11(b5) XI 12)Cma13(#11) 三 13) G9 VlI 14)D11 15)Ami13 XI 弹奏以上练习中的琶音，演奏时大声说出和弦名称、指型序号和声部构成。 “G大九和弦，指型4，‘1、3、5、7、9... D小九和弦，指型” 在指板上构建延伸和弦时，采用与七和弦一样的方法：升高八度或者降低八度，以使每根琴弦上仅有一个和弦音。通常，让延伸音在和弦的最高处比较好。 之前也曾... |
| 3 | 3 | Y | Y | 0.1666 | -0.1566 | `fretboard_handbook_clean_text` | `fretboard_text_0119` | 和弦 | ## 练习49 根据给出的声部构成，在下面的图示中构建延伸和弦。 5）F#7(#11) 6Db13 7）A13(#11) 8 E13 10）F9（#11) 弹奏上页练习中的延伸和弦，弹奏时大声说出和弦名称、指型序号和声部构成。 “C九和弦，指型1，‘1、3、b7、. G大十三和弦，指型4，‘1、3、7、13..” [图示引用 10 张，详见 image_refs] |
| 4 | 4 | Y | Y | 0.1801 | -0.1701 | `fretboard_handbook_clean_text` | `fretboard_text_0116` | 和弦 | ## 麻烦的十一度音 在音乐中，十一度音和四度音是等效的。当弹奏一个和弦时，如果和弦中包含了大三度，那么四度和五度音听上去就会不和谐。这就意味着对于大和弦和属和弦，在延伸至十一度或超过十一度时，就需要进行特别的考虑。在琶音中，这种不和谐不太明显，因为每个音符都是单独发音的，但是在弹奏和弦时，这种不和谐会非常明显。下面一些常用的练习可以有效地解决这一问题。 通常，在大和弦和属和弦中，采用将十一度音升高半音的方法来解决这个问题。它可以有效... |
| 5 | 5 | Y | Y | 0.1803 | -0.1703 | `fretboard_handbook_clean_text` | `fretboard_text_0135` | 和弦 | 学习目标：练习运用音程关系构建各种和弦。 除了七和弦和它的延伸和弦以及变化和弦，还有一些比较常用的和弦也应该了解。通常可以通过它们的名称推算出它们的构成音符。 ·挂留和弦：用音阶中的4级音代替三和弦中的三度音，就形成了 sus4—1、4、5挂四和弦（sus4)。现在也常用到sus2和弦。尽管它们不是真正 sus2—1、2、5意义上的三和弦，但应该将sus4和sus2和弦归到三和弦中去学习。它们十分常见。 ·六和弦：在三和弦中加入大六度... |

### fretboard_exercise_30_prompt - PASS

- Query: 练习30要求怎样构建D大三和弦琶音五种指型
- Expected sources: fretboard_handbook_clean_text
- Expected keywords any: 练习30, D大三和弦琶音, 五种指型
- Rerank: `True`, candidates: 20
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.040s = embed 0.038s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 2 | Y | Y | 0.1206 | -0.0906 | `fretboard_handbook_clean_text` | `fretboard_text_0079` | 和弦, 琶音, 练习 | ## 练习30 运用五种大调音阶指型中的音符，构建D大三和弦琶音的五种指型。注意不要使用品位标记以下的音符，并且在画出音符时，保证所有的音符都在左手所在的把位以内，最多不要超出1品以外。 1）D大三和弦琶音 指型1 2)D大三和弦琶音 指型2 3)D大三和弦琶音 = 指型3 4)D大三和弦琶音 IV VII 指型4 5)D大三和弦琶音 指型5 IX 弹奏以上这些D大三和弦琶音，演奏时要大声说出和弦名称及指型序号。弹奏时，从每一指型中最... |
| 2 | 3 | Y | Y | 0.1218 | -0.0918 | `fretboard_handbook_clean_text` | `fretboard_text_0081` | 和弦, 琶音, 练习 | ## 练习31 构建D小三和弦琶音的五种指型。注意不要用品位标记以下的音符，并且在画出音符时，保证所有的音符都在左手所在的把位以内，最多不要超出1品以外。 1)D小三和弦琶音 V 2)D小三和弦琶音 指型2 3)D小三和弦琶音 = VII 4)D小三和弦琶音 5）D小三和弦琶音 指型5 X XI 弹奏以上这些D小三和弦琶音，演奏时要大声说出和弦名称及指型序号。同时，要注意仔细聆听琶音中不同的音程性质。 [图示引用 5 张，详见 ima... |
| 3 | 1 | Y | Y | 0.1147 | -0.0947 | `fretboard_handbook_clean_text` | `fretboard_text_0149` | 和弦, 练习 | ## 练习30 1)D大三和弦指型1 b9 [图示引用 2 张，详见 image_refs] |
| 4 | 5 | Y |  | 0.1255 | -0.0955 | `fretboard_handbook_clean_text` | `fretboard_text_0083` | 和弦, 琶音, 练习 | ## 练习32 对应五种根音指型，构建D减三和弦琶音型式。注意不要用品位标记以下的音符，并且在画出音符时，保证所有的音符都在左手所在的把位以内，最多不要超出1品以外。其中在有些指型中需要越弦演奏。 1）D减三和弦琶音 2）D减三和弦琶音 指型2 3）D减三和弦琶音 III VI 4）D减三和弦琶音 5)D减三和弦琶音 X XI 弹奏以上这些D减三和弦琶音，演奏时要大声说出和弦名称及指型序号。同时，要注意仔细聆听琶音中不同的音程性质。 ... |
| 5 | 6 | Y |  | 0.1266 | -0.0966 | `fretboard_handbook_clean_text` | `fretboard_text_0085` | 和弦, 琶音, 练习 | ## 练习33 在五种根音指型中，构建D增三和弦琶音型式。不用圈出每个音符。其中有些指型需要越弦演奏。在构建增三和弦时会发现，有时同一指型中的一个音符有两种弹法，这两种都是正确的。 1)D增三和弦琶音 指型1 = 2)D增三和弦琶音 指型2 3）D增三和弦琶音 IV VI 4)D增三和弦琶音 IX 5)D增三和弦琶音 指型5 XI 弹奏以上这些D增三和弦琶音，演奏时要大声说出和弦名称及指型序号。同时，要注意仔细聆听琶音中不同的音程性质... |

### fretboard_answer_exercise_15 - PASS

- Query: 练习15答案里D大调指型1对应哪个小调指型
- Expected sources: fretboard_handbook_clean_text
- Expected keywords any: D大调指型1, B小调指型2, 练习15
- Rerank: `True`, candidates: 20
- Source first rank: 1
- Keyword first rank: 1
- Latency: total 0.041s = embed 0.038s + chroma 0.002s

| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |
|---:|---:|:---:|:---:|---:|---:|---|---|---|---|
| 1 | 1 | Y | Y | 0.0813 | -0.0613 | `fretboard_handbook_clean_text` | `fretboard_text_0143` | 大调指型, 练习 | ## 练习15 D大调指型1（B小调指型2） G大调指型4（E小调指型5） C大调指型2（A小调指型3） E大调指型5（C#小调指型1） Bb大调指型3（G小调指型4） [图示引用 5 张，详见 image_refs] |
| 2 | 2 | Y | Y | 0.0864 | -0.0664 | `fretboard_handbook_clean_text` | `fretboard_text_0045` | 大调指型, 练习 | ## 练习15 回到第7章中的练习12，在每种大调指型的上方标出其关系小调。然后用方形在指型图中画出其关系小调的根音。例如： D大调指型1 (B小调指型2) 再次弹奏练习12中的各种指型。首先从大调音阶的根音弹奏这个指型，然后从关系小调音阶的根音开始弹奏。弹奏之前先大声说出每种指型的序号。 [图示引用 1 张，详见 image_refs] |
| 3 | 3 | Y |  | 0.1033 | -0.0833 | `fretboard_handbook_clean_text` | `fretboard_text_0044` | 大调指型, 练习 | ## 练习14 回到练习13。在每种指型上方用圆括号写出它的关系大调。在指型图中用方形画出其关系大调的根音。下面是第一个指型的例子。 E小调指型5(G大调指型4） 再次弹奏练习13中的各种指型。首先从小调音阶的根音弹奏这个指型，然后从其关系大调音阶的根音开始弹奏。弹奏之前先大声说出每种指型的序号。 [图示引用 1 张，详见 image_refs] |
| 4 | 4 | Y |  | 0.1095 | -0.0995 | `fretboard_handbook_clean_text` | `fretboard_text_0142` | 练习 | ## 练习13 E小调指型5 2C小调指型2 E小调指型 A小调指型3 D小调指型3 小调指型4 小调指型 Bb小调指型3 小调指型2 F小调指型5 [图示引用 10 张，详见 image_refs] |
| 5 | 5 | Y |  | 0.1119 | -0.1019 | `fretboard_handbook_clean_text` | `fretboard_text_0053` | 练习 | ## 练习19 回到练习17中，写出每个图示中关系大调五声音阶的名称和指型序号，并且用方形画出关系大调五声音阶的根音。第一个图示的例子如右所示。 D小调五声音阶指型2 [图示引用 1 张，详见 image_refs] |
