# Query RAG Bundle Report

- Query: funk十六分切分节奏怎么让riff更有groove
- Intent: `style_arrangement`
- Sufficient: `True`
- Confidence: 0.71
- Total latency: 6.891s

## Query Analysis

```json
{
  "query": "funk十六分切分节奏怎么让riff更有groove",
  "intent": "style_arrangement",
  "style_hints": [
    "funk"
  ],
  "theory_terms": [],
  "technique_terms": [
    "groove",
    "riff",
    "切分"
  ],
  "needs_fretboard_text": false,
  "needs_visual": false,
  "needs_style_text": true,
  "needs_kg": true,
  "confidence": 0.7,
  "matched_rules": [
    "style_or_technique_terms",
    "arrangement_or_relation_terms"
  ]
}
```

## Retrieval Plan

| Name | Backend | Collection | TopK | Reason | Query |
|---|---|---|---:|---|---|
| `style_text` | `chroma` | `guitar_text_chunks_qwen3_06b` | 5 | 风格/riff/节奏/技法文本证据 | funk十六分切分节奏怎么让riff更有groove funk |
| `kg` | `neo4j_or_file` | `` | 8 | 技法关系/风格迁移/编配启发 | funk十六分切分节奏怎么让riff更有groove funk groove riff 切分 |

## Text Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `text:chunk_0011` | `cory_wong_funk_core` | 0.7592 | Cory Wong Funk 吉他大师课 | one of the signature moves that I have is hitting the strings.now that sounds a little bit weird on its own,why would I just hit the strings,but what it does is it helps me accomplish some of my signature moves,both in the ribbon guitar realm and lead ribbon ... |
| 2 | `text:chunk_0009` | `cory_wong_funk_core` | 0.7313 | Cory Wong Funk 吉他大师课 | now something to really note is.there's a difference between timing.patterns.and groove.they all kind of make up this thing that we call ribbon.那timing is。where you're placing something.right? the timing is a hundred and twenty bpm or whatever,and that's the ... |
| 3 | `text:chunk_0008` | `cory_wong_funk_core` | 0.7300 | Cory Wong Funk 吉他大师课 | let's dive deeper into that bongo conga style to me,that world of ribbon guitar playing is the bubble. now you hear this sort of thing on a lot of songs,it's classic.billy IE,Jean,you hear it on?a lot of other songs that I'm not going to play for you now caus... |
| 4 | `text:chunk_0007` | `mathrock_text_course` | 0.7091 | mathrock教学课 | we'll find more vents,one there.using some cool ideas of how we take an alternate tuning in an open minor or major court with some extensions,we might have thirteen and how we.can mix up the ribbon, here's simple movable core shapes,all right? thinking about ... |
| 5 | `text:chunk_0005` | `mathrock_text_course` | 0.7072 | mathrock教学课 | we're already going to sit for this mad Rock midwest emo progression. we're going to look at this special shooting right here,it's going to be a drop bf sharp,we're going to have AC sharp right there and e. ,so we have the fifth right here in AB,and then we h... |

## Visual Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| - | - | - | - | - | - |

## KG Evidence

| Rank | Evidence ID | Source | Score | Title | Preview |
|---:|---|---|---:|---|---|
| 1 | `kg:technique:upstroke_hit_downstroke:ENABLES:feature:percussive_ghost_note` | `GuitarIdiom` | 1.6100 | technique:upstroke_hit_downstroke -[ENABLES]-> feature:percussive_ghost_note | technique:upstroke_hit_downstroke -[ENABLES]-> feature:percussive_ghost_note Funk/R&B rhythm guitar comping requiring tight, percussive groove without full chord sustain. The core mechanic is a three-part right-hand motion: Upstroke -> Muted String Hit (Ghost... |
| 2 | `kg:voicing:sparse_funk_voicing:SUGGESTS:heuristic:leave_space_for_band` | `GuitarIdiom` | 1.4500 | voicing:sparse_funk_voicing -[SUGGESTS]-> heuristic:leave_space_for_band | voicing:sparse_funk_voicing -[SUGGESTS]-> heuristic:leave_space_for_band Comping with 'chucks' (muted strums) in a dense band arrangement. Focus on 2-3 string voicings (e.g., minor 7th shapes) and vary the ratio of notes to muted 'chucks' to avoid frequency c... |
| 3 | `kg:heuristic:make_rhythm_part_a_hook:EVOKES:task:riff_writing` | `GuitarIdiom` | 1.4500 | heuristic:make_rhythm_part_a_hook -[EVOKES]-> task:riff_writing | heuristic:make_rhythm_part_a_hook -[EVOKES]-> task:riff_writing Funk/Pop rhythm guitar comping where static strumming feels generic. Transform standard chord comping into a signature hook by integrating melodic lines (pentatonic/scale) within the chord shape,... |
| 4 | `kg:feature:staccato_bubble:ENABLES:heuristic:make_rhythm_part_a_hook` | `GuitarIdiom` | 1.4000 | feature:staccato_bubble -[ENABLES]-> heuristic:make_rhythm_part_a_hook | feature:staccato_bubble -[ENABLES]-> heuristic:make_rhythm_part_a_hook Funk/R&B rhythm guitar parts requiring melodic identity within the groove. Bubble parts (staccato single notes/ostinatos) should be constructed as distinct phrases or counter-melodies rath... |
| 5 | `kg:technique:downstroke_double_stop:ENABLES:color:driving_rimshot_quality` | `GuitarIdiom` | 1.3700 | technique:downstroke_double_stop -[ENABLES]-> color:driving_rimshot_quality | technique:downstroke_double_stop -[ENABLES]-> color:driving_rimshot_quality Funk/R&B rhythm guitar requiring aggressive, consistent attack without dynamic fluctuation from alternate picking. Strict all-downstroke picking on double stops ensures uniform accent... |
| 6 | `kg:task:rhythm_guitar_arrangement:EVOKES:heuristic:guitar_as_percussion` | `GuitarIdiom` | 1.3700 | task:rhythm_guitar_arrangement -[EVOKES]-> heuristic:guitar_as_percussion | task:rhythm_guitar_arrangement -[EVOKES]-> heuristic:guitar_as_percussion Treating the guitar as a pitched percussion instrument (tambourine/shaker/bongos) within the rhythm section. The guitar should weave in and out of the bass/drum foundation. It acts as a... |
| 7 | `kg:technique:right_hand_constant_motion:ENABLES:feature:sixteenth_note_undercurrent` | `GuitarIdiom` | 1.3700 | technique:right_hand_constant_motion -[ENABLES]-> feature:sixteenth_note_underc... | technique:right_hand_constant_motion -[ENABLES]-> feature:sixteenth_note_undercurrent Maintaining a consistent funk groove regardless of note density. The right hand maintains constant 16th-note motion (motor); articulation is controlled by left-hand fretting... |
| 8 | `kg:task:rhythm_guitar_arrangement:SUGGESTS:heuristic:make_rhythm_part_a_hook` | `GuitarIdiom` | 1.3700 | task:rhythm_guitar_arrangement -[SUGGESTS]-> heuristic:make_rhythm_part_a_hook | task:rhythm_guitar_arrangement -[SUGGESTS]-> heuristic:make_rhythm_part_a_hook When composing rhythm guitar parts for pop/funk/R&B tracks where the guitar needs to define the song's identity. The primary goal is to create a rhythm part that functions as an in... |

## Bundle Judgement

```json
{
  "sufficient": true,
  "confidence": 0.71,
  "missing": [],
  "warnings": [],
  "evidence_type_count": 2,
  "text_count": 5,
  "visual_count": 0,
  "kg_count": 8,
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
    "text:chunk_0011",
    "text:chunk_0009",
    "text:chunk_0008"
  ],
  "top_visual_ids": [],
  "top_kg_ids": [
    "kg:technique:upstroke_hit_downstroke:ENABLES:feature:percussive_ghost_note",
    "kg:voicing:sparse_funk_voicing:SUGGESTS:heuristic:leave_space_for_band",
    "kg:heuristic:make_rhythm_part_a_hook:EVOKES:task:riff_writing",
    "kg:feature:staccato_bubble:ENABLES:heuristic:make_rhythm_part_a_hook",
    "kg:technique:downstroke_double_stop:ENABLES:color:driving_rimshot_quality"
  ],
  "composer_instruction": "只能基于 evidence_id 引用证据；区分教材明确内容与系统推断；如果 judgement.missing 非空，需要先说明证据不足。"
}
```

## Timings

```json
{
  "model_load_seconds": 6.049373300003936,
  "style_text_seconds": 0.332453400013037,
  "kg_seconds": 0.4519570999982534,
  "total_seconds": 6.890636700001778,
  "kg_status": "neo4j"
}
```
