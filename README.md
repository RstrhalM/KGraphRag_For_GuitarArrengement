# Guitar Arrangement Inspiration Agent 项目报告

日期：2026-06-11

## 0. 后续开发路线图（固定版）

当前项目已经完成 Query Normalizer、混合 RAG 召回、规则 rerank、本地 Qwen reranker、Answer Composer、视觉证据侧栏、Session Memory 和 Prompt 版本控制的基础链路。后续 Agentic RAG 不再以“继续堆更多检索”为主，而是进入多 Agent 协作、记忆反馈和工程化评测阶段。

### 0.0 2026-06-11 当前优化快照

本轮已经把视觉召回从“语义相近即可”推进到“视觉任务类型、精确音乐实体和调弦共同约束”：

- 混合视觉试验库现包含 389 条指板练习答案 caption 与 9 条 Math Rock 风格谱例，共 398 条。
- canonical visual branch 已同时接入指板答案 sidecar 与 Math Rock 风格 sidecar，不需要把具体谱例强行写入 Neo4j 主图。
- 修正 Math Rock caption 的嵌套图片路径解析，前端可直接展示 `source_metadata.image_path` 对应裁图。
- 点弦/谱例 query 会优先匹配 `tab_excerpt`、`technique:tapping`、精确和弦与标准调弦，不再被普通大调指板图抢占。
- riff、谱例、拍号和复合节拍 query 会优先匹配 `riff_tab`、`meter:*` 与风格标签，普通和弦图和音阶图降权。
- 已验证 `Cmaj7 两手点弦琶音谱例` Top1 命中 `mr_style_010`。
- 已验证 `6/8 转 9/8 的 I-IV 数摇 riff` Top1 命中 `mr_style_015`。
- 本地后端统一使用 `http://127.0.0.1:8765`，不再保留 8000 端口的并行实例。

因此，当前检索主链路可以概括为：

```text
User Query
-> LLM Query Normalizer
-> 视觉任务类型与调弦边界修正
-> Text / Visual / KG 多路召回
-> Fretboard + Style canonical 精确补召回
-> Domain Rule Rerank
-> Qwen Reranker
-> Evidence Bundle
-> Answer Composer
```

### 0.1 已固定的 Agentic 模块边界

| 模块 | 当前状态 | 职责 |
|---|---|---|
| Query Normalizer Agent | 已完成 V1 | 把用户自然语言转成结构化 QueryPlan，强制输出 `target_tuning`，默认标准调弦 |
| Retrieval Orchestrator | 已跑通 | 调度文本库、视觉 caption 库、canonical terms、KG 与 rerank |
| Evidence Bundle Builder | 已跑通 | 汇总 TopK 文本、视觉、KG 证据，并保留图片路径和来源 |
| Answer Composer Agent | 已跑通 | 基于 Evidence Bundle 生成结构化编曲建议和 theory checks |
| Prompt Registry | 已完成 V1 | 管理 normalizer/composer/verifier prompt 版本，写入前端和 session log |
| Session Memory | 已完成基础版 | 保存人工 query、query plan、bundle、answer、评分和 prompt version |
| Answer Verifier / Critic Agent | 下一优先级 | 物理隔离为独立审查 Agent，检查调弦、和弦、证据引用和幻觉 |
| Dynamic Few-Shot Selector | 规划中 | 根据风格、意图、调弦和历史高分答案动态注入示例 |
| GP5 / Score Analysis Agent | 规划中 | 将本地 `.gp5` / MIDI / 音频分析结果转成 QueryPlan 上下文 |

### 0.2 Phase A：Answer Verifier / Critic Agent

下一步优先实现 Verifier，而不是继续扩大素材库。原因是现在 Full Chain 已经能生成答案，但还缺一个“独立挑错者”来判断答案是否可靠。

设计原则：

- Composer 只负责“基于证据整合答案”，不再承担全部自检压力。
- Verifier 使用独立 prompt，扮演严苛乐理审查员。
- 输入包括：原始 query、QueryPlan、Evidence Bundle、Composer Answer、prompt_versions。
- 输出包括：`passed`、`risk_level`、`issues`、`rewrite_required`、`suggested_fix`。
- 重点检查：调弦边界、和弦构成、调性/音阶术语、视觉证据是否匹配、证据 ID 是否真实、是否把风格教材内容误当通用规则。

### 0.3 Phase B：Defensive Prompting 与证据冲突策略

真实 RAG 召回不会永远干净。后续需要在 Evidence Bundle 和 Composer Prompt 中固定冲突处理策略：

- 如果证据之间存在调弦冲突，优先遵守 QueryPlan 的 `target_tuning`。
- 如果用户没有指明调弦，默认标准调弦，并降权非标准调弦图片。
- 指板底层知识优先信任《吉他指板手册》。
- 风格语汇、节奏、riff 和特殊调弦优先信任对应风格教材。
- 如果无法判断冲突，不允许模型自行缝合，必须写入 `uncertainties`。

当前已经固定一条可复用的视觉召回子策略：

```text
RHYTHMIC_VISUAL_RETRIEVAL_POLICY.md
```

该策略规定：当用户询问 riff、谱例、tab、节拍、拍号或非常规节拍时，视觉层优先召回 `tab_excerpt / riff_tab`，并使用 `meter:6_8`、`meter:9_8`、`rhythm_grouping:*` 等 canonical terms，而不是让普通和弦图或音阶图抢占首位。

### 0.4 Phase C：多轮对话与记忆反馈

当前 Session Memory 已能保存单次 query。后续要升级为可参与推理的会话状态：

- 保存用户已确认的目标风格、调弦、难度、乐器角色、偏好音区和禁用项。
- 对追问进行 query delta 解析，例如“那换成 funk 呢”“不要开放弦”“给我更简单的版本”。
- 将上一轮证据、用户评分和 Verifier issue 作为下一轮检索和生成的约束。
- 对低分答案形成 bad case，进入 prompt / rerank / corpus 修正闭环。

### 0.5 Phase D：动态 Few-Shot 注入

当人工评测积累到一定数量后，从 session memory 中筛选高质量问答作为 Golden Answers：

- 过滤条件：人工评分高、Verifier 通过、证据引用完整、风格标签清晰。
- 选择策略：按 `intent`、`style`、`target_tuning`、query embedding 相似度检索 1-2 条。
- 注入位置：Answer Composer prompt 的 few-shot 区域。
- 目标：让 Math Rock、Funk、Neo-Soul、Metal、Blues 等风格回答拥有不同侧重点，而不是一个通用口吻。

### 0.6 Phase E：Prompt A/B 与回归评测

Prompt 已纳入版本控制，后续要把 prompt 当成代码一样评测：

- 每次 query 保存 normalizer/composer/verifier prompt version。
- 前端增加 Prompt A/B 对比入口。
- 对同一 query 同时跑 `composer_v1.0` 和 `composer_v1.1`。
- 指标包括 schema 合法率、证据引用完整率、Verifier pass rate、人工评分、延迟和成本。

### 0.7 Phase F：GP5 / 乐谱分析 Agent

最终产品目标是处理吉他谱而不是只回答文本问题。后续 GP5 链路建议顺序：

1. 本地解析 `.gp5` / MIDI，提取 BPM、段落、riff、节奏型、和声进行、调性、调弦和技术标签。
2. 将分析结果转成 QueryPlan 的上下文字段。
3. RAG 检索匹配教材证据、风格语汇和可视化指型。
4. Composer 输出编配分析、替代方案、练习路径和可视化参考。
5. Verifier 检查建议是否与乐谱事实冲突。

### 0.8 当前阶段结论

Full Chain、混合视觉召回、canonical 精确补召回和领域 rerank 已经能够稳定联动。下一阶段优先实现独立 Answer Verifier / Critic Agent，并让 Session Memory、人工反馈、Prompt 版本和回归用例形成闭环；数据扩充继续保留为按风格逐步补充，而不是当前主阻塞项。

## 1. 项目定位

本项目是一个面向吉他编曲分析与灵感生成的本地 Agentic RAG / Knowledge Graph 系统。目标不是让 LLM 仅凭通用乐理知识泛泛回答，而是把吉他教材、风格课程、指板图、练习答案图、知识图谱和后续 GP5/乐谱分析结果组织成一个可检索、可追溯、可评测、可扩展的工程系统。

当前项目已经从“知识库构建”推进到“全链路 RAG 验证”阶段：

```text
用户 Query
-> LLM Query Normalizer
-> Text / Visual Caption / KG 多路召回
-> canonical + 规则 rerank
-> 可选 Qwen3 rerank
-> Evidence Bundle
-> LLM Answer Composer
-> 前端 Full Chain 展示与人工评测
```

最终目标是面向吉他编曲用户：

- 输入自然语言问题，后续可扩展为 `.gp5` / MIDI / 音频分析结果。
- 输出带证据引用的 riff、rhythm、voicing、指型、风格迁移和编配建议。
- 在前端可视化对应教材文本、视觉指板图、KG 关系和生成答案。

## 2. 当前成果快照

### 2.1 已完成能力

数据处理与知识构建：

- MinerU / Markdown 教材解析流程。
- 中文教材文本清洗。
- LLM 知识图谱抽取。
- Markdown 人工审核流程。
- Neo4j 本地图谱导入。
- Chroma 文本向量库。
- Chroma 视觉 caption 向量库。
- 本地 Qwen3 embedding 后端。
- SQLite embedding cache。
- VLM 视觉降维 caption 流程。
- 《吉他指板手册》题目级练习答案图切块、caption 和 canonical terms。

RAG 与 Agentic 链路：

- LLM Query Normalizer：自然语言 query -> QueryPlan。
- 多路召回：`fretboard_text`、`style_text`、`visual_caption`、`kg`。
- canonical visual retrieval：解决中英文调性/和弦/术语对照。
- Rhythmic Visual Retrieval：对 riff、谱例、拍号和非常规节拍 query 优先召回 `tab_excerpt / riff_tab`。
- domain rule rerank：处理风格边界、调弦边界、视觉需求、练习图使用边界。
- Qwen3-Reranker-0.6B 本地 rerank。
- Evidence Bundle 输出与 Markdown/JSON 报告。
- Answer Composer：基于证据生成结构化编曲建议。
- Theory Checks：答案中强制进行和弦构成、开放弦/tension 等乐理自检。
- 前端 Full Chain 测试模块。
- 前端图片证据侧栏：显示答案引用的视觉图片和文本 evidence 的 image_refs 对照。

前端与评测：

- FastAPI 后端。
- 前端 Workbench：
  - Dashboard
  - Datasets
  - Chunks
  - Visual Evidence
  - RAG Query
  - Full Chain
  - Graph
  - Eval Reports
- 人工 query 采集与日志保存。
- Query Normalizer 反馈评分表。
- RAG / rerank / Full Chain smoke reports。

### 2.2 当前代表性报告

```text
data/eval/FULL_CHAIN_RAG_EXECUTION_REPORT.md
data/eval/RERANK_BACKEND_INTEGRATION_REPORT.md
data/eval/RERANK_FRONTEND_EXPANSION_REPORT.md
data/eval/qwen_reranker_smoke_ab_report.md
data/eval/answer_composer_theory_check_smoke.md
data/eval/CANONICAL_RETRIEVAL_BRANCH_REPORT.md
data/eval/QUERY_NORMALIZER_INTEGRATION_REPORT.md
```

## 3. 总体架构

```text
Raw Materials
  data/book
  data/scores
  data/练习解答（图片）
        |
        v
Document Processing
  MinerU OCR / layout / Markdown / image crops
  text cleaning
  visual segmentation
        |
        v
Knowledge Extraction
  LLM KG extraction
  multimodal KG supplement
  manual markdown review
        |
        +--------------------+
        |                    |
        v                    v
Neo4j Knowledge Graph     Chroma Evidence Store
  concepts / relations      text chunks
  style / technique         visual captions
  constraints               local embeddings
        |                    |
        +---------+----------+
                  |
                  v
Agentic RAG Runtime
  Query Normalizer
  retrieval planner
  multi-tool retrieval
  canonical retrieval
  rule rerank
  Qwen rerank
  evidence bundle
  answer composer
        |
        v
Frontend Workbench
  evidence display
  image evidence sidebar
  query feedback
  reports
```

## 4. 数据与知识层

### 4.1 文本证据层

当前主要文本来源：

- 《吉他指板手册》清洗正文。
- Cory Wong Funk 节奏吉他课程文本。
- Math Rock 文本课程。
- Math Rock PDF 教材文本。

核心 collection：

```text
guitar_fretboard_handbook_text_qwen3_06b
guitar_text_chunks_qwen3_06b
```

《吉他指板手册》正文全文清洗层：

```text
script:
  scripts/clean_fretboard_handbook_text.py

output:
  data/processed/fretboard_handbook/text_clean/

collection:
  guitar_fretboard_handbook_text_qwen3_06b

chunks:
  174
```

清洗原则：

- 保留章节、学习目标、概念正文、练习题干和有文字内容的答案。
- 纯图片答案不进入文本 embedding。
- 图片答案统一由题目级视觉 caption 层负责。

### 4.2 视觉证据层

视觉层采用：

```text
VLM 离线 caption
-> caption 文本入 Chroma
-> query 时按文本语义召回
-> 前端展示原图
```

正式视觉层：

```text
data/processed/fretboard_handbook/question_answer_visual_caption_layer/
guitar_fretboard_answer_captions_qwen3_06b
```

特点：

- 每个练习答案图按题号/小题号/crop/caption 作为证据粒度。
- caption 包含调性、根音、指型、把位、图形说明、编配价值。
- 前端 Full Chain 可以展示答案实际引用的 visual evidence 图片。

### 4.3 canonical terms 层

为解决中英文术语不一致问题，项目增加了 canonical terms：

```text
G minor / G小调 -> key:g_minor
Fmaj7 -> root:f + chord_quality:maj7
scale pattern / 指型图 -> visual_type:scale_pattern
open string / 开放弦 -> technique:open_string
```

当前流程：

```text
caption text
-> LLM 离线抽取 canonical_terms
-> sidecar JSONL
-> query_plan canonical_terms
-> canonical visual branch
```

代表文件：

```text
data/processed/fretboard_handbook/question_answer_visual_caption_canonical/
scripts/extract_caption_canonical_terms.py
scripts/merge_caption_canonical_batches.py
```

### 4.4 Neo4j KG 层

Neo4j 保存抽象知识关系，而不是承载全部视觉练习图。

主要节点与关系：

```text
style
technique
feature
voicing
chord
scale
tuning
heuristic
caution
task
```

常见关系：

```text
ENABLES
SUGGESTS
CONSTRAINS
CAUTIONS
EVOKES
CAN_INSPIRE
CONFLICTS_WITH
```

KG 定位：

- 解释风格、技法、约束和编配启发之间的关系。
- 不把大量练习 caption 平铺进主 KG，避免图谱稀释。
- 视觉 caption 层负责具体图形证据，KG 负责抽象关系推理。

### 4.5 本地模型层

文本 embedding：

```text
Qwen/Qwen3-Embedding-0.6B
models/embedding/qwen3-embedding-0.6b
```

本地 rerank：

```text
Qwen/Qwen3-Reranker-0.6B
models/reranker/qwen3-reranker-0.6b
```

rerank backend：

```text
scripts/rerank_backend.py
```

当前支持：

- `RERANK_BACKEND=none`
- `RERANK_BACKEND=local`
- `RERANK_BACKEND=env`

Qwen rerank 使用 causal-LM yes/no token logit 差打分。

## 5. Query 与 RAG 层

### 5.1 Query Normalizer

文件：

```text
scripts/query_normalizer.py
QUERY_NORMALIZATION_PROMPT_SPEC.md
```

职责：

- 把用户自然语言问题转换为 QueryPlan。
- 判断是否需要文本、视觉、KG、风格课程。
- 抽取调性、根音、和弦性质、风格、技法、调弦边界。
- 输出 canonical terms 和工具 query。

典型输出字段：

```json
{
  "normalized_query": "...",
  "intent": "mixed_arrangement",
  "retrieval_plan": {
    "fretboard_text": {"enabled": true, "query": "..."},
    "style_text": {"enabled": true, "query": "..."},
    "visual_caption": {"enabled": true, "query": "..."},
    "kg": {"enabled": true, "query": "..."}
  },
  "canonical_terms": ["root:f", "chord_quality:maj7"]
}
```

### 5.2 Evidence Bundle

文件：

```text
scripts/query_rag_bundle.py
```

职责：

- 执行 Chroma 检索。
- 执行 Neo4j / KG 文件 fallback 检索。
- 执行 canonical visual branch。
- 合并 text / visual / kg evidence。
- 执行规则 rerank。
- 执行可选 Qwen rerank。
- 输出 judgement 和 answer_seed。

### 5.3 Rerank 设计

当前 rerank 顺序：

```text
Chroma / KG 初召回
-> canonical visual branch
-> domain rule rerank
-> Qwen model rerank
```

domain rule rerank 负责：

- 调性和根音匹配。
- 和弦性质匹配。
- 风格边界。
- 特殊调弦边界。
- 视觉 evidence 必要性。
- 练习图作为视觉证据的边界。

Qwen rerank 负责：

- 候选内部相关性微调。
- 不替代 Query Normalizer 和规则层。

## 6. Answer Composer

文件：

```text
scripts/answer_composer.py
```

职责：

- 接收 evidence bundle。
- 生成最终中文编曲建议。
- 必须引用 `evidence_id`。
- 区分证据事实和系统推断。
- 输出不确定点。
- 输出乐理自检。

输出字段：

```json
{
  "summary": "...",
  "answer": "...",
  "evidence_used": [],
  "fretboard_options": [],
  "style_arrangement_advice": [],
  "kg_reasoning": [],
  "theory_checks": [],
  "uncertainties": [],
  "next_steps": []
}
```

当前已发现并修正的问题：

- 初版 Answer Composer 曾把 B 空弦误说成 Fmaj7 的三音。
- Prompt 加入乐理自检后，已能输出：

```text
Fmaj7 和弦内音为 F, A, C, E。
B 音在 F 大调中为 #11/Lydian 色彩音，不应称为三音。
```

代表报告：

```text
data/eval/answer_composer_theory_check_smoke.md
```

## 7. 前端 Workbench

前端是本地 Agentic RAG 研发工作台，不是公开产品。目标是：

- 看数据。
- 看图。
- 看图谱。
- 收集人工 query。
- 跑 RAG / Full Chain。
- 做人工评测。

页面：

```text
Dashboard
Datasets
Chunks
Visual Evidence
RAG Query
Full Chain
Graph
Eval Reports
```

Full Chain 页面当前支持：

- 输入编曲 query。
- 设置 top_k、kg_limit。
- 设置 rerank backend、weight、batch、max length。
- 一键运行完整链路。
- 展示最终回答。
- 展示 theory checks。
- 展示答案引用的视觉图片。
- 展示文本 evidence 的 image_refs 图片代码/路径对照。

## 8. 当前评测结果与发现

### 8.1 Qwen reranker smoke A/B

报告：

```text
data/eval/qwen_reranker_smoke_ab_report.md
```

测试 query：

- `给出G小调的吉他指型参考`
- `funk 十六分闷音 groove 伴奏怎么编`
- `Fmaj7 做 mathrock riff 怎么结合开放弦和高把位指型`

初步发现：

- G 小调视觉召回 top visual 保持正确。
- mathrock Fmaj7 的 top text / top visual 稳定。
- funk 文本 top1 有变化，需要人工判断是否更优。
- local rerank 增加耗时约 `2s-5s`。

### 8.2 Full Chain smoke

报告：

```text
data/eval/FULL_CHAIN_RAG_EXECUTION_REPORT.md
data/eval/manual_queries/manual_query_20260610_142028_753269dd36.md
```

测试 query：

```text
Fmaj7 做 math rock 开放弦 riff 怎么编配，给我可用的指型和节奏建议
```

结果：

- 完整链路跑通。
- Answer Composer 成功生成结构化答案。
- 前端可显示答案、证据、图片和 image_refs。
- 发现并修正了乐理自检缺失问题。

耗时示例：

```json
{
  "model_rerank_seconds": 7.143,
  "total_seconds": 19.986,
  "answer_composer_seconds": 40.613
}
```

## 9. 当前边界与设计决策

### 9.1 不把练习 caption 大量导入主 KG

原因：

- 视觉 caption 已经可以通过 Chroma + canonical terms 精确召回。
- 如果把所有练习图导入 Neo4j，会稀释主 KG。
- KG 应负责抽象关系，视觉层负责具体指型图。

当前边界：

```text
Visual Caption：具体图片证据
KG：风格、技法、编配关系和约束
Text RAG：教材解释和上下文 grounding
Rerank：排序和证据选择
```

### 9.2 Qwen rerank 不替代规则层

当前采用：

```text
规则层先保证边界
Qwen rerank 后做相关性微调
```

这避免模型把特殊调弦、风格不匹配或视觉相似但语义不匹配的证据强行推高。

### 9.3 Answer Composer 必须可被验证

LLM 生成答案不可避免可能出现乐理或证据使用错误，因此当前已加入：

- evidence_id 引用约束。
- theory_checks。
- uncertainties。

后续会加入独立 Verifier / Critic Agent。

## 10. 后续 Agentic 模块设计

### Phase A：可信答案

优先级最高。

1. **Answer Verifier / Critic Agent**

检查：

- evidence_id 是否存在。
- 是否把推断写成教材事实。
- 是否有乐理错误。
- 是否过度使用不精确视觉证据。
- 是否忽略 uncertainties。
- 是否违反用户调弦/风格边界。

输出：

```json
{
  "pass": true,
  "issues": [],
  "fix_suggestions": [],
  "risk_level": "low|medium|high"
}
```

2. **Answer Revision Agent**

流程：

```text
compose answer
-> verify
-> if issues: revise answer
-> verify again
-> final
```

### Phase B：检索更聪明

3. **Evidence Sufficiency Agent**

判断：

- 证据是否足够生成答案。
- 是否缺少视觉指型。
- 是否 KG 都来自特殊调弦但用户没有允许。
- text / visual / KG 是否冲突。

输出：

```json
{
  "sufficient": false,
  "missing": ["exact_visual_fingering"],
  "next_action": "retrieve_more|ask_clarification|compose_with_uncertainty"
}
```

4. **Iterative Retrieval Agent**

根据 Sufficiency Agent 的结果自动补检索：

```text
第一轮：Fmaj7 mathrock open string riff
第二轮：Fmaj7 arpeggio guitar fingering open string voicing
第三轮：F Lydian open string scale pattern
```

### Phase C：乐谱输入

5. **GP5 / Score Analysis Agent**

职责：

- 解析 `.gp5` / MIDI。
- 提取 BPM、节奏密度、调性、和声进行、段落结构、riff 特征。
- 转换成 RAG query。
- 调用当前知识系统生成分析和建议。

输出：

```json
{
  "song_features": {
    "bpm": 168,
    "key": "E minor",
    "rhythm_profile": "syncopated_16th",
    "harmony": ["Em9", "Cmaj7", "G", "D"],
    "guitar_idioms": ["open_string_drone", "tapped_dyads"]
  },
  "rag_queries": []
}
```

### Phase D：作品级工作流

6. **Session Manager**

保存：

- 输入 query / score 文件。
- QueryPlan。
- evidence bundle。
- answer。
- verifier 结果。
- 用户反馈。

7. **Report Generator**

生成最终编曲分析报告：

- 歌曲结构。
- 风格判断。
- 节奏/和声/指型建议。
- 引用证据。
- 可执行练习或改编路线。

## 11. 下一步建议

短期顺序：

```text
1. 在 Full Chain 页面人工跑 10 条 query
2. 记录答案问题：乐理、证据引用、视觉误用、KG 误迁移
3. 开发 Answer Verifier / Critic Agent
4. 给 Full Chain 页面加 verifier 结果展示
5. 再做 Answer Revision Agent
```

中期顺序：

```text
6. Evidence Sufficiency Agent
7. Iterative Retrieval Agent
8. GP5 / Score Analysis Agent
```

长期目标：

```text
从“带证据的 RAG 编曲问答”
升级为
“可分析乐谱、可规划检索、可自检答案、可生成编曲报告的 Agentic RAG 系统”
```
# Prompt Version Control Update

2026-06-10 新增 Prompt 版本控制层：

- `prompts/query_normalizer_v1.1.md`
- `prompts/answer_composer_v1.0.md`
- `prompts/answer_verifier_v0.1.md`
- `scripts/prompt_registry.py`

QueryPlan、Answer、manual query log 与 Session Memory 会记录 `prompt_versions`。这为后续 Answer Verifier、动态 Few-Shot 和 Prompt A/B 测试提供可回溯基础。
