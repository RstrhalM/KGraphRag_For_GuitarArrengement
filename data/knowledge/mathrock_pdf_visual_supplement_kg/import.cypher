// Generated from curated KG JSONL.
CREATE CONSTRAINT kg_node_id IF NOT EXISTS FOR (n:KGNode) REQUIRE n.id IS UNIQUE;

MERGE (n:KGNode {id: "caution:large_fretboard_jumps_disrupt_flow"}) SET n.type = "caution", n.name = "large_fretboard_jumps_disrupt_flow";
MERGE (n:KGNode {id: "caution:muddy_distortion"}) SET n.type = "caution", n.name = "muddy_distortion";
MERGE (n:KGNode {id: "chord:m7b5"}) SET n.type = "chord", n.name = "m7b5";
MERGE (n:KGNode {id: "chord:maj7"}) SET n.type = "chord", n.name = "maj7";
MERGE (n:KGNode {id: "chord:maj9"}) SET n.type = "chord", n.name = "maj9";
MERGE (n:KGNode {id: "chord:min7"}) SET n.type = "chord", n.name = "min7";
MERGE (n:KGNode {id: "chord:open_Fmaj9"}) SET n.type = "chord", n.name = "open_Fmaj9";
MERGE (n:KGNode {id: "chord:shell_voicing"}) SET n.type = "chord", n.name = "shell_voicing";
MERGE (n:KGNode {id: "chord_progression:facgce_loop_1"}) SET n.type = "chord_progression", n.name = "facgce_loop_1";
MERGE (n:KGNode {id: "color:ethereal_mathrock_texture"}) SET n.type = "color", n.name = "ethereal_mathrock_texture";
MERGE (n:KGNode {id: "color:lush_ambient_texture"}) SET n.type = "color", n.name = "lush_ambient_texture";
MERGE (n:KGNode {id: "color:surprise_epiphany"}) SET n.type = "color", n.name = "surprise_epiphany";
MERGE (n:KGNode {id: "concept:alternate_tuning_scale_layout"}) SET n.type = "concept", n.name = "alternate_tuning_scale_layout";
MERGE (n:KGNode {id: "concept:voice_leading"}) SET n.type = "concept", n.name = "voice_leading";
MERGE (n:KGNode {id: "guitar_idiom:high_gain_riff_clarity"}) SET n.type = "guitar_idiom", n.name = "high_gain_riff_clarity";
MERGE (n:KGNode {id: "guitar_idiom:rootless_shell_voicing_on_4_strings"}) SET n.type = "guitar_idiom", n.name = "rootless_shell_voicing_on_4_strings";
MERGE (n:KGNode {id: "heuristic:drop2_voicing_for_mid_range_clarity"}) SET n.type = "heuristic", n.name = "drop2_voicing_for_mid_range_clarity";
MERGE (n:KGNode {id: "heuristic:non_linear_fretboard_navigation"}) SET n.type = "heuristic", n.name = "non_linear_fretboard_navigation";
MERGE (n:KGNode {id: "heuristic:voice_leading_via_open_strings"}) SET n.type = "heuristic", n.name = "voice_leading_via_open_strings";
MERGE (n:KGNode {id: "pattern:barre_chord_mobility"}) SET n.type = "pattern", n.name = "barre_chord_mobility";
MERGE (n:KGNode {id: "pattern:movable_barre_shapes_root_6"}) SET n.type = "pattern", n.name = "movable_barre_shapes_root_6";
MERGE (n:KGNode {id: "pattern:polyrhythmic_subdivision"}) SET n.type = "pattern", n.name = "polyrhythmic_subdivision";
MERGE (n:KGNode {id: "pattern:wide_interval_leap_utilization"}) SET n.type = "pattern", n.name = "wide_interval_leap_utilization";
MERGE (n:KGNode {id: "progression:borrowed_bIII_major"}) SET n.type = "progression", n.name = "borrowed_bIII_major";
MERGE (n:KGNode {id: "scale:major_box_pattern_6th_string_root"}) SET n.type = "scale", n.name = "major_box_pattern_6th_string_root";
MERGE (n:KGNode {id: "technique:hybrid_picking_arpeggio"}) SET n.type = "technique", n.name = "hybrid_picking_arpeggio";
MERGE (n:KGNode {id: "technique:tapping_arpeggio"}) SET n.type = "technique", n.name = "tapping_arpeggio";
MERGE (n:KGNode {id: "technique:tapping_harmonics"}) SET n.type = "technique", n.name = "tapping_harmonics";
MERGE (n:KGNode {id: "tuning:DAEAC#E"}) SET n.type = "tuning", n.name = "DAEAC#E";
MERGE (n:KGNode {id: "tuning:FACGCE"}) SET n.type = "tuning", n.name = "FACGCE";
MERGE (n:KGNode {id: "voicing:drop_2_shell"}) SET n.type = "voicing", n.name = "drop_2_shell";
MERGE (n:KGNode {id: "voicing:open_string_maj9_cluster"}) SET n.type = "voicing", n.name = "open_string_maj9_cluster";

MATCH (source:KGNode {id: "tuning:FACGCE"})
MATCH (target:KGNode {id: "chord:open_Fmaj9"})
MERGE (source)-[r:ENABLES {review_id: "mathrock_pdf_visual:chunk_0004:001"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 1.0, context_condition: "在 FACGCE 调弦下，无需按任何品位（全空弦）即可直接获得 Fmaj9 和弦。", review_note: "这是该调弦的核心优势，利用开放弦构建复杂的九和弦色彩，极大简化了 voicing 的指法复杂度，适合作为编曲中的持续背景或起始动机。", evidence: "图示显示 Fmaj9 和弦图所有弦均为空弦 (oooooo)。", needs_visual_context: false, review_id: "mathrock_pdf_visual:chunk_0004:001", chunk_id: "chunk_0004", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-06-01T15:18:04.125810+00:00", source_review_file: "data\\processed\\mathrock\\pdf_kg_multimodal_supplement\\arrangement_kg_review.synced.jsonl" };

MATCH (source:KGNode {id: "tuning:FACGCE"})
MATCH (target:KGNode {id: "pattern:movable_barre_shapes_root_6"})
MERGE (source)-[r:SUGGESTS {review_id: "mathrock_pdf_visual:chunk_0004:002"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.95, context_condition: "在 FACGCE 调弦下编写和弦进行或 Riff 时。", review_note: "图示展示了基于第6弦根音的移动和弦指型（如 G7, Am, Bm7b5）。由于调弦改变了音程关系，标准调弦的指法失效，需建立基于新调弦的“移动把位”逻辑，特别是利用低弦组构建复杂和声。", evidence: "图示展示了从第6弦起始的 G7, Am, Am+11, Bm7b5 等可移动和弦指型。", needs_visual_context: false, review_id: "mathrock_pdf_visual:chunk_0004:002", chunk_id: "chunk_0004", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-06-01T15:18:04.125810+00:00", source_review_file: "data\\processed\\mathrock\\pdf_kg_multimodal_supplement\\arrangement_kg_review.synced.jsonl" };

MATCH (source:KGNode {id: "tuning:FACGCE"})
MATCH (target:KGNode {id: "scale:major_box_pattern_6th_string_root"})
MERGE (source)-[r:CONSTRAINS {review_id: "mathrock_pdf_visual:chunk_0004:003"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "在 FACGCE 调弦下进行旋律创作或 Solo 编配时。", review_note: "图示的大调音阶指板图显示，由于非标准音程，音阶在指板上并非均匀分布，存在特定的“盒子”形状。编曲时应优先记忆这些特定把位的音符落点，而非依赖标准调弦的几何直觉，特别是在 3-5 品区域的密集音符排列。", evidence: "FACGCE调弦的大调实用音符指板图，显示了非对称的音阶分布及根音位置。", needs_visual_context: false, review_id: "mathrock_pdf_visual:chunk_0004:003", chunk_id: "chunk_0004", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-06-01T15:18:04.125810+00:00", source_review_file: "data\\processed\\mathrock\\pdf_kg_multimodal_supplement\\arrangement_kg_review.synced.jsonl" };

MATCH (source:KGNode {id: "technique:tapping_harmonics"})
MATCH (target:KGNode {id: "color:ethereal_mathrock_texture"})
MERGE (source)-[r:EVOKES {review_id: "mathrock_pdf_visual:chunk_0004:004"}]->(target)
SET r += { knowledge_type: "ColorEmotion", confidence: 0.85, context_condition: "在 FACGCE 调弦下，结合开放弦共鸣使用点弦（Tapping）技法时。", review_note: "谱例展示了在开放弦持续音背景下，利用点弦在高把位演奏旋律。这种技法利用了特殊调弦的和谐共振，产生典型的 Math Rock “晶莹剔透”且带有空间感的听感，适合用于过门或氛围段落。", evidence: "谱例中包含 'T' (Tapping) 标记，配合开放弦延音，以及变调夹3品的设定。", needs_visual_context: false, review_id: "mathrock_pdf_visual:chunk_0004:004", chunk_id: "chunk_0004", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-06-01T15:18:04.125810+00:00", source_review_file: "data\\processed\\mathrock\\pdf_kg_multimodal_supplement\\arrangement_kg_review.synced.jsonl" };

MATCH (source:KGNode {id: "chord_progression:facgce_loop_1"})
MATCH (target:KGNode {id: "heuristic:voice_leading_via_open_strings"})
MERGE (source)-[r:CAN_INSPIRE {review_id: "mathrock_pdf_visual:chunk_0004:005"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.8, context_condition: "设计 FACGCE 调弦下的循环和弦进行（Loop）时。", review_note: "图示的和弦进行范例（虽未标注名称）展示了如何通过保留部分开放弦或共同音，在不同和弦形状间实现平滑的声部连接。这是特殊调弦编曲的关键：利用空弦作为“锚点”减少左手移动，增加连贯性。", evidence: "更多FACGCE和弦及进行1/2/3的图示序列，展示了不同把位和弦形状的连续组合。", needs_visual_context: false, review_id: "mathrock_pdf_visual:chunk_0004:005", chunk_id: "chunk_0004", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-06-01T15:18:04.125810+00:00", source_review_file: "data\\processed\\mathrock\\pdf_kg_multimodal_supplement\\arrangement_kg_review.synced.jsonl" };

MATCH (source:KGNode {id: "tuning:DAEAC#E"})
MATCH (target:KGNode {id: "voicing:open_string_maj9_cluster"})
MERGE (source)-[r:ENABLES {review_id: "mathrock_pdf_visual:chunk_0005:001"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.95, context_condition: "编配 DAEAC#E 调弦下的和声织体时", review_note: "图示显示该调弦下，利用空弦（D-A-E-A-C#-E）可轻松构建包含根音、3音、7音及9音的 Maj9 和弦，且无需大跨度指法。这种 Voicing 利用了调弦特性产生的自然共鸣，适合 Math Rock 中清澈、延音长的背景铺底。", evidence: "Page 38 diagrams show Dmaj9 and Amaj9 shapes utilizing multiple open strings (x0", needs_visual_context: false, review_id: "mathrock_pdf_visual:chunk_0005:001", chunk_id: "chunk_0005", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-06-01T15:18:04.125810+00:00", source_review_file: "data\\processed\\mathrock\\pdf_kg_multimodal_supplement\\arrangement_kg_review.synced.jsonl" };

MATCH (source:KGNode {id: "technique:tapping_arpeggio"})
MATCH (target:KGNode {id: "pattern:wide_interval_leap_utilization"})
MERGE (source)-[r:SUGGESTS {review_id: "mathrock_pdf_visual:chunk_0005:002"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "编写高难度独奏乐句或分解和弦 Riff 时", review_note: "谱例展示了在 FACGCE 调弦下，通过右手点弦（T）结合左手击勾弦，跨越多个八度演奏分解和弦。这种技法利用了非标准调弦带来的特殊音程排列，使得在单把位内实现大跨度音程跳跃成为可能，是 Math Rock 标志性听感的来源之一。", evidence: "Page 36 & 40 tabs show extensive tapping patterns (marked 'T') spanning strings", needs_visual_context: false, review_id: "mathrock_pdf_visual:chunk_0005:002", chunk_id: "chunk_0005", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-06-01T15:18:04.125810+00:00", source_review_file: "data\\processed\\mathrock\\pdf_kg_multimodal_supplement\\arrangement_kg_review.synced.jsonl" };

MATCH (source:KGNode {id: "concept:alternate_tuning_scale_layout"})
MATCH (target:KGNode {id: "heuristic:non_linear_fretboard_navigation"})
MERGE (source)-[r:CONSTRAINS {review_id: "mathrock_pdf_visual:chunk_0005:003"}]->(target)
SET r += { knowledge_type: "Caution", confidence: 0.85, context_condition: "在 DAEAC#E 调弦下进行即兴或旋律编写时", review_note: "指板图明确显示，由于调弦改变，相邻弦之间的音程关系不再规则（如 5 弦到 4 弦是大三度而非纯四度）。这意味着传统的‘平移指型’失效，编曲时必须重新记忆音阶在指板上的非线性分布，避免依赖肌肉记忆的惯性指法。", evidence: "Page 39 fretboard maps show irregular scale patterns where adjacent strings do n", needs_visual_context: false, review_id: "mathrock_pdf_visual:chunk_0005:003", chunk_id: "chunk_0005", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-06-01T15:18:04.125810+00:00", source_review_file: "data\\processed\\mathrock\\pdf_kg_multimodal_supplement\\arrangement_kg_review.synced.jsonl" };

MATCH (source:KGNode {id: "chord:maj9"})
MATCH (target:KGNode {id: "color:lush_ambient_texture"})
MERGE (source)-[r:EVOKES {review_id: "mathrock_pdf_visual:chunk_0005:004"}]->(target)
SET r += { knowledge_type: "ColorEmotion", confidence: 0.8, context_condition: "使用开放弦 Maj9 指型进行慢速分解时", review_note: "结合 Page 38 的和弦图与 Page 40 的演奏谱例，Maj9 和弦在该调弦下大量保留空弦音，产生丰富的泛音列和延音。这种色彩指向‘梦幻’、‘开阔’的氛围，常用于 Math Rock 乐曲的 Intro 或 Bridge 段落，以平衡复杂的节奏部分。", evidence: "Diagrams on Page 38 highlight open-string heavy Maj9 voicings; Page 40 shows the", needs_visual_context: false, review_id: "mathrock_pdf_visual:chunk_0005:004", chunk_id: "chunk_0005", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-06-01T15:18:04.125810+00:00", source_review_file: "data\\processed\\mathrock\\pdf_kg_multimodal_supplement\\arrangement_kg_review.synced.jsonl" };

MATCH (source:KGNode {id: "technique:hybrid_picking_arpeggio"})
MATCH (target:KGNode {id: "pattern:polyrhythmic_subdivision"})
MERGE (source)-[r:ENABLES {review_id: "mathrock_pdf_visual:chunk_0005:005"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.85, context_condition: "处理复杂节拍（如 7/8, 11/8）中的快速分解和弦时", review_note: "谱例中频繁出现跨弦的快速十六分音符或三十二分音符分解，且伴有滑音（sl.）和击勾弦。这种编排通常暗示使用混合拨弦（Hybrid Picking）来保证音色统一和速度稳定性，特别是在非对称节奏型中，手指拨弦能提供更细腻的动态控制。", evidence: "Tabs on Page 36-37 show rapid cross-string arpeggios with slurs and slides, typi", needs_visual_context: false, review_id: "mathrock_pdf_visual:chunk_0005:005", chunk_id: "chunk_0005", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-06-01T15:18:04.125810+00:00", source_review_file: "data\\processed\\mathrock\\pdf_kg_multimodal_supplement\\arrangement_kg_review.synced.jsonl" };

MATCH (source:KGNode {id: "chord:m7b5"})
MATCH (target:KGNode {id: "guitar_idiom:rootless_shell_voicing_on_4_strings"})
MERGE (source)-[r:ENABLES {review_id: "mathrock_pdf_visual:chunk_0007:001"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "编配半减七和弦（m7b5）时，使用第4-3-2-1弦组的高把位指法", review_note: "图示展示了Bm7b5在9品的高把位形态（x-x-9-8-9-9），这是一种典型的无根音Voicing。在Math Rock中，这种紧凑的4弦结构便于快速切换且音色明亮，避免了低音区的浑浊，适合与贝斯声部互补。", evidence: "Page 49 Bm7b5 diagram (4th string config): x-x-9-8-9-9", needs_visual_context: false, review_id: "mathrock_pdf_visual:chunk_0007:001", chunk_id: "chunk_0007", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-06-01T15:18:04.125810+00:00", source_review_file: "data\\processed\\mathrock\\pdf_kg_multimodal_supplement\\arrangement_kg_review.synced.jsonl" };

MATCH (source:KGNode {id: "chord:maj7"})
MATCH (target:KGNode {id: "heuristic:drop2_voicing_for_mid_range_clarity"})
MERGE (source)-[r:SUGGESTS {review_id: "mathrock_pdf_visual:chunk_0007:002"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.85, context_condition: "在中高把位（如8-10品）演奏大七和弦以获取清晰、不拥挤的听感", review_note: "图示CM7 (8fr: x-8-7-7-8-x) 和 GM7 (10fr: x-10-9-9-10-x) 均为Drop 2或类似结构的封闭和弦。这种指法省略了根音或五音，将色彩音（3度、7度）置于高音区，是Math Rock吉他手保持声部清晰度的核心手段。", evidence: "Page 51 CM7/GM7 diagrams showing closed voicings at 8fr/10fr", needs_visual_context: false, review_id: "mathrock_pdf_visual:chunk_0007:002", chunk_id: "chunk_0007", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-06-01T15:18:04.125810+00:00", source_review_file: "data\\processed\\mathrock\\pdf_kg_multimodal_supplement\\arrangement_kg_review.synced.jsonl" };

MATCH (source:KGNode {id: "concept:voice_leading"})
MATCH (target:KGNode {id: "caution:large_fretboard_jumps_disrupt_flow"})
MERGE (source)-[r:CONSTRAINS {review_id: "mathrock_pdf_visual:chunk_0007:003"}]->(target)
SET r += { knowledge_type: "Caution", confidence: 0.8, context_condition: "设计和弦进行（Progression）的指法路径时", review_note: "虽然文字提到了“邻近配置”，但图示通过Example 2 (Page 50) 直观展示了如何通过选择同一把位区域（如5-8品区间）的和弦变体来最小化左手移动距离。这是编曲时保证乐句连贯性（Legato feel）的物理基础。", evidence: "Page 50 Example 2 progression staying within 5fr-8fr range vs Example 1 open pos", needs_visual_context: false, review_id: "mathrock_pdf_visual:chunk_0007:003", chunk_id: "chunk_0007", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-06-01T15:18:04.125810+00:00", source_review_file: "data\\processed\\mathrock\\pdf_kg_multimodal_supplement\\arrangement_kg_review.synced.jsonl" };

MATCH (source:KGNode {id: "chord:min7"})
MATCH (target:KGNode {id: "pattern:barre_chord_mobility"})
MERGE (source)-[r:CAN_INSPIRE {review_id: "mathrock_pdf_visual:chunk_0007:004"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.75, context_condition: "需要快速转调或在不同把位重复相同和声色彩时", review_note: "Dm7的三种指法（10fr barre, 5fr partial, 12fr high）展示了同一和弦在不同弦组和把位的形态。编曲时可利用这种“可移动性”在同一乐句中制造音区对比（Register shift），例如从5品的温暖音色跳至12品的尖锐音色。", evidence: "Page 49 Dm7 diagrams at 10fr, 5fr, and 12fr", needs_visual_context: false, review_id: "mathrock_pdf_visual:chunk_0007:004", chunk_id: "chunk_0007", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-06-01T15:18:04.125810+00:00", source_review_file: "data\\processed\\mathrock\\pdf_kg_multimodal_supplement\\arrangement_kg_review.synced.jsonl" };

MATCH (source:KGNode {id: "chord:shell_voicing"})
MATCH (target:KGNode {id: "guitar_idiom:high_gain_riff_clarity"})
MERGE (source)-[r:ENABLES {review_id: "mathrock_pdf_visual:chunk_0009:001"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.95, context_condition: "编配高增益（High Gain/Distortion）吉他 Riff 或声部时", review_note: "图示展示了省略五音、仅保留根/三/七音的 Shell Voicing。这种稀疏排列能有效避免失真音色下的低频浑浊，是 Math Rock 中构建清晰、有力 Riff 的核心手段。", evidence: "Page 61 diagrams show Dm7/G7 shell voicings (Root-3rd-7th only); text mentions s", needs_visual_context: false, review_id: "mathrock_pdf_visual:chunk_0009:001", chunk_id: "chunk_0009", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-06-01T15:18:04.125810+00:00", source_review_file: "data\\processed\\mathrock\\pdf_kg_multimodal_supplement\\arrangement_kg_review.synced.jsonl" };

MATCH (source:KGNode {id: "progression:borrowed_bIII_major"})
MATCH (target:KGNode {id: "color:surprise_epiphany"})
MERGE (source)-[r:EVOKES {review_id: "mathrock_pdf_visual:chunk_0009:002"}]->(target)
SET r += { knowledge_type: "ColorEmotion", confidence: 0.85, context_condition: "在大调歌曲中寻求意外转折或情感升华时", review_note: "图示展示了借用平行小调的大三和弦（如 E 大调中的 G#m 被替换为 B 大调借用的 G# Major? No, text says C major borrowing from C minor -> Eb major. Image shows specific example: TubeLord style. The image on p67 shows a progression where a minor chord is replaced by a borrowed major chord creating surprise. Specifically, the text mentions replacing iii minor with borrowed III major from parallel minor. This creates a 'surprise' effect.", evidence: "Page 67 text & diagram: 'replaced by major triad borrowed from parallel minor...", needs_visual_context: false, review_id: "mathrock_pdf_visual:chunk_0009:002", chunk_id: "chunk_0009", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-06-01T15:18:04.125810+00:00", source_review_file: "data\\processed\\mathrock\\pdf_kg_multimodal_supplement\\arrangement_kg_review.synced.jsonl" };

MATCH (source:KGNode {id: "voicing:drop_2_shell"})
MATCH (target:KGNode {id: "caution:muddy_distortion"})
MERGE (source)-[r:CONSTRAINS {review_id: "mathrock_pdf_visual:chunk_0009:003"}]->(target)
SET r += { knowledge_type: "Caution", confidence: 0.75, context_condition: "使用高增益音色演奏密集和弦时", review_note: "虽然文本未直接说“禁止”，但图示反复强调 Shell Voicing（稀疏排列）在增益音色下的适用性。隐含的避坑规则是：在 Distortion 下避免使用包含五音或密集排列的完整和弦，否则会导致频段浑浊。", evidence: "Page 61 diagrams consistently show 3-note shells; text links them to 'gain tones", needs_visual_context: false, review_id: "mathrock_pdf_visual:chunk_0009:003", chunk_id: "chunk_0009", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-06-01T15:18:04.125810+00:00", source_review_file: "data\\processed\\mathrock\\pdf_kg_multimodal_supplement\\arrangement_kg_review.synced.jsonl" };
