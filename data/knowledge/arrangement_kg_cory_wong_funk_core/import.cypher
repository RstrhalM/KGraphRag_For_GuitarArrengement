// Generated from curated KG JSONL.
CREATE CONSTRAINT kg_node_id IF NOT EXISTS FOR (n:KGNode) REQUIRE n.id IS UNIQUE;

MERGE (n:KGNode {id: "caution:overcrowded_frequency_range"}) SET n.type = "caution", n.name = "overcrowded_frequency_range";
MERGE (n:KGNode {id: "caution:overcrowded_sixteenth_grid"}) SET n.type = "caution", n.name = "overcrowded_sixteenth_grid";
MERGE (n:KGNode {id: "caution:range_tone_mismatch"}) SET n.type = "caution", n.name = "range_tone_mismatch";
MERGE (n:KGNode {id: "chord:minor_seven_dorian_implication"}) SET n.type = "chord", n.name = "minor_seven_dorian_implication";
MERGE (n:KGNode {id: "color:driving_rimshot_quality"}) SET n.type = "color", n.name = "driving_rimshot_quality";
MERGE (n:KGNode {id: "color:environmental_depth"}) SET n.type = "color", n.name = "environmental_depth";
MERGE (n:KGNode {id: "color:percussive_funk_momentum"}) SET n.type = "color", n.name = "percussive_funk_momentum";
MERGE (n:KGNode {id: "color:percussive_momentum"}) SET n.type = "color", n.name = "percussive_momentum";
MERGE (n:KGNode {id: "color:signature_iconic_identity"}) SET n.type = "color", n.name = "signature_iconic_identity";
MERGE (n:KGNode {id: "color:sophisticated_harmonic_texture"}) SET n.type = "color", n.name = "sophisticated_harmonic_texture";
MERGE (n:KGNode {id: "color:suspended_tension"}) SET n.type = "color", n.name = "suspended_tension";
MERGE (n:KGNode {id: "color:tight_percussive_groove"}) SET n.type = "color", n.name = "tight_percussive_groove";
MERGE (n:KGNode {id: "color:tonal_character_change"}) SET n.type = "color", n.name = "tonal_character_change";
MERGE (n:KGNode {id: "feature:high_usability_for_comping"}) SET n.type = "feature", n.name = "high_usability_for_comping";
MERGE (n:KGNode {id: "feature:mixed_articulation_groove"}) SET n.type = "feature", n.name = "mixed_articulation_groove";
MERGE (n:KGNode {id: "feature:muted_chuck_density"}) SET n.type = "feature", n.name = "muted_chuck_density";
MERGE (n:KGNode {id: "feature:percussive_ghost_note"}) SET n.type = "feature", n.name = "percussive_ghost_note";
MERGE (n:KGNode {id: "feature:register_range"}) SET n.type = "feature", n.name = "register_range";
MERGE (n:KGNode {id: "feature:rhythmic_density"}) SET n.type = "feature", n.name = "rhythmic_density";
MERGE (n:KGNode {id: "feature:sixteenth_note_undercurrent"}) SET n.type = "feature", n.name = "sixteenth_note_undercurrent";
MERGE (n:KGNode {id: "feature:spatial_effects"}) SET n.type = "feature", n.name = "spatial_effects";
MERGE (n:KGNode {id: "feature:staccato_bubble"}) SET n.type = "feature", n.name = "staccato_bubble";
MERGE (n:KGNode {id: "feature:tone_aggressiveness"}) SET n.type = "feature", n.name = "tone_aggressiveness";
MERGE (n:KGNode {id: "feature:tone_shaping_via_register"}) SET n.type = "feature", n.name = "tone_shaping_via_register";
MERGE (n:KGNode {id: "feature:triplet_feel"}) SET n.type = "feature", n.name = "triplet_feel";
MERGE (n:KGNode {id: "heuristic:downbeat_emphasis_via_density"}) SET n.type = "heuristic", n.name = "downbeat_emphasis_via_density";
MERGE (n:KGNode {id: "heuristic:explore_articulation_variants"}) SET n.type = "heuristic", n.name = "explore_articulation_variants";
MERGE (n:KGNode {id: "heuristic:guitar_as_percussion"}) SET n.type = "heuristic", n.name = "guitar_as_percussion";
MERGE (n:KGNode {id: "heuristic:leave_space_for_band"}) SET n.type = "heuristic", n.name = "leave_space_for_band";
MERGE (n:KGNode {id: "heuristic:make_rhythm_part_a_hook"}) SET n.type = "heuristic", n.name = "make_rhythm_part_a_hook";
MERGE (n:KGNode {id: "heuristic:melodic_riff_from_scale"}) SET n.type = "heuristic", n.name = "melodic_riff_from_scale";
MERGE (n:KGNode {id: "heuristic:section_energy_stair_step"}) SET n.type = "heuristic", n.name = "section_energy_stair_step";
MERGE (n:KGNode {id: "scale:mixolydian_pentatonic_hybrid"}) SET n.type = "scale", n.name = "mixolydian_pentatonic_hybrid";
MERGE (n:KGNode {id: "shape:a_shape_minor_7"}) SET n.type = "shape", n.name = "a_shape_minor_7";
MERGE (n:KGNode {id: "shape:e_shape_minor_7"}) SET n.type = "shape", n.name = "e_shape_minor_7";
MERGE (n:KGNode {id: "shape:g_and_d_complexity"}) SET n.type = "shape", n.name = "g_and_d_complexity";
MERGE (n:KGNode {id: "style:funk"}) SET n.type = "style", n.name = "funk";
MERGE (n:KGNode {id: "style:rhythm_guitar"}) SET n.type = "style", n.name = "rhythm_guitar";
MERGE (n:KGNode {id: "task:comping"}) SET n.type = "task", n.name = "comping";
MERGE (n:KGNode {id: "task:funk_comping"}) SET n.type = "task", n.name = "funk_comping";
MERGE (n:KGNode {id: "task:rhythm_guitar_arrangement"}) SET n.type = "task", n.name = "rhythm_guitar_arrangement";
MERGE (n:KGNode {id: "task:riff_writing"}) SET n.type = "task", n.name = "riff_writing";
MERGE (n:KGNode {id: "technique:caged_system_fragmentation"}) SET n.type = "technique", n.name = "caged_system_fragmentation";
MERGE (n:KGNode {id: "technique:chromatic_approach_to_chord_tone"}) SET n.type = "technique", n.name = "chromatic_approach_to_chord_tone";
MERGE (n:KGNode {id: "technique:downstroke_double_stop"}) SET n.type = "technique", n.name = "downstroke_double_stop";
MERGE (n:KGNode {id: "technique:dynamic_matching"}) SET n.type = "technique", n.name = "dynamic_matching";
MERGE (n:KGNode {id: "technique:dynamic_voicing_contrast"}) SET n.type = "technique", n.name = "dynamic_voicing_contrast";
MERGE (n:KGNode {id: "technique:helicopter_hand_sweep"}) SET n.type = "technique", n.name = "helicopter_hand_sweep";
MERGE (n:KGNode {id: "technique:hybrid_pentatonic_dorian_lines"}) SET n.type = "technique", n.name = "hybrid_pentatonic_dorian_lines";
MERGE (n:KGNode {id: "technique:left_hand_muting"}) SET n.type = "technique", n.name = "left_hand_muting";
MERGE (n:KGNode {id: "technique:m7_to_m6_voice_leading"}) SET n.type = "technique", n.name = "m7_to_m6_voice_leading";
MERGE (n:KGNode {id: "technique:motif_weaving"}) SET n.type = "technique", n.name = "motif_weaving";
MERGE (n:KGNode {id: "technique:palm_muting"}) SET n.type = "technique", n.name = "palm_muting";
MERGE (n:KGNode {id: "technique:percussive_string_selection"}) SET n.type = "technique", n.name = "percussive_string_selection";
MERGE (n:KGNode {id: "technique:pod_based_comping"}) SET n.type = "technique", n.name = "pod_based_comping";
MERGE (n:KGNode {id: "technique:register_specific_triads"}) SET n.type = "technique", n.name = "register_specific_triads";
MERGE (n:KGNode {id: "technique:rhythmic_melodic_hybrid"}) SET n.type = "technique", n.name = "rhythmic_melodic_hybrid";
MERGE (n:KGNode {id: "technique:right_hand_constant_motion"}) SET n.type = "technique", n.name = "right_hand_constant_motion";
MERGE (n:KGNode {id: "technique:upstroke_hit_downstroke"}) SET n.type = "technique", n.name = "upstroke_hit_downstroke";
MERGE (n:KGNode {id: "voicing:generic_jamming"}) SET n.type = "voicing", n.name = "generic_jamming";
MERGE (n:KGNode {id: "voicing:poly_chord_structure"}) SET n.type = "voicing", n.name = "poly_chord_structure";
MERGE (n:KGNode {id: "voicing:sparse_adjacent_double_stops"}) SET n.type = "voicing", n.name = "sparse_adjacent_double_stops";
MERGE (n:KGNode {id: "voicing:sparse_funk_voicing"}) SET n.type = "voicing", n.name = "sparse_funk_voicing";
MERGE (n:KGNode {id: "voicing:sparse_to_dense_layering"}) SET n.type = "voicing", n.name = "sparse_to_dense_layering";
MERGE (n:KGNode {id: "voicing:string_set_selection"}) SET n.type = "voicing", n.name = "string_set_selection";
MERGE (n:KGNode {id: "voicing:sus_triad_over_root"}) SET n.type = "voicing", n.name = "sus_triad_over_root";
MERGE (n:KGNode {id: "voicing:triad_pods"}) SET n.type = "voicing", n.name = "triad_pods";

MATCH (source:KGNode {id: "heuristic:make_rhythm_part_a_hook"})
MATCH (target:KGNode {id: "task:riff_writing"})
MERGE (source)-[r:EVOKES {review_id: "chunk_0003:funk_scale:001"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.95, context_condition: "Funk/Pop rhythm guitar comping where static strumming feels generic.", review_note: "Transform standard chord comping into a signature hook by integrating melodic lines (pentatonic/scale) within the chord shape, rather than just strumming full voicings.", evidence: "what makes something more signature? is if you actually make a part from it some", needs_visual_context: false, review_id: "chunk_0003:funk_scale:001", chunk_id: "chunk_0003", page_hint: "scale.1 major,minor,dominant / part 1", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "voicing:sparse_funk_voicing"})
MATCH (target:KGNode {id: "heuristic:leave_space_for_band"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0003:funk_scale:002"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.92, context_condition: "Playing in a band with keys, horns, or bass; dominant 7th contexts.", review_note: "Break complex chord voicings into smaller 'pods' (2-3 notes, e.g., Root+b7) to imply harmony while leaving frequency space for other instruments.", evidence: "break these chord voicings up into little pods... creates more space in the cont", needs_visual_context: false, review_id: "chunk_0003:funk_scale:002", chunk_id: "chunk_0003", page_hint: "scale.1 major,minor,dominant / part 1", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "technique:chromatic_approach_to_chord_tone"})
MATCH (target:KGNode {id: "color:percussive_funk_momentum"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0003:funk_scale:003"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.88, context_condition: "Dominant 7th chords, specifically targeting the 3rd.", review_note: "Use half-step approaches (b3 to 3) on dominant chords to create tension/release and rhythmic momentum within the comping pattern.", evidence: "flat three to three thing... half step move into it... based off the mixolydian", needs_visual_context: false, review_id: "chunk_0003:funk_scale:003", chunk_id: "chunk_0003", page_hint: "scale.1 major,minor,dominant / part 1", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "scale:mixolydian_pentatonic_hybrid"})
MATCH (target:KGNode {id: "task:funk_comping"})
MERGE (source)-[r:CAN_INSPIRE {review_id: "chunk_0003:funk_scale:004"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.85, context_condition: "Improvising lines over static dominant or major funk vamps.", review_note: "Combine Major Pentatonic safety with Mixolydian color tones (b7, 9) to create comping lines that define the harmony without overcrowding.", evidence: "adding some mixolydian lines in with the comping... pentatonic lines mixed in", needs_visual_context: false, review_id: "chunk_0003:funk_scale:004", chunk_id: "chunk_0003", page_hint: "scale.1 major,minor,dominant / part 1", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "voicing:triad_pods"})
MATCH (target:KGNode {id: "caution:range_tone_mismatch"})
MERGE (source)-[r:CONSTRAINS {review_id: "chunk_0003:funk_scale:005"}]->(target)
SET r += { knowledge_type: "Caution", confidence: 0.75, context_condition: "Using small voicings (pods) on lower strings vs higher strings.", review_note: "When breaking chords into pods, ensure the selected intervals (e.g., Root+b7) are voiced in a register that doesn't clash with the bassist's fundamental frequencies.", evidence: "root and the flat seven... sounds kind of bad on its own, but in the context...", needs_visual_context: false, review_id: "chunk_0003:funk_scale:005", chunk_id: "chunk_0003", page_hint: "scale.1 major,minor,dominant / part 1", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "technique:caged_system_fragmentation"})
MATCH (target:KGNode {id: "feature:staccato_bubble"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0003:funk_scale:006"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.82, context_condition: "Creating rhythmic variety within a single position.", review_note: "Fragment CAGED shapes into smaller sub-groups (triads/dyads) to facilitate staccato, percussive 'bubble' parts that are easier to mute and articulate than full barre chords.", evidence: "break it up into smaller groups, little subgroups of that shape... triad here or", needs_visual_context: false, review_id: "chunk_0003:funk_scale:006", chunk_id: "chunk_0003", page_hint: "scale.1 major,minor,dominant / part 1", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "style:funk"})
MATCH (target:KGNode {id: "chord:minor_seven_dorian_implication"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0004:funk_scale:007"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "When arranging funk rhythm parts in minor keys", review_note: "In funk, minor 7 chords often imply the Dorian mode (natural 6) rather than Aeolian. Arrangers should prioritize voicings and lines that highlight the natural 6th interval.", evidence: "minor seven chords are super common in funk... implying dorian... natural six", needs_visual_context: false, review_id: "chunk_0004:funk_scale:007", chunk_id: "chunk_0004", page_hint: "scale.1 major,minor,dominant / part 2", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "task:funk_comping"})
MATCH (target:KGNode {id: "technique:m7_to_m6_voice_leading"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0004:funk_scale:008"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.85, context_condition: "Creating movement within a static minor funk groove", review_note: "A core funk comping move is alternating between Minor 7 and Minor 6 voicings (lowering the 7th by a semitone to the 6th) within the same chord shape to create rhythmic and harmonic interest.", evidence: "moving the seven down a half step... putting it from a minor seven to a minor si", needs_visual_context: false, review_id: "chunk_0004:funk_scale:008", chunk_id: "chunk_0004", page_hint: "scale.1 major,minor,dominant / part 2", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "task:riff_writing"})
MATCH (target:KGNode {id: "technique:hybrid_pentatonic_dorian_lines"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0004:funk_scale:009"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.8, context_condition: "Writing single-note hooks or fills over minor funk chords", review_note: "Combine minor pentatonic phrases with Dorian scale notes (specifically the major 6th) within the same position to create sophisticated funk lines that bridge bluesy and jazzy sounds.", evidence: "minor PE ni tonic scale and the dorian scale working with in this shape... come", needs_visual_context: false, review_id: "chunk_0004:funk_scale:009", chunk_id: "chunk_0004", page_hint: "scale.1 major,minor,dominant / part 2", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "voicing:sparse_funk_voicing"})
MATCH (target:KGNode {id: "heuristic:leave_space_for_band"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0004:funk_scale:010"}]->(target)
SET r += { knowledge_type: "ColorEmotion", confidence: 0.9, context_condition: "Comping in a full band mix (bass/drums/keys)", review_note: "Split full chord shapes into smaller 'pods' (2-3 notes) to reduce frequency clutter and leave sonic space for other instruments, a key principle in tight funk arrangements.", evidence: "split it up,i play little pods of it to kind of make.more space for the other in", needs_visual_context: false, review_id: "chunk_0004:funk_scale:010", chunk_id: "chunk_0004", page_hint: "scale.1 major,minor,dominant / part 2", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "shape:e_shape_minor_7"})
MATCH (target:KGNode {id: "technique:pod_based_comping"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0004:funk_scale:011"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.75, context_condition: "Using 6th-string rooted minor 7 shapes in funk", review_note: "The E-shape minor 7 is effective for funk when broken into smaller fragments ('pods') rather than played as a full barre chord, facilitating rhythmic precision and tonal clarity.", evidence: "e shape classic sixth string rooted minor seven cord... split it up,i play littl", needs_visual_context: false, review_id: "chunk_0004:funk_scale:011", chunk_id: "chunk_0004", page_hint: "scale.1 major,minor,dominant / part 2", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "shape:a_shape_minor_7"})
MATCH (target:KGNode {id: "feature:high_usability_for_comping"})
MERGE (source)-[r:EVOKES {review_id: "chunk_0004:funk_scale:012"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.8, context_condition: "Selecting primary voicing positions for minor funk grooves", review_note: "The A-shape minor 7 (5th string root) is highly recommended for funk comping due to its ergonomic layout, allowing easy integration of pentatonic lines and m7-m6 voice leading.", evidence: "if I had to pick one spot to play for minor seven chords.it would be this spot [", needs_visual_context: false, review_id: "chunk_0004:funk_scale:012", chunk_id: "chunk_0004", page_hint: "scale.1 major,minor,dominant / part 2", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "task:rhythm_guitar_arrangement"})
MATCH (target:KGNode {id: "shape:g_and_d_complexity"})
MERGE (source)-[r:CAUTIONS {review_id: "chunk_0004:funk_scale:013"}]->(target)
SET r += { knowledge_type: "Caution", confidence: 0.6, context_condition: "Choosing voicings for live or tight studio funk tracks", review_note: "G-shape and D-shape minor voicings are often less ideal for dense funk comping due to finger complexity; prefer using them for single-note extensions or simpler lines unless specifically required.", evidence: "g shape honestly is not one that I really go to a lot for comping... d shape...", needs_visual_context: false, review_id: "chunk_0004:funk_scale:013", chunk_id: "chunk_0004", page_hint: "scale.1 major,minor,dominant / part 2", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "voicing:triad_pods"})
MATCH (target:KGNode {id: "heuristic:leave_space_for_band"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0005:funk_scale:014"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "Arranging rhythm guitar parts where bass and keys occupy full harmonic space.", review_note: "Triads on specific string groups (e.g., strings 1-2-3 or 2-3-4) reduce frequency clutter, allowing the bass to define the root and other instruments to fill mid/low frequencies.", evidence: "Triads in groupings of three strings... real power is understanding how they fit", needs_visual_context: false, review_id: "chunk_0005:funk_scale:014", chunk_id: "chunk_0005", page_hint: "scale.2 Triads", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "voicing:poly_chord_structure"})
MATCH (target:KGNode {id: "color:sophisticated_harmonic_texture"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0005:funk_scale:015"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.85, context_condition: "Creating extended harmony (7ths, 9ths, sus) using simple major/minor triad shapes over a different bass note.", review_note: "Analyze GP5 for triad shapes that do not match the track's root chord. E.g., Eb Major triad shape over C bass implies Cm7. This allows complex harmony with simple fingerings.", evidence: "Eb major triad over a C cord... AC minor seven... G minor triad over AC... C dom", needs_visual_context: false, review_id: "chunk_0005:funk_scale:015", chunk_id: "chunk_0005", page_hint: "scale.2 Triads", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "technique:register_specific_triads"})
MATCH (target:KGNode {id: "voicing:string_set_selection"})
MERGE (source)-[r:CONSTRAINS {review_id: "chunk_0005:funk_scale:016"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.95, context_condition: "Selecting voicings based on desired tonal range and interaction with other band members.", review_note: "Map triad shapes to specific string sets: Strings 1-2-3 (High/Bright), 2-3-4 (Mid), 3-4-5 (Low-Mid), 4-5-6 (Low/Thick). Use higher sets for funk/pop clarity, lower sets for rock/blues weight.", evidence: "Strings one,two,three... two,three,four... three,four,five... four,five,six.", needs_visual_context: false, review_id: "chunk_0005:funk_scale:016", chunk_id: "chunk_0005", page_hint: "scale.2 Triads", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "voicing:sus_triad_over_root"})
MATCH (target:KGNode {id: "color:suspended_tension"})
MERGE (source)-[r:EVOKES {review_id: "chunk_0005:funk_scale:017"}]->(target)
SET r += { knowledge_type: "ColorEmotion", confidence: 0.8, context_condition: "Using a major triad built on the 5th degree over the tonic bass (e.g., G triad over C bass).", review_note: "Identify 'Sus' sounds created by triad/bass combinations. A major triad on the 5th scale degree over the root creates a Csus4/add9 feel without complex fingering.", evidence: "Put a G in the base... it's just an A minor... cover D this sort of suss sound..", needs_visual_context: false, review_id: "chunk_0005:funk_scale:017", chunk_id: "chunk_0005", page_hint: "scale.2 Triads", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "task:rhythm_guitar_arrangement"})
MATCH (target:KGNode {id: "heuristic:make_rhythm_part_a_hook"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0006:funk_scale:018"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.95, context_condition: "When composing rhythm guitar parts for pop/funk/R&B tracks where the guitar needs to define the song's identity.", review_note: "The primary goal is to create a rhythm part that functions as an instrumental hook, distinct from generic comping. It should be memorable enough that cover bands must replicate it exactly.", evidence: "find something that could stand up on its own... ribbon guitar part be an instru", needs_visual_context: false, review_id: "chunk_0006:funk_scale:018", chunk_id: "chunk_0006", page_hint: "scale.3 和声编配分享", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "heuristic:make_rhythm_part_a_hook"})
MATCH (target:KGNode {id: "color:signature_iconic_identity"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0006:funk_scale:019"}]->(target)
SET r += { knowledge_type: "ColorEmotion", confidence: 0.9, context_condition: "When the rhythm guitar part is designed to be integral to the arrangement rather than background filler.", review_note: "A successful hook-based rhythm part weaves into the fabric of the song, creating a signature sound that defines the track's identity.", evidence: "weaves into the fabric of the song... create something that's signature iconic", needs_visual_context: false, review_id: "chunk_0006:funk_scale:019", chunk_id: "chunk_0006", page_hint: "scale.3 和声编配分享", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "task:riff_writing"})
MATCH (target:KGNode {id: "technique:motif_weaving"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0006:funk_scale:020"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.85, context_condition: "Constructing complex rhythmic hooks by combining different musical elements.", review_note: "Create signature hooks by weaving together single-note lines, double stops (dyads), triads, pentatonic shapes, and chord voicings rather than sticking to one texture.", evidence: "get single note lines, two note lines dyads, triads, pentatonic shapes... woven", needs_visual_context: false, review_id: "chunk_0006:funk_scale:020", chunk_id: "chunk_0006", page_hint: "scale.3 和声编配分享", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "task:comping"})
MATCH (target:KGNode {id: "heuristic:leave_space_for_band"})
MERGE (source)-[r:CONSTRAINS {review_id: "chunk_0006:funk_scale:021"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.8, context_condition: "When accompanying a vocalist or lead instrument.", review_note: "Rhythm guitar must support and enhance the lead/vocal without overcrowding. The part should serve the song, not just display technical skill.", evidence: "not the focal point... comp behind it... enhances what they're doing", needs_visual_context: false, review_id: "chunk_0006:funk_scale:021", chunk_id: "chunk_0006", page_hint: "scale.3 和声编配分享", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "voicing:generic_jamming"})
MATCH (target:KGNode {id: "heuristic:make_rhythm_part_a_hook"})
MERGE (source)-[r:CONFLICTS_WITH {review_id: "chunk_0006:funk_scale:022"}]->(target)
SET r += { knowledge_type: "Caution", confidence: 0.9, context_condition: "Avoiding undefined, random strumming that lacks compositional intent.", review_note: "Generic jamming on chords (e.g., random Am7 strumming) fails to create a signature part. Specificity in voicing and rhythm is required to make the part essential to the song.", evidence: "does it just feel like you're jamming on a chord... vs exact part", needs_visual_context: false, review_id: "chunk_0006:funk_scale:022", chunk_id: "chunk_0006", page_hint: "scale.3 和声编配分享", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "style:rhythm_guitar"})
MATCH (target:KGNode {id: "color:percussive_momentum"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0007:funk_rhythm:001"}]->(target)
SET r += { knowledge_type: "ColorEmotion", confidence: 0.9, context_condition: "When the guitar part functions as the primary driver of song energy rather than just harmonic support.", review_note: "Rhythm guitar is defined here not just as chords, but as the engine for 'momentum' and 'vibe'. In GP5 analysis, look for consistent rhythmic density that aligns with the drum groove to fulfill this role.", evidence: "helps propel the momentum and the vibe and the feel of the song forward", needs_visual_context: false, review_id: "chunk_0007:funk_rhythm:001", chunk_id: "chunk_0007", page_hint: "rythmn.1 introduction", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "technique:percussive_string_selection"})
MATCH (target:KGNode {id: "feature:tone_shaping_via_register"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0007:funk_rhythm:002"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.85, context_condition: "Using specific string sets (heavy vs. light) to mimic percussion instruments like shakers or tambourines.", review_note: "Selecting lower strings creates a 'deeper' percussive sound (like a heavy shaker), while higher strings create a 'lighter' sound. This is a crucial voicing decision for texture.", evidence: "get that here by literally just picking the the heavier strings... different sha", needs_visual_context: false, review_id: "chunk_0007:funk_rhythm:002", chunk_id: "chunk_0007", page_hint: "rythmn.1 introduction", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "task:rhythm_guitar_arrangement"})
MATCH (target:KGNode {id: "heuristic:guitar_as_percussion"})
MERGE (source)-[r:EVOKES {review_id: "chunk_0007:funk_rhythm:003"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.95, context_condition: "Treating the guitar as a pitched percussion instrument (tambourine/shaker/bongos) within the rhythm section.", review_note: "The guitar should weave in and out of the bass/drum foundation. It acts as a 'pitched tambourine'. This implies using muted strums or staccato notes that lock with the hi-hat or shaker patterns.", evidence: "can kind of be like a pitched tambourine... or shaker... filling the same rhythm", needs_visual_context: false, review_id: "chunk_0007:funk_rhythm:003", chunk_id: "chunk_0007", page_hint: "rythmn.1 introduction", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "voicing:sparse_to_dense_layering"})
MATCH (target:KGNode {id: "heuristic:section_energy_stair_step"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0007:funk_rhythm:004"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.8, context_condition: "Building arrangement intensity by increasing note count in voicings (1 to 5 notes) over time.", review_note: "Start with percussive/single-note elements and gradually add harmonic information (voicings) to build energy. Don't start with full chords if the song needs room to grow.", evidence: "keep building on top of that playing different voicings one,two,three,four,five", needs_visual_context: false, review_id: "chunk_0007:funk_rhythm:004", chunk_id: "chunk_0007", page_hint: "rythmn.1 introduction", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "technique:rhythmic_melodic_hybrid"})
MATCH (target:KGNode {id: "feature:mixed_articulation_groove"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0007:funk_rhythm:005"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.85, context_condition: "Combining percussive hits with melodic/harmonic fragments in the same phrase.", review_note: "Mix percussive 'bongo-like' rhythms with actual notes. This creates a hybrid role that fills rhythmic space while providing harmonic/melodic cues.", evidence: "adding melodic... harmonic information... BA tup tup tup tu t tum like bongos", needs_visual_context: false, review_id: "chunk_0007:funk_rhythm:005", chunk_id: "chunk_0007", page_hint: "rythmn.1 introduction", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "feature:staccato_bubble"})
MATCH (target:KGNode {id: "heuristic:make_rhythm_part_a_hook"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0008:funk_rhythm:006"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "Funk/R&B rhythm guitar parts requiring melodic identity within the groove.", review_note: "Bubble parts (staccato single notes/ostinatos) should be constructed as distinct phrases or counter-melodies rather than random notes to create a 'hook' that stands out in the mix.", evidence: "Make it feel like a phrase... hopefully will end up feeling like hooks... counte", needs_visual_context: false, review_id: "chunk_0008:funk_rhythm:006", chunk_id: "chunk_0008", page_hint: "rythmn.2 Bubbles and Chucks", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "voicing:sparse_funk_voicing"})
MATCH (target:KGNode {id: "heuristic:leave_space_for_band"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0008:funk_rhythm:007"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.95, context_condition: "Comping with 'chucks' (muted strums) in a dense band arrangement.", review_note: "Focus on 2-3 string voicings (e.g., minor 7th shapes) and vary the ratio of notes to muted 'chucks' to avoid frequency clashes with keys/horns and leave space for bass/drums.", evidence: "Focus on two or three strings at a time... less notes more chucks... allows a li", needs_visual_context: false, review_id: "chunk_0008:funk_rhythm:007", chunk_id: "chunk_0008", page_hint: "rythmn.2 Bubbles and Chucks", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "feature:muted_chuck_density"})
MATCH (target:KGNode {id: "caution:overcrowded_sixteenth_grid"})
MERGE (source)-[r:CAUTIONS {review_id: "chunk_0008:funk_rhythm:008"}]->(target)
SET r += { knowledge_type: "Caution", confidence: 0.9, context_condition: "High-density 16th note comping where timing precision is critical.", review_note: "If outlining the entire 16th note grid with chucks, strict locking with the drummer is required; otherwise, reduce chuck density to prevent a messy sound.", evidence: "If you're outlining the entire sixteenth note grid and it's not lining up... can", needs_visual_context: false, review_id: "chunk_0008:funk_rhythm:008", chunk_id: "chunk_0008", page_hint: "rythmn.2 Bubbles and Chucks", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "technique:right_hand_constant_motion"})
MATCH (target:KGNode {id: "feature:sixteenth_note_undercurrent"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0008:funk_rhythm:009"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.95, context_condition: "Maintaining a consistent funk groove regardless of note density.", review_note: "The right hand maintains constant 16th-note motion (motor); articulation is controlled by left-hand fretting pressure and right-hand strike intensity, not by stopping the hand.", evidence: "Right hand motor is just moving the whole time. It's just when do I press down.", needs_visual_context: false, review_id: "chunk_0008:funk_rhythm:009", chunk_id: "chunk_0008", page_hint: "rythmn.2 Bubbles and Chucks", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "heuristic:section_energy_stair_step"})
MATCH (target:KGNode {id: "task:rhythm_guitar_arrangement"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0008:funk_rhythm:010"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "Arranging rhythm guitar parts across song sections (Verse -> Pre-Chorus -> Chorus).", review_note: "Build energy by progressively opening up the strumming stroke, increasing velocity, and allowing more notes through from verse to chorus, creating a 'stair-step' momentum.", evidence: "First half of verse... second half... pre chorus, I'll open up my stroke... chor", needs_visual_context: false, review_id: "chunk_0008:funk_rhythm:010", chunk_id: "chunk_0008", page_hint: "rythmn.2 Bubbles and Chucks", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "style:funk"})
MATCH (target:KGNode {id: "color:percussive_funk_momentum"})
MERGE (source)-[r:EVOKES {review_id: "chunk_0008:funk_rhythm:011"}]->(target)
SET r += { knowledge_type: "ColorEmotion", confidence: 0.85, context_condition: "Combining bubbles and chucks to drive the song forward.", review_note: "The interplay of staccato bubbles and percussive chucks creates a rhythmic undercurrent that propels the song's momentum, acting like a shaker or percussion instrument.", evidence: "Blends the both... rhythmic momentum... undercurrent... propel the momentum of a", needs_visual_context: false, review_id: "chunk_0008:funk_rhythm:011", chunk_id: "chunk_0008", page_hint: "rythmn.2 Bubbles and Chucks", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "heuristic:explore_articulation_variants"})
MATCH (target:KGNode {id: "task:rhythm_guitar_arrangement"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0009:funk_rhythm:012"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.75, context_condition: "When arranging or practicing a rhythm part to find the optimal feel.", review_note: "To define a rhythm part's character, systematically vary muting levels, staccato/legato balance, and dynamics on the same underlying pattern.", evidence: "explore what it's like to play different dynamic levels different levels of muti", needs_visual_context: false, review_id: "chunk_0009:funk_rhythm:012", chunk_id: "chunk_0009", page_hint: "rythmn.3 时值，模式，律动", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "feature:rhythmic_density"})
MATCH (target:KGNode {id: "task:rhythm_guitar_arrangement"})
MERGE (source)-[r:CONSTRAINS {review_id: "chunk_0010:funk_rhythm:013"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "When analyzing a section requiring high energy or 'motion' vs. sparse accompaniment.", review_note: "High rhythmic density (e.g., continuous 16th notes) implies a driving funk/rock role; low density implies space/half-time feel. GP5 note density is a primary trigger.", evidence: "Song calls for rhythmically dense part with lot of action/motion vs chunking alo", needs_visual_context: false, review_id: "chunk_0010:funk_rhythm:013", chunk_id: "chunk_0010", page_hint: "rythmn.4 节奏密度、音域、音色、空间", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "feature:register_range"})
MATCH (target:KGNode {id: "color:tonal_character_change"})
MERGE (source)-[r:EVOKES {review_id: "chunk_0010:funk_rhythm:014"}]->(target)
SET r += { knowledge_type: "ColorEmotion", confidence: 0.85, context_condition: "Same rhythmic pattern played in different fretboard positions (low vs. high register).", review_note: "Changing the register (range) of a riff while keeping rhythm/voicing shape constant alters the emotional weight and frequency slot in the mix. High register = brighter/thinner; Low = heavier/muddier.", evidence: "Same rhythmic density but range changed... affects way guitar part feels and fun", needs_visual_context: false, review_id: "chunk_0010:funk_rhythm:014", chunk_id: "chunk_0010", page_hint: "rythmn.4 节奏密度、音域、音色、空间", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "feature:tone_aggressiveness"})
MATCH (target:KGNode {id: "technique:dynamic_matching"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0010:funk_rhythm:015"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.8, context_condition: "Clean tone feels inappropriate for a dense/aggressive rhythmic part.", review_note: "If GP5 indicates heavy distortion/overdrive settings or aggressive articulation, clean tones may lack the necessary sustain/compression. Match tone to rhythmic intensity.", evidence: "Clean tone... calls for something with overdrive... feels more right for that sp", needs_visual_context: false, review_id: "chunk_0010:funk_rhythm:015", chunk_id: "chunk_0010", page_hint: "rythmn.4 节奏密度、音域、音色、空间", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "feature:spatial_effects"})
MATCH (target:KGNode {id: "color:environmental_depth"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0010:funk_rhythm:016"}]->(target)
SET r += { knowledge_type: "ColorEmotion", confidence: 0.75, context_condition: "Dry signal feels flat or mono; part needs 'air' or separation.", review_note: "Adding reverb/delay creates a sense of space/environment. Essential for parts that need to sit back in the mix or create atmosphere, distinct from dry 'in-your-face' funk chops.", evidence: "Adds an air to it... feels like I'm in a different environment... reverb open th", needs_visual_context: false, review_id: "chunk_0010:funk_rhythm:016", chunk_id: "chunk_0010", page_hint: "rythmn.4 节奏密度、音域、音色、空间", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "heuristic:section_energy_stair_step"})
MATCH (target:KGNode {id: "task:rhythm_guitar_arrangement"})
MERGE (source)-[r:CAN_INSPIRE {review_id: "chunk_0010:funk_rhythm:017"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "Arranging multiple sections (Verse/Chorus) to avoid monotony.", review_note: "Build energy by varying density, range, and voicing size across sections. E.g., Verse = sparse/low range; Chorus = dense/high range/fuller voicings.", evidence: "Next section just needs two notes... how it builds... same guitar part in three", needs_visual_context: false, review_id: "chunk_0010:funk_rhythm:017", chunk_id: "chunk_0010", page_hint: "rythmn.4 节奏密度、音域、音色、空间", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "voicing:sparse_funk_voicing"})
MATCH (target:KGNode {id: "caution:overcrowded_sixteenth_grid"})
MERGE (source)-[r:CONFLICTS_WITH {review_id: "chunk_0010:funk_rhythm:018"}]->(target)
SET r += { knowledge_type: "Caution", confidence: 0.8, context_condition: "High rhythmic density combined with complex chord voicings.", review_note: "High 16th-note density often requires simpler voicings (2-3 notes) to maintain clarity and groove. Complex chords + fast strumming = mud.", evidence: "Should this be bubble chucks... single notes... two notes... pretty much same pa", needs_visual_context: false, review_id: "chunk_0010:funk_rhythm:018", chunk_id: "chunk_0010", page_hint: "rythmn.4 节奏密度、音域、音色、空间", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "technique:upstroke_hit_downstroke"})
MATCH (target:KGNode {id: "feature:percussive_ghost_note"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0011:funk_signature:001"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.95, context_condition: "Funk/R&B rhythm guitar comping requiring tight, percussive groove without full chord sustain.", review_note: "The core mechanic is a three-part right-hand motion: Upstroke -> Muted String Hit (Ghost) -> Downstroke. This creates a rhythmic 'filler' or syncopated accent between standard strums.", evidence: "right hand... upstroke hit the string... downstroke... hitting the strings with", needs_visual_context: false, review_id: "chunk_0011:funk_signature:001", chunk_id: "chunk_0011", page_hint: "cory wong绝招.1 hitting the strings", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "technique:upstroke_hit_downstroke"})
MATCH (target:KGNode {id: "feature:sixteenth_note_undercurrent"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0011:funk_signature:002"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "Practicing or performing continuous 16th note funk patterns where the 'hit' acts as the off-beat or subdivision filler.", review_note: "This technique is often practiced as 16th notes (4-note phrases with 3 moves: Up-Hit-Down), creating a symmetrical rhythmic cell that drives the 16th note grid.", evidence: "practice as sixteenth notes... four note phrases with three moves... symmetrical", needs_visual_context: false, review_id: "chunk_0011:funk_signature:002", chunk_id: "chunk_0011", page_hint: "cory wong绝招.1 hitting the strings", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "technique:upstroke_hit_downstroke"})
MATCH (target:KGNode {id: "task:riff_writing"})
MERGE (source)-[r:CAN_INSPIRE {review_id: "chunk_0011:funk_signature:003"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.85, context_condition: "Creating melodic riffs or lead lines that need rhythmic punctuation similar to rhythm comping.", review_note: "The 'Up-Hit-Down' motion can be applied to single-note lines or double-stops in lead playing to add percussive articulation and rhythmic interest, blurring the line between rhythm and lead.", evidence: "bring it into your lead guitar realm... part of a different lead guitar sort of", needs_visual_context: false, review_id: "chunk_0011:funk_signature:003", chunk_id: "chunk_0011", page_hint: "cory wong绝招.1 hitting the strings", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "technique:left_hand_muting"})
MATCH (target:KGNode {id: "technique:upstroke_hit_downstroke"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0011:funk_signature:004"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.9, context_condition: "Executing the 'hit' portion of the Up-Hit-Down sequence to ensure it produces a percussive 'chuck' rather than a pitch.", review_note: "Left hand must mute strings completely during the 'hit' phase to achieve the signature percussive sound. Without left-hand muting, the 'hit' becomes a accidental chord/note.", evidence: "mute the strings like this go up stroke hit downstroke", needs_visual_context: false, review_id: "chunk_0011:funk_signature:004", chunk_id: "chunk_0011", page_hint: "cory wong绝招.1 hitting the strings", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "feature:triplet_feel"})
MATCH (target:KGNode {id: "color:percussive_funk_momentum"})
MERGE (source)-[r:EVOKES {review_id: "chunk_0011:funk_signature:005"}]->(target)
SET r += { knowledge_type: "ColorEmotion", confidence: 0.8, context_condition: "Applying the Up-Hit-Down pattern in triplet subdivisions instead of straight 16ths.", review_note: "Using the 3-move pattern over triplets changes the phrasing feel, offering a swung or shuffle-like momentum while maintaining the percussive articulation.", evidence: "do it as triplets... gives it a little bit of a different thing", needs_visual_context: false, review_id: "chunk_0011:funk_signature:005", chunk_id: "chunk_0011", page_hint: "cory wong绝招.1 hitting the strings", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "technique:downstroke_double_stop"})
MATCH (target:KGNode {id: "color:driving_rimshot_quality"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0012:funk_signature:006"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.95, context_condition: "Funk/R&B rhythm guitar requiring aggressive, consistent attack without dynamic fluctuation from alternate picking.", review_note: "Strict all-downstroke picking on double stops ensures uniform accentuation and a 'rimshot' percussive tone, avoiding the softening effect of upstrokes.", evidence: "all downstrokes... changes the attack... not as driving... Rimba quality", needs_visual_context: false, review_id: "chunk_0012:funk_signature:006", chunk_id: "chunk_0012", page_hint: "cory wong绝招.2 downstroke double stop", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "technique:palm_muting"})
MATCH (target:KGNode {id: "color:tight_percussive_groove"})
MERGE (source)-[r:EVOKES {review_id: "chunk_0012:funk_signature:007"}]->(target)
SET r += { knowledge_type: "ColorEmotion", confidence: 0.9, context_condition: "Double stop or single note lines where clarity and rhythmic definition are prioritized over sustain.", review_note: "Palm muting is essential to achieve the signature tight, dry, and percussive 'Cory Wong' sound; without it, the tone lacks the specific rhythmic punch.", evidence: "if i didn't palm mute... doesn't quite have that... Rimba quality", needs_visual_context: false, review_id: "chunk_0012:funk_signature:007", chunk_id: "chunk_0012", page_hint: "cory wong绝招.2 downstroke double stop", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "voicing:sparse_adjacent_double_stops"})
MATCH (target:KGNode {id: "heuristic:melodic_riff_from_scale"})
MERGE (source)-[r:SUGGESTS {review_id: "chunk_0012:funk_signature:008"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.85, context_condition: "Creating rhythmic hooks using pentatonic scales harmonized in thirds/sixths on adjacent strings.", review_note: "Use adjacent string pairs within pentatonic shapes to create moving double-stop riffs. This simplifies left-hand movement while maintaining harmonic context.", evidence: "harmonize the strings that are adjacent... thinking pentatonic scale", needs_visual_context: false, review_id: "chunk_0012:funk_signature:008", chunk_id: "chunk_0012", page_hint: "cory wong绝招.2 downstroke double stop", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "voicing:sparse_funk_voicing"})
MATCH (target:KGNode {id: "caution:overcrowded_frequency_range"})
MERGE (source)-[r:CONSTRAINS {review_id: "chunk_0012:funk_signature:009"}]->(target)
SET r += { knowledge_type: "Caution", confidence: 0.9, context_condition: "Strumming full 6-string chords in a dense funk mix.", review_note: "Avoid strumming all 6 strings continuously. Sparse voicings (2-3 notes) provide groove clarity and space, whereas full chords can sound muddy or 'in your face' aggressively.", evidence: "don't have a lot of notes in my chord voicing... helps with the groove... too mu", needs_visual_context: false, review_id: "chunk_0012:funk_signature:009", chunk_id: "chunk_0012", page_hint: "cory wong绝招.2 downstroke double stop", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "technique:dynamic_voicing_contrast"})
MATCH (target:KGNode {id: "heuristic:downbeat_emphasis_via_density"})
MERGE (source)-[r:ENABLES {review_id: "chunk_0012:funk_signature:010"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.88, context_condition: "Structuring a comping pattern to highlight the downbeat.", review_note: "Hit a fuller voicing (or all strings) on the downbeat for impact, then switch to sparse/double-stop voicings for the rest of the measure to create 'float' and dynamic contrast.", evidence: "hit all of them on the down beat... rest of the measure only have a couple notes", needs_visual_context: false, review_id: "chunk_0012:funk_signature:010", chunk_id: "chunk_0012", page_hint: "cory wong绝招.2 downstroke double stop", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "technique:helicopter_hand_sweep"})
MATCH (target:KGNode {id: "feature:muted_chuck_density"})
MERGE (source)-[r:CAN_INSPIRE {review_id: "chunk_0012:funk_signature:011"}]->(target)
SET r += { knowledge_type: "GuitarIdiom", confidence: 0.8, context_condition: "Adding percussive texture over a static or simple harmonic background.", review_note: "Combine a consistent right-hand sweeping motion with selective left-hand fretting/muting to generate 'chucks' (percussive hits) and accented notes, creating a complex rhythmic surface from simple harmony.", evidence: "full motor sweep... embellishing with extra chucks... holding some notes", needs_visual_context: false, review_id: "chunk_0012:funk_signature:011", chunk_id: "chunk_0012", page_hint: "cory wong绝招.2 downstroke double stop", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };

MATCH (source:KGNode {id: "voicing:triad_pods"})
MATCH (target:KGNode {id: "caution:range_tone_mismatch"})
MERGE (source)-[r:CONFLICTS_WITH {review_id: "chunk_0012:funk_signature:012"}]->(target)
SET r += { knowledge_type: "Caution", confidence: 0.75, context_condition: "Choosing between full barre chords and sparse voicings in a band context.", review_note: "Full 6-string voicings often clash with bass and keys in funk arrangements. Sparse voicings prevent frequency overcrowding and allow the guitar to sit better in the mix.", evidence: "sometimes as your sidestepping it gets dissonant... too much for me... focus on", needs_visual_context: false, review_id: "chunk_0012:funk_signature:012", chunk_id: "chunk_0012", page_hint: "cory wong绝招.2 downstroke double stop", review_decision: "accept", revision_status: "accepted", ingested_at: "2026-05-30T08:40:30.866858+00:00", source_review_file: "data\\processed\\style_rhythm\\cory_wong_funk_review_core\\arrangement_kg_review.all_accept.jsonl" };
