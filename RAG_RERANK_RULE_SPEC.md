# RAG Rerank Rule Spec

本文档定义当前吉他编曲 Agentic RAG 的领域 rerank 规则。目标是在接入独立 rerank 模型前，先稳定“候选证据如何被筛选、降权、升权”的项目语义边界。

## 1. 总体原则

RAG 的排序分为四层：

1. Query Normalizer 将用户输入转换为结构化 QueryPlan。
2. Chroma / Neo4j 根据各自工具 query 召回较大的候选池。
3. Domain Rerank 根据乐理、风格、指板和工具边界重排候选。
4. Evidence Selector 从候选池中选出少量证据交给最终回答生成器。

Rerank 的核心原则：

- 用户明确指定的条件优先于语义相似度。
- 未被用户指定的特殊条件只能作为可选扩展，不应进入主答案证据顶部。
- 视觉证据必须服务于具体指型、把位、voicing、音阶图或和弦图需求。
- KG 证据必须服务于编配逻辑、风格迁移、技法关系或创作启发，不应替代具体图示。
- top5/top8 是候选池，不是最终答案内容。

## 2. QueryPlan 需要提供的约束字段

后续 Query Normalizer 应尽量补充以下字段：

```json
{
  "target_keys": [],
  "target_roots": [],
  "chord_qualities": [],
  "scale_or_mode": [],
  "meter_or_rhythm": "",
  "style_hints": [],
  "techniques": [],
  "fret_region": "",
  "position_constraints": [],
  "requires_exact_key": false,
  "requires_exact_chord": false,
  "visual_evidence_required": false,
  "allow_alternate_tuning": false,
  "allow_exercise_reference": true
}
```

字段含义：

- `target_keys`: 例如 `G minor`, `D major`, `B minor`。
- `target_roots`: 例如 `C`, `Ab`, `E`。
- `chord_qualities`: 例如 `7#9`, `7b9`, `m11`, `maj9#11`。
- `scale_or_mode`: 例如 `natural minor`, `major scale`, `dorian`。
- `fret_region`: `low`, `middle`, `high`。
- `requires_exact_key`: 用户明确指定调性、同把位映射、相对大小调时为 true。
- `requires_exact_chord`: 用户明确指定和弦性质或扩展音时为 true。
- `visual_evidence_required`: 用户要求图示、指型、把位、排列、voicing 图时为 true。
- `allow_alternate_tuning`: 只有用户提到 DADGAD、特殊调弦、drop tuning、开放调弦时为 true。
- `allow_exercise_reference`: 默认 true。未来如果用户明确不要练习题来源，则设 false。

## 3. 工具级路由规则

### 3.1 fretboard_text

启用条件：

- 用户问调式、音阶、和弦构成、指板位置、同把位映射。
- 用户问 voicing 的构成逻辑。
- 用户问具体根音/调性/把位的基础解释。

不应承担：

- 风格性节奏/Riff 的完整编配建议。
- 具体图形答案的唯一来源。

### 3.2 style_text

启用条件：

- 用户指定 funk、math rock、emo、blues、jazz、metal 等风格。
- 用户问 riff、节奏型、groove、风格化伴奏。

不启用条件：

- 只问某调指型、某和弦图、某把位参考。

### 3.3 visual_caption

启用条件：

- 用户出现 `图`、`指型`、`把位`、`排列`、`voicing`、`diagram`、`fingering`。
- 用户问同把位映射、根音位置、和弦图示、音阶图示。
- 用户问 `riff`、`谱例`、`tab`、`节拍`、`拍号`、`groove` 或非常规节拍时，启用节奏谱例视觉召回。

排序要求：

- 明确调性时，精确调性图优先。
- 明确和弦性质时，精确和弦性质优先。
- 明确高/低把位时，对应把位优先。
- 如果只命中同类但不命中调性，应排在精确命中之后。
- 明确问 riff / 谱例 / 节拍时，`tab_excerpt` / `riff_tab` 优先于普通 `chord_diagram` / `scale_pattern`。

### 3.4 kg

启用条件：

- 用户问“怎么编”“适合什么 riff 写法”“如何安排”“如何迁移风格”。
- 用户问题包含多个约束，需要关系型启发。
- 用户问技法之间的组合关系，例如 open string + tapping + odd meter。

不应启用或应弱化：

- 单纯索要静态指型图。
- 单纯查某个和弦构成音。

## 4. 领域加权规则

### 4.1 精确调性

当 `requires_exact_key=true`：

- caption/text/kg 中命中 `target_keys`，强加分。
- 命中相对调关系，例如 `D major / B minor`，强加分。
- 只命中同类音阶但不命中指定调性，中性或轻微扣分。
- 命中明显无关调性，扣分。

例：

- Query: `G 小调指型`
- `G minor scale pattern` 应高于 `A natural minor`。
- `C major` 只有在解释关系时可作为辅助，不应排第一。

### 4.2 精确和弦

当 `requires_exact_chord=true`：

- 根音 + 和弦性质同时命中，强加分。
- 只命中根音或只命中和弦性质，中等加分。
- 命中相似扩展和弦，例如 `m11` 查询命中 `m7`，只能作为辅助。

例：

- Query: `Ab m11 / maj9#11 高把位`
- `Abm11`、`Abmaj9#11` 优先。
- `F#m11` 或 `D11` 不能作为主证据，只能作为形状迁移参考。

### 4.3 把位区域

当 `fret_region` 有值：

- caption 中出现高把位、低把位、中把位、具体品位范围，按匹配程度加分。
- 与用户要求相反的把位扣分。

### 4.4 风格匹配

当 `style_hints` 有值：

- 对应风格教材来源加分。
- KG 中 style、technique、heuristic 与风格匹配加分。
- 非目标风格但可迁移的证据保留，但不得压过目标风格证据。

### 4.5 技法匹配

当 `techniques` 有值：

- 同时命中多个技法的证据加分。
- 只命中泛化概念，例如 `riff`、`voicing`，轻微加分。
- 与技法冲突的证据扣分。

例：

- Query: `open string + tapping + 7/8 math rock riff`
- 同时出现 open string、tapping、odd meter、math rock 的证据优先。

## 5. 特殊调弦边界

默认：

```json
"allow_alternate_tuning": false
```

当用户没有明确提到以下内容时，特殊调弦节点应降权：

- DADGAD
- open tuning
- alternate tuning
- drop tuning
- 特殊调弦
- 开放调弦
- 降弦

如果 query 中没有特殊调弦意图：

- `tuning:*` KG 节点不得作为 top1 主证据。
- 可作为“可选扩展”出现在后置建议。

如果 query 中明确需要开放弦，但没有说特殊调弦：

- 可以推荐标准调弦下的开放弦用法。
- DADGAD 只能作为可选路径。

## 6. 练习图与视觉证据边界

练习答案 caption 可以作为编曲系统的视觉证据层，但排序时要遵守：

- 用户问具体指型、和弦图、音阶图时，可以召回练习答案图。
- 用户没有问练习题时，不应在最终回答中强调“练习第几题”，而应转写为“可视化指型参考”。
- 练习号只作为 provenance，不作为回答主体。
- 如果图中 caption 只能说明题号，不能说明乐理内容，应降权。

## 7. 节奏谱例视觉召回策略

节奏、拍号、riff、谱例类 query 使用独立视觉策略。完整规范见：

```text
RHYTHMIC_VISUAL_RETRIEVAL_POLICY.md
```

触发条件：

- query 包含 `riff`、`谱例`、`tab`、`节拍`、`拍号`、`节奏型`、`groove`；
- query 包含具体拍号，例如 `6/8`、`9/8`、`5/8`、`7/8`；
- query 包含 `odd meter`、`irregular meter`、`polymeter`、`metric modulation` 等节奏概念。

Query 侧抽取：

```text
6/8 -> meter:6_8
9/8 -> meter:9_8
```

视觉侧优先 required / optional terms：

```text
visual_type:tab_excerpt
visual_subtype:riff_tab
technique:riff
concept:riff_composition
style:math_rock   # 当 query 明确为数摇 / math rock 时
meter:6_8
meter:9_8
```

边界：

- `I-IV` 只作为和声框架，不应让 `chord_quality:maj` 抢占谱例图。
- 当用户问 riff / 谱例 / 节拍时，普通和弦图、音阶图和指板图应排在具体 tab/riff 图之后。
- 调弦仍是硬边界：未指定特殊调弦时默认 `tuning:standard`。

已验证样例：

```text
query: 给我一个6/8转9/8的I-IV数摇riff
top1: visual_caption:mr_style_015
matched: meter:6_8, meter:9_8, style:math_rock, tuning:standard, visual_type:tab_excerpt
```

## 8. 建议评分公式

在没有模型 rerank 时：

```text
final_score =
  0.55 * vector_score
+ 0.25 * domain_constraint_score
+ 0.10 * source_priority_score
+ 0.10 * lexical_overlap_score
```

接入 rerank 模型后：

```text
final_score =
  0.55 * model_rerank_score
+ 0.25 * domain_constraint_score
+ 0.10 * vector_score
+ 0.10 * source_priority_score
```

说明：

- `model_rerank_score` 负责语义相关性。
- `domain_constraint_score` 负责音乐硬条件和项目边界。
- `vector_score` 保留原始召回信号。
- `source_priority_score` 保证风格教材、指板教材、视觉层在各自场景下被合理使用。

## 9. Evidence Selector 规则

最终回答前，应从 rerank 后候选池中选择证据：

- 简单指型查询：`fretboard_text` 1-2 条，`visual_caption` 1-3 条，通常不需要 KG。
- 风格编配查询：`style_text` 1-3 条，`kg` 1-3 条，必要时 `visual_caption` 1-2 条。
- 和弦 voicing 查询：`fretboard_text` 1-2 条，`visual_caption` 1-3 条，KG 0-2 条。
- 复杂约束查询：每类最多 3 条，总证据不超过 8 条。

选择优先级：

1. 满足用户硬条件。
2. 能直接支持回答策略。
3. 来源互补，避免同一类证据重复堆叠。
4. 保留可追溯路径，包括 source、chunk、caption/image path、KG edge。

## 10. 近期测试暴露的问题对应规则

### G 小调指型

问题：正确图片在第 4 条。

规则修正：

- `requires_exact_key=true`
- `target_keys=["G minor"]`
- G minor caption 强加分。
- 非 G minor 音阶图降权。

### D 大调转 B 小调色彩

问题：KG top1 召回 DADGAD。

规则修正：

- `allow_alternate_tuning=false`
- DADGAD 节点降权。
- 相对大小调、同把位、riff phrasing 相关节点加权。

### Ab m11 / maj9#11 高把位

问题：视觉图可能命中同类扩展和弦，但不命中 Ab。

规则修正：

- `requires_exact_chord=true`
- `target_roots=["Ab"]`
- `chord_qualities=["m11", "maj9#11"]`
- 只命中 m11 但不命中 Ab 时只能作为迁移参考。

### Funk C7#9 / C7b9 低把位

规则要求：

- C 根音 + dominant altered chord 优先。
- 低把位优先。
- KG 中 `leave_space_for_band`、`sparse_funk_voicing`、`percussive_ghost_note` 加权。

### Math Rock 6/8 -> 9/8 I-IV riff

问题：QueryPlan 将 `I-IV` 泛化为 `chord_quality:maj`，导致普通 C 大三和弦图抢占视觉 Top1。

规则修正：

- 节拍 / riff / 谱例 query 优先 `visual_type:tab_excerpt`。
- 抽取 `meter:6_8`、`meter:9_8`。
- 明确数摇时加入 `style:math_rock`。
- `chord_quality:maj` 在该场景下只保留为弱信号，不进入 required terms。

## 11. 实施顺序

1. 扩展 QueryPlan schema，增加硬约束字段。
2. 在 `query_rag_bundle.py` 中实现 domain constraint scoring。
3. 将 Chroma 每路召回候选池扩大到 top 20-30，最终展示仍保留 top 5。
4. 增加 Evidence Selector，避免直接把 top5/top8 交给回答器。
5. 积累人工反馈 30-50 条后，再接本地 rerank 模型做 A/B 测试。
