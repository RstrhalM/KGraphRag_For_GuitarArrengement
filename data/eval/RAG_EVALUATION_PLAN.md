# RAG 评测规划

本规划用于在正式设计 Agent 前，把当前 Neo4j + Chroma + Embedding Cache 的 RAG 层评测做扎实。目标不是追求单次分数好看，而是确认系统在自然语言检索、教材专项检索、跨风格融合、视觉证据召回和后续 GP5 特征检索上都可解释、可回归、可优化。

## 1. 当前基线

当前已经跑过的小批量评测：

- Math Rock PDF 专项 global：`2/3`
- Math Rock PDF 专项 source_focus：`3/3`
- 全项目 global：`4/4`

已验证：

- Neo4j KG 命中稳定。
- 视觉 Chroma 在小样本中表现稳定。
- 文本 Chroma 对同风格相近教材会互相抢 Top1。
- `source_focus` 能把专项评测的 primary source 边界拉清楚。
- Embedding 缓存命中后，评测速度可以进入亚秒级。

当前风险：

- 测试样本太少。
- query 类型覆盖不够。
- 还没有明确区分“单源精确命中”和“跨源有用补充”。
- 还没有足够的负样本、模糊 query、中文 query、混合中英文 query。
- 还没有 GP5 特征 query。

## 2. 评测目标

RAG 层需要回答四个问题：

1. **能不能找准来源？**
   当用户或评测指定某本教材/某种风格时，primary pool 是否能稳定命中。

2. **能不能跨源补充？**
   全项目模式下，系统是否能把 Funk、Math Rock、指板基础、视觉证据组合起来，而不是只命中单一来源。

3. **能不能找对证据形态？**
   文本知识、图谱关系、谱例图/指板图/和弦图是否能各司其职。

4. **能不能解释失败？**
   失败时能区分是 query intent、embedding、source filter、KG 节点缺失、视觉 metadata，还是评测期望写得不合理。

## 3. 检索模式

### `global`

开放式全项目检索。

适用：

- 用户自然语言问答。
- 编配诊断。
- 跨风格启发。
- 不指定教材来源的 query。

评测重点：

- bundle 是否召回有用证据。
- 多源结果是否合理。
- KG 是否能提供结构化建议。

### `source_focus`

指定 primary source 的专项检索。

适用：

- 单教材评测。
- 某个知识包导入后的回归测试。
- 需要确认新导入教材是否可独立召回。

评测重点：

- primary source Top1 / Recall@5。
- support pool 是否只作为辅助，不污染 primary 判定。

### 后续新增：`style_focus`

指定风格而不是指定教材。

例：

- `math_rock`
- `funk`
- `fretboard`

评测重点：

- 风格内多教材融合。
- 同风格不同来源之间的合理排序。

### 后续新增：`diagnostic`

问题诊断模式。

例：

- “这段太糊”
- “律动不稳”
- “riff 不够数摇”
- “和弦太满”

评测重点：

- caution / constrains / sparse / muting / voicing 类 KG 是否被优先召回。
- 是否能召回解决策略，而不是只召回概念解释。

## 4. 测试集结构

建议拆成多个 JSON 文件，避免一个大测试集难维护。

```text
data/eval/
  testsets/
    nl_mathrock_pdf_source_focus.json
    nl_mathrock_style_focus.json
    nl_funk_style_focus.json
    nl_fretboard_foundation.json
    nl_cross_style_arrangement.json
    nl_diagnostic_queries.json
    nl_visual_grounding.json
    gp5_feature_queries.json
```

每条 case 建议字段：

```json
{
  "id": "mathrock_facgce_open_string_voicing",
  "query": "FACGCE tuning open strings Fmaj9 movable barre shapes math rock voicing",
  "retrieval_mode": "source_focus",
  "primary_sources": ["mathrock_pdf_steve_h"],
  "text_sources": ["mathrock_pdf_steve_h"],
  "visual_sources": ["mathrock_pdf_steve_h"],
  "style_tags": ["math_rock", "alternate_tuning", "voicing"],
  "kg_nodes_any": ["tuning:FACGCE", "chord:open_Fmaj9"],
  "expected_behavior": "PDF 文本和视觉图示应作为 primary evidence，Math Rock 文本课程只能作为 support evidence。"
}
```

## 5. Query 分类与规模

### 第一阶段：小扩容，约 30 条

目标：快速发现明显排序问题。

| 类别 | 数量 | 模式 |
| --- | ---: | --- |
| Math Rock PDF 专项 | 6 | `source_focus` |
| Math Rock 风格融合 | 5 | `global` / `style_focus` |
| Funk 节奏吉他 | 5 | `global` / `style_focus` |
| 指板基础与视觉图 | 5 | `source_focus` |
| 跨风格编配建议 | 5 | `global` |
| 诊断类 query | 4 | `diagnostic` |

### 第二阶段：中等规模，约 80-120 条

目标：稳定评估模型/检索参数。

| 类别 | 数量 | 重点 |
| --- | ---: | --- |
| 单教材 source_focus | 25 | 新知识包独立可召回 |
| 风格 style_focus | 25 | 风格内融合 |
| 全项目 global | 25 | 跨源综合 |
| 视觉依赖 | 15 | 图片证据召回 |
| 模糊/中文/中英混合 | 15 | NLP 鲁棒性 |
| 负样本/不该召回 | 10 | 误召回控制 |

### 第三阶段：回归集，固定 30-50 条

目标：每次新增教材、改脚本、改 embedding 模型都跑。

特点：

- 不追求覆盖所有知识。
- 只保留最能暴露系统问题的 case。
- 每条都有明确 expected behavior。

## 6. 指标设计

### 文本检索

- `text_top1_accuracy`
- `text_recall_at_5`
- `text_precision_at_5`
- `primary_text_recall_at_5`
- `support_text_usefulness`

说明：

- source_focus 下优先看 `primary_text_recall_at_5`。
- global 下 Top1 不一定是唯一目标，Recall@5 和 evidence diversity 更重要。

### 视觉检索

- `visual_top1_accuracy`
- `visual_recall_at_5`
- `visual_precision_at_5`
- `visual_source_accuracy`
- `visual_priority_accuracy`

说明：

- 指板手册需要 priority，例如 `P2_arpeggios_chords`。
- Math Rock PDF 需要 source_id + page/image granularity。

### Neo4j

- `kg_hit_rate`
- `kg_expected_node_hit_count`
- `kg_edge_context_match`
- `kg_relation_type_coverage`

说明：

- 只命中节点还不够，后续要看关系类型是否合理，例如 `enables`、`constrains`、`cautions`。

### Bundle

- `bundle_pass_rate`
- `primary_bundle_pass`
- `global_bundle_pass`
- `evidence_diversity`
- `total_seconds`
- `cache_hit_rate`

说明：

- Bundle 不应只看单个 Top1。
- 对 Agent 有意义的是：文本、视觉、KG 至少有两类证据能互相支撑。

## 7. 通过标准

### 当前短期门槛

30 条小扩容测试：

- source_focus primary text Recall@5 >= 90%
- global text Recall@5 >= 85%
- visual Recall@5 >= 85%
- KG hit rate >= 85%
- bundle pass >= 80%
- cache-hit 平均耗时 < 0.5s

### 中期门槛

80-120 条测试：

- source_focus primary text Recall@5 >= 90%
- style_focus text Recall@5 >= 85%
- global bundle pass >= 80%
- diagnostic KG hit rate >= 80%
- visual Recall@5 >= 85%
- 明显误召回 case 可解释率 >= 90%

## 8. 误差分类

每个失败 case 应标记一个主因：

- `query_intent_ambiguous`：query 本身太模糊。
- `source_boundary_conflict`：同风格不同教材抢占。
- `embedding_semantic_drift`：embedding 语义漂移。
- `metadata_missing`：Chroma metadata 缺 source/style/priority。
- `kg_node_missing`：Neo4j 缺期望节点。
- `kg_alias_missing`：节点存在但 alias 没覆盖。
- `visual_priority_mismatch`：视觉 priority 规则不准。
- `test_expectation_wrong`：评测期望写得过窄或不合理。

## 9. 下一步执行计划

### Step 1：完善评测脚本输出

新增字段：

- primary/support 分池指标。
- source diversity。
- KG relation type 命中。
- 失败主因占位字段。

### Step 2：扩容到 30 条

新增：

- `data/eval/testsets/nl_mathrock_pdf_source_focus.json`
- `data/eval/testsets/nl_mathrock_style_focus.json`
- `data/eval/testsets/nl_funk_style_focus.json`
- `data/eval/testsets/nl_fretboard_foundation.json`
- `data/eval/testsets/nl_cross_style_arrangement.json`
- `data/eval/testsets/nl_diagnostic_queries.json`

### Step 3：跑 global/source_focus 对照

输出：

- `data/eval/reports/rag_eval_30_global.md`
- `data/eval/reports/rag_eval_30_source_focus.md`
- `data/eval/reports/rag_eval_30_summary.md`

### Step 4：根据误差修 RAG

优先优化：

1. source-aware rerank。
2. KG alias。
3. visual priority metadata。
4. diagnostic 模式的 KG relation preference。

### Step 5：再接 GP5 特征 query

等自然语言 RAG 稳定后，再把 GP5 特征转 query：

```json
{
  "id": "gp5_odd_meter_tapping_open_string",
  "features": {
    "style_hint": "math_rock",
    "time_signature": "7/8",
    "techniques": ["tapping", "pull_off"],
    "texture": ["open_string_drone", "wide_interval"]
  },
  "query": "math rock 7/8 tapping pull off open string drone wide interval riff"
}
```

## 10. 近期建议

下一步先做 30 条小扩容评测，不急着接 Agent：

1. 将现有 7 条小样本扩展到 30 条。
2. 每条 query 标注模式、primary source、期望节点和失败解释。
3. 跑一次 cold/warm，再跑 cache-hit。
4. 根据失败样本优化检索层。

只有当 30 条集能稳定跑到 80% 以上 bundle pass，并且失败原因可解释，再进入 GP5 工作流会更稳。
