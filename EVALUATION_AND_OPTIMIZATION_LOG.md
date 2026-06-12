# 项目评测与优化记录

日期：2026-06-11

本文记录 Guitar Arrangement Inspiration Agent 从教材处理、KG 构建、RAG 召回、视觉 caption、rerank、Query Normalizer 到 Full Chain Answer Composer 的主要评测过程、问题发现和优化决策。它不是单次实验报告，而是项目持续迭代的评测台账。

## 0. 后续评测与优化计划（固定版）

项目下一阶段评测目标从“链路能不能跑通”升级为“Agentic RAG 是否稳定、可解释、可回归优化”。后续每个 Agentic 模块都要有独立指标，并且与人工反馈、Prompt 版本和 Session Memory 绑定。

### 0.1 当前已建立的评测基础

- 人工 query 已能从前端保存到本地 session / eval 日志。
- Query Normalizer 已能输出结构化 QueryPlan。
- Full Chain 已能返回 Evidence Bundle、Answer、图片证据和耗时。
- 本地 Qwen reranker 已接入，可在前端开关。
- Prompt version 已能记录 normalizer/composer/verifier 版本。
- 视觉 caption 已完成指板练习答案大批量处理，并完成 Math Rock 风格小批量视觉试验。

### 0.1.1 2026-06-11 当前优化结果

本轮重点不是继续增加模型，而是修复“已经存在正确视觉证据，却被错误约束和错误类型候选压住”的问题。

#### 用例 A：Cmaj7 两手点弦琶音

Query：

```text
给我一个Cmaj7两手点弦琶音谱例
```

原问题：

- Normalizer 已识别点弦和标准调弦，但附带了不合适的 `visual_type:scale_pattern`。
- 普通 C 大调指板图依靠调性相似度排在真正的点弦 tab 前面。
- Math Rock canonical 数据的图片路径位于嵌套 `source_metadata.image_path`，前端无法稳定解析。

优化：

- 对 tapping / arpeggio / tab 请求增加视觉任务精炼。
- 从 QueryPlan 提取精确和弦 canonical terms：`chord:c_maj7`、`chord_quality:maj7`。
- 强化 `technique:tapping`、`visual_type:tab_excerpt` 和 `tuning:standard`。
- 移除与谱例任务冲突的普通 scale-pattern 强约束。
- 修复 Math Rock sidecar 嵌套图片路径读取。

结果：

```text
Top1 = visual_caption:mr_style_010
```

#### 用例 B：6/8 转 9/8 的 I-IV 数摇 riff

Query：

```text
给我一个6/8转9/8的I-IV数摇riff
```

原问题：

- Normalizer 把 `chord_quality:maj` 当成 required term。
- 普通大和弦图因此获得高分，压过包含目标拍号的 riff 谱例。

优化：

- 对 riff / tab / 谱例任务统一优先 `visual_type:tab_excerpt` 与 `visual_subtype:riff_tab`。
- 从原始 query 提取 `meter:6_8`、`meter:9_8`。
- 明确 Math Rock 风格标签与标准调弦边界。
- 在节奏谱例任务中降低普通和弦图、音阶图的优先级。

结果：

```text
Top1 = visual_caption:mr_style_015
```

#### 数据状态同步

- 指板答案正式视觉库：389 条。
- Math Rock 风格视觉试验：9 条，审核状态已统一为 `accepted`。
- 混合视觉库：398 条。
- canonical visual branch 会按当前视觉 collection 同时读取指板与风格 sidecar。

对应回归报告：

```text
data/eval/query_rag_bundle_cmaj7_tapping_after_canonical_fix.md
data/eval/query_rag_bundle_mathrock_6_8_9_8_after_riff_fix.md
```

新增建议指标：

| 指标 | 含义 |
|---|---|
| `visual_exact_match@1` | Top1 是否为人工指定的目标视觉条目 |
| `visual_type_match@1` | Top1 是否属于 query 所需的图类，如 tab、riff、chord diagram |
| `meter_match@1` | Top1 是否覆盖 query 指定拍号 |
| `tuning_match@1` | Top1 调弦是否满足显式或默认调弦约束 |
| `canonical_entity_match@1` | Top1 是否匹配精确和弦、调性、技法等 canonical entities |

### 0.2 Answer Verifier 评测

Verifier 上线后需要单独评测，不能只看最终答案：

| 指标 | 含义 |
|---|---|
| `verifier_pass_rate` | Verifier 判定通过的比例 |
| `issue_recall` | 对人工标注问题的召回率 |
| `false_alarm_rate` | 把正确答案误判为问题的比例 |
| `tuning_check_accuracy` | 对标准调弦 / FACGCE / Drop D 等边界的识别准确率 |
| `evidence_id_valid_rate` | 答案引用的 evidence id 是否真实存在 |
| `rewrite_required_precision` | 要求重写的样例是否真的需要重写 |

优先 bad case：

- 用户未指定调弦，但视觉结果返回特殊调弦图。
- 数摇问题误召回普通标准调弦指型。
- Funk rhythm query 被 Math Rock 证据污染。
- Composer 引用了不存在或不相关的图片证据。

### 0.3 Defensive Prompting / 证据冲突评测

需要构造小型冲突评测集：

- 标准调弦 query + FACGCE 视觉证据混入。
- 同一和弦名在不同调弦下的指型证据混入。
- 风格教材与底层指板教材同时命中但侧重点不同。
- 文本证据说“省略五音”，视觉 caption 未体现或相反。

期望结果：

- Composer 不自行缝合矛盾证据。
- Verifier 能指出冲突来源。
- `uncertainties` 字段记录无法判断的点。
- Rerank 应将符合 QueryPlan 约束的证据排在前面。

### 0.4 多轮对话与记忆评测

多轮链路完成后，需要评测“上下文是否正确继承”：

| 场景 | 期望 |
|---|---|
| “给我 Fmaj7 数摇开放和弦” -> “换成 G” | 保留数摇、开放和弦、默认调弦，仅替换根音/调性 |
| “不要开放弦” | 后续检索和答案降权开放弦图片 |
| “太难了，简单点” | 调整 difficulty，不丢失风格 |
| “刚才那个图不对” | 将对应 evidence id 记录为负反馈 |
| “还是标准调弦” | 覆盖上一轮特殊调弦约束 |

核心指标：

- `context_carryover_accuracy`
- `stale_constraint_rate`
- `memory_update_accuracy`
- `user_correction_follow_rate`

### 0.5 动态 Few-Shot 评测

当 Golden Answer 库形成后，做 baseline vs dynamic few-shot 对比：

- Baseline：不注入 few-shot。
- Treatment：按 style / intent / tuning / query similarity 注入 1-2 条高分样例。

指标：

- 风格贴合度人工评分。
- 证据引用完整率。
- Verifier pass rate。
- 回答可执行性评分。
- 回复冗余度和幻觉率。

### 0.6 Prompt A/B 与回归指标

Prompt 后续按版本管理，修改 prompt 必须留下评测记录：

| 指标 | 适用模块 |
|---|---|
| `schema_valid_rate` | Query Normalizer / Verifier |
| `required_terms_hit_rate` | Query Normalizer |
| `visual_tuning_match@k` | Visual Retrieval / Rerank |
| `kg_hit_rate` | KG retrieval |
| `evidence_precision@5` | Text / Visual / KG |
| `rerank_delta@5` | Rule rerank / Qwen reranker |
| `verifier_pass_rate` | Composer + Verifier |
| `human_overall_score` | Full Chain |
| `latency_ms` | 全链路 |
| `api_cost_estimate` | 外部 LLM 调用 |

### 0.7 Golden / Bad Case 数据集建设

从前端人工反馈中沉淀两类数据：

- Golden Answers：评分高、证据引用正确、Verifier 通过，进入动态 few-shot 候选。
- Bad Cases：评分低、召回偏离、调弦错误、图片不匹配、乐理错误，进入回归测试集。

每条样例至少保存：

```json
{
  "query": "",
  "query_plan": {},
  "expected_constraints": {},
  "bundle_ids": [],
  "answer_id": "",
  "human_score": 0,
  "human_notes": "",
  "prompt_versions": {},
  "verifier_result": {}
}
```

## 1. 评测目标

当前项目评测不只看“最终回答好不好”，而是分层评估：

```text
数据层：
  教材文本是否完整、干净、可分块。

视觉层：
  图片是否能被切成可召回的最小语义单元。
  caption 是否准确表达指板图、和弦图、音阶图。

KG 层：
  节点和关系是否能支撑风格、技法、编配关系。
  是否过度碎片化，无法形成可用网络。

召回层：
  文本、视觉、KG 是否能命中相关证据。
  中英文术语、调性、和弦名是否能稳定匹配。

重排层：
  rule rerank 和模型 rerank 是否提升 TopK 可用性。

生成层：
  Answer Composer 是否基于证据回答。
  是否出现乐理错误、过度推断或证据误用。

前端层：
  是否能收集人工 query、显示证据、展示图片、保存反馈。
```

核心原则：

- 先让链路可观察，再追求自动化。
- 先做小批量可解释评测，再扩大规模。
- 每次优化都要能回到具体失败样例。
- 视觉图不盲目进 KG，优先作为可召回证据层。
- LLM 生成必须接受证据约束和乐理自检。

## 2. 已完成评测概览

| 阶段 | 评测对象 | 主要产物 | 当前结论 |
|---|---|---|---|
| 教材解析 | MinerU Markdown / 图片切分 | 指板手册、Math Rock PDF 转换结果 | 文本可用，但复杂图文页需要人工视觉补充 |
| KG 抽取 | LLM KG JSON / Markdown 审核 | 多批 `arrangement_kg_review.md` | 人工审核流程有效，KG 适合抽象关系，不适合承载所有练习图 |
| Neo4j 导入 | 本地 Neo4j 节点关系 | `import.cypher`、Neo4j 检查脚本 | 导入可用，但早期节点偏“两两相连”，需要靠更多教材和规范关系增强网络 |
| 文本 RAG | Chroma 文本召回 | `text_rag_expanded_rerank_report.md` | 本地 embedding 可用，缓存后速度可接受 |
| 视觉 RAG | VLM caption -> 文本 embedding | 多批 `visual_caption_review.md` | VLM 降维路线成立，优于直接多模态 embedding 主检索 |
| 指板答案视觉层 | 题目级切块 + caption | `question_answer_visual_caption_batches` | 新版题目级切块比 MinerU 原始切图更可靠 |
| canonical terms | caption 中英文术语规范 | `canonical_terms_review.md` | 能缓解 G minor / G小调、和弦名、乐理术语不匹配问题 |
| Query Normalizer | LLM query plan | `QUERY_NORMALIZER_INTEGRATION_REPORT.md` | 比靠用户随机词直接召回更稳定，适合作为 Agentic 子 Agent |
| rule rerank | 领域规则重排 | `RAG_RERANK_RULE_SPEC.md` | 能处理风格、调性、视觉需求、特殊调弦等边界 |
| Qwen reranker | 本地 reranker A/B | `qwen_reranker_smoke_ab_report.md` | 可作为规则后的相关性微调，但不应替代规则层 |
| Full Chain | RAG -> Answer Composer | `FULL_CHAIN_RAG_EXECUTION_REPORT.md` | 链路跑通，发现并修正过乐理自检问题 |

## 3. 数据层评测与优化

### 3.1 指板手册 Markdown 不完整问题

发现：

- 前端浏览 chunk 时发现指板教材并非整本均有完整 Markdown chunk。
- 早期处理只覆盖到部分页，后续答案区和练习区存在缺失或图片化内容。

优化：

- 不再只依赖 MinerU Markdown。
- 对练习答案建立独立的“练习题目 + 参考答案 + 图片切块”流程。
- 将新版练习-答案整合块放回指板教材母目录下，便于前端浏览。

结论：

- 教材正文和练习答案应分层处理。
- 正文适合文本清洗和 embedding。
- 答案图适合视觉 caption，而不是强行 OCR。

### 3.2 Math Rock PDF 图文密集问题

发现：

- Math Rock PDF 知识量明显大，图文、谱例、练习密度高。
- 缺图片段如果直接 KG 抽取会比较保守。
- 补图后同一文本段可能产生更丰富的新知识。

优化：

- 先文本抽取并标记 `missing_visual_context`。
- 将缺图片段单独拆出审核。
- 再进行多模态 KG 补抽。

结论：

- 对图文密集教材，先文本、后补图是可控路线。
- 缺图版本可以入库，但应带 `missing_visual_context` 标记，避免误以为证据完整。

## 4. KG 层评测与优化

### 4.1 早期 KG 两两相连问题

发现：

- Neo4j 中很多节点呈现“两两相连”，整体网络不够网状。
- 这不是导入错误，而是抽取粒度和教材覆盖不足导致。

原因：

- 单本教材偏基础概念，关系天然局部。
- 抽取 prompt 更关注“这句话里有什么关系”，较少主动建立跨章节、跨风格连接。
- 练习图若直接导入 KG，会增加大量孤立节点。

优化决策：

- 主 KG 只承载抽象、稳定、可迁移关系。
- 视觉练习图保留在 caption RAG 层。
- 风格教材继续补充 funk、math rock、后续 blues / jazz / metal / neo soul 等内容。

结论：

- KG 不应追求把所有材料都节点化。
- KG 的价值在“关系推理”和“风格/技法迁移”，不是替代向量库。

### 4.2 视觉 caption 是否入 KG

讨论结论：

- 不把所有指板练习 caption 导入主 KG。
- 原因是视觉 caption 与现有视觉 RAG 的检索功能高度重叠。
- 如果导入 KG，容易造成节点膨胀和噪声关系。

当前策略：

```text
视觉 caption：
  负责具体图片、指型、答案图证据。

Neo4j KG：
  负责风格、技法、约束、启发式编配关系。

Answer Composer：
  同时引用视觉证据和 KG 证据。
```

## 5. 视觉层评测与优化

### 5.1 直接图片 embedding 的问题

早期方案：

- 将图片直接送入多模态 embedding。

发现：

- 指板图之间视觉外观高度相似。
- 直接视觉相似容易跨章节误召回。
- 用户 query 通常是乐理语义，不是视觉形状本身。

优化：

- 改为 VLM 生成结构化 caption。
- 再用文本 embedding 存入 Chroma。

结论：

```text
图片 -> VLM caption -> 文本 embedding -> Chroma
```

这是当前视觉层主路线。

### 5.2 MinerU 答案图切分不可靠

发现：

- MinerU 对全图答案页切分效果不稳定。
- 有些图片混入其他题目。
- 有些 block 只切到图，没切到对应文字。
- 有些 block 把两个指型合并成一个。

优化：

- 建立本地 bbox / question segment v2 流程。
- 按每道题、每个小题，将“文字 + 指型图”作为整体切块。
- 对纯文字答案也保留大块，用 VLM 或后续 OCR 处理音乐符号。

人工审核结论：

- 旧的 local segment 容易漏文字。
- v2 question segment 更符合最终召回需求。
- 47-48 等复杂页验证后，决定将之前审核过的也按 v2 重切。

### 5.3 题目级 caption 评测

发现：

- 一张大图对应多道题、多堆指型时，召回价值低。
- 用户真正需要的是某个可用指型或某个答案图单元。

优化：

- 不再以“6 张大图”作为 caption 单位。
- 改成“题目 / 小题 / crop”级别 caption。

结论：

- 对视觉 RAG，粒度比模型能力更关键。
- 正确粒度应接近最终用户可引用的图片证据。

## 6. canonical terms 评测与优化

### 6.1 问题来源

发现：

- caption 中常出现中文术语，例如“G小调”。
- 用户 query 可能写 `G minor`。
- 单靠 embedding 有时能近似匹配，但不稳定。
- 和弦、调性、音阶、乐理名词都存在中英文混用问题。

### 6.2 方案比较

方案 A：硬编码中英文词典。

- 优点：快、稳定。
- 缺点：维护成本高，覆盖不完各种和弦/调式/简写。

方案 B：Query Normalizer 负责把用户 query 规范化。

- 优点：能处理自然语言。
- 缺点：只解决 query 侧，不解决 caption 侧。

方案 C：增加 canonical retrieval branch。

- caption 侧离线抽取 canonical terms。
- query 侧也由 LLM 输出 canonical terms。
- 检索时增加一路专门匹配 canonical terms。

当前采用：

```text
Query Normalizer + caption canonical terms + canonical visual branch
```

结论：

- 这一路不能完全替代 Query Normalizer。
- Query Normalizer 负责理解用户意图。
- canonical branch 负责术语对齐和精确召回补强。

## 7. Query Normalizer 评测与优化

### 7.1 为什么需要 Query Normalizer

发现：

- 用户自然 query 可能非常口语化。
- 如果直接用原始 query 召回，KG 和视觉 caption 容易漏掉关键实体。
- 靠不断改代码适配用户随机词不可持续。

优化：

- 让 LLM 将用户 query 规范化成项目内部可检索的 QueryPlan。

QueryPlan 应包含：

```text
intent
style_hints
theory_terms
technique_terms
canonical_terms
retrieval_plan
tool_queries
constraints
```

### 7.2 前端人工评测

已接入：

- “只规范化”按钮。
- query plan 展示。
- 人工反馈打分。
- query log 保存。

评测重点：

- 是否正确理解用户意图。
- 是否误判风格。
- 是否提取正确调性 / 和弦 / 技法。
- 是否决定了正确检索工具。
- 是否给出适合 Chroma / KG 的检索 query。

结论：

- LLM normalizer 当前表现较稳定。
- 适合作为 Agentic RAG 的第一个子 Agent。

## 8. RAG 召回与 rerank 评测

### 8.1 TopK 如何使用

当前策略：

- Top5 / Top8 不直接等于最终答案材料。
- 它们是候选证据池。
- 后续需要经过规则、模型 rerank、证据 sufficiency 判断和 Answer Composer 选择。

建议理解：

```text
TopK retrieve:
  尽量召回相关候选，不要求排序完美。

Rerank:
  将最适合回答当前 query 的证据提前。

Answer Composer:
  从 evidence bundle 中选择并引用真正使用的证据。
```

### 8.2 rule rerank

当前 rule rerank 负责：

- 调性匹配。
- 和弦品质匹配。
- 风格匹配。
- 特殊调弦过滤。
- 视觉需求提升。
- 练习图使用边界。
- KG 关系类型偏好。

结论：

- rule rerank 是领域边界层。
- 它比模型 rerank 更适合处理“不要误用”的规则。

### 8.3 Qwen reranker

测试对象：

```text
Qwen3-Reranker-0.6B
```

测试结论：

- 可以作为规则后的相关性微调。
- 对部分 query 的排序有帮助。
- 但会增加数秒耗时。
- 不应替代 Query Normalizer 和 rule rerank。

推荐使用方式：

```text
召回 -> canonical branch -> rule rerank -> Qwen rerank -> Evidence Bundle
```

## 9. Answer Composer 评测与优化

### 9.1 初版问题

Full Chain smoke 中发现：

- LLM 在回答 Fmaj7 + 开放弦时，曾把 B 误称为 Fmaj7 的三音。
- 这说明即使证据召回正确，最终生成仍可能出现乐理错误。

### 9.2 Prompt 优化

加入：

- 和弦构成自检。
- tension / non-chord tone 说明。
- evidence_id 引用要求。
- 不确定点输出。
- 不允许把推断写成教材事实。

优化后要求：

```text
Fmaj7 = F A C E
B 不是三音
B 可解释为 #11 / Lydian 色彩
```

结论：

- Answer Composer 必须内置 theory_checks。
- 后续还需要独立 Answer Verifier。

## 10. 前端评测与优化

### 10.1 Query Workbench

已完成：

- 人工 query 输入。
- query 保存。
- Query Normalizer 测试。
- RAG bundle 展示。
- rerank 参数设置。
- 人工反馈表。

作用：

- 收集真实 query。
- 让 prompt 和规则优化有数据依据。

### 10.2 Full Chain 页面

已完成：

- 完整 RAG 链路一键运行。
- 最终答案展示。
- theory checks 展示。
- 视觉证据图片展示。
- 文本 evidence image_refs 代码对照。

当前价值：

- 能直观看到答案是否真的调取了图片证据。
- 能分辨问题发生在召回、重排还是生成。

## 11. 当前主要问题清单

| 问题 | 当前状态 | 下一步 |
|---|---|---|
| 指板教材正文是否全部入本地 embedding | 已清洗并入库核心文本，但仍需继续确认覆盖范围 | 前端按教材目录抽查 |
| 视觉 caption 早期小批量质量不稳定 | 已决定旧 caption 不作为主依据 | 使用新版题目级 caption 层 |
| 视觉 evidence 是否应进 KG | 当前不导入主 KG | 仅在必要时设计 VisualEvidence 节点子图 |
| query 术语中英文匹配 | canonical branch 已建立 | 扩大评测 query |
| RAG 召回 TopK 如何选用 | 已明确 TopK 是候选池 | Answer Composer / Verifier 决定最终使用 |
| rerank 模型是否必要 | Qwen smoke 可用，但不是主规则 | 前端 A/B 扩大评测 |
| LLM 生成乐理错误 | 已加入 theory_checks | 下一步做独立 verifier |
| GP5 工作流尚未接入 | 已规划 | 在 RAG 链路稳定后接入 |

## 12. 后续评测计划

### 12.1 Query Normalizer 评测

规模：

- 先收集 30 条人工 query。

维度：

- intent 准确率。
- canonical terms 准确率。
- retrieval_plan 合理率。
- 是否过度召回视觉。
- 是否漏掉 KG / style text。

### 12.2 RAG 召回评测

规模：

- 30 条 query，每条人工标注期望证据类型。

指标：

```text
text_hit@5
visual_hit@5
kg_hit@8
canonical_hit@5
top1_usable
top3_usable
evidence_diversity
latency_uncached
latency_cached
```

### 12.3 Rerank A/B

比较：

```text
rule only
rule + qwen reranker
```

人工评分：

- top1 是否更好。
- top3 是否更集中。
- 是否把风格不相关证据推高。
- 是否误伤视觉证据。
- 耗时是否可接受。

### 12.4 Answer Composer 评测

指标：

- 是否引用 evidence_id。
- 是否使用了正确证据。
- 是否出现乐理错误。
- 是否区分事实与推断。
- 是否给出可执行编曲动作。
- 是否正确表达不确定性。

### 12.5 Full Chain 评测

query 桶：

```text
fretboard_voicing
visual_shape_recommendation
style_rhythm
mathrock_open_string
funk_groove
mixed_arrangement
future_gp5_context
```

输出：

- 每条 query 保存 JSON / Markdown。
- 前端人工反馈。
- 失败案例归类。
- 下一轮 prompt / rerank / retrieval 优化建议。

## 13. 下一步优化优先级

优先级 1：Answer Verifier

- 解决最终答案可靠性。
- 检查证据引用和乐理错误。
- 比继续扩大数据更能提升系统可信度。

优先级 2：Rerank A/B 前端扩大评测

- 用人工 query 判断 Qwen reranker 是否值得默认启用。

优先级 3：canonical branch 扩大测试

- 专门测试中英文调性、和弦、音阶、技法名。

优先级 4：Session / Query Dataset

- 把用户前端 query 和反馈稳定沉淀为项目评测集。

优先级 5：GP5 接入

- 在 RAG 链路稳定后，将 `.gp5` 分析结果作为 query context 输入。

## 14. 当前结论

项目已经完成从“资料处理”到“端到端 RAG 生成”的关键闭环：

```text
教材处理
-> 文本 / 视觉 / KG 多层知识库
-> Query Normalizer
-> 多路召回
-> canonical 对齐
-> rule rerank / Qwen rerank
-> Evidence Bundle
-> Answer Composer
-> 前端 Full Chain 展示
-> 人工反馈
```

当前最重要的优化方向不是继续盲目加教材，而是把评测闭环做实：

- query 是否被正确理解。
- 证据是否被正确召回。
- rerank 是否真的提升排序。
- 最终答案是否基于证据且乐理正确。

等这些稳定后，再接入 GP5 / 乐谱分析，项目会从“吉他知识 RAG”升级为“面向真实谱例的吉他编曲 Agent”。

## 15. 2026-06-10 前端 Full Chain 人工测试

本轮人工测试：

1. `我想写一段基于G大调的funky riff,律动要足，同时给bass流空间，怎么设计？`
2. `我想设计数摇riff,E大调，可以设计开放和弦和一些点弦，该怎么设计`
3. `想设计A小调的blues riff,旋律线该怎么构建`
4. `给我FM9的指型图`

四条均成功完成：

```text
Query Normalizer
-> Text / Visual / KG 召回
-> Rerank
-> Answer Composer
-> evidence_id 引用
```

结果摘要：

| Query | Text | Visual | KG | Answer |
|---|---:|---:|---:|---|
| G 大调 funky riff | 10 | 5 | 8 | ok |
| E 大调数摇开放弦点弦 riff | 10 | 5 | 8 | ok |
| A 小调 blues riff | 10 | 5 | 8 | ok |
| FM9 指型图 | 10 | 5 | 0 | ok |

主要发现：

- 基础和声/指板视觉层表现良好。
- FM9 成功召回 `C/F = Fma9` 指型图。
- A 小调 Blues 成功引用 A 小调五声音阶指型图。
- Funk 和 Math Rock query 也能得到 G/E 大调通用指板图。
- 但当前 Math Rock 图片主要是“调性基础图”，缺少开放调弦、点弦谱例、特殊 voicing、琶音组合和非常规节拍等风格视觉证据。

额外观察：

- Funk query 的 QueryPlan 中 `visual_caption.enabled=false`。
- canonical visual 补召回仍返回了 G 大调指型图。
- 后续需要明确 canonical branch 是允许独立补召回，还是必须服从 visual tool gate。

下一步已建立 15 张 Math Rock 风格视觉试验清单：

```text
data/processed/mathrock/style_visual_caption_trial/style_visual_caption_candidates.md
```

本轮只准备裁切任务，不发送图片到外部 API。
# 2026-06-10 Prompt Version Control

完成 Prompt 版本控制接入：

- Query Normalizer prompt：`query_normalizer_v1.1`
- Answer Composer prompt：`answer_composer_v1.0`
- Answer Verifier prompt：`answer_verifier_v0.1`，planned

验证：

- 静态编译通过。
- QueryPlan 后处理会写入 `prompt_versions.query_normalizer`。
- Answer Composer 会写入 `composer.prompt_version` 和 `prompt_versions.answer_composer`。
- 前端结果面板显示 Prompt Versions。

优化意义：

- Bad Case 可以回溯到具体 prompt 版本。
- 后续可做 Prompt A/B。
- Session Memory 可作为 prompt 迭代的数据闭环。
