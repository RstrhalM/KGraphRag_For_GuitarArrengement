# Guitar Arrangement Inspiration Agent 完整项目报告

日期：2026-06-09

## 1. 项目概述

本项目是一个面向吉他编曲分析与灵感生成的本地 Agentic RAG / Knowledge Graph 系统。它的核心目标不是让大模型凭通用乐理知识直接回答“怎么编曲”，而是把吉他教材、风格课程、指板图、练习答案图、知识图谱和后续 GP5/乐谱分析结果组织成一个可检索、可追溯、可评测、可扩展的工程系统。

当前项目已经完成了从教材处理、知识抽取、人工审核、Neo4j 图谱导入、Chroma 向量库、视觉 caption 降维、本地 embedding、query 层、前后端可视化到小规模评测的完整闭环。下一阶段的重点是把现有 RAG 能力包装成 Agentic RAG：让系统能够理解用户编曲目标，主动规划检索路径，判断证据缺口，并生成带来源的编配分析与建议。

最终使用场景：

```text
输入：
  - 用户自然语言编曲问题
  - 后续可接入 GP5 / MIDI / 音频分析结果

系统处理：
  - 分析风格、调性、和声材料、节奏需求、riff / voicing / 把位需求
  - 检索教材文本、视觉 caption、Neo4j KG 关系
  - 判断证据是否足够
  - 组织可追溯 evidence bundle

输出：
  - 编曲分析
  - riff / rhythm / voicing / 指型建议
  - 可视化指板证据
  - KG 风格关系和技法启发
```

## 2. 项目定位

### 2.1 面向的问题

吉他编曲类问题有三个特点：

1. 只靠 LLM 通用知识容易泛泛而谈，缺少教材证据。
2. 许多建议需要具体落到指板、把位、voicing 和演奏动作。
3. 风格语言并不只是乐理关系，还包括节奏、右手动作、开放弦、音色、密度和乐队角色。

因此本项目把知识拆成三类证据：

```text
文本证据：
  教材正文、课程讲解、练习题干、风格课程文字。

视觉证据：
  指板图、和弦图、音阶图、练习答案图，经 VLM caption 降维后进入文本向量库。

结构化图谱：
  技法、风格、约束、启发式建议、适用条件、注意事项。
```

### 2.2 当前已落地能力

当前已完成：

- MinerU / Markdown 教材解析流程。
- 中文教材文本清洗。
- LLM 知识图谱抽取。
- 人工 Markdown 审核流程。
- Neo4j 本地图谱导入。
- Chroma 文本向量库。
- Chroma 视觉 caption 向量库。
- 本地 Qwen3 embedding 后端。
- SQLite embedding cache。
- VLM 视觉降维 caption 流程。
- 指板手册题目级练习答案图 caption 层。
- Query layer：自然语言 query -> evidence bundle。
- FastAPI 后端。
- 前端 Workbench：chunk、visual evidence、graph、report、manual query collector。
- 小规模 RAG / retrieval 评测。

### 2.3 当前未完成但已预留的能力

后续重点：

- GP5 / MIDI / 音频分析结果接入。
- Agent Planner / Critic / Composer。
- Entity Linker。
- Style-aware rerank。
- 前端最终回答生成视图。
- LoRA 微调 query intent classifier 或 entity linker。
- 更多风格教材扩展。

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
  nodes / edges             text chunks
  relations                 visual captions
  constraints               local embeddings
        |                    |
        +---------+----------+
                  |
                  v
Query Layer
  analyze_query
  plan_retrieval
  search_chroma
  search_kg
  merge_evidence
  judge_bundle
        |
        v
RAG Workbench
  manual query collection
  evidence bundle display
  reports
        |
        v
Future Agentic RAG
  planner
  retriever tools
  critic
  composer
  GP5 analysis tools
```

## 4. 数据与知识层

### 4.1 原始资料层

当前项目使用的资料类型：

- 中文吉他指板教材。
- Funk 节奏吉他课程文本。
- Math Rock 文本课程。
- Math Rock PDF 教材。
- 指板练习答案图片。

原始资料不提交到 GitHub。当前 `.gitignore` 已忽略：

```text
data/book/
data/sources/
data/scores/
data/练习解答（图片）/
data/processed/
data/chroma/
models/
.env
```

这样做的原因：

- 避免提交版权教材、原始图片和大体量向量库。
- 让 GitHub 仓库更像工程作品集。
- 保留数据处理脚本和轻量 KG / eval 样例，便于展示工程能力。

### 4.2 文本清洗层

《吉他指板手册》经过专门清洗，输出独立文本层：

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

chunk 类型：

```text
chapter_intro: 1
lesson_goal: 22
concept: 65
exercise_prompt: 59
answer_text: 27
```

清洗策略：

- 跳过重复书目信息。
- 保留章节、学习目标、概念正文、练习题干。
- 纯图片答案不进入文本 embedding。
- 有文字内容的答案作为 `answer_text` 保留。
- 视觉答案图交由题目级 caption 层处理。

这个设计避免文本 RAG 被 OCR 图像残片污染，同时保留教材概念解释。

### 4.3 知识图谱层

Neo4j 用于保存结构化关系。当前图谱主要包含：

- 技法与风格关系。
- 风格语言与编配启发。
- 指板、音程、和弦、琶音、调式、voicing 等概念。
- 适用条件、限制、注意事项。

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

图谱定位：

```text
回答“这个技法能启发什么编配动作”
回答“某个风格为什么常用这种节奏或指型”
回答“某个做法有什么限制和适用条件”
回答“从一个素材迁移到另一个风格时有哪些关系路径”
```

轻量 KG 样例保存在：

```text
data/knowledge/
```

Neo4j 导入脚本：

```text
scripts/import_kg_to_neo4j.py
scripts/export_kg_to_neo4j_cypher.py
scripts/check_neo4j_kg.py
```

### 4.4 向量证据层

Chroma 保存文本和视觉 caption 的向量索引。

当前重要 collection：

```text
guitar_text_chunks_qwen3_06b
  68 docs
  funk / mathrock / general style text

guitar_fretboard_handbook_text_qwen3_06b
  174 docs
  吉他指板手册清洗正文

guitar_fretboard_answer_captions_qwen3_06b
  389 docs
  指板手册题目级练习答案视觉 caption

guitar_visual_captions_qwen3_06b
  60 docs
  早期视觉 caption 实验库

guitar_visual_chunks
  504 docs
  原始视觉 embedding 旧库，当前不是主证据层
```

当前主路线：

```text
文本：
  本地 Qwen3 embedding -> Chroma

视觉：
  VLM 生成结构化 caption -> 本地文本 embedding -> Chroma
```

放弃“在线直接图片 embedding 作为主检索”的原因：

- 图片相似性容易跨章节误召回。
- 指板图真正需要匹配的是音乐语义，不只是视觉外观。
- VLM caption 可以把图转换成乐理语言。
- 后续 query 检索变成文本到文本，速度更快，也更易评测。

### 4.5 视觉 caption 层

项目中最重要的视觉层是《吉他指板手册》练习答案图。

处理过程：

1. 本地切分练习答案图片。
2. 人工审核题目级切块。
3. 将题目、答案图、上下文一起交给 VLM。
4. 生成结构化 caption。
5. all accept 后构建正式 caption layer。
6. 用本地 Qwen3 embedding 入 Chroma。

正式输出：

```text
data/processed/fretboard_handbook/question_answer_visual_caption_layer/
guitar_fretboard_answer_captions_qwen3_06b
389 docs
```

重要边界：

练习题编号不是最终用户 query 的主入口。练习答案图的作用是校准 VLM 是否读懂指板图，并在正式编曲 query 中作为可视化指型证据。

例如正式 query 应该是：

```text
D 大调旋律想转成 B 小调色彩时，有没有同把位指型可以参考？
```

而不是：

```text
练习15答案里 D 大调指型1对应哪个小调指型？
```

后者只保留为 caption 回归测试。

## 5. 核心模块说明

### 5.1 `scripts/query_rag_bundle.py`

这是当前 Agentic RAG 的核心前置模块。它不生成最终回答，而是构造 evidence bundle。

核心数据结构：

```python
@dataclass
class QueryAnalysis:
    query: str
    intent: str
    style_hints: list[str]
    theory_terms: list[str]
    technique_terms: list[str]
    needs_fretboard_text: bool
    needs_visual: bool
    needs_style_text: bool
    needs_kg: bool

@dataclass
class SearchTask:
    name: str
    backend: str
    collection: str | None
    query: str
    top_k: int
    reason: str

@dataclass
class EvidenceItem:
    evidence_id: str
    evidence_type: str
    source_id: str
    title: str
    content: str
    score: float
    metadata: dict

@dataclass
class EvidenceBundle:
    query: str
    analysis: QueryAnalysis
    plan: list[SearchTask]
    text_evidence: list[EvidenceItem]
    visual_evidence: list[EvidenceItem]
    kg_evidence: list[EvidenceItem]
    judgement: dict
    answer_seed: dict
    timings: dict
```

核心函数：

```text
analyze_query
  识别 query 意图、风格、理论词、技法词，判断需要哪些证据。

plan_retrieval
  将 QueryAnalysis 转成多个 SearchTask。

search_chroma
  检索本地 Chroma 文本库或视觉 caption 库。

search_kg
  优先查 Neo4j，失败时回退到 data/knowledge/**/edges.jsonl。

rerank_kg_items
  对 KG 候选做轻量重排，提升风格、技法和 query 词命中的关系。

merge_evidence
  合并 text / visual / KG 证据并去重。

judge_bundle
  判断证据是否足够，生成 missing / warnings / next_queries。

render_markdown
  将 bundle 输出为可读报告。
```

当前接入的正式库：

```python
COLLECTIONS = {
    "fretboard_text": "guitar_fretboard_handbook_text_qwen3_06b",
    "visual_caption": "guitar_fretboard_answer_captions_qwen3_06b",
    "style_text": "guitar_text_chunks_qwen3_06b",
}
```

缓存优化：

```text
get_cached_embedder
get_cached_chroma_client
```

作用是在 FastAPI 常驻进程里复用本地 embedding 模型和 Chroma client，避免每次 query 都重新冷加载模型。

### 5.2 `backend/app.py`

后端使用 FastAPI，承担本地工作台 API。

核心数据源配置：

```text
CHUNK_SOURCES
MARKDOWN_CHUNK_SOURCES
VISUAL_SOURCES
BOOKS
```

已有基础 API：

```text
GET /api/dashboard
GET /api/sources
GET /api/books
GET /api/chunks
GET /api/chunk
GET /api/visuals
GET /api/graph/summary
GET /api/graph/filters
GET /api/graph/search
GET /api/reports
GET /api/report
GET /api/file
```

本轮新增 query API：

```text
GET /api/query/prompts
GET /api/query/logs
POST /api/query/save
POST /api/query/run
```

新增 request model：

```python
class QueryRunRequest(BaseModel):
    query: str
    notes: str
    tags: list[str]
    context: dict[str, Any]
    top_k: int
    kg_limit: int

class QuerySaveRequest(BaseModel):
    query: str
    notes: str
    tags: list[str]
    context: dict[str, Any]
    status: str
```

`POST /api/query/run` 的流程：

```text
1. 接收人工 query、tags、notes、top_k、kg_limit。
2. 组装 argparse.Namespace。
3. 调用 run_bundle。
4. 写入 data/eval/manual_queries/*.md / *.json。
5. 写入 data/eval/manual_query_log.jsonl。
6. 返回 bundle、report path、log item。
```

### 5.3 `frontend/`

前端是本地只读/半交互工作台。

已有视图：

```text
Dashboard
Datasets
Chunks
Visual Evidence
Graph
Eval Reports
```

新增视图：

```text
RAG Query
```

RAG Query 页面功能：

- 人工 query 输入。
- tags / top_k / kg_limit / notes。
- 保存 query 草稿。
- 运行 query 层。
- 展示 Query Analysis。
- 展示 Judgement 和 Timings。
- 展示 Text Evidence / Visual Evidence / KG Evidence。
- 展示人工 query 历史。
- 提供 query 模板和评测提示。

前端 query 设计提示强调：

```text
面向编曲任务，不面向练习编号。
写清风格目标。
写清和声材料和演奏限制。
需要具体指型时明确要求可视化指型、和弦图或把位参考。
```

### 5.4 `scripts/local_text_embedding.py`

本地 embedding backend，当前使用：

```text
Qwen/Qwen3-Embedding-0.6B
本地路径：models/embedding/qwen3-embedding-0.6b
维度：1024
device：cuda
```

核心类：

```python
class LocalTransformerEmbedder:
    def embed(self, texts: list[str], batch_size: int = 8) -> list[list[float]]:
        ...
```

内部策略：

- `AutoTokenizer.from_pretrained`
- `AutoModel.from_pretrained`
- attention mask mean pooling
- L2 normalize

这个模块的意义：

- 降低 API 成本。
- 提升本地可复现性。
- 让项目更适合展示工程能力。
- 为后续本地 agent 部署打基础。

### 5.5 `scripts/ingest_text_chunks_to_chroma.py`

文本入库脚本，支持：

```text
hash
api
local_qwen3
```

关键类：

```text
HashEmbedder
APIEmbedder
LocalEmbedder
```

核心流程：

```text
读取 catalog
加载 JSON / JSONL / Markdown chunks
标准化文本和 metadata
生成 embedding
写入 Chroma
写入 collection metadata
```

### 5.6 `scripts/build_fretboard_answer_caption_layer.py`

用于构建正式指板答案 caption 层。

核心作用：

```text
读取已审核的 visual_caption_review.md / jsonl
标准化题号、小题号、视觉类型、音乐对象、caption
输出 accepted_all.jsonl
生成 review/report
```

这个模块把早期“图片大块检索”升级成“题目级视觉证据检索”。

## 6. 人工审核流程

项目没有完全依赖 LLM 自动抽取，而是建立了人工审核闭环。

### 6.1 KG 审核

流程：

```text
LLM 抽取 JSON
  -> render review markdown
  -> 用户 accept / revise / reject
  -> sync review markdown
  -> accepted_edges.jsonl
  -> import.cypher
  -> Neo4j
```

相关脚本：

```text
scripts/render_kg_review_md.py
scripts/sync_kg_review_md.py
scripts/curate_reviewed_kg.py
scripts/export_kg_to_neo4j_cypher.py
scripts/import_kg_to_neo4j.py
```

### 6.2 视觉 caption 审核

流程：

```text
本地图像切块
  -> 人工审核 bbox / question segment
  -> VLM 生成 caption
  -> 用户 all accept
  -> build caption layer
  -> Chroma 入库
  -> 检索评测
```

这样做的原因：

- MinerU 对全图片答案页切分不稳定。
- 题目级视觉证据必须保证“图、题目、答案语义”对齐。
- 指板图 caption 是后续可视化推荐的关键证据，不能只靠大图召回。

## 7. 评测体系

当前评测不是只看生成答案，而是先评测 retrieval 和 evidence bundle。

### 7.1 评测指标

文本检索：

```text
Pass all
Source Hit@1
Source Hit@K
Keyword Hit@1
Keyword Hit@K
Avg latency/query
Median latency/query
```

视觉 caption 检索：

```text
Hit@1
Hit@K
Avg latency/query
Median latency/query
Expected visual id
Caption semantic match
```

Query bundle：

```text
intent
style_hints
retrieval plan
text evidence count
visual evidence count
kg evidence count
sufficient
confidence
missing
warnings
timings
```

### 7.2 本地 embedding 接入评测

报告：

```text
data/eval/LOCAL_EMBEDDING_QWEN3_EXECUTION_REPORT.md
```

结果摘要：

```text
模型：Qwen/Qwen3-Embedding-0.6B
模型体量：约 1.21 GB
本地路径：models/embedding/qwen3-embedding-0.6b
device：cuda
dimensions：1024
本地 Qwen3 Math Rock PDF source_focus：3/3
本地 Qwen3 全项目 global：4/4
```

模型 smoke test：

```json
{
  "device": "cuda",
  "dimensions": 1024,
  "load_seconds": 5.1535,
  "embed_seconds": 0.2762,
  "vectors": 2,
  "sample_norm": 0.99999998
}
```

### 7.3 扩展文本 RAG 评测

报告：

```text
data/eval/text_rag_expanded_rerank_report.md
```

结果：

```text
Collection: guitar_text_chunks_qwen3_06b
Docs: 68
Tests: 40
TopK: 5
Rerank: True
Pass all: 40/40
Source Hit@1: 39/40
Source Hit@K: 40/40
Keyword Hit@1: 33/40
Keyword Hit@K: 40/40
Avg latency/query: 0.048s
Median latency/query: 0.038s
```

解读：

- 本地 Qwen3 对风格文本检索已经可用。
- Rerank 对跨教材混合 collection 有明显价值。
- Source Hit@1 仅 1 例未命中，说明可以进入更大规模人工 query 评测。

### 7.4 指板手册清洗正文评测

报告：

```text
data/eval/fretboard_handbook_text_retrieval_report.md
```

结果：

```text
Collection: guitar_fretboard_handbook_text_qwen3_06b
Docs: 174
Tests: 10
TopK: 5
Rerank: True
Pass all: 10/10
Source Hit@1: 10/10
Source Hit@K: 10/10
Keyword Hit@1: 10/10
Keyword Hit@K: 10/10
Avg latency/query: 0.077s
Median latency/query: 0.040s
```

解读：

- 清洗后的指板正文适合作为理论和教材解释证据。
- 对基础指板、音阶、琶音、和弦声部等 query 命中稳定。
- 后续可作为 GP5 编配分析的底层指板知识来源。

### 7.5 正式指板答案 caption 评测

报告：

```text
data/eval/fretboard_answer_caption_retrieval_report.md
```

结果：

```text
Collection: guitar_fretboard_answer_captions_qwen3_06b
Docs: 389
Tests: 8
TopK: 5
Rerank: True
Candidates: 30
Hit@1: 8/8
Hit@K: 8/8
Avg latency/query: 0.092s
Median latency/query: 0.040s
```

解读：

- 题目级视觉 caption 可以准确召回具体指板图。
- 这证明 VLM 降维路线可行。
- 后续需要把测试 query 从“练习题校准”改成“编曲指型推荐”。

### 7.6 Query layer smoke test

报告：

```text
data/eval/QUERY_LAYER_EXECUTION_REPORT.md
```

测试 1：

```text
Fmaj7琶音怎么发展成math rock风格riff
intent: mixed_arrangement
style_hints: mathrock
plan: fretboard_text, style_text, kg
text evidence: 10
kg evidence: 8
total time: 6.95s
```

测试 2：

```text
练习15答案里D大调指型1对应哪个小调指型
intent: visual_voicing_lookup
plan: fretboard_text, visual_caption
text evidence: 5
visual evidence: 5
total time: 7.06s
```

说明：这条是视觉 caption 回归测试，不是最终用户 query。

测试 3：

```text
funk十六分切分节奏怎么让riff更有groove
intent: style_arrangement
style_hints: funk
plan: style_text, kg
text evidence: 5
kg evidence: 8
total time: 6.89s
```

### 7.7 RAG Query Workbench smoke test

报告：

```text
data/eval/RAG_QUERY_WORKBENCH_REPORT.md
```

接口测试：

```text
GET /api/query/prompts -> 200
POST /api/query/save -> 200
POST /api/query/run -> 200
```

编曲用户 query：

```text
我想把 Fmaj7 琶音发展成 math rock 风格的开放弦 riff，有哪些把位和指型可选？
```

结果：

```json
{
  "intent": "mixed_arrangement",
  "style": ["mathrock"],
  "judgement": {
    "sufficient": true,
    "confidence": 0.71,
    "missing": [],
    "warnings": [],
    "evidence_type_count": 2,
    "text_count": 6,
    "visual_count": 0,
    "kg_count": 8
  },
  "returned_text": 6,
  "returned_visual": 0,
  "returned_kg": 5,
  "total_seconds": 7.6594,
  "kg_status": "neo4j"
}
```

解读：

- query 没有明确要求视觉图，所以 visual evidence 为 0 可以接受。
- 文本 + KG 已足够支持风格 riff 分析。
- 后续应增加显式 visual query，例如“给我同把位指型图/和弦图/可视化 voicing”。

## 8. 当前 Agentic RAG 设计

当前已经完成 Agentic RAG 的底层工具链，但还没有完成最终 Agent。

### 8.1 当前已落地的 Agent 前置能力

```text
Query Analyzer
  analyze_query

Tool Planner
  plan_retrieval

Retriever Tools
  search_chroma
  search_kg

Evidence Merger
  merge_evidence

Evidence Critic
  judge_bundle

Answer Seed Builder
  build_answer_seed

Workbench
  manual query collection
  bundle report
  eval report
```

这些模块已经具备 agent 化的雏形：输入 query 后，系统不是一次性搜索一个库，而是先判断需求，再选择不同检索工具。

### 8.2 未来 Agent 角色划分

建议后续将系统拆成 5 个 agent / tool role。

#### 1. Query Planner

职责：

```text
理解用户问题
识别任务类型
提取风格、调性、和声、节奏、限制
决定需要哪些工具
```

当前对应：

```text
analyze_query
plan_retrieval
```

后续增强：

```text
LLM planner
小模型 intent classifier
Entity linker
```

#### 2. Evidence Retriever

职责：

```text
检索文本教材
检索视觉 caption
检索 Neo4j 图谱
检索 GP5 分析结果
```

当前对应：

```text
search_chroma
search_kg
```

后续增强：

```text
style-aware rerank
hybrid sparse+dense retrieval
source-scoped retrieval
visual evidence gating
```

#### 3. Evidence Critic

职责：

```text
检查证据是否足够
检查是否缺少视觉证据
检查是否风格跑偏
检查是否只有 KG 没有教材文本支撑
生成下一轮 query
```

当前对应：

```text
judge_bundle
build_next_queries
```

后续增强：

```text
LLM critic
confidence calibration
automatic second-pass retrieval
```

#### 4. Arrangement Composer

职责：

```text
基于 evidence bundle 生成最终自然语言建议
区分教材明确内容和系统推断
引用 evidence_id
输出可执行的编配动作
```

当前状态：

```text
未接入最终回答生成
已通过 answer_seed 预留结构
```

建议输出结构：

```text
结论
相关教材证据
视觉/指法证据
KG/风格关系
可操作编配建议
不确定点
```

#### 5. Score / GP5 Analyzer

职责：

```text
解析 GP5 / MIDI / 音频
提取 BPM
提取节奏型
提取和声进行
提取调性
提取 riff 轮廓
把分析结果送入 Query Planner
```

当前状态：

```text
作为下一阶段核心入口
```

## 9. Query 层设计原则

正式 query 面向吉他编曲用户，而不是教材练习编号。

好 query 示例：

```text
我想把 Fmaj7 琶音发展成 math rock 风格的开放弦 riff，有哪些把位和指型可选？

funk 十六分切分节奏里，如何选择更省动作的双音或三音和弦指型，让 riff 更有 groove？

D 大调旋律想转成 B 小调色彩时，有没有同把位指型可以参考，并说明适合怎样的 riff 写法？

在 5 到 9 品范围内，用 E 小调五声音阶做 funk riff，哪些指型适合和闷音切分结合？
```

不适合作为最终用户主评测的 query：

```text
练习15答案是什么？
练习22第6题是哪张图？
```

这些只适合作为视觉 caption 回归测试。

## 10. 面向面试的项目亮点

### 10.1 多源知识整合

项目不是简单文档 RAG，而是同时整合：

- 教材文本。
- 课程文本。
- 图片 caption。
- Neo4j KG。
- 人工审核。
- 本地 embedding。
- 前端 query collection。

### 10.2 可追溯 RAG

系统不直接输出“凭空建议”，而是先构造 evidence bundle：

```text
text_evidence
visual_evidence
kg_evidence
judgement
timings
answer_seed
```

这非常适合展示 Agentic RAG 的可控性。

### 10.3 人工审核闭环

项目中多次使用：

```text
LLM 生成
人工审核
同步入库
重新评测
```

这体现了现实 RAG 项目中比“调 prompt”更重要的数据治理能力。

### 10.4 本地模型能力

本地 Qwen3 embedding 已接入并完成评测，说明项目不是完全依赖 API。

后续可以扩展：

```text
LoRA 微调 Query Intent Classifier
LoRA 微调 KG Entity Linker
本地 rerank model
```

### 10.5 领域特化视觉降维

VLM caption 不是泛泛描述图片，而是要求输出音乐语义：

```text
根音
调性
音阶/和弦类型
指型
把位
构成音
应用价值
检索关键词
```

这比直接图片 embedding 更适合指板图检索。

## 11. 当前限制

### 11.1 Query intent 仍是规则层

当前 `analyze_query` 依靠关键词和规则判断需求。优点是透明，缺点是复杂口语 query 可能判断不稳定。

改进方向：

```text
收集人工 query
构造 intent 标签
小模型 LoRA 微调 intent classifier
替换部分规则
```

### 11.2 视觉证据 gating 还需要优化

当前只有 query 明确出现视觉相关词时才会进入视觉 caption 检索。真实用户可能不会写“给我图”，但问题本身其实需要指型。

改进方向：

```text
识别 voicing / fingering / position / shape 类需求
自动加入 visual_caption task
对视觉证据设置单独 judge
```

### 11.3 风格库还不够全

当前主要覆盖：

```text
funk
math rock
midwest emo
指板基础
```

后续需要补充：

```text
blues
rock
metal
jazz guitar
neo soul
fingerstyle
country
pop rhythm guitar
```

### 11.4 最终 Composer 未接入

当前 query 层只输出 evidence bundle，不输出最终答案。这是有意设计，因为当前阶段优先保证检索质量。

下一步应接入：

```text
LLM Composer
引用 evidence_id
区分证据和推断
输出编配建议
```

### 11.5 GP5 工作流尚未接入

最终目标需要把 `.gp5` 分析结果接入 query 层。

建议 GP5 输出结构：

```json
{
  "tempo_bpm": 120,
  "key": "A minor",
  "sections": [],
  "chord_progression": ["Am", "F", "C", "G"],
  "rhythm_features": [],
  "riff_features": [],
  "technique_features": [],
  "style_hints": []
}
```

然后作为 `context_json` 输入 `run_bundle`。

## 12. 后续路线图

### Phase 1：完善人工 query 评测

目标：

```text
通过前端 RAG Query Workbench 收集 20 到 50 条真实编曲 query。
```

query 桶：

```text
style_arrangement
fretboard_voicing
visual_shape_recommendation
rhythm_riff_design
mixed_arrangement
gp5_analysis_context
```

产出：

```text
manual_query_log.jsonl
人工标注 expected evidence
query eval report
```

### Phase 2：视觉证据进入编曲推荐

目标：

```text
让视觉 caption 不再只是练习图校准，而是能在编曲 query 中召回具体指型图。
```

重点测试：

```text
同把位大小调转换
Fmaj7 / F7 / Fdim7 琶音指型
五声音阶 riff 指型
开放和弦 / 六九和弦 / sus4 voicing
```

### Phase 3：Agentic Composer

目标：

```text
将 evidence bundle 交给 LLM 生成最终编曲建议。
```

约束：

```text
必须引用 evidence_id
必须说明哪些是教材证据，哪些是系统推断
缺证据时不能硬答
```

### Phase 4：GP5 / MIDI 接入

目标：

```text
读取真实吉他谱，提取节奏、BPM、和声进行、调性、riff 特征。
```

然后生成 query：

```text
给定当前谱例分析结果，如何改写为 funk / mathrock / neo soul 风格？
```

### Phase 5：小模型微调

最高性价比方向：

```text
Query Intent Classifier
KG Entity Linker
```

原因：

- 输入短。
- 标签明确。
- 1.5B 小模型足够。
- 可以用现有 query log 和 KG node id 构造伪标注数据。
- 对 Agentic RAG 的 tool planning 有直接价值。

建议训练目标：

```json
{
  "query": "Fmaj7琶音怎么发展成math rock风格riff",
  "intent": "mixed_arrangement",
  "style_hints": ["mathrock"],
  "entities": ["chord:Fmaj7", "style:math_rock", "task:riff_writing"],
  "tools": ["fretboard_text", "style_text", "kg"]
}
```

## 13. 运行与文件索引

### 13.1 本地前端

当前 FastAPI 前端入口：

```text
http://127.0.0.1:8765
```

启动方式：

```powershell
.\.venv-mineru\Scripts\python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8765
```

### 13.2 关键文件

```text
backend/app.py
frontend/index.html
frontend/app.js
frontend/styles.css

scripts/query_rag_bundle.py
scripts/local_text_embedding.py
scripts/ingest_text_chunks_to_chroma.py
scripts/build_fretboard_answer_caption_layer.py
scripts/eval_text_retrieval.py
scripts/eval_visual_caption_retrieval.py
scripts/import_kg_to_neo4j.py

PROJECT_FRAMEWORK.md
data/eval/QUERY_LAYER_EXECUTION_REPORT.md
data/eval/RAG_QUERY_WORKBENCH_REPORT.md
data/eval/LOCAL_EMBEDDING_QWEN3_EXECUTION_REPORT.md
data/eval/text_rag_expanded_rerank_report.md
data/eval/fretboard_answer_caption_retrieval_report.md
```

### 13.3 当前 Git 状态说明

当前项目有本地 Git 仓库，远端分支为：

```text
project-bootstrap
```

最新 GitHub 同步点：

```text
15bd48e Clarify user-facing query scope
```

本地已有未同步提交：

```text
c5f9356 Add RAG query workbench
```

按当前约定，后续不主动同步 GitHub，除非明确要求 push。

## 14. 总结

本项目已经从“教材转 Markdown + LLM 抽取”推进到一个完整的本地 Agentic RAG 雏形：

```text
数据处理 -> 人工审核 -> KG/Chroma 入库 -> 本地 embedding -> 评测 -> Query layer -> 前端 Query Workbench
```

它的核心价值在于：

- 不是单一 RAG，而是文本、视觉、图谱三类证据协同。
- 不是只做 demo，而是有数据治理、人工审核、评测报告和前端工作台。
- 不是只面向问答，而是朝“吉他编曲 Agent”方向设计。
- 当前 query 层已经具备 agent planner / retriever / critic 的雏形。

下一步只要接入 composer 和 GP5 分析，就可以从“可检索的知识系统”升级为“可执行编配分析的 Agentic RAG 系统”。
