# 混合视觉库接入报告

## 目标

在不覆盖正式视觉库的前提下，将 9 条 Math Rock 风格视觉 caption 接入前端 RAG 与 Full Chain，支持正式库/混合库 A/B 测试。

## 视觉库

| Profile | Chroma Collection | 数量 | 用途 |
|---|---|---:|---|
| `formal` | `guitar_fretboard_answer_captions_qwen3_06b` | 389 | 正式基础指板视觉召回 |
| `mathrock_mixed_trial` | `guitar_visual_mixed_mathrock_trial_qwen3_06b` | 398 | 389 条正式数据 + 9 条 Math Rock 试验数据 |

正式集合未被修改。混合集合仅用于试验和人工评测。

## 接口变更

`POST /api/query/run` 新增请求字段：

```json
{
  "visual_collection": "formal"
}
```

允许值：

- `formal`
- `mathrock_mixed_trial`

后端通过白名单映射到真实 Chroma collection，不接受前端直接传任意集合名。

返回的 `bundle.visual_collection`、query log 和 session memory 会记录：

- profile
- collection
- label

同一条 query 使用不同视觉库时，报告文件名会带 profile 后缀，避免 A/B 结果相互覆盖。

## 前端变更

以下模块新增 `Visual Library` 选择器：

- Manual Query Collector
- Full Chain Test

Manual Query 默认使用正式库；Full Chain Test 默认使用 Math Rock 混合试验库，方便当前阶段扩大风格视觉测试。

历史 query 会显示当时使用的视觉库，并在点击历史记录时恢复该选项。

## 风格边界规则

风格边界在本地模型 rerank 之后执行，作为最终领域约束。

1. 明确包含 `math rock`、`mathrock`、`数摇`、`数学摇滚` 时，允许并提升 `mathrock_style_visual_caption_v1`。
2. 未明确提出 Math Rock 意图时，Math Rock 视觉证据降权并标记为 `optional_expansion_only`。
3. 查询明确要求标准调弦时：
   - `standard` 调弦视觉证据加分；
   - 明确的非标准调弦证据降权。
4. 查询明确排除点弦、琶音或开放弦时，包含对应技法的视觉证据强降权。
5. 原有调性、和弦性质、canonical terms、把位和调弦规则继续参与最终排序。

## 节奏谱例视觉召回策略

已将 `RHYTHMIC_VISUAL_RETRIEVAL_POLICY.md` 固定为通用策略。该策略用于所有带节拍、riff、谱例、tab 的视觉召回。

触发条件：

- query 包含 `riff`、`谱例`、`tab`、`节拍`、`拍号`、`groove`；
- query 包含具体拍号，例如 `6/8`、`9/8`；
- query 包含 `odd meter`、`irregular meter`、`polymeter`、`metric modulation`。

召回约束：

```text
visual_type:tab_excerpt
visual_subtype:riff_tab
concept:riff_composition
meter:6_8
meter:9_8
style:math_rock   # 明确数摇 / math rock 时
```

边界：

- `I-IV` 不再被当成普通 `chord_quality:maj` 的强视觉 required term。
- 普通 chord diagram / scale pattern 在节奏谱例 query 中降到具体 tab/riff 图之后。
- 调弦仍按 `target_tuning` 作为硬边界。

已验证：

```text
query: 给我一个6/8转9/8的I-IV数摇riff
top1: visual_caption:mr_style_015
matched: meter:6_8, meter:9_8, style:math_rock, tuning:standard, visual_type:tab_excerpt
```

## 建议前端 A/B 用例

先关闭 Answer Composer，仅测试 Evidence Bundle；每条 query 分别选择正式库与混合库运行。

### 风格正例

1. `FACGCE 调弦下有哪些适合 math rock 的开放和弦指型？`
2. `给我一个带点弦动作的数摇和弦指型参考。`
3. `标准调弦下，Math Rock 的 Cmaj7 可以怎么按？`

预期：混合库应出现 Math Rock 视觉证据；正式库通常不会出现这 9 条试验数据。

### 基础保护

1. `标准调弦的普通 G7 和弦指型，不要点弦。`
2. `给我基础 Cmaj7 指型，不需要开放弦和琶音。`
3. `找一个常规小调音阶指板图，不考虑特殊调弦。`

预期：混合库中的 Math Rock 视觉证据不应位于首位；带 FACGCE、点弦或开放弦冲突的证据应被降权。

## 当前验证状态

- Python 静态编译在首次接入后通过。
- 先前独立混合库评测为 14/14 Hit@1。
- 最终重排顺序已调整为“模型 rerank -> 领域边界规则”。
- 2026-06-10 已使用 `.venv-mineru` 完成本地 Chroma 烟测与后端 API 烟测。

## 2026-06-10 检查结果

### 修正点

抗干扰测试发现：旧规则把 `点弦/tapping` 放在 Math Rock 风格关键词里，导致 `不要点弦` 也会误触发 `mathrock` 意图。

已调整为：

- `点弦/tapping`、`开放弦/open string` 只作为技法词，不再自动等于 Math Rock 风格；
- Math Rock 风格意图只由 `math rock`、`mathrock`、`数摇`、`数学摇滚` 等明确风格词触发；
- 未明确 Math Rock 意图时，`mathrock_style_visual_caption_v1` 视觉证据强降权并标记为 `optional_expansion_only`。

### 追加修正：target_tuning 必填

前端测试发现：用户明确提出 `FACGCE 调弦` 时，LLM QueryPlan 虽然把 `tuning:facgce` 写入 `canonical_terms`，但没有写入 `required_terms`，导致视觉层优先满足 `G 大调`，返回标准调弦的 G 大调指型图。

已调整为：

- Query Normalizer 每次必须输出 `target_tuning`；
- 用户未指定调弦时，`target_tuning=standard`；
- 用户指定 FACGCE/DADGAD/Drop D/开放调弦时，`target_tuning` 写为 `facgce/dadgad/drop_d/open`；
- `tuning:target_tuning` 必须进入 `canonical_terms` 和 `required_terms`；
- RAG 侧会兜底补齐 `target_tuning`，即使 LLM 漏字段也会从 query 中推断；
- 指板手册视觉答案与 canonical sidecar 默认视作 `tuning:standard`；
- 非目标调弦视觉证据会强降权，并标记为 `optional_expansion_only`。

本地单元测试：

```json
{
  "target_tuning": "facgce",
  "canonical_terms": ["tuning:facgce", "key:g_major", "root:g", "technique:riff"],
  "required_terms": ["tuning:facgce", "key:g_major"]
}
```

本地 RAG 烟测：

- query：`FACGCE 调弦下的 数摇riff,G调要怎么设计`
- context：`target_tuning=facgce`
- top5 visual：均来自 `mathrock_style_visual_caption_v1` 且 `tuning=FACGCE`
- 标准调弦 G 大调 canonical 图不再进入 top visual。

### 本地脚本烟测

命令入口：`scripts/query_rag_bundle.py`

1. `FACGCE 调弦下的 math rock G7 和弦指型图`
   - 视觉库：`guitar_visual_mixed_mathrock_trial_qwen3_06b`
   - top1：`visual_caption:mr_style_001_g7`
   - top5：均来自 `mathrock_style_visual_caption_v1`
   - 结果：通过

2. `标准调弦的普通 G7 和弦指型，不要点弦`
   - 视觉库：`guitar_visual_mixed_mathrock_trial_qwen3_06b`
   - top5：均来自 `fretboard_handbook_question_answer`
   - 结果：通过，Math Rock 视觉层没有污染基础查询首位

本地耗时参考：

- 首次模型加载约 4.5-5.2 秒；
- 单路 Chroma 视觉检索约 0.22 秒；
- 总查询约 5.9-6.8 秒。

### 后端 API 烟测

接口：`POST /api/query/run`

请求字段包含：

```json
{
  "visual_collection": "mathrock_mixed_trial",
  "use_normalizer": false,
  "compose_answer": false
}
```

结果：

- HTTP 200；
- 最新 query log 正确记录 `visual_collection.profile = mathrock_mixed_trial`；
- 报告文件：`data/eval/manual_queries/manual_query_20260610_181935_e45bcee3fd_mathrock_mixed_trial.json`；
- top1：`visual_caption:mr_style_001_g7`。

### 前端静态检查

已确认 `frontend/index.html` 包含：

- `rag-visual-collection`
- `chain-visual-collection`
- `Math Rock 混合试验库 · 398`

已确认 `frontend/app.js` 会：

- 将 `visual_collection` 写入 Query 和 Full Chain payload；
- 在结果摘要中显示当前 visual profile；
- 在历史记录中显示并恢复 visual profile。

浏览器插件当前未暴露可用浏览器控制入口，因此本轮未做截图级浏览器点击检查；本地首页已通过 HTTP 200 验证。
