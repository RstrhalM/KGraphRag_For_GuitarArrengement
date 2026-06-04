# Guitar Arrangement Inspiration Agent 项目框架

## 项目定位

本项目是一个面向吉他编曲分析与灵感生成的本地知识系统。目标不是只让 LLM 泛泛回答“怎么编曲”，而是把吉他教材、风格课程、指板图、谱例和后续 GP5/音频分析结果组织成可检索、可追溯、可评测的知识层。

最终使用场景：

- 解析 `.gp5`、MIDI 或音频特征，得到节奏型、BPM、和声进行、调性、段落结构、riff 特征。
- 检索吉他教材与风格知识，找到相关技法、指板图、声部构成、节奏语言和风格惯用法。
- 结合 Neo4j 知识图谱与 Chroma 向量证据，让 LLM 输出有出处的编配分析和建议。

## 当前系统分层

```text
原始资料层
  -> data/book, data/scores, data/练习解答（图片）

教材解析层
  -> MinerU OCR / layout / Markdown / images
  -> data/processed

知识抽取层
  -> LLM 抽取节点与关系
  -> 人工 Markdown 审核
  -> data/knowledge/*/accepted_edges.jsonl

图谱层
  -> Neo4j
  -> 技法、风格、概念、约束、建议、色彩关系

向量证据层
  -> Chroma text collection
  -> Chroma visual collection
  -> API / local embedding 可切换

缓存层
  -> SQLite embedding cache
  -> data/cache/embeddings.sqlite

评测层
  -> data/eval/*.md / *.json
  -> scripts/eval_retrieval_bundle.py
```

## 核心存储组件

### Neo4j

Neo4j 用于保存结构化知识图谱。

当前主要保存：

- 吉他技法与编配建议之间的关系。
- 风格语言，例如 funk、math rock、midwest emo。
- 指板、音程、琶音、和弦、声部构成等概念关系。
- `ENABLES`、`SUGGESTS`、`CONSTRAINS`、`CAUTIONS`、`EVOKES`、`CAN_INSPIRE`、`CONFLICTS_WITH` 等关系。

Neo4j 的定位：

```text
回答“概念之间有什么关系”
回答“某个技法能启发什么编配动作”
回答“某个做法有什么限制或避坑”
```

### Chroma

Chroma 用于保存向量证据。

当前主要 collection：

```text
guitar_text_chunks
guitar_visual_chunks
```

文本 collection 后续按 embedding backend 独立维护，避免不同维度/不同模型的向量混用：

```text
guitar_text_chunks              # API text-embedding-v4 基线
guitar_text_chunks_qwen3_06b    # 本地 Qwen3-Embedding-0.6B 文本库
guitar_visual_chunks            # qwen3-vl-embedding 视觉库
guitar_visual_captions_qwen3_06b # 早期 VLM caption 实验库
guitar_fretboard_answer_captions_qwen3_06b # 指板手册题目级答案图正式 caption 库
```

`guitar_text_chunks` 保存教材和课程文本 chunk：

- 《吉他指板手册》
- Cory Wong funk 节奏吉他课程
- math rock 文本课程

`guitar_visual_chunks` 保存教材局部图片向量：

- 指板图
- 音程图
- 琶音图
- 和弦图
- 常用和弦/音阶图

旧版《吉他指板手册》视觉 manifest 已剔除练习/答案相关图片块，练习类视觉证据只保留新版题目级答案 caption 层：

```text
data/processed/fretboard_handbook/question_answer_visual_caption_layer/
guitar_fretboard_answer_captions_qwen3_06b
```

这样可以避免同一道练习同时从 MinerU 原始图块和题目级 caption 层召回，后续练习答案图统一以题号/小题号/crop/caption 作为证据粒度。

Chroma 的定位：

```text
回答“哪段教材文本能作为证据”
回答“哪张图最接近当前问题”
回答“这个建议来自哪一页、哪一段、哪张图”
```

### SQLite

SQLite 用于保存 query embedding 缓存。

缓存文件：

```text
data/cache/embeddings.sqlite
```

缓存内容：

- `text-embedding-v4` 的文本查询向量。
- 本地文本 embedding 的 query 向量。
- `qwen3-vl-embedding` 的视觉文本查询向量。

SQLite 的定位：

```text
避免相同 query 重复调用 embedding API
让回归评测从分钟级降到秒级
降低 API 成本
保持现有 embedding 质量
```

### 本地 Text Embedding

为提升项目的离线能力、成本控制和面试展示价值，文本 embedding 增加本地 backend。

当前计划模型：

```text
Qwen/Qwen3-Embedding-0.6B
```

本地 embedding 的定位：

```text
作为 text-embedding-v4 的本地对照组
用于教材文本 chunk 和自然语言 query
不替换视觉 embedding
通过同一套 RAG eval 对比 Recall@5、Bundle Pass、耗时和成本
```

当前实现入口：

```text
scripts/local_text_embedding.py
scripts/ingest_text_chunks_to_chroma.py --embedding-provider local_qwen3
scripts/eval_text_retrieval.py
scripts/eval_retrieval_bundle.py --text-embedding-provider local_qwen3
```

模型与 collection 不混用：

```text
API 文本库：guitar_text_chunks
本地文本库：guitar_text_chunks_qwen3_06b
视觉库：guitar_visual_chunks
实验视觉 caption 库：guitar_visual_captions_qwen3_06b
正式指板答案 caption 库：guitar_fretboard_answer_captions_qwen3_06b
```

当前本地文本库：

```text
collection：guitar_text_chunks_qwen3_06b
docs：68
来源：
  mathrock_text_course：7
  cory_wong_funk_core：14
  fretboard_handbook_mineru：37
  mathrock_pdf_steve_h：10
```

《吉他指板手册》正文全文清洗层已入独立 Chroma collection：

```text
script：scripts/clean_fretboard_handbook_text.py
output：data/processed/fretboard_handbook/text_clean/
collection：guitar_fretboard_handbook_text_qwen3_06b
chunks：174
chunk types：
  chapter_intro：1
  lesson_goal：22
  concept：65
  exercise_prompt：59
  answer_text：27
review：data/processed/fretboard_handbook/text_clean/fretboard_text_clean_review.md
eval：
  data/eval/fretboard_handbook_text_retrieval_report.md
  data/eval/fretboard_handbook_text_retrieval_no_rerank_report.md
  10 tests，rerank / no-rerank 均为 10/10，Top1 均命中
```

清洗原则：从整本 MinerU Markdown 的“引言”开始，跳过重复书目信息；保留章节、学习目标、概念正文、练习题干和有文字内容的练习答案；纯图片答案不进入文本 embedding，交由新版题目级答案 caption 层负责。

### VLM 视觉降维 Caption 层

视觉证据层采用“VLM 离线降维 + 文本 embedding 在线检索”的路线：

```text
图片 + nearby_text + page/chapter context
  -> VLM structured caption
  -> local Qwen3 text embedding
  -> Chroma visual caption collection
```

目标是把和弦图、指板图、谱例图从“视觉相似检索”降维为“乐理语义文本检索”。这样用户查询 `Emaj13 省略5音`、`FACGCE open Fmaj9`、`七和弦高把位 voicing` 时，可以直接命中结构化 caption，并回链到原图。

历史试验 collection：

```text
guitar_visual_captions_qwen3_06b
```

正式题目级指板答案 collection：

```text
guitar_fretboard_answer_captions_qwen3_06b
```

当前试验脚本：

```text
scripts/build_visual_caption_candidates.py
scripts/extract_visual_captions.py
scripts/ingest_visual_captions_to_chroma.py
scripts/eval_visual_caption_retrieval.py
```

当前策略：

- VLM 只在离线 ingestion 阶段调用一次。
- 在线 query 阶段只走文本 embedding + Chroma。
- 原 `guitar_visual_chunks` 保留为 raw visual embedding fallback。
- caption 中必须记录 `image_path`、`page`、`nearby_text`，保证可回溯。

历史 visual caption 试验层：

```text
accepted caption：60 条
来源：吉他指板手册 30 条，Math Rock PDF 30 条
错误：0
collection：guitar_visual_captions_qwen3_06b
本地 embedding：Qwen3-Embedding-0.6B / CUDA / 1024 dims
定位：早期路线验证，不作为正式指板答案图证据层
```

当前正式指板答案 caption 层：

```text
accepted caption：389 条
来源：《吉他指板手册》练习答案题目级 crop
粒度：每道题/小题对应单张 crop，metadata 保留 exercise_number、subquestion_number、crop_path、bbox、question_text
collection：guitar_fretboard_answer_captions_qwen3_06b
本地 embedding：models/embedding/qwen3-embedding-0.6b / CUDA / 1024 dims

小规模题目级回归评测：
  测试数：8
  rerank Hit@1：8/8
  Hit@5：8/8
  平均耗时：0.092s/query
  中位耗时：0.040s/query
```

历史试验层评测：

```text

扩容后回归评测：
  测试数：10
  Hit@1：10/10
  Hit@5：10/10
  平均耗时：0.073s/query
  中位耗时：0.049s/query

扩展视觉 query 评测：
  测试数：30
  无 rerank Hit@1：29/30
  rerank Hit@1：30/30
  Hit@5：30/30
  rerank 平均耗时：0.048s/query
  rerank 中位耗时：0.037s/query
  修正 case：同页 DAEAC#E 总览图压过具体 9 品 Am9/G#m7b5 图块，rerank 后具体图块升至 Top1

smoke 回归评测：
  测试数：10
  rerank Hit@1：10/10
  rerank Hit@5：10/10
  平均耗时：0.066s/query
```

报告文件：

```text
data/processed/visual_caption_trial/visual_caption_review.md
data/processed/visual_caption_batch_002/visual_caption_review.md
data/processed/visual_caption_layer/visual_caption_accepted_all.jsonl
data/processed/visual_caption_layer/visual_caption_layer_report.json
data/eval/visual_caption_trial_report.md
data/eval/visual_caption_trial_report.json
data/eval/visual_caption_layer_report.md
data/eval/visual_caption_layer_report.json
data/eval/visual_caption_layer_expanded_report.md
data/eval/visual_caption_layer_expanded_report.json
data/eval/visual_caption_layer_expanded_no_rerank_report.md
data/eval/visual_caption_layer_expanded_no_rerank_report.json
data/eval/visual_caption_layer_expanded_rerank_report.md
data/eval/visual_caption_layer_expanded_rerank_report.json
data/eval/visual_caption_layer_rerank_smoke_report.md
data/eval/visual_caption_layer_rerank_smoke_report.json
```

## 当前数据资产

```text
data/
  book/
    原始教材 PDF / 文本课程

  processed/
    MinerU 转换结果
    KG 抽取中间结果
    人工审核 Markdown
    视觉层 manifest

  knowledge/
    arrangement_kg/
    arrangement_kg_chunks_006_010/
    arrangement_kg_integrated_chunks_011_015/
    arrangement_kg_visual_answer_chunks_002_010/
    arrangement_kg_cory_wong_funk_core/
    arrangement_kg_mathrock_text/
    kg_aliases.json

  chroma/
    Chroma 本地向量库

  cache/
    embeddings.sqlite

  eval/
    retrieval_bundle_report*.md
    retrieval_bundle_report*.json
```

## 当前教材与知识来源

### 《吉他指板手册》

用途：

- 指板结构
- 根音型式
- 音程
- 五声音阶
- 大小调音阶
- 琶音
- 三和弦/七和弦
- 延伸和弦
- 常用和弦图

当前处理方式：

```text
PDF
  -> MinerU OCR / layout
  -> Markdown + image blocks
  -> 文本 KG 抽取
  -> 视觉答案/图片补充
  -> Neo4j + Chroma text + Chroma visual
```

视觉层当前分为：

```text
P0_root_fingering_forms
P1_scales_intervals
P2_arpeggios_chords
P3_common_scales_chords
```

### Cory Wong Funk 课程

用途：

- funk 节奏吉他
- muted chuck
- ghost note
- bubble groove
- sparse voicing
- timing / groove / density / range / tone / space

当前处理方式：

```text
课程文本
  -> LLM KG 抽取
  -> 人工 all accept
  -> Neo4j
  -> Chroma text
```

### Math Rock 文本课程

用途：

- DADGAD
- alternate tuning
- open string drone
- two hand tapping
- tapped power chord
- tapped dyads
- pull-off to open string
- non-diatonic passing chord

当前处理方式：

```text
课程文本
  -> LLM KG 抽取
  -> 人工 all accept
  -> Neo4j
  -> Chroma text
```

## 风格教材扩展规范

后续会持续加入 blues、metal、jazz、bossa、country、fingerstyle、fusion、pop rock 等吉他相关教材。新增教材必须按统一 source package 接入，避免每本教材各自生成零散目录、metadata 和 collection。

### 目录结构

每个风格教材使用统一目录：

```text
data/processed/style_sources/{style_family}/{source_slug}/
  raw_info.json
  clean_text.md
  chunks.json
  kg_review.md
  kg_review.all_accept.jsonl
  ingest_report.md
  eval_report.md
```

示例：

```text
data/processed/style_sources/blues/texas_blues_rhythm/
data/processed/style_sources/metal/djent_riffing/
data/processed/style_sources/jazz/chord_melody_intro/
data/processed/style_sources/bossa/bossa_guitar_comping/
data/processed/style_sources/country/hybrid_picking_licks/
```

### Source Metadata

每个教材必须有稳定 `source_id` 和风格 metadata：

```json
{
  "source_id": "style_blues_texas_rhythm",
  "title": "Texas Blues Rhythm Guitar",
  "style_family": "blues",
  "substyles": ["texas_blues", "shuffle", "swing"],
  "instrument_scope": ["electric_guitar"],
  "knowledge_scope": ["rhythm", "riff", "comping", "tone"],
  "input_type": "pdf | transcript | markdown",
  "status": "cleaned | kg_reviewed | embedded | evaluated"
}
```

字段含义：

```text
style_family
  主风格，用于 query router 的第一层路由和 source boost。

substyles
  子风格，例如 texas_blues、neo_soul、djent、bebop、bossa_nova。

instrument_scope
  电吉他、木吉他、指弹、七弦、开放调弦等适用范围。

knowledge_scope
  rhythm、riff、comping、voicing、tone、technique、song_form、improvisation。

status
  表示当前 source 是否已经清洗、KG 审核、embedding、评测。
```

### Chroma Collection 策略

当前阶段保留综合风格文本库：

```text
guitar_text_chunks_qwen3_06b
```

当风格教材数量增加后，拆成两层：

```text
综合风格库：
  guitar_style_text_chunks_qwen3_06b

专项风格库：
  guitar_style_funk_qwen3_06b
  guitar_style_mathrock_qwen3_06b
  guitar_style_blues_qwen3_06b
  guitar_style_metal_qwen3_06b
  guitar_style_jazz_qwen3_06b
```

拆分标准：

```text
单一风格 source 超过 100-200 chunks
或 query router 经常把某风格误召回到其他风格
或需要单独做风格专项评测
```

### KG 命名规范

风格教材进入 Neo4j 时，节点命名必须可跨风格复用。

推荐节点前缀：

```text
style:funk
style:mathrock
style:blues
style:jazz

technique:muted_16th
technique:hybrid_picking
technique:two_hand_tapping
technique:string_skipping

rhythm:shuffle
rhythm:straight_16th
rhythm:odd_grouping
rhythm:clave_like_accent

riff:pedal_tone
riff:call_response
riff:chromatic_approach

tone:clean_compression
tone:edge_of_breakup
tone:high_gain_tight_mute

arrangement_task:build_contrast_section
arrangement_task:thicken_chorus
arrangement_task:create_intro_hook
```

关系类型沿用当前项目，不为每种风格发明新关系：

```text
enables
suggests
evokes
constrains
can_inspire
conflicts_with
cautions
```

### 新增风格教材流程

统一接入流程：

```text
1. raw PDF / transcript / markdown
2. 清洗为 clean_text.md
3. 结构化分块 chunks.json
4. LLM KG 抽取候选
5. 人工 review markdown
6. all accept / revise 后写入 KG
7. 本地 Qwen3 embedding 入 Chroma
8. 小规模风格专项 eval
9. 更新 source catalog 和 PROJECT_FRAMEWORK.md
```

### Query Router 预留

新增风格教材后，query router 通过 metadata 做 source boost：

```text
query 包含 funk / groove / muted / ghost note
  -> boost style_family=funk

query 包含 mathrock / tapping / DADGAD / odd grouping
  -> boost style_family=mathrock

query 包含 blues / shuffle / turnaround / bending
  -> boost style_family=blues

query 包含 metal / palm mute / djent / alternate picking
  -> boost style_family=metal

query 包含 jazz / chord melody / ii-V-I / shell voicing
  -> boost style_family=jazz
```

风格教材只补与吉他编曲、节奏、riff、指法、voicing、tone、技法迁移相关的知识。通用和声理论不作为主要入库目标，除非它在吉他指法或风格编配中有明确用途。

## 检索流程

当前 RAG 检索流程：

```text
用户问题
  -> 判断 style / source / visual intent
  -> 生成 text embedding
       -> API backend: text-embedding-v4
       -> local backend: Qwen3-Embedding-0.6B
  -> SQLite cache lookup
  -> Chroma text 检索
  -> 如果需要视觉证据：
       -> local Qwen3 text embedding
       -> Chroma visual caption 检索
       -> 回链 image_path/page/nearby_text
       -> 必要时再调用 raw visual embedding fallback
       -> rerank
  -> Neo4j 查询相关关系
  -> 组合证据给 LLM
```

## Query 层设计

Query 层定位为 Agentic-ready RAG 的证据编排层。它不直接生成最终回答，而是把自然语言问题、可选 GP5/音频分析结果和用户上下文转成结构化 evidence bundle，供后续 LLM composer 或 agent 使用。

### 输入输出

输入：

```json
{
  "query": "如何把Fmaj7琶音发展成math rock风格riff？",
  "context": {
    "gp5_features": null,
    "preferred_style": null,
    "need_visual": null
  }
}
```

输出：

```json
{
  "query_analysis": {},
  "retrieval_plan": {},
  "text_evidence": [],
  "visual_evidence": [],
  "kg_evidence": [],
  "bundle_judgement": {},
  "answer_seed": {}
}
```

### 模块拆分

Query 层按可被 agent 调用的工具链设计：

```text
analyze_query()
  -> plan_retrieval()
  -> retrieve_text()
  -> retrieve_visual_caption()
  -> retrieve_kg()
  -> merge_evidence()
  -> judge_bundle()
  -> render_report()
```

#### 1. analyze_query

识别问题意图、风格线索、理论术语、技法术语和需要的证据类型。

第一版采用规则 + 关键词，不让 LLM 自由规划：

```text
出现 指板 / 根音 / 音阶 / 琶音 / 和弦 / 音程
  -> needs_fretboard_text = true

出现 指型图 / 答案图 / 指法 / voicing / 省略音 / 高把位 / 和弦图
  -> needs_visual = true

出现 funk / mathrock / riff / 节奏 / groove / tapping / open string
  -> needs_style_text = true

出现 怎么发展 / 如何编配 / 可迁移 / 技法关系 / 风格建议
  -> needs_kg = true
```

目标输出：

```json
{
  "intent": "mixed_arrangement",
  "style_hints": ["mathrock"],
  "theory_terms": ["Fmaj7", "arpeggio"],
  "technique_terms": ["riff"],
  "needs_fretboard_text": true,
  "needs_visual": true,
  "needs_style_text": true,
  "needs_kg": true
}
```

#### 2. plan_retrieval

把 query analysis 转成检索计划。

```text
指板基础 / 乐理位置问题
  -> guitar_fretboard_handbook_text_qwen3_06b

具体指型 / 和弦图 / 答案图 / voicing 问题
  -> guitar_fretboard_answer_captions_qwen3_06b

风格 / 节奏 / riff / 编配语言问题
  -> guitar_text_chunks_qwen3_06b

技法关系 / 风格迁移 / 编配启发问题
  -> Neo4j KG
```

计划示例：

```json
{
  "searches": [
    {"name": "fretboard_text", "collection": "guitar_fretboard_handbook_text_qwen3_06b", "top_k": 5},
    {"name": "visual_caption", "collection": "guitar_fretboard_answer_captions_qwen3_06b", "top_k": 5},
    {"name": "style_text", "collection": "guitar_text_chunks_qwen3_06b", "top_k": 5},
    {"name": "kg", "backend": "neo4j", "top_k": 12}
  ]
}
```

#### 3. Retriever tools

每个知识源封装成独立工具，返回统一 evidence item：

```text
search_text_collection(collection, query, top_k)
search_visual_caption(query, top_k)
search_neo4j_terms(terms, limit)
```

统一返回结构：

```json
{
  "evidence_id": "text:fretboard_text_0079",
  "evidence_type": "text | visual_caption | kg",
  "source_id": "fretboard_handbook_clean_text",
  "title": "练习30",
  "content": "...",
  "score": 0.82,
  "metadata": {},
  "trace": {}
}
```

#### 4. merge_evidence

合并多库召回结果，重点是去重和跨层配对。

合并规则：

```text
同一本书同一章节去重
同一个 exercise_number 合并题干文本 + 答案 caption
KG 边按 source-target-relation 去重
优先保留：
  1. 指板正文概念
  2. 题目级视觉 caption
  3. 风格文本
  4. KG 关系
```

#### 5. judge_bundle

判断证据是否足够，给出缺口和下一轮 query 建议。

第一版规则：

```text
指型 / voicing 问题没有 visual_evidence
  -> insufficient

风格问题没有 style_text
  -> insufficient

编配建议问题没有 kg_evidence
  -> weak

只有 KG 没有教材文本证据
  -> weak

文本、视觉、KG 至少两类互相支持
  -> sufficient
```

输出示例：

```json
{
  "sufficient": true,
  "confidence": 0.78,
  "missing": [],
  "next_queries": []
}
```

### 数据结构

第一版使用 dataclass，保持可调试和可测试：

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
```

### 第一版实现目标

先实现命令行脚本，不急着 agent 化：

```text
scripts/query_rag_bundle.py
```

命令示例：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\query_rag_bundle.py `
  --query "Fmaj7琶音怎么发展成math rock风格riff" `
  --top-k 5 `
  --report-md data/eval/query_rag_bundle_fmaj7_mathrock.md
```

输出：

```text
data/eval/query_rag_bundle_fmaj7_mathrock.md
data/eval/query_rag_bundle_fmaj7_mathrock.json
```

Markdown 报告结构：

```text
# Query RAG Bundle Report

## Query Analysis
## Retrieval Plan
## Text Evidence
## Visual Evidence
## KG Evidence
## Bundle Judgement
## Answer Seed
```

### 设计原则

Query 层最重要的是证据边界清晰：

```text
指板正文回答理论和教材解释
视觉 caption 回答具体图形、指法、voicing 和可视化指型证据
风格文本回答风格语言、节奏和 riff
KG 回答技法关系、风格迁移和编配启发
```

练习答案图不是最终用户 query 的主要入口。它们在项目中的核心作用是：

```text
1. 校准 VLM caption 是否真的读懂具体指板图、音阶图、和弦图
2. 为编曲用户 query 提供可视化答案，例如和声替代、riff 指型、把位选择、大小调指型映射
3. 在最终回答中作为可追溯图证据，而不是要求用户按“练习编号”检索
```

因此后续正式评测集应优先使用编曲用户语言，例如：

```text
我想把 Fmaj7 琶音发展成 math rock 风格的开放弦 riff，有哪些把位和指型可选？
funk 十六分切分节奏里，如何选择更省动作的双音/三音和弦指型？
D 大调旋律想转成 B 小调色彩时，有没有同把位指型可以参考？
```

练习编号 query 只保留为 caption 层回归测试，用来检查视觉识别是否稳定。

后续 Agentic RAG 只是在这个工具链上加入 LLM planner / critic / composer，不改变底层检索工具。

## Agentic RAG 总体框架

### Query 层当前落地状态

已实现第一版命令行 query 层：

```text
scripts/query_rag_bundle.py
```

已完成三条 smoke test：

```text
Fmaj7琶音怎么发展成math rock风格riff
练习15答案里D大调指型1对应哪个小调指型
funk十六分切分节奏怎么让riff更有groove
```

其中“练习15”只作为视觉 caption 层的内部校准题，证明图像 caption 能和教材正文对上具体指型关系。最终用户 query 不应围绕练习编号设计，而应围绕编曲任务、风格目标、和声色彩、riff/voicing/把位选择来设计。

测试报告：

```text
data/eval/QUERY_LAYER_EXECUTION_REPORT.md
data/eval/query_rag_bundle_fmaj7_mathrock.md
data/eval/query_rag_bundle_exercise15_answer.md
data/eval/query_rag_bundle_funk_groove.md
```

当前 CLI 冷启动主要耗时来自本地 embedding 模型加载，约 6 秒；单次 Chroma / Neo4j 检索本身通常低于 0.5 秒。后续接入 FastAPI 时应常驻加载 embedding 模型，避免每轮 query 重复加载。

Agentic RAG 的目标不是把普通 RAG 包一层聊天，而是让系统能够围绕“吉他谱/用户问题/风格目标”主动规划证据、检查证据缺口，并生成可追溯的编配分析和建议。

### 总体链路

```text
用户自然语言 query
或 GP5 / 音频分析结果
  -> Query Understanding
  -> Retrieval Planning
  -> Tool Calling
  -> Evidence Critic
  -> Optional Query Rewrite
  -> Evidence Bundle
  -> Answer Composer
  -> Final Arrangement Advice
```

### Agentic-ready 第一版

第一版先不让 LLM 自由控制工具，而是做可解释的规则化编排：

```text
scripts/query_rag_bundle.py
  -> 规则 analyze_query
  -> 规则 plan_retrieval
  -> Chroma / Neo4j 工具调用
  -> 规则 judge_bundle
  -> Markdown / JSON evidence bundle
```

这一版重点验证：

```text
路由是否选对库
证据是否来自正确来源
文本、视觉、KG 边界是否清晰
多库结果是否能合成可用 evidence bundle
```

### Agent 角色

后续完整 Agentic RAG 可以拆成 5 个角色。

#### 1. Query Understanding Agent

职责：

```text
理解用户问题
识别风格、理论、技法、视觉需求
读取可选 GP5 features
输出 QueryAnalysis
```

输入：

```json
{
  "query": "这段riff怎么改得更像funk？",
  "gp5_features": {
    "bpm": 108,
    "key": "E minor",
    "rhythm_density": "medium",
    "syncopation": "low",
    "chord_progression": ["Em7", "A7"]
  }
}
```

输出：

```json
{
  "intent": "style_arrangement",
  "style_hints": ["funk"],
  "needs_style_text": true,
  "needs_kg": true,
  "needs_visual": false,
  "needs_score_features": true
}
```

#### 2. Retrieval Planner

职责：

```text
根据 QueryAnalysis 决定查哪些库
决定 top_k / rerank_candidates
为不同库生成 query rewrite
```

示例：

```text
funk riff 改编
  -> style_text: guitar_text_chunks_qwen3_06b
  -> kg: Neo4j style/technique/rhythm nodes
  -> no visual unless query asks for voicing/指型图

Emaj13 省略5音指法
  -> fretboard_text: guitar_fretboard_handbook_text_qwen3_06b
  -> visual_caption: guitar_fretboard_answer_captions_qwen3_06b
  -> kg: chord/voicing relation if available

Fmaj7 琶音发展成 math rock riff
  -> fretboard_text
  -> style_text
  -> kg
  -> visual_caption optional
```

#### 3. Retriever Tools

职责：

```text
执行实际检索
统一 evidence item 格式
记录 source trace
```

工具：

```text
search_fretboard_text()
search_fretboard_visual_caption()
search_style_text()
search_neo4j_graph()
search_gp5_feature_index()  # 后续加入
```

#### 4. Evidence Critic

职责：

```text
检查证据是否足够
判断是否存在错库召回
判断是否需要二次查询
为 answer composer 标记证据置信度
```

判断规则：

```text
具体指法问题没有 visual_caption
  -> 要求补查 visual_caption

风格改编问题没有 style_text
  -> 要求补查 style_text

只有 KG 没有教材文本支撑
  -> 降低置信度

召回来源全来自非目标风格
  -> 标记 possible_style_mismatch

同一 exercise_number 同时命中题干和答案 caption
  -> 标记 strong_grounding
```

#### 5. Answer Composer

职责：

```text
基于 evidence bundle 生成最终回答
引用文本证据、视觉证据、KG 关系
明确不确定点
给出可操作编配建议
```

输出结构：

```text
1. 结论
2. 当前素材/问题识别
3. 教材证据
4. 视觉证据
5. KG/风格关系
6. 编配建议
7. 不确定点与下一步
```

### 与 GP5 工作流的关系

GP5 解析不是替代 RAG，而是为 agent 提供结构化上下文。

GP5 本地解析目标：

```text
bpm
meter
key / mode
chord progression
riff contour
note density
syncopation
rest density
open string usage
muting / dead notes
slide / hammer / pull-off / tapping
range and position hints
section contrast
```

进入 Agentic RAG 后：

```text
GP5 features
  -> Query Understanding Agent
  -> style_hints / technique_terms / rhythm_terms
  -> Retrieval Planner
  -> 风格教材 + KG + 指板证据
  -> Answer Composer
```

示例：

```text
输入：一段 gp5 riff，检测到高开放弦比例、DADGAD、two hand tapping
Agent:
  -> style_hints = mathrock / midwest_emo
  -> search style_text for DADGAD + tapping + open string drone
  -> search KG for technique:tapped_power_chord / feature:open_string_drone
  -> output arrangement suggestions
```

### 阶段路线

#### Phase 1：Agentic-ready RAG Bundle

```text
实现 scripts/query_rag_bundle.py
输出 evidence bundle JSON/Markdown
不调用 LLM 生成最终回答
规则化 planner + critic
```

完成标准：

```text
20 条人工 query 小评测
能正确路由文本/视觉/KG
报告可读
证据边界清晰
```

#### Phase 2：前端 RAG Workbench

```text
新增查询页
展示 query analysis
展示 retrieval plan
展示 text / visual / kg evidence
展示 bundle judgement
显示耗时
```

完成标准：

```text
用户能看到系统为什么查这些库
能点开文本 chunk 和图片证据
能看到 KG 边和来源
```

#### Phase 3：LLM Composer

```text
把 evidence bundle 发送给已配置 LLM
生成最终回答
要求引用 evidence_id
不允许凭空补教材证据
```

完成标准：

```text
回答能回链证据
可以区分“教材明确说了”和“系统推断”
可以指出证据不足
```

#### Phase 4：GP5 Analysis Agent

```text
GP5 -> 本地音乐特征抽取
特征进入 QueryAnalysis
Agent 给出编配分析和建议
```

完成标准：

```text
输入真实吉他谱
输出节奏/和声/风格/技法分析
能引用教材与 KG 作为建议依据
```

### Agentic RAG 评测

评测不只看单库召回，而看完整 evidence bundle。

测试类别：

```text
1. 指板基础 query
   期望：fretboard_text 命中，visual 可选，KG 可选

2. 具体指型 / voicing query
   期望：visual_caption 必须命中，fretboard_text 辅助

3. 风格节奏 / riff query
   期望：style_text + KG 命中

4. 混合编配 query
   期望：至少两类证据互相支持

5. GP5 特征 query
   期望：score_features 触发正确风格库与 KG
```

核心指标：

```text
Router Accuracy
  该查的库是否被查到。

Evidence Hit@K
  证据包内是否包含期望文本/图片/KG。

Bundle Sufficiency
  judge_bundle 是否正确判断证据够不够。

Grounding Quality
  最终回答是否引用正确 evidence_id。

Latency
  各工具耗时和总耗时。
```

### 关键约束

```text
Agent 不能绕过证据直接编答案。
Query layer 不直接负责最终回答。
LLM planner/critic/composer 只能在工具层稳定后加入。
任何新风格教材必须携带 style_family / knowledge_scope metadata。
视觉证据优先使用结构化 caption，不优先使用 raw visual embedding。
```

## 视觉检索策略

视觉检索不是直接全库向量搜索，而是使用三层策略。

### 1. 视觉意图识别

根据 query 判断可能属于哪类视觉资料：

```text
P0_root_fingering_forms
  根音型式、根音指型、五种根音、root pattern

P1_scales_intervals
  音程、八度、纯五度、五声音阶、interval、octave、scale

P2_arpeggios_chords
  琶音、三和弦、七和弦、CAGED、arpeggio、triad

P3_common_scales_chords
  常用和弦、六和弦、九和弦、add9、6/9
```

### 2. Priority 补召回

因为指板图视觉形态很相似，单靠向量召回可能漏掉正确类别。

当前策略：

```text
先按 source 全局召回
再按推断 priority 各自补召回
合并去重
```

### 3. Rerank

visual caption 检索使用轻量 rerank。流程：

```text
Chroma 先取更宽候选池，例如 Top20
  -> 保留向量距离作为基础分
  -> query token 命中 topic/caption/nearby_text 加分
  -> 和弦名、调弦名、品位号、指型词加权
  -> 当 query 明确是具体图块需求时：
       image_block 加小分
       full_page 减小分
  -> 重排回 TopK
```

典型修正：

```text
query：DAEAC#E 第九品附近的 Am9 G#m7b5 和弦图

无 rerank：
  Top1 = DAEAC#E_tuning_chord_voicings_progressions  # 同页总览
  Top2 = DAEAC#E_tuning_chord_shape_9th_fret         # 具体图块

rerank 后：
  Top1 = DAEAC#E_tuning_chord_shape_9th_fret
```

这样可以避免“页级总览图”和“具体局部图块”距离几乎相同时，总览图压过更精确证据。

## KG Alias 层

当前 KG 抽取来自不同教材和不同批次，节点命名不可能完全一致。

因此使用：

```text
data/knowledge/kg_aliases.json
```

把用户/评测中的概念节点映射到实际图谱节点。

例子：

```text
concept:八度
  -> interval:octave
  -> technique:octave_displacement_rule
  -> pattern:octave_minus_one_fret

concept:根音
  -> concept:root_pattern_cycle
  -> concept:root_pattern_system
  -> pattern:root_shape_1
  -> pattern:root_shape_4
```

Alias 层的作用：

```text
减少同义词导致的 KG miss
让中文概念、英文概念、教材抽取 ID 能对齐
为后续 canonical node 归一做准备
```

## 评测体系

主评测脚本：

```text
scripts/eval_text_retrieval.py          # text-only 主干评测
scripts/eval_visual_caption_retrieval.py # visual caption 视觉证据评测
scripts/eval_retrieval_bundle.py
```

评测输出：

```text
data/eval/text_rag_expanded_rerank_report.md
data/eval/text_rag_expanded_rerank_report.json
data/eval/text_rag_expanded_no_rerank_report.md
data/eval/text_rag_expanded_no_rerank_report.json
data/eval/retrieval_bundle_report_expanded.md
data/eval/retrieval_bundle_report_expanded.json
```

当前评测覆盖：

- funk 文本检索
- math rock 文本检索
- Math Rock PDF 文本检索
- 指板手册文本检索
- 跨来源文本 query
- 指板视觉检索
- KG alias 命中
- bundle 组合成功率
- 每条检索耗时
- embedding cache hit/miss

核心指标：

```text
Text Top1
Text Recall@5
Text Precision@5
Visual Top1
Visual Recall@5
Visual Precision@5
Neo4j KG hit
Bundle pass
Total seconds
Text seconds
Visual seconds
KG seconds
Embedding cache rows/hits
```

当前扩展评测结果：

```text
Text-only 本地 Qwen3 RAG：
  collection：guitar_text_chunks_qwen3_06b
  docs：68
  测试数：40
  no-rerank pass：33/40
  rerank pass：40/40
  source Hit@1：39/40
  source Hit@5：40/40
  keyword Hit@5：40/40
  rerank 平均耗时：0.048s/query

Visual caption RAG：
  collection：guitar_fretboard_answer_captions_qwen3_06b
  docs：389
  测试数：8
  rerank Hit@1：8/8
  Hit@5：8/8

Visual caption 历史实验层：
  collection：guitar_visual_captions_qwen3_06b
  docs：60
  扩展测试数：30
  no-rerank Hit@1：29/30
  rerank Hit@1：30/30
  Hit@5：30/30

Bundle 综合旧评测：
测试数：22
Bundle：22/22
文本 Top1：100%
视觉 Top1：100%
KG hit：100%

缓存预热前：
  总耗时约 1362s

缓存命中后：
  总耗时约 1.31s
```

## 关键脚本说明

### 教材与 KG 抽取

```text
scripts/extract_arrangement_kg.py
scripts/extract_style_rhythm_kg.py
scripts/extract_mathrock_kg.py
scripts/extract_visual_answer_kg.py
```

用途：

```text
调用 LLM 从教材文本或视觉补充内容中抽取 KG 候选边
```

### 人工审核与同步

```text
scripts/render_kg_review_md.py
scripts/sync_kg_review_md.py
scripts/curate_reviewed_kg.py
scripts/merge_kg_review_sources.py
```

用途：

```text
将 JSONL 评审数据转为 Markdown
同步人工 accept / reject / revise
整理 accepted_edges.jsonl
```

### Neo4j 导入与检查

```text
scripts/export_kg_to_neo4j_cypher.py
scripts/import_kg_to_neo4j.py
scripts/check_neo4j_kg.py
scripts/check_kg_import_duplicates.py
```

用途：

```text
生成 Cypher
导入本地 Neo4j
检查节点、关系、重复导入风险
```

### Chroma 入库与查询

```text
scripts/ingest_text_chunks_to_chroma.py
scripts/ingest_fretboard_visuals_to_chroma.py
scripts/retrieve_guitar_evidence.py
scripts/query_visual_evidence.py
```

用途：

```text
文本 chunk 入 Chroma
教材图片块入 Chroma
查询文本证据
查询视觉证据
```

### 评测与缓存

```text
scripts/eval_retrieval_bundle.py
scripts/embedding_cache.py
```

用途：

```text
运行组合检索评测
统计准确率和耗时
缓存 query embedding
```

## 常用命令

运行扩展评测：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\eval_retrieval_bundle.py `
  --out-md data\eval\retrieval_bundle_report_expanded.md `
  --out-json data\eval\retrieval_bundle_report_expanded.json
```

禁用 embedding 缓存运行评测：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\eval_retrieval_bundle.py `
  --no-embedding-cache `
  --out-md data\eval\retrieval_bundle_report_no_cache.md `
  --out-json data\eval\retrieval_bundle_report_no_cache.json
```

查询视觉证据：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\query_visual_evidence.py `
  --source-id fretboard_handbook_mineru `
  --query "大三和弦 琶音 指型"
```

检查 Neo4j：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\check_neo4j_kg.py
```

## 环境配置

环境变量主要放在：

```text
.env
.env.example
```

常见配置项：

```text
LLM_API_KEY
LLM_BASE_URL
EMBEDDING_MODEL
VL_EMBEDDING_MODEL
MULTIMODAL_EMBEDDING_API_URL
NEO4J_URI
NEO4J_USER
NEO4J_PASSWORD
NEO4J_DATABASE
```

注意：

```text
.env 不应提交到公开仓库
不要在文档或日志中暴露 API key / Neo4j 密码
```

## 当前结论

当前系统已经形成了可工作的三层检索结构：

```text
Neo4j：结构化关系
Chroma：文本/视觉证据召回
SQLite：query embedding 缓存
```

在当前 22 条扩展评测中，缓存命中后可以做到秒级回归测试。下一阶段的重点不再是单纯提高这 22 条指标，而是扩大负例、引入新的教材和谱例输入，验证系统是否仍能保持稳定。

## 下一步建议

1. 增加负例评测

```text
包含 root 但不应该进入 P0
包含 chord 但不应该进入 P2/P3
包含 scale 但需要区分 P1 与 P3
```

2. 为 math rock PDF 建立独立视觉 taxonomy

```text
riff diagram
tablature example
rhythm pattern
alternate tuning diagram
tapping example
```

3. 建立 GP5 分析输出 schema

```text
tempo
meter
sections
chord_progression
key
riff_motifs
rhythmic_density
technique_markers
```

4. 将检索结果接入最终编配 Agent

```text
GP5 features
  -> retrieve text evidence
  -> retrieve visual evidence if needed
  -> query KG
  -> LLM 编配分析
  -> 引用证据与建议
```
