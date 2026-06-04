// Generated from curated KG JSONL.
CREATE CONSTRAINT kg_node_id IF NOT EXISTS FOR (n:KGNode) REQUIRE n.id IS UNIQUE;

MERGE (n:KGNode {id: "benefit:minimal_hand_movement"}) SET n.type = "benefit", n.name = "minimal_hand_movement";
MERGE (n:KGNode {id: "concept:caged_system"}) SET n.type = "concept", n.name = "caged_system";
MERGE (n:KGNode {id: "concept:fretboard_navigation"}) SET n.type = "concept", n.name = "fretboard_navigation";
MERGE (n:KGNode {id: "concept:guitar_tuning_standard"}) SET n.type = "concept", n.name = "guitar_tuning_standard";
MERGE (n:KGNode {id: "concept:relative_key_mapping"}) SET n.type = "concept", n.name = "relative_key_mapping";
MERGE (n:KGNode {id: "guitar_idiom:overlapping_patterns"}) SET n.type = "guitar_idiom", n.name = "overlapping_patterns";
MERGE (n:KGNode {id: "guitar_idiom:root_on_string_1_6_and_4"}) SET n.type = "guitar_idiom", n.name = "root_on_string_1_6_and_4";
MERGE (n:KGNode {id: "guitar_idiom:root_on_string_2_and_5"}) SET n.type = "guitar_idiom", n.name = "root_on_string_2_and_5";
MERGE (n:KGNode {id: "guitar_idiom:root_on_string_3_5_and_6"}) SET n.type = "guitar_idiom", n.name = "root_on_string_3_5_and_6";
MERGE (n:KGNode {id: "guitar_idiom:root_on_string_4_and_2"}) SET n.type = "guitar_idiom", n.name = "root_on_string_4_and_2";
MERGE (n:KGNode {id: "guitar_idiom:root_on_string_5_and_3"}) SET n.type = "guitar_idiom", n.name = "root_on_string_5_and_3";
MERGE (n:KGNode {id: "heuristic:avoid_same_finger_repetition"}) SET n.type = "heuristic", n.name = "avoid_same_finger_repetition";
MERGE (n:KGNode {id: "heuristic:minimal_position_shift"}) SET n.type = "heuristic", n.name = "minimal_position_shift";
MERGE (n:KGNode {id: "idiom:two_notes_per_string_pattern"}) SET n.type = "idiom", n.name = "two_notes_per_string_pattern";
MERGE (n:KGNode {id: "pattern:caged_root_pattern_1"}) SET n.type = "pattern", n.name = "caged_root_pattern_1";
MERGE (n:KGNode {id: "pattern:caged_root_pattern_2"}) SET n.type = "pattern", n.name = "caged_root_pattern_2";
MERGE (n:KGNode {id: "pattern:caged_root_pattern_3"}) SET n.type = "pattern", n.name = "caged_root_pattern_3";
MERGE (n:KGNode {id: "pattern:caged_root_pattern_4"}) SET n.type = "pattern", n.name = "caged_root_pattern_4";
MERGE (n:KGNode {id: "pattern:caged_root_pattern_5"}) SET n.type = "pattern", n.name = "caged_root_pattern_5";
MERGE (n:KGNode {id: "pattern:interval_shift_g_b_strings"}) SET n.type = "pattern", n.name = "interval_shift_g_b_strings";
MERGE (n:KGNode {id: "pattern:shared_fingerboard_geometry"}) SET n.type = "pattern", n.name = "shared_fingerboard_geometry";
MERGE (n:KGNode {id: "scale:pentatonic_major"}) SET n.type = "scale", n.name = "pentatonic_major";
MERGE (n:KGNode {id: "scale:pentatonic_minor"}) SET n.type = "scale", n.name = "pentatonic_minor";
MERGE (n:KGNode {id: "style:rock_blues_country_soloing"}) SET n.type = "style", n.name = "rock_blues_country_soloing";
MERGE (n:KGNode {id: "technique:fingering_logic"}) SET n.type = "technique", n.name = "fingering_logic";
MERGE (n:KGNode {id: "technique:position_playing"}) SET n.type = "technique", n.name = "position_playing";

MATCH (source:KGNode {id: "pattern:caged_root_pattern_1"})
MATCH (target:KGNode {id: "guitar_idiom:root_on_string_2_and_5"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0002:001"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "定位CAGED系统中的E型指法根音位置", review_note: "指型1（对应E形状）的根音位于第2弦和第5弦，两音在指板上相差2品。这是构建该把位和弦与音阶的基础锚点。", evidence: "指型1的根音在第2和第5弦上，两个根音相差2品！", needs_visual_context: false, review_id: "chunk_0002:001", chunk_id: "chunk_0002", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T07:15:50.989733+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_002_005\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "pattern:caged_root_pattern_2"})
MATCH (target:KGNode {id: "guitar_idiom:root_on_string_5_and_3"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0002:002"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "定位CAGED系统中的A型指法根音位置", review_note: "指型2（对应A形状）的根音位于第5弦和第3弦，两音在指板上相差2品。此指型与指型1在第5弦共享根音，形成指板连接。", evidence: "指型2的根音在第5和第3弦上，两个根音相差2品！...指型2和其上方的指型1共用同一个第5弦上的根音", needs_visual_context: false, review_id: "chunk_0002:002", chunk_id: "chunk_0002", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T07:15:50.989733+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_002_005\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "pattern:caged_root_pattern_3"})
MATCH (target:KGNode {id: "guitar_idiom:root_on_string_3_5_and_6"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0002:003"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "定位CAGED系统中的D型指法根音位置", review_note: "指型3（对应D形状）的根音分布在第3、5、6弦，相邻根音间相差3品。这种跨弦的大跨度是D型指法的物理特征。", evidence: "指型3的根音在第3弦、第5弦和第6弦上，相差3品！", needs_visual_context: false, review_id: "chunk_0002:003", chunk_id: "chunk_0002", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T07:15:50.989733+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_002_005\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "pattern:caged_root_pattern_4"})
MATCH (target:KGNode {id: "guitar_idiom:root_on_string_1_6_and_4"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0002:004"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "定位CAGED系统中的G型指法根音位置", review_note: "指型4（对应G形状）的根音位于第1、6、4弦，相邻根音间相差2品。注意第1弦和第6弦的根音通常由同一手指（如1指）大横按覆盖。", evidence: "指型4的根音在第1弦、第6弦和第4弦上，相差2品！", needs_visual_context: false, review_id: "chunk_0002:004", chunk_id: "chunk_0002", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T07:15:50.989733+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_002_005\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "pattern:caged_root_pattern_5"})
MATCH (target:KGNode {id: "guitar_idiom:root_on_string_4_and_2"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0002:005"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "定位CAGED系统中的C型指法根音位置", review_note: "指型5（对应C形状）的根音位于第4弦和第2弦，两音在指板上相差3品。这是连接高把位回到指型1的关键过渡形态。", evidence: "指型5的根音在第4弦、第2弦上，相差3品！", needs_visual_context: false, review_id: "chunk_0002:005", chunk_id: "chunk_0002", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T07:15:50.989733+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_002_005\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "concept:caged_system"})
MATCH (target:KGNode {id: "guitar_idiom:overlapping_patterns"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0002:006"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.85, context_condition: "在指板上进行把位转换或扩展音域时", review_note: "五种根音型式在指板上并非孤立存在，而是通过共享根音或音符相互重叠（Overlap）。理解这种重叠关系是实现无缝把位切换和全指板导航的核心。", evidence: "每个指型都和随后的指型有所重叠。这种重叠也会应用到我们以后学习的所有和弦、音阶和琶音中。", needs_visual_context: false, review_id: "chunk_0002:006", chunk_id: "chunk_0002", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T07:15:50.989733+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_002_005\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "concept:fretboard_navigation"})
MATCH (target:KGNode {id: "heuristic:minimal_position_shift"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0003:001"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.85, context_condition: "在即兴演奏、视奏或快速寻找音符时，为了保持流畅性和减少错误", review_note: "教材提出“最小把位移动”原则，建议以当前手型为锚点，优先在邻近品位寻找目标音，而非跳跃到理论上的其他位置，这有助于维持演奏的连贯性。", evidence: "使用最小的把位移动...尽量在接近当前所在的把位附近寻找", needs_visual_context: false, review_id: "chunk_0003:001", chunk_id: "chunk_0003", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T07:15:50.989733+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_002_005\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "concept:guitar_tuning_standard"})
MATCH (target:KGNode {id: "pattern:interval_shift_g_b_strings"})
MERGE (source)-[r:CONSTRAINS {review_id: "chunk_0004:001"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.95, context_condition: "在指板上跨弦构建音阶或和弦指型，特别是涉及第2弦（B）和第3弦（G）时", review_note: "由于标准调弦中2弦与3弦之间是大三度（而非其他弦间的纯四度），导致跨这两根弦时，全音/半音的品位间距需比常规少1品（全音为2品而非3品，半音为3品而非4品）。这是吉他指板几何的核心约束。", evidence: "当从一根弦向上至另外一根弦时...特例，就是第2弦与第3弦，这时一个全音是相差2品的距离...半音的关系...第2弦和第3弦是相差3品的距离。", needs_visual_context: false, review_id: "chunk_0004:001", chunk_id: "chunk_0004", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T07:15:50.989733+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_002_005\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "technique:position_playing"})
MATCH (target:KGNode {id: "benefit:minimal_hand_movement"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0004:002"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.85, context_condition: "构建和使用固定的音阶指型（如CAGED系统或五种指型）进行独奏或伴奏时", review_note: "采用固定把位的音阶指型（每弦约3音）而非单弦演奏，旨在最小化左手把位移动，从而在Solo或和弦转换中获得更好的控制力和流畅度。", evidence: "构建一些标准的指型，这样就可以减少把位的移动，以便在演奏的时候可以更好地控制各个音符...顺畅地演奏SOLO...流畅地演奏伴奏部分。", needs_visual_context: false, review_id: "chunk_0004:002", chunk_id: "chunk_0004", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T07:15:50.989733+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_002_005\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "scale:pentatonic_major"})
MATCH (target:KGNode {id: "idiom:two_notes_per_string_pattern"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0005:001"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "构建大调五声音阶指型时，利用其音程结构特性", review_note: "大调五声音阶在吉他指板上具有独特的物理优势：每根弦上通常只包含两个音符。这种“每弦两音”的结构简化了左右手配合，使得快速演奏、连奏（legato）和跨弦移动比七声音阶更容易执行，是摇滚/布鲁斯速弹的基础物理逻辑。", evidence: "在五声音阶的每种指型中，每根琴弦上都只有2个音符，这让五声音阶演奏起来非常容易并且很有趣", needs_visual_context: false, review_id: "chunk_0005:001", chunk_id: "chunk_0005", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T07:15:50.989733+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_002_005\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "scale:pentatonic_minor"})
MATCH (target:KGNode {id: "style:rock_blues_country_soloing"})
MERGE (source)-[r:CAN_INSPIRE {review_id: "chunk_0005:002"}]->(target)
SET r += { knowledge_type: "ColorEmotion", confidence: 0.85, context_condition: "需要创作或即兴演奏摇滚、布鲁斯或乡村风格的独奏时", review_note: "小调五声音阶是摇滚、布鲁斯和乡村音乐独奏的核心语汇。它去除了自然小调中的2级和6级音（避免了半音冲突和不稳定感），提供了安全且富有表现力的音符集合，直接指向这些风格的听觉特征。", evidence: "五声音阶是许多摇滚乐、布鲁斯音乐和乡村音乐独奏的基础", needs_visual_context: false, review_id: "chunk_0005:002", chunk_id: "chunk_0005", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T07:15:50.989733+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_002_005\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "concept:relative_key_mapping"})
MATCH (target:KGNode {id: "pattern:shared_fingerboard_geometry"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0005:003"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.8, context_condition: "在指板上转换关系大小调视角时", review_note: "关系大调和小调共享完全相同的指板几何形状（指型）。编曲或即兴时，无需学习新的指法图案，只需改变“根音”的心理定位（大调6级=小调1级；小调3级=大调1级）。这是一种高效的指板复用策略。", evidence: "这些音阶指型和之前我们学过的大调音阶指型是基本相同的。唯一不同的地方就是指型中的根音不同", needs_visual_context: false, review_id: "chunk_0005:003", chunk_id: "chunk_0005", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-29T07:15:50.989733+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_002_005\\arrangement_kg_review.jsonl" };

MATCH (source:KGNode {id: "technique:fingering_logic"})
MATCH (target:KGNode {id: "heuristic:avoid_same_finger_repetition"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0003:003"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.75, context_condition: "编写吉他Riff或旋律乐句时", review_note: "在Riff编写中，为避免音色呆板并提升流畅度，建议避免同指连续按弦，优先采用交替指法或结合滑音/击勾弦技巧。", evidence: "尽量避免用同一个手指连续两次按弦...如果这样弹奏会造成移出把位，那么就需要避免这一点", needs_visual_context: false, review_id: "chunk_0003:003", chunk_id: "chunk_0003", review_decision: "revise", revision_status: "llm_revised", human_revision_note: "语境修改：作为riff编写时的手法建议（这通常意味着需要使用交替指法或滑音/击勾弦技巧。）保存而不作为演奏建议", ingested_at: "2026-05-29T07:15:50.989733+00:00", source_review_file: "data\\processed\\mineru_full_gpu\\kg_extract_chunks_002_005\\arrangement_kg_review.jsonl" };
