# Query Normalizer Integration Report

## 目标

把前端用户的自然语言 query 先交给已配置的 LLM API 规范化，生成稳定的 `QueryPlan`，再由 `QueryPlan` 驱动文本 Chroma、视觉 caption Chroma 与 Neo4j KG 检索。

这一步的重点不是让 LLM 直接回答问题，而是让它承担 agentic RAG 的入口规划职责：

- 改写用户原始 query 为适合检索的 `normalized_query`
- 判断意图与风格、和声、技法、指板约束
- 决定使用 `fretboard_text`、`style_text`、`visual_caption`、`kg` 哪些工具
- 为每个工具生成专用检索 query 和 reason
- 将结果写入人工 query 日志，方便后续评测集沉淀

## 新增与修改模块

### `scripts/query_normalizer.py`

新增 LLM Query Normalizer。

核心函数：

- `normalize_query(query, context, env_file)`：主入口，读取 `.env` 中的 LLM API 配置，返回清洗后的 QueryPlan。
- `LLMClient.chat_json(...)`：调用 OpenAI-compatible `/chat/completions` 接口，要求 JSON object 输出。
- `sanitize_query_plan(...)`：校验并补全 QueryPlan，确保工具开关、query、reason 存在。
- `infer_style_hints(...)`、`infer_technique_hints(...)`、`infer_harmonic_materials(...)`：当 LLM 漏填结构化槽位时，从原 query 与 normalized query 中兜底补全。

### `scripts/query_rag_bundle.py`

扩展 evidence bundle，使其可以被 LLM QueryPlan 驱动。

新增函数：

- `query_plan_enabled_tools(query_plan)`：读取 QueryPlan 中启用的工具。
- `analysis_from_query_plan(raw_query, query_plan)`：把 QueryPlan 转换为原有 `QueryAnalysis`，兼容旧评测报告。
- `plan_retrieval_from_query_plan(query_plan, top_k)`：把每个工具的专用 query 转换为 `SearchTask`。

`run_bundle(...)` 现在会优先读取 `context["query_plan"]`。如果不存在，则回退到原规则层 `analyze_query(...)`。

### `backend/app.py`

新增后端接口：

- `POST /api/query/normalize`：只运行 LLM Query Normalizer，返回 QueryPlan，并写入 `manual_query_log.jsonl`。
- `POST /api/query/run`：默认先 normalize，再运行 evidence bundle；如果 LLM normalizer 失败，会记录错误并回退到规则层。

报告增强：

- `data/eval/manual_queries/*.json` 中保存 `query_plan`
- `data/eval/manual_queries/*.md` 追加 `LLM QueryPlan` 章节
- query log 中保存 `normalized_query`、`normalizer_used`、`normalizer_error` 与完整 `query_plan`

### 前端 Query Workbench

修改文件：

- `frontend/index.html`
- `frontend/app.js`
- `frontend/styles.css`

新增交互：

- `使用 LLM Query Normalizer` 开关
- `只规范化` 按钮
- QueryPlan 展示区：显示 normalized query、intent、tools、goals 和每个工具的专用 query/reason
- 历史记录优先显示 `normalized_query`
- 人工反馈评分表：对 Schema、Intent、工具选择、槽位抽取、工具 Query、下游 Bundle 和总体效果打分

## 环境变量

`.env.example` 新增 query normalizer 专用参数：

```env
QUERY_NORMALIZER_TEMPERATURE=0
QUERY_NORMALIZER_TIMEOUT_SECONDS=60
QUERY_NORMALIZER_MAX_RETRIES=1
QUERY_NORMALIZER_MAX_OUTPUT_TOKENS=4096
QUERY_NORMALIZER_ENABLE_THINKING=false
```

这些参数与 KG 抽取的长上下文配置分开，因为 query normalizer 是短文本、低温、结构化 JSON 任务。

## 验证结果

### 1. Python 编译检查

通过：

```text
backend/app.py
scripts/query_rag_bundle.py
scripts/query_normalizer.py
```

### 2. 本地 QueryPlan dry smoke

手工塞入 QueryPlan，不调用外部 LLM，只验证 RAG bundle 能按 plan 调度工具。

结果：

```json
{
  "intent": "mixed_arrangement",
  "plan": ["fretboard_text", "style_text", "visual_caption", "kg"],
  "text": 4,
  "visual": 2,
  "kg": 3,
  "sufficient": true,
  "kg_status": "neo4j",
  "total_seconds": 6.211
}
```

报告：

- `data/eval/query_normalizer_smoke_report.md`
- `data/eval/query_normalizer_smoke_report.json`

### 3. LLM normalizer API smoke

测试 query：

```text
我想把 Fmaj7 琶音发展成 math rock 风格的开放弦 riff，有哪些把位和指型可选？
```

返回摘要：

```json
{
  "normalized_query": "Fmaj7 arpeggio math rock open string riff voicings and positions",
  "intent": "mixed_arrangement",
  "confidence": 0.87,
  "style_hints": ["mathrock"],
  "harmonic_materials": ["Fmaj7"],
  "techniques": ["riff", "开放弦", "open string", "voicing"],
  "enabled_tools": ["fretboard_text", "style_text", "visual_caption", "kg"]
}
```

### 4. 后端 `/api/query/normalize` smoke

通过 FastAPI TestClient 调用成功：

```text
HTTP 200
status: normalized
intent: mixed_arrangement
enabled_tools: fretboard_text, style_text, visual_caption, kg
```

### 5. 后端 `/api/query/run` smoke

测试 query：

```text
funk 十六分切分节奏里，如何选择更省动作的双音或三音和弦指型，让 riff 更有 groove？
```

结果：

```json
{
  "ok": true,
  "intent": "mixed_arrangement",
  "plan": ["fretboard_text", "style_text", "visual_caption", "kg"],
  "text": 6,
  "visual": 3,
  "kg": 4,
  "normalizer_error": ""
}
```

生成报告：

- `data/eval/manual_queries/manual_query_20260609_180530_c2e512fb73.md`

## 现状判断

Query 层已经从“关键词规则触发工具”升级为“LLM 规划 + 规则兜底”。

这比继续手动补关键词更适合后续 agentic RAG：

- 用户可以自然描述编曲问题
- 系统内部仍然得到稳定结构
- 人工 query 日志可以沉淀为未来 LoRA 微调数据
- 前端可以直接查看 normalizer 是否误判，而不是只看最终召回结果

## 后续建议

下一步可以围绕人工 query 评测继续收紧：

- 建立 30-50 条面向编曲用户的 query set
- 标注期望 intent、应启用工具、关键证据类型
- 分别评估 `QueryPlan Accuracy`、`Tool Selection Accuracy`、`Evidence Sufficiency`
- 积累到 300-500 条后，再考虑训练本地小模型替代 API normalizer

## 人工反馈闭环

前端 Query Workbench 已加入反馈提交入口。每次执行 `只规范化` 或 `运行 Query 层` 后，可以直接在结果区填写：

```text
Schema 合规
Intent 准确度
工具选择
槽位抽取
工具 Query 质量
下游 Bundle
总体评分
期望 Intent
期望工具
错误标签
备注
```

提交后写入：

```text
data/eval/query_normalizer_feedback.jsonl
```

这份 JSONL 是后续 prompt 迭代和小模型微调的数据来源。推荐用法：

```text
1. 每条人工 query 至少先点“只规范化”并评分。
2. 对需要检查召回质量的 query，再点“运行 Query 层”并评分下游 Bundle。
3. 每轮 prompt 修改后，对同一批 query 重新跑，比较 intent_score / tool_selection_score / slot_score / overall_score。
```
## 2026-06-09 Domain Rerank Update

本轮将 Query Normalizer 之后的候选排序从“纯向量距离 + 少量关键词加权”升级为“向量召回候选池 + 领域约束 rerank”。

### 已完成

- `scripts/query_normalizer.py`
  - 扩展 QueryPlan 约束字段：
    - `target_keys`
    - `target_roots`
    - `chord_qualities`
    - `scale_or_mode`
    - `fret_region`
    - `position_constraints`
    - `requires_exact_key`
    - `requires_exact_chord`
    - `visual_evidence_required`
    - `allow_alternate_tuning`
    - `allow_exercise_reference`
  - 即使 LLM 未显式输出这些字段，也会从中文/英文 query 中进行基础回填。

- `scripts/query_rag_bundle.py`
  - Chroma 每路先召回更大的候选池，默认约为最终 `top_k * 5`。
  - KG 先保留更大的候选池，再做领域重排。
  - 新增 `domain_rerank` metadata，记录每条 evidence 的加权/降权原因。
  - 默认将未被用户指定的 DADGAD、drop tuning、open tuning、特殊调弦证据降权，并标记为 `optional_expansion_only`。
  - 对明确调性、根音、和弦性质、把位、风格和技法的候选进行加权。

### 烟测

测试 query：

```text
D 大调旋律想转成 B 小调色彩时，有没有同把位指型可以参考，并说明适合怎样的 riff 写法？
```

输出文件：

- `data/eval/rerank_rule_smoke.md`
- `data/eval/rerank_rule_smoke.json`

结果摘要：

- RAG 链路运行成功。
- 候选池扩大后，实际参与重排的候选数为：
  - text: 41
  - visual: 25
  - kg: 24
- 最终展示仍保持：
  - text: 10
  - visual: 5
  - kg: 10
- KG top 结果未再被 DADGAD 特调节点占据。

### 后续

下一步应基于前端人工反馈继续验证：

- `G 小调指型参考`：正确视觉图是否能从第 4 条提升到 top1/top2。
- `Ab m11 / maj9#11 高把位图示`：是否优先命中 Ab 和目标和弦性质，而不是只命中相似 m11/11 图。
- `Funk C7#9 / C7b9 低把位`：是否同时保留 altered dominant voicing 与 funk 留出贝斯空间的 KG 证据。

如果 30-50 条人工 query 反馈显示规则 rerank 已稳定，再接入本地 rerank 模型做 A/B 测试。
