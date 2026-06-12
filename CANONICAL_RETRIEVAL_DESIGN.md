# Canonical Retrieval Design

本文档固定吉他编曲 Agentic RAG 的“乐理标准术语层”设计。目标是解决中文、英文、符号化乐理表达不一致导致的召回和 rerank 不稳定问题。

## 1. 设计动机

当前系统已经具备：

- `fretboard_text`：指板/乐理教材文本召回
- `style_text`：风格、节奏、riff 教材文本召回
- `visual_caption`：视觉 caption 文本召回
- `kg`：Neo4j 知识图谱召回
- `domain_rerank`：领域规则重排序

但仍有一个关键问题：

```text
用户 query: G minor 指型
caption: G小调指型图
```

两者语义相同，但字符串不同。如果只靠 embedding 或普通字符串匹配，正确结果可能排不进 top1/top3。

因此新增一层 canonical music terms：

```text
G minor / G小调 / Gm
-> key:g_minor
```

然后用标准术语做精确对照。

## 2. 总体架构

```text
用户 query
  -> LLM Query Normalizer
  -> query canonical_terms
  -> 多路召回
      1. vector retrieval: fretboard_text / style_text / visual_caption
      2. graph retrieval: Neo4j KG
      3. canonical retrieval: 标准术语精确对照
  -> merge candidates
  -> domain rerank
  -> Evidence Selector
  -> Answer Composer
```

离线知识处理：

```text
现有 caption 文字
  -> Caption Canonical Extractor
  -> canonical_terms sidecar
  -> 在线 canonical retrieval 使用
```

注意：

- 不需要重跑图片 VLM。
- 不直接覆盖原始 caption。
- 先用 sidecar 旁路文件验证。
- 验证稳定后再考虑写回 Chroma metadata。

## 3. 关键分工

### 3.1 Query Normalizer

中文名：查询规范化器

职责：

- 理解用户自然语言 query。
- 判断用户意图。
- 选择检索工具。
- 生成每个工具的检索 query。
- 输出 query 侧 canonical terms。

示例：

```text
用户 query:
给我 G 小调高把位指型参考
```

输出：

```json
{
  "intent": "visual_shape_recommendation",
  "canonical_terms": [
    "key:g_minor",
    "visual_type:scale_pattern",
    "fret_region:high"
  ],
  "required_terms": [
    "key:g_minor",
    "visual_type:scale_pattern"
  ],
  "optional_terms": [
    "fret_region:high"
  ],
  "negative_constraints": [
    "tuning:dadgad",
    "tuning:drop",
    "tuning:open"
  ],
  "visual_evidence_required": true,
  "allow_alternate_tuning": false
}
```

### 3.2 Caption Canonical Extractor

中文名：视觉 caption 标准术语抽取器

职责：

- 离线读取已有视觉 caption 文字。
- 不读取图片，不重跑 VLM。
- 把 caption 中的中文/英文/符号乐理词转成 canonical terms。
- 输出人工可审核的 sidecar。

示例：

```text
caption:
G小调第七把位音阶指型图
```

输出：

```json
{
  "visual_id": "fretboard_answer_E15_3",
  "canonical_terms": [
    "key:g_minor",
    "scale:natural_minor",
    "visual_type:scale_pattern",
    "fret_region:high"
  ],
  "aliases_detected": [
    {
      "surface": "G小调",
      "canonical": "key:g_minor"
    }
  ],
  "confidence": 0.94
}
```

### 3.3 Canonical Retrieval Branch

中文名：标准术语检索分支

职责：

- 用 query canonical terms 精确查 caption/text 的 canonical terms。
- 补足向量召回漏掉的精确目标。
- 将命中结果合并回 visual/text evidence 候选池。

它不是替代 Query Normalizer，而是使用 Query Normalizer 的结果。

```text
Query Normalizer = 翻译器
Canonical Retrieval = 精确对照检索器
```

### 3.4 Domain Rerank

中文名：领域规则重排序

职责：

- 根据乐理和项目边界重排候选。
- 对精确调性、根音、和弦性质、把位、风格、技法加权。
- 对未指定的特殊调弦降权。

示例：

- 用户没说 DADGAD，则 `tuning:dadgad` 不应作为主证据 top1。
- 用户说 G 小调，则 `key:g_minor` 图优先。
- 用户说 high position，则 `fret_region:high` 图优先。

### 3.5 Evidence Selector

中文名：证据选择器

职责：

- 从 rerank 后候选中选择少量证据进入最终回答。
- top5/top8 是候选池，不是最终答案。
- 最终回答通常只需要每类 1-3 条高质量证据。

## 4. 中英文术语对照

| English | 中文 | 项目含义 |
|---|---|---|
| canonical_terms | 标准术语标签 | 系统内部统一乐理表达 |
| canonical term | 标准术语 | 单个标准标签，例如 `key:g_minor` |
| Query Normalizer | 查询规范化器 | 把用户 query 转成 QueryPlan |
| QueryPlan | 查询计划 | 包含意图、工具选择、标准术语、检索 query |
| required_terms | 必须命中术语 | 召回结果最好必须包含的术语 |
| optional_terms | 可选加分术语 | 命中更好，不命中不一定错 |
| negative_constraints | 负向约束 | 不应作为主证据的条件 |
| visual_evidence_required | 需要视觉证据 | 是否必须召回指型图/和弦图 |
| allow_alternate_tuning | 允许特殊调弦 | 是否允许 DADGAD/drop/open tuning 作为主证据 |
| Caption Canonical Extractor | Caption 标准术语抽取器 | 离线把 caption 转成 canonical terms |
| sidecar | 旁路索引文件 | 不改原始数据，额外保存 canonical terms |
| Canonical Retrieval Branch | 标准术语检索分支 | 用 canonical terms 精确查证据 |
| vector retrieval | 向量召回 | 用 embedding 做语义召回 |
| graph retrieval | 图谱召回 | 从 Neo4j KG 查关系证据 |
| domain rerank | 领域重排序 | 用吉他/乐理规则重排候选 |
| Evidence Selector | 证据选择器 | 从候选池挑最终回答证据 |
| Answer Composer | 回答生成器 | 基于证据生成最终分析/建议 |

## 5. Canonical Term 命名约定

### 5.1 调性

```text
key:g_minor
key:d_major
key:bb_major
key:ab_minor
```

示例对照：

| 表达 | canonical |
|---|---|
| G小调 | `key:g_minor` |
| G minor | `key:g_minor` |
| Gm | `key:g_minor` |
| D大调 | `key:d_major` |
| D major | `key:d_major` |
| Bb大调 / B♭ major | `key:bb_major` |

### 5.2 根音

```text
root:g
root:ab
root:c_sharp
```

### 5.3 音阶与调式

```text
scale:natural_minor
scale:major
scale:pentatonic_minor
scale:pentatonic_major
mode:dorian
mode:mixolydian
```

### 5.4 和弦性质

```text
chord_quality:maj7
chord_quality:m7
chord_quality:m11
chord_quality:maj9_sharp11
chord_quality:dominant7_sharp9
chord_quality:dominant7_flat9
```

示例对照：

| 表达 | canonical |
|---|---|
| m11 / 小十一 | `chord_quality:m11` |
| maj9#11 / 大九升十一 | `chord_quality:maj9_sharp11` |
| 7#9 / 属七升九 | `chord_quality:dominant7_sharp9` |
| 7b9 / 属七降九 | `chord_quality:dominant7_flat9` |

### 5.5 视觉类型

```text
visual_type:scale_pattern
visual_type:chord_diagram
visual_type:text_answer
visual_type:fretboard_map
```

### 5.6 把位与指板约束

```text
fret_region:low
fret_region:middle
fret_region:high
fret_range:2-5
fretboard:position_shape
```

### 5.7 技法与编配概念

```text
technique:tapping
technique:open_string
technique:voicing
technique:riff
concept:root_form
concept:caged
concept:relative_major_minor
concept:voice_leading
```

### 5.8 调弦

```text
tuning:standard
tuning:dadgad
tuning:drop
tuning:open
```

默认：

```json
"allow_alternate_tuning": false
```

只有用户明确提到特殊调弦时，`tuning:dadgad`、`tuning:drop`、`tuning:open` 才能作为主证据。

## 6. 数据文件规划

### 6.1 当前 trial 文件

```text
data/processed/fretboard_handbook/question_answer_visual_caption_canonical_trial/
├─ canonical_terms_review.md
├─ canonical_terms_review.jsonl
├─ canonical_terms_report.json
└─ canonical_terms_trial_report.md
```

### 6.2 后续稳定文件

```text
data/processed/fretboard_handbook/question_answer_visual_caption_canonical/
├─ fretboard_answer_visual_caption_canonical_terms.jsonl
├─ canonical_terms_review.md
└─ canonical_terms_report.json
```

### 6.3 推荐 sidecar schema

```json
{
  "visual_id": "fretboard_answer_E15_3",
  "status": "accepted",
  "canonical_terms": [
    "key:g_minor",
    "scale:natural_minor",
    "visual_type:scale_pattern"
  ],
  "required_terms": [],
  "optional_terms": [],
  "aliases_detected": [
    {
      "surface": "G小调",
      "canonical": "key:g_minor"
    }
  ],
  "confidence": 0.94,
  "source_preview": {}
}
```

## 7. 实施顺序

### Phase 1: Query 规范化升级

- 扩展 Query Normalizer 输出：
  - `canonical_terms`
  - `required_terms`
  - `optional_terms`
  - `negative_constraints`
- 前端“只规范化”面板展示这些字段。

当前状态：已完成第一版。

- `scripts/query_normalizer.py` 已输出 canonical terms。
- LLM 输出的非规范标签会再次经过 sanitizer 收敛。
- 示例：

```text
写复杂voicing，Ab调，用m11和maj9#11，高把位，需要排列图示
```

会输出：

```json
{
  "canonical_terms": [
    "root:ab",
    "chord_quality:m11",
    "chord_quality:maj9_sharp11",
    "fret_region:high",
    "visual_type:chord_diagram",
    "technique:voicing"
  ],
  "required_terms": [
    "root:ab",
    "chord_quality:m11",
    "chord_quality:maj9_sharp11",
    "visual_type:chord_diagram"
  ],
  "optional_terms": [
    "fret_region:high"
  ],
  "negative_constraints": [
    "tuning:dadgad",
    "tuning:drop",
    "tuning:open"
  ]
}
```

### Phase 2: Caption canonical sidecar

- 对视觉 caption 文本进行离线 LLM canonical extraction。
- 先批量生成审核 Markdown。
- 人工通过后写入 accepted sidecar。

### Phase 3: Canonical retrieval branch

- 在 `query_rag_bundle.py` 中新增 canonical retrieval。
- 用 query canonical terms 匹配 sidecar canonical terms。
- 命中结果转成 EvidenceItem 并合并到 visual evidence。

### Phase 4: Domain rerank 整合

- canonical overlap 加权。
- required terms 缺失降权。
- negative constraints 命中降权。
- 特殊调弦边界继续保留。

### Phase 5: Evidence Selector

- 从候选池选择最终证据。
- 主证据和可选扩展分开。
- 为 Answer Composer 输出更干净的 evidence bundle。

## 8. 与 Rerank 模型的关系

Canonical retrieval 不替代 rerank 模型。

分工：

```text
canonical retrieval:
  负责精确术语命中，防止正确证据漏召回。

rerank model:
  负责语义相关性重排。

domain rerank:
  负责乐理边界和项目规则。
```

推荐最终分数：

```text
final_score =
  0.45 * model_rerank_score
+ 0.25 * canonical_overlap_score
+ 0.20 * domain_constraint_score
+ 0.10 * vector_score
```

在未接 rerank 模型前：

```text
final_score =
  0.40 * vector_score
+ 0.35 * canonical_overlap_score
+ 0.25 * domain_constraint_score
```

## 9. 当前结论

- 这一路不能替代 Query Normalizer。
- 它依赖 Query Normalizer 输出 canonical terms。
- 它可以替代大量中英硬编码字符串匹配。
- 它能补足 embedding 漏召回的问题。
- 它适合先从视觉 caption 层开始，因为视觉图对调性/和弦/把位精确命中要求最高。
