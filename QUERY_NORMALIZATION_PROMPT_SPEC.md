# Query Normalization Prompt & Query Spec

日期：2026-06-09

## 1. 设计目标

前端用户 query 不应直接驱动底层检索规则。用户输入往往是口语化、混合意图、缺少术语边界的，例如：

```text
写一段funk节奏吉他，E调，用9和弦和13和弦，强调16分音符切分，要紧凑的闷音groove
```

这类 query 不适合靠不断扩关键词解决。更合理的结构是：

```text
用户原始 query
  -> Query Normalizer / Planner Agent
  -> 标准化 QueryPlan JSON
  -> RAG tools
  -> Evidence Bundle
  -> Composer Agent
```

当前文档定义第一版 query 规范和 normalizer prompt。它的作用是让 agent 把用户自然语言转换成系统内部稳定可执行的检索任务。

## 2. 总体原则

### 2.1 用户说人话，系统说检索语言

用户可以随便说：

```text
想写一个有点math rock感觉的分解和弦，D调，最好有开放弦，别太难按
```

Normalizer 应转换为：

```text
style: mathrock
task: riff_or_accompaniment_arrangement
key: D
materials: arpeggio, open_string, easy_fingering
retrieval_tools: style_text, fretboard_text, visual_caption, kg
```

### 2.2 不用用户主动说“查 KG”

用户不会说“请调用知识图谱”。只要问题涉及：

- 编配建议
- 风格迁移
- riff / rhythm / voicing 设计
- 技法选择
- 风格约束
- “怎么写”“怎么编”“适合什么”

就应触发 KG。

### 2.3 不用用户主动说“查视觉库”

只要问题需要：

- 指型
- 把位
- 按法
- voicing
- 和弦图
- 音阶图
- 同把位映射
- 高把位 / 低把位
- 省略音 / 构成音排列

就应触发 visual caption。

### 2.4 练习编号不是正式用户入口

练习题 query 只用于视觉 caption 回归测试。正式用户 query 应被规范化为编曲问题：

```text
练习15答案里D大调指型1对应哪个小调指型
```

可以规范化为：

```text
D大调旋律想借用关系小调色彩时，检索同把位大小调指型映射。
```

## 3. QueryPlan JSON Schema

Normalizer 输出必须是 JSON，不输出自然语言解释。

```json
{
  "raw_query": "",
  "normalized_query": "",
  "intent": "",
  "confidence": 0.0,
  "style_hints": [],
  "key_or_tonality": "",
  "target_tuning": "standard",
  "meter_or_rhythm": "",
  "tempo_hint": "",
  "harmonic_materials": [],
  "melodic_materials": [],
  "techniques": [],
  "fretboard_constraints": [],
  "arrangement_goals": [],
  "retrieval_plan": {
    "fretboard_text": {
      "enabled": false,
      "query": "",
      "reason": ""
    },
    "style_text": {
      "enabled": false,
      "query": "",
      "reason": ""
    },
    "visual_caption": {
      "enabled": false,
      "query": "",
      "reason": ""
    },
    "kg": {
      "enabled": false,
      "query": "",
      "reason": ""
    }
  },
  "composer_intent": {
    "answer_type": "",
    "must_include": [],
    "avoid": [],
    "uncertainty_notes": []
  },
  "eval_tags": []
}
```

## 4. Intent 枚举

第一版 intent 建议固定为以下类型：

```text
style_arrangement
  风格编配建议，例如 funk / mathrock / blues 的节奏、riff、伴奏写法。

fretboard_voicing
  指板、voicing、和弦构成、把位选择。

visual_shape_recommendation
  明确需要图形证据、指型图、和弦图、音阶图。

rhythm_riff_design
  以 rhythm / riff / groove / meter 为核心。

harmonic_reharmonization
  和声替代、延伸和弦、借用和弦、调式色彩。

mixed_arrangement
  同时需要风格文本、指板文本、视觉证据和 KG。

score_analysis_followup
  后续 GP5 / MIDI / 音频分析结果驱动的问题。

caption_regression_test
  内部测试用，用户正式入口不应优先使用。
```

## 5. 工具选择规则

### 5.1 `fretboard_text`

启用条件：

- 用户问音阶、和弦、琶音、指板、根音、音程、调式、voicing。
- 用户需要解释构成音、理论定义、把位逻辑。

检索 query 应包含：

```text
调性 / 和弦 / 音阶 / 琶音 / 指型 / 构成音 / 把位限制
```

### 5.2 `style_text`

启用条件：

- 用户明确风格：funk、math rock、midwest emo、blues、jazz、metal 等。
- 用户问 groove、riff、comping、rhythm guitar、开放弦织体、tapping 等风格语言。

检索 query 应包含：

```text
style + rhythm / riff / voicing / groove / arrangement role
```

### 5.3 `visual_caption`

启用条件：

- 需要具体指型、和弦图、音阶图、把位、同把位映射、按法。
- 用户说“图示”“参考”“指型”“高把位”“低把位”“voicing”“省略音”。

检索 query 应包含：

```text
root / quality / mode / scale / chord / position / shape / intervals / visual evidence
```

注意：

- visual caption 是图形证据，不是风格证据。
- 如果 query 只是问风格概念，不必强制 visual。
- visual caption 必须受 `target_tuning` 约束。用户未指定调弦时默认 `standard`；用户指定 FACGCE/DADGAD/Drop D/开放调弦时，视觉证据必须优先匹配对应 tuning。

### 5.3.1 `target_tuning`

`target_tuning` 是必填槽位，不允许省略。

默认规则：

```text
用户没有指定调弦 -> target_tuning=standard
```

显式调弦规则：

```text
FACGCE -> target_tuning=facgce
DADGAD -> target_tuning=dadgad
Drop D -> target_tuning=drop_d
Drop/降弦但不明确具体类型 -> target_tuning=drop
开放调弦/open tuning -> target_tuning=open
```

约束规则：

```text
canonical_terms 必须包含 tuning:target_tuning
required_terms 必须包含 tuning:target_tuning
```

例：

```json
{
  "target_tuning": "facgce",
  "canonical_terms": ["tuning:facgce", "key:g_major", "technique:riff"],
  "required_terms": ["tuning:facgce", "key:g_major"]
}
```

### 5.4 `kg`

启用条件：

- 用户要求编配建议、风格迁移、技法选择、riff 发展、适用条件、限制、避坑。
- 用户输入包含“写、编、怎么、如何、适合、推荐、发展、改写、生成”等任务词。
- 后续 GP5 分析结果进入系统时，默认启用 KG。

检索 query 应包含：

```text
style + technique + harmony + arrangement goal + constraint
```

## 6. Normalizer System Prompt

```text
你是 Guitar Arrangement Inspiration Agent 的 Query Normalizer。

你的任务不是回答用户问题，而是把用户自然语言 query 转换成系统内部稳定可执行的 QueryPlan JSON。

系统有四类检索工具：
1. fretboard_text：吉他指板、音阶、和弦、琶音、调式、voicing 的教材文本。
2. style_text：funk、math rock、midwest emo 等风格课程文本。
3. visual_caption：指板图、和弦图、音阶图、练习答案图的结构化 caption。它用于具体指型/把位/voicing 图证据。
4. kg：Neo4j 知识图谱，包含技法关系、风格迁移、编配启发、约束、注意事项。

重要规则：
- 用户 query 面向吉他编曲用户，不面向教材练习编号。
- 如果用户问“怎么写、怎么编、如何安排、推荐、适合、发展成某风格”，通常需要 kg。
- 如果用户问具体指型、voicing、把位、和弦图、音阶图、同把位映射，通常需要 visual_caption。
- 如果用户提到风格，通常需要 style_text。
- 如果用户提到音阶、和弦、琶音、根音、音程、调式、指板，通常需要 fretboard_text。
- 每次都必须输出 target_tuning。用户没有明确指定调弦时，target_tuning="standard"。
- 如果用户明确指定 FACGCE、DADGAD、Drop D、开放调弦、特殊调弦等，target_tuning 必须写对应稳定小写标签，并把 tuning:xxx 同时写入 canonical_terms 和 required_terms。
- 用户没有明确提到 DADGAD、FACGCE、开放调弦、drop tuning、特殊调弦时，target_tuning="standard"，allow_alternate_tuning=false，并把 tuning:standard 写入 canonical_terms 和 required_terms。
- 练习编号 query 只作为 caption_regression_test；正式产品中应把它改写为编曲语义。

只输出 JSON，不要输出 Markdown，不要解释。
如果信息不足，也要输出最合理的计划，并在 uncertainty_notes 里说明缺口。
```

## 7. Normalizer User Prompt Template

```text
请将下面用户 query 标准化为 QueryPlan JSON。

用户 query：
{{USER_QUERY}}

可选上下文：
{{CONTEXT_JSON}}

输出要求：
- 必须是合法 JSON。
- normalized_query 要适合直接用于 RAG 检索。
- retrieval_plan 中每个工具都要给 enabled、query、reason。
- 如果需要图形证据，visual_caption.enabled=true。
- 如果是编曲建议或风格迁移，kg.enabled=true。
- 不要回答用户问题。
```

## 8. 示例

### 8.1 Funk rhythm guitar

输入：

```text
写一段funk节奏吉他，E调，用9和弦和13和弦，强调16分音符切分，要紧凑的闷音groove
```

输出：

```json
{
  "raw_query": "写一段funk节奏吉他，E调，用9和弦和13和弦，强调16分音符切分，要紧凑的闷音groove",
  "normalized_query": "E调 funk rhythm guitar 编配：使用9和弦、13和弦、16分音符切分、muted groove，寻找节奏型、voicing和编配建议。",
  "intent": "mixed_arrangement",
  "confidence": 0.9,
  "style_hints": ["funk"],
  "key_or_tonality": "E",
  "meter_or_rhythm": "16分音符切分",
  "tempo_hint": "",
  "harmonic_materials": ["9 chord", "13 chord"],
  "melodic_materials": [],
  "techniques": ["muted groove", "syncopation", "rhythm guitar"],
  "fretboard_constraints": ["紧凑voicing"],
  "arrangement_goals": ["写一段funk节奏吉他", "保持紧凑闷音groove"],
  "retrieval_plan": {
    "fretboard_text": {
      "enabled": true,
      "query": "E调 9和弦 13和弦 funk rhythm guitar 紧凑 voicing 指板",
      "reason": "需要和弦构成与voicing指板证据"
    },
    "style_text": {
      "enabled": true,
      "query": "funk rhythm guitar 16th syncopation muted groove comping",
      "reason": "需要funk节奏吉他风格语言"
    },
    "visual_caption": {
      "enabled": true,
      "query": "E 9 chord 13 chord compact voicing guitar chord shape visual",
      "reason": "用户需要紧凑和弦排列，适合召回voicing图证据"
    },
    "kg": {
      "enabled": true,
      "query": "funk muted groove syncopation 9 chord 13 chord rhythm guitar arrangement relation",
      "reason": "用户要求写一段编配，需要技法关系与编配启发"
    }
  },
  "composer_intent": {
    "answer_type": "arrangement_suggestion",
    "must_include": ["节奏安排", "voicing选择", "右手闷音/ghost note处理", "证据引用"],
    "avoid": ["只讲泛泛乐理", "不引用证据"],
    "uncertainty_notes": []
  },
  "eval_tags": ["funk", "rhythm", "voicing", "kg_required", "visual_recommended"]
}
```

### 8.2 Math rock open string riff

输入：

```text
Math rock riff，E调，用开放弦和tapping，7/8拍，需要高把位指型参考
```

输出：

```json
{
  "raw_query": "Math rock riff，E调，用开放弦和tapping，7/8拍，需要高把位指型参考",
  "normalized_query": "E调 math rock riff 编配：7/8拍，结合开放弦、tapping和高把位指型，寻找riff写法、指型证据和风格关系。",
  "intent": "mixed_arrangement",
  "confidence": 0.92,
  "style_hints": ["mathrock"],
  "key_or_tonality": "E",
  "meter_or_rhythm": "7/8",
  "tempo_hint": "",
  "harmonic_materials": [],
  "melodic_materials": ["riff"],
  "techniques": ["open string", "tapping"],
  "fretboard_constraints": ["高把位指型"],
  "arrangement_goals": ["math rock riff writing"],
  "retrieval_plan": {
    "fretboard_text": {
      "enabled": true,
      "query": "E调 高把位 指型 riff 开放弦 tapping 指板",
      "reason": "需要把位与指型文本证据"
    },
    "style_text": {
      "enabled": true,
      "query": "math rock riff open string tapping odd meter 7/8",
      "reason": "需要math rock风格语言"
    },
    "visual_caption": {
      "enabled": true,
      "query": "E high position fretboard shape open string tapping riff visual",
      "reason": "用户明确需要高把位指型参考"
    },
    "kg": {
      "enabled": true,
      "query": "math rock open string tapping 7/8 riff arrangement technique relation",
      "reason": "需要开放弦、tapping、奇数拍之间的技法关系"
    }
  },
  "composer_intent": {
    "answer_type": "riff_design",
    "must_include": ["7/8节奏组织", "开放弦处理", "tapping使用位置", "高把位指型证据"],
    "avoid": ["把math rock泛化成普通摇滚"],
    "uncertainty_notes": []
  },
  "eval_tags": ["mathrock", "riff", "odd_meter", "visual_required", "kg_required"]
}
```

### 8.3 Relation minor mapping

输入：

```text
D 大调旋律想转成 B 小调色彩时，有没有同把位指型可以参考？
```

输出：

```json
{
  "raw_query": "D 大调旋律想转成 B 小调色彩时，有没有同把位指型可以参考？",
  "normalized_query": "D大调到B小调关系调色彩转换：检索同把位大小调指型映射、关系大小调解释和可视化指型证据。",
  "intent": "visual_shape_recommendation",
  "confidence": 0.88,
  "style_hints": [],
  "key_or_tonality": "D major / B minor",
  "meter_or_rhythm": "",
  "tempo_hint": "",
  "harmonic_materials": ["relative major minor"],
  "melodic_materials": ["D major melody", "B minor color"],
  "techniques": [],
  "fretboard_constraints": ["同把位指型映射"],
  "arrangement_goals": ["关系大小调色彩转换"],
  "retrieval_plan": {
    "fretboard_text": {
      "enabled": true,
      "query": "D大调 B小调 关系大小调 同把位 指型 映射",
      "reason": "需要关系大小调和指型理论解释"
    },
    "style_text": {
      "enabled": false,
      "query": "",
      "reason": "未指定风格"
    },
    "visual_caption": {
      "enabled": true,
      "query": "D major B minor relative scale same position fingering shape visual",
      "reason": "用户明确需要同把位指型参考"
    },
    "kg": {
      "enabled": true,
      "query": "relative major minor same position fingering mapping arrangement relation",
      "reason": "需要关系调映射对编曲色彩的启发"
    }
  },
  "composer_intent": {
    "answer_type": "fretboard_visual_recommendation",
    "must_include": ["关系大小调解释", "同把位指型证据", "如何用于旋律改写"],
    "avoid": ["只给抽象乐理不落指板"],
    "uncertainty_notes": []
  },
  "eval_tags": ["relative_minor", "visual_required", "fretboard", "kg_recommended"]
}
```

## 9. 前端采集规范

前端人工 query 采集时，建议额外保存以下字段：

```json
{
  "raw_query": "",
  "user_notes": "",
  "human_expected_tools": [],
  "human_expected_style": [],
  "human_expected_visual": false,
  "human_expected_kg": false,
  "evaluation_bucket": "",
  "accepted_result": null
}
```

用途：

- 后续评测 query normalizer。
- 构造 LoRA 微调数据。
- 判断 agent tool planning 是否正确。

## 10. 后续接入建议

### 10.1 第一阶段：LLM Normalizer

先用已配置的大模型 API 做 query normalizer。

流程：

```text
POST /api/query/run
  -> normalize_query(raw_query)
  -> QueryPlan JSON
  -> run_bundle_by_plan(QueryPlan)
  -> evidence bundle
```

优点：

- 不需要继续堆规则。
- 可以快速验证 prompt 是否稳定。
- 前端用户 query 可以更自然。

### 10.2 第二阶段：评测 query normalizer

从前端收集 50 到 100 条 query，人工标注 expected tools：

```text
fretboard_text
style_text
visual_caption
kg
```

评测：

```text
intent accuracy
tool selection precision / recall
style extraction accuracy
visual required recall
kg required recall
```

### 10.3 第三阶段：小模型微调

将 query normalizer 拆成两个小任务：

```text
Query Intent Classifier
KG Entity Linker
```

训练数据来自：

```text
raw_query -> QueryPlan JSON
raw_query -> entity ids / style / tools
```

这比让小模型直接生成编曲回答更稳，也更适合项目展示。

## 11. 与现有规则层的关系

现有规则层不需要废掉，可以降级为 fallback：

```text
优先：
  LLM Query Normalizer 输出 QueryPlan

失败时：
  规则层 analyze_query / plan_retrieval
```

也可以让规则层做 sanity check：

```text
如果 Normalizer 输出 visual_caption=false，但 query 包含“指型/图/把位/voicing”，给出 warning。
如果 Normalizer 输出 kg=false，但 query 包含“编/写/怎么/推荐”，给出 warning。
```

这样比每次改代码扩关键词更稳。
