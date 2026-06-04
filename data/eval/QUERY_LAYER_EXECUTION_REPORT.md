# Query Layer Execution Report

Date: 2026-06-04

## Scope

本轮实现并测试第一版 query 层：输入自然语言问题，输出可审查的 evidence bundle。当前版本只负责“分析问题、规划召回、组合证据、判断证据是否足够”，不直接生成最终回答。

实现文件：

- `scripts/query_rag_bundle.py`

## Core Functions

- `analyze_query`: 识别 query 意图、风格提示、理论词、技法词，以及是否需要指板文本、视觉 caption、风格文本、KG。
- `plan_retrieval`: 根据意图生成检索计划，例如 `fretboard_text`、`visual_caption`、`style_text`、`kg`。
- `search_chroma`: 查询本地 Chroma 文本/视觉 caption 向量库，使用本地 Qwen3 embedding。
- `search_kg`: 优先查询 Neo4j；如果 Neo4j 不可用，则回退到本地 `data/knowledge/**/edges.jsonl`。
- `rerank_kg_items`: 对 KG 候选结果做轻量重排，提升 query 关键词、风格关键词、技法关键词命中的关系。
- `merge_evidence`: 合并并去重文本证据、视觉证据和 KG 证据。
- `judge_bundle`: 判断证据是否足够，并给出缺失项和下一轮 query 建议。
- `render_markdown`: 输出可读 Markdown 报告，方便人工检查每轮 query 的证据边界。

## Search Backends

当前接入的正式库：

- `guitar_fretboard_handbook_text_qwen3_06b`: 指板手册清洗正文。
- `guitar_fretboard_answer_captions_qwen3_06b`: 指板练习答案题目级视觉 caption。
- `guitar_text_chunks_qwen3_06b`: funk、mathrock 等风格文本。
- Neo4j: 技法、风格、启发式关系。

## Smoke Tests

### 1. Fmaj7 -> Math Rock Riff

Query:

```text
Fmaj7琶音怎么发展成math rock风格riff
```

Result:

- intent: `mixed_arrangement`
- style_hints: `mathrock`
- plan: `fretboard_text`, `style_text`, `kg`
- text evidence: 10
- visual evidence: 0
- kg evidence: 8
- total time: 6.95s
- model load: 6.09s
- actual retrieval after model load: about 0.80s
- KG backend: Neo4j

Top KG evidence after rerank includes DADGAD/open string anchor、tapped power chord、FACGCE、open string drone、32nd note bursts 等 mathrock 相关关系。

Report:

- `data/eval/query_rag_bundle_fmaj7_mathrock.md`
- `data/eval/query_rag_bundle_fmaj7_mathrock.json`

### 2. Exercise 15 Visual/Fretboard Lookup

Query:

```text
练习15答案里D大调指型1对应哪个小调指型
```

Result:

- intent: `visual_voicing_lookup`
- plan: `fretboard_text`, `visual_caption`
- text evidence: 5
- visual evidence: 5
- kg evidence: 0
- total time: 7.06s
- model load: 6.48s
- actual retrieval after model load: about 0.53s

Top text evidence and top visual caption both命中 `D大调指型1（B小调指型2）`，说明新版题目级视觉 caption 层可以和清洗正文互相印证。

Report:

- `data/eval/query_rag_bundle_exercise15_answer.md`
- `data/eval/query_rag_bundle_exercise15_answer.json`

### 3. Funk Groove/Riff

Query:

```text
funk十六分切分节奏怎么让riff更有groove
```

Result:

- intent: `style_arrangement`
- style_hints: `funk`
- plan: `style_text`, `kg`
- text evidence: 5
- visual evidence: 0
- kg evidence: 8
- total time: 6.89s
- model load: 6.05s
- actual retrieval after model load: about 0.78s
- KG backend: Neo4j

Top text evidence 来自 Cory Wong Funk 吉他大师课，Top KG evidence 命中 ghost note、sparse funk voicing、rhythm hook、staccato bubble 等 funk 编配关系。

Report:

- `data/eval/query_rag_bundle_funk_groove.md`
- `data/eval/query_rag_bundle_funk_groove.json`

## Timing Notes

CLI 冷启动耗时主要来自本地 embedding 模型加载，约 6 秒。单次 Chroma/Neo4j 检索本身通常是 0.08 到 0.45 秒级。

后续接入 FastAPI 后，模型应作为常驻对象复用；在线 query 不应每次重新加载 embedding 模型。

## Current Limitations

- 意图识别目前是规则层，不是微调模型；优点是透明，缺点是对复杂口语 query 的边界判断还需要更多测试。
- 风格文本库目前混合了 funk、mathrock 等教材，虽然 query 层已经做轻量 boost，但后续最好增加 style-aware rerank 或按风格 collection 分层检索。
- KG 召回已经加入轻量 rerank，但实体链接还比较粗。后续可引入 Entity Linker，把 `Fmaj7`、`DADGAD`、`ghost note`、`指型1` 等稳定映射到节点 ID。
- 当前只生成 evidence bundle，不生成最终自然语言答案。下一阶段可以加入 composer，并要求每条建议绑定证据来源。

## Next Steps

1. 将 `query_rag_bundle.py` 接入后端 API，做一个 RAG Workbench 页面。
2. 增加 20 到 50 条人工 query 测试集，覆盖指板、视觉答案、funk、mathrock、混合编配。
3. 增加 style-aware rerank 与 entity linker。
4. 再考虑用小模型 LoRA 微调 query intent classifier / entity linker，作为可展示的增强模块。
