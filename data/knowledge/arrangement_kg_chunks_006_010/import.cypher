// Generated from curated KG JSONL.
CREATE CONSTRAINT kg_node_id IF NOT EXISTS FOR (n:KGNode) REQUIRE n.id IS UNIQUE;

MERGE (n:KGNode {id: "caution:finger_span_limit"}) SET n.type = "caution", n.name = "finger_span_limit";
MERGE (n:KGNode {id: "caution:muddy_low_freq_clash"}) SET n.type = "caution", n.name = "muddy_low_freq_clash";
MERGE (n:KGNode {id: "chord:11"}) SET n.type = "chord", n.name = "11";
MERGE (n:KGNode {id: "chord:13"}) SET n.type = "chord", n.name = "13";
MERGE (n:KGNode {id: "chord:aug_triad"}) SET n.type = "chord", n.name = "aug_triad";
MERGE (n:KGNode {id: "chord:dim7"}) SET n.type = "chord", n.name = "dim7";
MERGE (n:KGNode {id: "chord:m7b5"}) SET n.type = "chord", n.name = "m7b5";
MERGE (n:KGNode {id: "chord:maj7"}) SET n.type = "chord", n.name = "maj7";
MERGE (n:KGNode {id: "chord:voicing_dense"}) SET n.type = "chord", n.name = "voicing_dense";
MERGE (n:KGNode {id: "chord:voicing_open"}) SET n.type = "chord", n.name = "voicing_open";
MERGE (n:KGNode {id: "color:bright_spacious"}) SET n.type = "color", n.name = "bright_spacious";
MERGE (n:KGNode {id: "concept:chord_extension"}) SET n.type = "concept", n.name = "chord_extension";
MERGE (n:KGNode {id: "concept:close_voicing_triads"}) SET n.type = "concept", n.name = "close_voicing_triads";
MERGE (n:KGNode {id: "concept:extended_chord_voicing"}) SET n.type = "concept", n.name = "extended_chord_voicing";
MERGE (n:KGNode {id: "concept:guitar_tuning"}) SET n.type = "concept", n.name = "guitar_tuning";
MERGE (n:KGNode {id: "concept:universal_heuristic"}) SET n.type = "concept", n.name = "universal_heuristic";
MERGE (n:KGNode {id: "finger:index_barre_muting"}) SET n.type = "finger", n.name = "index_barre_muting";
MERGE (n:KGNode {id: "guitar_idiom:string_crossing_riff_design"}) SET n.type = "guitar_idiom", n.name = "string_crossing_riff_design";
MERGE (n:KGNode {id: "interval:major_3rd"}) SET n.type = "interval", n.name = "major_3rd";
MERGE (n:KGNode {id: "interval:major_seventh"}) SET n.type = "interval", n.name = "major_seventh";
MERGE (n:KGNode {id: "interval:perfect_11"}) SET n.type = "interval", n.name = "perfect_11";
MERGE (n:KGNode {id: "interval:perfect_fifth"}) SET n.type = "interval", n.name = "perfect_fifth";
MERGE (n:KGNode {id: "pattern:extension_on_top"}) SET n.type = "pattern", n.name = "extension_on_top";
MERGE (n:KGNode {id: "pattern:interval_shape_shift"}) SET n.type = "pattern", n.name = "interval_shape_shift";
MERGE (n:KGNode {id: "pattern:octave_minus_one_fret"}) SET n.type = "pattern", n.name = "octave_minus_one_fret";
MERGE (n:KGNode {id: "pattern:shell_voicing_1-7-3-5"}) SET n.type = "pattern", n.name = "shell_voicing_1-7-3-5";
MERGE (n:KGNode {id: "pattern:string_set_grouping"}) SET n.type = "pattern", n.name = "string_set_grouping";
MERGE (n:KGNode {id: "pattern:symmetric_fingering"}) SET n.type = "pattern", n.name = "symmetric_fingering";
MERGE (n:KGNode {id: "structure:no_duplicate_notes_on_same_string"}) SET n.type = "structure", n.name = "no_duplicate_notes_on_same_string";
MERGE (n:KGNode {id: "technique:omit_11_and_maybe_9"}) SET n.type = "technique", n.name = "omit_11_and_maybe_9";
MERGE (n:KGNode {id: "technique:omit_3rd"}) SET n.type = "technique", n.name = "omit_3rd";
MERGE (n:KGNode {id: "technique:omit_5th_for_space"}) SET n.type = "technique", n.name = "omit_5th_for_space";
MERGE (n:KGNode {id: "technique:omit_root_and_5th"}) SET n.type = "technique", n.name = "omit_root_and_5th";
MERGE (n:KGNode {id: "technique:strumming_chords"}) SET n.type = "technique", n.name = "strumming_chords";
MERGE (n:KGNode {id: "technique:strumming_mute"}) SET n.type = "technique", n.name = "strumming_mute";

MATCH (source:KGNode {id: "concept:guitar_tuning"})
MATCH (target:KGNode {id: "pattern:interval_shape_shift"})
MERGE (source)-[r:CONSTRAINS {review_id: "chunk_0006:001"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.95, context_condition: "在指板上构建跨越第2弦（B弦）和第3弦（G弦）的音程或和弦指型时", review_note: "吉他标准调弦中，除2-3弦为大三度外，其余相邻弦均为纯四度。这意味着通用的音程指型在跨越2-3弦时，必须向高音方向移动1品（或低音方向减少1品）进行补偿，这是吉他指板几何的核心约束。", evidence: "每根弦都比其下方的弦高四度，除了第2弦的B音比第3弦的G音高一个大三度音程外", needs_visual_context: false, review_id: "chunk_0006:001", chunk_id: "chunk_0006", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "interval:major_seventh"})
MATCH (target:KGNode {id: "pattern:octave_minus_one_fret"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0006:003"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "在指板上快速定位或构建大七度音程时", review_note: "利用八度指型的熟悉度，大七度可视为“同弦或跨弦八度位置回退1品”，这是一种高效的指板导航启发式规则，避免了重新计算音数。", evidence: "确定大七度的方法很容易，记住比八度音低1品就可以了", needs_visual_context: false, review_id: "chunk_0006:003", chunk_id: "chunk_0006", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "chord:aug_triad"})
MATCH (target:KGNode {id: "pattern:symmetric_fingering"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0008:001"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.95, context_condition: "在指板上构建或移动增三和弦时", review_note: "增三和弦由两个大三度构成，具有对称性。在吉他指板上，这种对称性意味着和弦内各音之间的物理距离相等，导致任何组成音都可以被视为根音，且指型具有高度的可平移性和重复性。", evidence: "形成了一种对称的构建关系...使得每个音都可以看作是根音", needs_visual_context: false, review_id: "chunk_0008:001", chunk_id: "chunk_0008", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "technique:strumming_chords"})
MATCH (target:KGNode {id: "structure:no_duplicate_notes_on_same_string"})
MERGE (source)-[r:CONSTRAINS {review_id: "chunk_0008:002"}]->(target)
SET r += { knowledge_type: "Caution", confidence: 0.9, context_condition: "将琶音概念转化为扫弦和弦编配时", review_note: "与琶音不同，扫弦和弦受限于物理发声原理，同一根弦上不能同时存在两个音符。因此，在从琶音推导和弦指型时，必须确保每根弦上只有一个有效音符，这限制了声部排列的可能性。", evidence: "一根弦一次只能发出一个音...在和弦中不会[出现同一根弦上有2个音符]", needs_visual_context: false, review_id: "chunk_0008:002", chunk_id: "chunk_0008", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "concept:close_voicing_triads"})
MATCH (target:KGNode {id: "pattern:string_set_grouping"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0008:003"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.85, context_condition: "在六根弦上构建密集三和弦声部时", review_note: "虽然理论上可以在六根弦上排列密集三和弦，但为了演奏可行性和声部清晰度，建议将六弦指型拆分为以三根弦为一组的子集（String Sets）进行练习和应用，避免一次性跨越所有琴弦造成的演奏困难。", evidence: "不要尝试去一次弹奏每种指型的全部六根琴弦...分成四种以三根琴弦为一组的指型", needs_visual_context: false, review_id: "chunk_0008:003", chunk_id: "chunk_0008", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "chord:voicing_dense"})
MATCH (target:KGNode {id: "caution:muddy_low_freq_clash"})
MERGE (source)-[r:CAUTIONS {review_id: "chunk_0009:001"}]->(target)
SET r += { knowledge_type: "Caution", confidence: 0.9, context_condition: "在吉他低把位或低音区演奏包含密集音程（如相邻弦上的小三度/大二度）的七和弦时", review_note: "教材指出密集排列的七和弦在吉他上不仅难按，更因为含有较多相近的低音，会导致音色暗淡浑浊。这是重要的频段避坑指南。", evidence: "这样的和弦中也含有较多相近的低音，使得音色也会变得暗淡浑浊。", needs_visual_context: false, review_id: "chunk_0009:001", chunk_id: "chunk_0009", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "chord:voicing_open"})
MATCH (target:KGNode {id: "color:bright_spacious"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0009:002"}]->(target)
SET r += { knowledge_type: "ColorEmotion", confidence: 0.85, context_condition: "将七和弦中的内声部（如3音或5音）移高或移低一个八度，形成开放排列时", review_note: "通过八度位移将密集和弦转化为开放和弦，能获得更宽广、悦耳的声音，避免局促感。", evidence: "开放和弦有时更加悦耳好听...得到更加宽广的和弦声音。", needs_visual_context: false, review_id: "chunk_0009:002", chunk_id: "chunk_0009", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "pattern:shell_voicing_1-7-3-5"})
MATCH (target:KGNode {id: "concept:universal_heuristic"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0009:003"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.95, context_condition: "构建指型4（根音在第6或第5弦）的七和弦常用声部时", review_note: "提取了具体的通用声部排列逻辑 '1-7-3-5'（即根音、七音、三音、五音），适用于maj7, m7, dom7等多种七和弦类型，是高效的编曲启发式规则。", evidence: "“1、7、3、5”是ma7、mi7、dom7、mi7(b5)和dim7这些和弦指型4中的常用声部构成。", needs_visual_context: false, review_id: "chunk_0009:003", chunk_id: "chunk_0009", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "technique:strumming_mute"})
MATCH (target:KGNode {id: "finger:index_barre_muting"})
MERGE (source)-[r:CONSTRAINS {review_id: "chunk_0009:004"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "向下扫弦演奏根音在6弦、5弦 muted 的开放七和弦指型时", review_note: "明确了左手食指在扫弦时的双重功能：既要按住6弦根音，又要对5弦进行消音，这是保证音色干净的关键物理限制/技巧。", evidence: "左手的1指需要同时完成以下两项任务：（1）牢牢按住六弦上的和弦根音。（2）对第5弦进行消音。", needs_visual_context: false, review_id: "chunk_0009:004", chunk_id: "chunk_0009", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "chord:maj7"})
MATCH (target:KGNode {id: "caution:finger_span_limit"})
MERGE (source)-[r:CONFLICTS_WITH {review_id: "chunk_0009:005"}]->(target)
SET r += { knowledge_type: "Caution", confidence: 0.8, context_condition: "尝试在吉他指板上按奏密集排列的大七和弦（如Amaj7原位密集排列）时", review_note: "指出某些理论上的密集和弦在吉他物理指板上因跨度太大而难以实现，提示编曲时需考虑乐器的人体工学限制。", evidence: "像Amaj7这样的密集和弦...和弦中的音符在指板上的跨度太大，以致很难全部按住。", needs_visual_context: false, review_id: "chunk_0009:005", chunk_id: "chunk_0009", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "chord:dim7"})
MATCH (target:KGNode {id: "technique:omit_5th_for_space"})
MERGE (source)-[r:CONSTRAINS {review_id: "chunk_0010:001"}]->(target)
SET r += { knowledge_type: "Caution", confidence: 0.95, context_condition: "在吉他指板上构建紧凑声部或节省手指时，试图通过省略五音来增加根音八度", review_note: "减七和弦（dim7）的减五度音是定义其和弦性质的核心音程，不可像大/小/属七和弦那样随意省略以换取空间或重复根音。", evidence: "但对于mi7(b5)和dim7和弦不适用，因为对于这两个和弦，b5是影响它们性质的重要音符。", needs_visual_context: false, review_id: "chunk_0010:001", chunk_id: "chunk_0010", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "chord:m7b5"})
MATCH (target:KGNode {id: "technique:omit_5th_for_space"})
MERGE (source)-[r:CONSTRAINS {review_id: "chunk_0010:002"}]->(target)
SET r += { knowledge_type: "Caution", confidence: 0.95, context_condition: "在吉他指板上构建紧凑声部或节省手指时，试图通过省略五音来增加根音八度", review_note: "半减七和弦（m7b5）的减五度音是定义其和弦性质的核心音程，不可像大/小/属七和弦那样随意省略。", evidence: "但对于mi7(b5)和dim7和弦不适用，因为对于这两个和弦，b5是影响它们性质的重要音符。", needs_visual_context: false, review_id: "chunk_0010:002", chunk_id: "chunk_0010", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "interval:perfect_11"})
MATCH (target:KGNode {id: "interval:major_3rd"})
MERGE (source)-[r:CONFLICTS_WITH {review_id: "chunk_0010:003"}]->(target)
SET r += { knowledge_type: "Caution", confidence: 0.98, context_condition: "在大和弦（Major）或属和弦（Dominant）中同时演奏自然11音和大三度音", review_note: "自然11音与大三度音形成小二度冲突（听觉上的不和谐），在块状和弦（Voicing）中应避免同时出现，除非作为经过音或在琶音中分离。", evidence: "如果和弦中包含了大三度，那么四度和五度音听上去就会不和谐...在弹奏和弦时，这种不和谐会非常明显。", needs_visual_context: false, review_id: "chunk_0010:003", chunk_id: "chunk_0010", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "chord:13"})
MATCH (target:KGNode {id: "technique:omit_11_and_maybe_9"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0010:004"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "构建大十三或属十三和弦时，受限于吉他6弦或手指跨度", review_note: "在13和弦中，11音通常被省略以避免冲突，甚至9音也可省略，重点保留3、7、13音以确立和弦性质与延伸色彩。", evidence: "构建大十三和弦或者属十三和弦时，可去掉十一度音。Cma13 一1、3、5、7、9、13", needs_visual_context: false, review_id: "chunk_0010:004", chunk_id: "chunk_0010", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "chord:11"})
MATCH (target:KGNode {id: "technique:omit_3rd"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0010:005"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "构建属十一和弦（Dom11）时，希望保留自然11音的悬停感", review_note: "若必须使用自然11音，通常需省略大三度音，使和弦变为sus4性质的延伸，从而消除冲突。这在属功能和声中很常见。", evidence: "去除三度音，特别是在延伸属和弦中。C11 →1、5、b7、9、11", needs_visual_context: false, review_id: "chunk_0010:005", chunk_id: "chunk_0010", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "concept:extended_chord_voicing"})
MATCH (target:KGNode {id: "pattern:extension_on_top"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0010:006"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.85, context_condition: "在吉他指板上排列延伸和弦（9/11/13）的声部", review_note: "在吉他编曲中，将延伸音（Extension）置于最高声部（Top Voice）通常能获得更清晰、更具色彩感的听感，且符合泛音列的自然分布逻辑。", evidence: "通常，让延伸音在和弦的最高处比较好。", needs_visual_context: false, review_id: "chunk_0010:006", chunk_id: "chunk_0010", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "concept:extended_chord_voicing"})
MATCH (target:KGNode {id: "technique:omit_root_and_5th"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0010:007"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.85, context_condition: "乐队合奏或有贝斯手伴奏时，吉他手构建延伸和弦", review_note: "在有贝斯或其他低音乐器覆盖根音的情况下，吉他手应优先省略根音和五音，为3音、7音及延伸音腾出指板空间，避免低频浑浊。", evidence: "可以尝试去掉五度音和（或）根音，听听会产生什么效果...忽略哪个音取决于...贝司及其他乐器是如何演奏的。", needs_visual_context: false, review_id: "chunk_0010:007", chunk_id: "chunk_0010", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "chord:dim7"})
MATCH (target:KGNode {id: "concept:chord_extension"})
MERGE (source)-[r:CONSTRAINS {review_id: "chunk_0010:008"}]->(target)
SET r += { knowledge_type: "Caution", confidence: 0.9, context_condition: "尝试对减七和弦添加9/11/13等延伸音", review_note: "减七和弦由于其对称性和高度不稳定性，通常不进行常规的延伸（如add9, add13等），这与大/小/属七和弦不同。", evidence: "减七和弦通常不被延伸", needs_visual_context: false, review_id: "chunk_0010:008", chunk_id: "chunk_0010", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "interval:perfect_fifth"})
MATCH (target:KGNode {id: "guitar_idiom:string_crossing_riff_design"})
MERGE (source)-[r:CONSTRAINS {review_id: "chunk_0006:002"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.85, context_condition: "编配Riff或独奏乐句时", review_note: "纯五度音程需跨弦演奏，受第2弦非四度调弦影响，指型逻辑断裂。编曲时应规避复杂跨弦或简化指法，以确保Riff的流畅性与可演奏性。", evidence: "对于五度及以上的音程，需要跨越相邻的琴弦。在跨越琴弦的时候，经常要用到第2弦，因此这里需要学习更多在指板上的型式", needs_visual_context: false, review_id: "chunk_0006:002", chunk_id: "chunk_0006", review_decision: "revise", revision_status: "llm_revised", human_revision_note: "将语境中的演奏改为编配riff/独奏,我们的重心在编配上，这点可以沉淀进prompt", ingested_at: "2026-05-29T09:24:31.648141+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_006_010\\arrangement_kg_review.jsonl" };
