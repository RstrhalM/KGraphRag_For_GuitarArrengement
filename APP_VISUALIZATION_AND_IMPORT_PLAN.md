# 前后端可视化与知识导入方案

## 目标定位

当前项目已经有较完整的离线数据处理链路：教材解析、LLM 抽取、人工 Markdown 审核、Neo4j 图谱、Chroma RAG、SQLite 缓存和评测脚本。下一步如果做成一个有展示价值的前后端系统，核心不应该只是“聊天框”，而应该把这个项目最有竞争力的部分展示出来：

```text
教材分块可视化
+ 图谱可视化
+ 知识导入流水线
+ RAG 检索验证
+ 后续 GP5 分析入口
```

这个前后端的第一阶段目标是做一个本地知识工作台，让用户能看见：

- 一本教材如何被切成文本块、图片块、视觉证据。
- 某个 chunk 抽出了哪些知识边。
- 哪些边进入了 Neo4j。
- 哪些文本或图片进入了 Chroma。
- 一个自然语言 query 最终召回了哪些文本块、图谱节点和证据图。

视觉 caption 里如果不能精确召回具体指型图，暂时不作为主线。视觉层应先回到更可靠的原则：

```text
能定位到具体图片/区域的视觉证据，才进入正式可视化链路。
不能定位的 caption 只作为实验结果，不进入主证据层。
```

## 推荐技术栈

### 后端

推荐使用：

```text
FastAPI
+ Pydantic
+ Neo4j Python Driver
+ ChromaDB PersistentClient
+ SQLite
+ 本地脚本封装
```

原因：

- 项目已有大量 Python 脚本，FastAPI 最容易复用。
- Neo4j、Chroma、SQLite 都有稳定 Python 客户端。
- 后续 GP5 解析、embedding、RAG eval 都可以直接挂成后端任务。
- 本地部署简单，适合面试演示。

后端目录建议：

```text
backend/
  app.py
  api/
    datasets.py
    chunks.py
    graph.py
    rag.py
    imports.py
    jobs.py
  core/
    settings.py
    paths.py
    schemas.py
  services/
    chunk_service.py
    graph_service.py
    chroma_service.py
    import_service.py
    eval_service.py
    visual_service.py
  workers/
    job_runner.py
  db/
    sqlite.py
    neo4j.py
    chroma.py
```

### 前端

推荐使用：

```text
React + Vite + TypeScript
+ TanStack Query
+ React Router
+ Cytoscape.js 或 Sigma.js
+ Monaco Editor / Markdown Preview
+ Tailwind 或普通 CSS modules
```

原因：

- 页面以工具台为主，不需要营销式页面。
- Cytoscape.js 适合图谱交互：节点展开、关系筛选、局部子图。
- React Query 适合处理后端任务、轮询导入状态、缓存查询结果。
- Monaco/Markdown Preview 适合做审核和 JSON/Markdown 对照。

前端目录建议：

```text
frontend/
  src/
    app/
      routes.tsx
      layout.tsx
    pages/
      Dashboard.tsx
      DatasetExplorer.tsx
      ChunkViewer.tsx
      GraphExplorer.tsx
      RagPlayground.tsx
      ImportWorkbench.tsx
      EvalReports.tsx
    components/
      ChunkList.tsx
      ChunkDetail.tsx
      EvidencePanel.tsx
      GraphCanvas.tsx
      ImportStepper.tsx
      JobStatus.tsx
      JsonInspector.tsx
      ImageEvidenceViewer.tsx
    api/
      client.ts
      datasets.ts
      graph.ts
      rag.ts
      imports.ts
```

## 页面设计

### 1. Dashboard

用途：展示项目总览。

核心信息：

- 已导入教材数。
- 文本 chunk 数。
- 图片证据数。
- Neo4j 节点数、关系数。
- Chroma collection 数和文档数。
- 最近一次 RAG eval 结果。
- 最近导入任务状态。

示例卡片：

```text
Text Chunks: 68
Visual Evidence: 60
Neo4j Nodes: xxx
Neo4j Edges: xxx
Text RAG Pass@K: 40/40
Visual Caption Hit@1: 30/30
```

这个页面适合面试开场：它能一眼说明项目不是 demo，而是有数据资产和评测闭环。

### 2. Dataset Explorer

用途：管理教材和数据源。

展示对象：

```text
data/book
data/processed/*
data/knowledge/*
data/chroma
```

每个数据源展示：

- source_id
- source_title
- source_type
- 文件路径
- 处理状态
- chunk 数
- image 数
- KG review 状态
- Chroma 入库状态
- Neo4j 入库状态

操作：

- 查看 Markdown。
- 查看原始 PDF / 文本。
- 查看图片 manifest。
- 跳转到 Chunk Viewer。
- 发起导入任务。

### 3. Chunk Viewer

这是最重要的页面之一。

用途：把教材分块可视化。

布局建议：

```text
左侧：chunk 列表
中间：chunk 文本 / Markdown 渲染
右侧：图片证据 + 抽取结果 + 入库状态
```

Chunk 列表字段：

- chunk_id
- page_hint
- source_id
- chars
- image_refs_count
- kg_edges_count
- review_status
- visual_missing_count

Chunk 详情：

- 原始文本。
- Markdown 渲染。
- 图片引用。
- nearby_text。
- 对应 KG 抽取结果。
- 人工审核状态。

图片证据区：

- 显示 MinerU 切出来的小图。
- 显示答案图或 PDF 页图。
- 显示 image_path。
- 未来支持 bbox/crop_path。

关键原则：

```text
所有知识都必须能回到 chunk。
所有图谱边都必须能回到 evidence。
所有视觉证据都必须能回到 image_path。
```

### 4. Graph Explorer

用途：Neo4j 图谱可视化。

建议功能：

- 输入节点名或关键词搜索。
- 展示局部子图，而不是全图。
- 支持按关系类型筛选：
  - `ENABLES`
  - `SUGGESTS`
  - `CONSTRAINS`
  - `CAUTIONS`
  - `EVOKES`
  - `CAN_INSPIRE`
  - `CONFLICTS_WITH`
- 支持按 source_id 筛选。
- 点击节点显示属性。
- 点击边显示 evidence、source_chunk、review_status。

后端查询示例：

```cypher
MATCH p=(n)-[r]-(m)
WHERE n.name CONTAINS $keyword
RETURN p
LIMIT 80
```

图谱页面不要追求一次性展示全部节点。全图会很乱，也不利于分析。更好的交互是：

```text
搜索一个概念
-> 展开 1 跳
-> 手动展开 2 跳
-> 按关系类型过滤
-> 回看证据 chunk
```

### 5. RAG Playground

用途：测试 query 的召回链路。

输入：

```text
用户自然语言 query
```

输出分区：

```text
文本召回
视觉证据召回
图谱相关节点
rerank 后结果
最终 bundle
耗时
```

每条召回结果显示：

- score
- source_id
- chunk_id / visual_id / node_id
- 文本摘要
- evidence path
- 是否命中预期关键词

这个页面是展示 RAG 工程能力的关键。它可以把现在的 eval 脚本能力产品化。

### 6. Import Workbench

用途：可视化知识导入流程。

建议做成 stepper：

```text
1. 选择数据源
2. 转 Markdown / MinerU 解析
3. 生成 chunks
4. LLM KG 抽取
5. Markdown 人工审核
6. 同步 accepted/revised/rejected
7. 写入 data/knowledge
8. 导入 Neo4j
9. 写入 Chroma
10. 运行小规模 eval
```

每一步显示：

- 输入文件。
- 输出文件。
- 状态。
- 日志。
- 错误信息。
- 可重跑按钮。

注意：第一版不要真的做复杂任务编排系统，可以先把现有脚本包装成后端 job。

Job 数据可以先用 SQLite 管：

```sql
jobs(
  id TEXT PRIMARY KEY,
  job_type TEXT,
  status TEXT,
  source_id TEXT,
  command TEXT,
  input_path TEXT,
  output_path TEXT,
  log_path TEXT,
  created_at TEXT,
  updated_at TEXT
)
```

### 7. Eval Reports

用途：展示评测结果。

读取：

```text
data/eval/*.md
data/eval/*.json
```

展示：

- text RAG expanded report
- visual caption report
- bundle retrieval report
- query latency
- hit@1 / hit@5
- pass_all
- rerank 前后对比

这一页可以直接把项目的“可验证性”展示出来。

## 后端 API 设计

### Dataset API

```http
GET /api/datasets
GET /api/datasets/{source_id}
GET /api/datasets/{source_id}/files
```

返回示例：

```json
{
  "source_id": "fretboard_handbook_mineru",
  "title": "吉他指板手册",
  "type": "mineru_markdown",
  "text_chunks": 37,
  "visual_items": 236,
  "kg_edges": 120,
  "chroma_docs": 37,
  "neo4j_imported": true
}
```

### Chunk API

```http
GET /api/chunks?source_id=fretboard_handbook_mineru
GET /api/chunks/{chunk_id}
GET /api/chunks/{chunk_id}/images
GET /api/chunks/{chunk_id}/kg
```

### Visual Evidence API

```http
GET /api/visuals?source_id=fretboard_handbook_mineru
GET /api/visuals/{visual_id}
GET /api/visuals/file?path=...
```

第一版可以只返回完整图片。后续如果做 bbox/crop：

```http
GET /api/visuals/{visual_id}/crop
```

### Graph API

```http
GET /api/graph/search?q=七和弦
GET /api/graph/neighborhood?node_id=...
GET /api/graph/source/{source_id}
```

返回前端图结构：

```json
{
  "nodes": [
    {
      "id": "concept:七和弦",
      "label": "七和弦",
      "type": "Concept",
      "properties": {}
    }
  ],
  "edges": [
    {
      "id": "edge:001",
      "source": "concept:七和弦",
      "target": "technique:voice_leading",
      "type": "ENABLES",
      "evidence": "..."
    }
  ]
}
```

### RAG API

```http
POST /api/rag/query
```

请求：

```json
{
  "query": "怎么根据根音切换不同把位做 solo？",
  "mode": "text_graph_visual",
  "top_k": 8,
  "use_rerank": true
}
```

响应：

```json
{
  "query": "...",
  "latency_ms": 48,
  "text_hits": [],
  "visual_hits": [],
  "graph_hits": [],
  "bundle": []
}
```

### Import API

```http
POST /api/imports/jobs
GET /api/imports/jobs/{job_id}
POST /api/imports/jobs/{job_id}/run
POST /api/imports/jobs/{job_id}/cancel
```

任务类型：

```text
mineru_convert
build_chunks
extract_kg
sync_review
import_neo4j
ingest_chroma
run_eval
```

## 数据模型建议

### Source

```json
{
  "source_id": "fretboard_handbook_mineru",
  "title": "吉他指板手册",
  "source_type": "book_pdf",
  "raw_path": "...",
  "processed_path": "...",
  "status": "processed"
}
```

### Chunk

```json
{
  "chunk_id": "chunk_0014",
  "source_id": "fretboard_handbook_mineru",
  "page_hint": [75, 76],
  "text": "...",
  "image_refs": [],
  "kg_status": "reviewed",
  "chroma_status": "indexed"
}
```

### Visual Evidence

```json
{
  "visual_id": "fretboard_handbook:p045:xxx",
  "source_id": "fretboard_handbook_mineru",
  "image_path": "...",
  "page": 45,
  "bbox": [0, 0, 100, 100],
  "visual_type": "fretboard_diagram",
  "linked_chunk_id": "chunk_0008",
  "status": "indexed"
}
```

### Knowledge Edge

```json
{
  "edge_id": "...",
  "source": "七和弦",
  "relation": "ENABLES",
  "target": "声部连接",
  "evidence": "...",
  "source_id": "...",
  "chunk_id": "...",
  "review_status": "accepted"
}
```

### Import Job

```json
{
  "job_id": "...",
  "job_type": "extract_kg",
  "source_id": "mathrock_pdf_steve_h",
  "status": "running",
  "progress": 0.42,
  "log_path": "...",
  "output_path": "..."
}
```

## 视觉证据的处理原则

这部分需要收紧。

当前不建议把“大答案图 caption item”直接作为正式视觉证据，因为它不能定位到具体指型图。正式策略应该是：

```text
可入正式视觉证据层：
  1. MinerU 已切好的单张指板图
  2. PDF 页图中能裁剪出明确区域的谱例/指型图
  3. 有 bbox/crop_path 的答案区域图

暂缓入正式视觉证据层：
  1. 一张大答案图覆盖多个练习
  2. 只有泛 caption，无法定位到具体图形
  3. 只能说明题目答案，缺少可复用知识
```

更好的视觉路线：

```text
答案大图
  -> 自动/半自动区域切分
  -> 每个 crop 对应 exercise_no / item_no
  -> VLM 生成结构化 caption
  -> Chroma 存 caption_text
  -> visual_id 回链 crop_path + answer_image_path
```

这样前端才能做到：

```text
query 召回
  -> caption item
  -> 展示具体 crop 指型图
  -> 可跳转查看原始大图
```

也就是说，最终召回目标应该是：

```text
具体 crop 指型图 + caption + 来源 chunk
```

而不是：

```text
一张大答案图 + 泛描述
```

## 实现阶段

### Phase 1：只读知识工作台

目标：不改变现有导入流程，只把已有数据可视化。

内容：

- FastAPI 后端读取本地 JSONL、Markdown、Chroma、Neo4j。
- 前端展示 Dashboard。
- Dataset Explorer。
- Chunk Viewer。
- Graph Explorer。
- RAG Playground。

优点：

- 风险低。
- 不影响现有数据。
- 很快能做出演示效果。

### Phase 2：导入任务封装

目标：把现有脚本变成可点击任务。

内容：

- Import Workbench。
- SQLite jobs 表。
- 后端调用脚本并记录日志。
- 前端轮询任务状态。

先封装这些脚本：

```text
extract_arrangement_kg.py
sync_kg_review_md.py
import_neo4j_kg.py
ingest_text_chunks_to_chroma.py
eval_text_retrieval.py
eval_visual_caption_retrieval.py
```

### Phase 3：证据闭环

目标：让图谱、chunk、图片、RAG 互相跳转。

核心交互：

```text
图谱边 -> evidence chunk -> 原文段落 -> 图片证据
RAG hit -> chunk/image -> Neo4j 相关节点
导入任务 -> 输出文件 -> 审核 Markdown
```

这个阶段是项目质感提升最大的地方。

### Phase 4：GP5 工作流入口

目标：把最终业务场景接进来。

页面：

```text
Score Analyzer
```

输入：

```text
.gp5 / .gp4 / MusicXML / MIDI
```

输出：

- BPM
- 调性
- 和声进行
- riff 片段
- 节奏密度
- 技法标签
- 可能风格
- RAG 推荐证据
- 编配建议

这时前面的知识工作台就变成 GP5 Agent 的底座，而不是孤立的数据工具。

## 第一版最小可行产品

建议第一版只做 5 个页面：

```text
Dashboard
Dataset Explorer
Chunk Viewer
Graph Explorer
RAG Playground
```

先不做：

- 复杂权限系统。
- 云端部署。
- 多用户。
- 在线编辑大规模审核。
- 自动视觉区域切分。

第一版最重要的是展示：

```text
数据如何进入系统
知识如何被抽取
证据如何被追溯
RAG 如何被评测
图谱如何辅助解释
```

## 面试展示角度

这个前后端如果做出来，项目亮点会很清晰：

- 不是普通 Chatbot，而是本地知识工程系统。
- 有结构化图谱，也有向量证据。
- 有人工审核闭环。
- 有评测报告。
- 有可视化导入流程。
- 有未来 GP5 分析场景。
- 有对视觉证据粒度的工程判断，而不是盲目把图片都塞进向量库。

一句话版本：

```text
这是一个面向吉他编曲分析的本地 Knowledge Workbench：
它能把教材、谱例和未来 GP5 分析结果转成可审核、可检索、可追溯的图谱与 RAG 证据。
```

