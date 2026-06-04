# Guitar Arrangement Inspiration Agent 项目引导

## 1. 项目目标

本项目目标是构建一个面向吉他编曲灵感生成的本地知识系统。系统需要从吉他教材、乐谱、MIDI、Guitar Pro 文件等资料中抽取可检索、可推理的音乐知识，并进一步服务于编曲建议、技法推荐、指板/和弦/声部关系分析。

核心能力包括：

- 从吉他教材中抽取概念、技法、练习、图例、指板结构和谱例信息。
- 从乐谱/MIDI/Guitar Pro 文件中抽取和声、旋律、节奏、指法和编曲特征。
- 构建知识图谱，表达概念之间、教材证据之间、谱例之间的关系。
- 为后续 Agent 提供“有出处的编曲灵感”，而不是只返回泛泛的文本建议。

## 2. 当前数据资产

当前仓库中的主要数据：

```text
data/
  book/
    吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org).pdf
  scores/
    mathrock/
      song_1.gp5
      song_1.mid
      song_2.gp5
      song_2.mid
      song_3.gp5
      song_3.mid
```

已检查的教材 PDF 特征：

```text
文件大小：约 39.22 MB
页数：约 85 页
图片对象：85 个
字体对象：0 个
ToUnicode 文本映射：0 个
图片编码：DCTDecode / JPEG
```

判断：这本教材基本是“每页一张扫描图”的 PDF，不是带文字层的电子 PDF。因此不适合直接使用普通 PDF 文本抽取或轻量 PDF-to-Markdown 工具作为主流程。

## 3. 文档处理原则

### 3.1 不把 Markdown 当作唯一真相

Markdown 适合人工校对和调试，但知识图谱入库不应依赖 Markdown 文本本身。推荐保留三类产物：

```text
原始文件：PDF / GP5 / MIDI
结构化中间层：JSON，包括 page、block、bbox、reading_order、confidence
人工可读层：Markdown，用于检查解析质量
```

### 3.2 对扫描教材按页面图像处理

这本中文图文复杂教材应按以下方式处理：

```text
PDF 页面渲染为图片
  -> OCR + 版面分析
  -> 切分 text / title / figure / table / music_example 等 block
  -> 文本块走 LLM 知识抽取
  -> 图像块走 VLM 或专用识别
  -> 统一进入知识图谱
```

不要只从 PDF 中抽图片对象，因为当前 PDF 中的图片对象大概率是整页扫描图，不是局部的指板图、谱例或和弦图。

## 4. 推荐工具路线

### 4.1 主解析器：MinerU

适合场景：

- 中文扫描教材
- 图文混排
- OCR
- 版面分析
- Markdown/JSON 输出
- 本地化部署

建议作为教材解析主链路。

### 4.2 备选解析器：Docling

适合场景：

- 结构化 JSON 输出
- 版面、阅读顺序、表格处理
- 本地执行
- 与 MinerU 做解析质量对照

建议作为第二解析器，用于评测和兜底。

### 4.3 快速路径：PyMuPDF4LLM

适合场景：

- 带文字层的电子 PDF
- 干净英文资料
- 快速生成 Markdown/page chunks

当前这本扫描教材不适合作为 PyMuPDF4LLM 主流程。

## 5. 建议目录结构

后续可以逐步整理为：

```text
data/
  raw/
    book/
    scores/
  processed/
    books/
      guitar_fretboard_workbook/
        pages/
          p001.png
          p002.png
        blocks/
          p001_b001.png
          p001_b002.png
        ocr/
          p001.json
        markdown/
          book.md
        layout.json
        entities.json
        relations.json
    scores/
      mathrock/
        song_1_features.json
        song_2_features.json
        song_3_features.json
docs/
  extraction_pipeline.md
  knowledge_graph_schema.md
```

当前仓库已经有 `data/book` 和 `data/scores`，是否迁移到 `data/raw` 可以后续再决定。短期内可以先保持现状，避免无意义移动。

## 6. 教材解析中间层 Schema

每一页建议保存为：

```json
{
  "book_id": "guitar_fretboard_workbook",
  "source_path": "data/book/吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org).pdf",
  "page": 23,
  "width": 1190,
  "height": 1650,
  "blocks": [
    {
      "block_id": "p023_b001",
      "type": "title",
      "bbox": [80, 120, 980, 190],
      "text": "第3章 大调音阶指型",
      "reading_order": 1,
      "confidence": 0.94
    },
    {
      "block_id": "p023_b002",
      "type": "figure",
      "bbox": [120, 420, 1020, 780],
      "image_path": "data/processed/books/guitar_fretboard_workbook/blocks/p023_b002.png",
      "nearby_text_blocks": ["p023_b001", "p023_b003"],
      "reading_order": 2,
      "confidence": 0.88
    }
  ]
}
```

Block 类型建议先使用：

```text
title
paragraph
caption
figure
table
music_staff
tablature
chord_diagram
fretboard_diagram
exercise
unknown
```

## 7. 知识图谱核心实体

建议先从小而稳的实体集合开始：

```text
Book
Page
Block
Concept
Technique
Chord
Scale
Mode
Interval
FretboardPosition
StringSet
Exercise
MusicExample
ScoreFile
Song
Section
```

吉他教材重点实体：

```text
指板位置
音名
音程
把位
弦组
音阶指型
和弦形状
转位
练习目标
```

编曲 Agent 重点实体：

```text
编曲技法
声部进行
低音线
旋律置顶
内声部填充
风格
节奏型
可替代和弦
```

## 8. 知识图谱核心关系

推荐关系：

```text
Book -HAS_PAGE-> Page
Page -HAS_BLOCK-> Block
Block -MENTIONS-> Concept
Block -EXPLAINS-> Technique
Block -SHOWS-> FretboardPosition
Block -HAS_IMAGE-> ImageAsset
Block -NEAR-> Block
Block -IN_SECTION-> Section

Concept -RELATED_TO-> Concept
Technique -APPLIES_TO-> Style
Technique -REQUIRES-> Concept
Technique -HAS_EXAMPLE-> MusicExample
Scale -CONTAINS_INTERVAL-> Interval
Chord -HAS_SHAPE-> FretboardPosition
FretboardPosition -ON_STRING_SET-> StringSet

ScoreFile -HAS_SECTION-> Section
Section -USES_CHORD-> Chord
Section -USES_TECHNIQUE-> Technique
Section -HAS_RHYTHM_PATTERN-> RhythmPattern
```

关系应该保存出处：

```json
{
  "source": "p023_b002",
  "source_page": 23,
  "evidence_text": "本页展示了大调音阶在指板上的五种常见指型。",
  "confidence": 0.82,
  "extractor": "llm_v1"
}
```

## 9. 教材图文对应策略

知识图谱不会天然知道图片对应哪段文字，必须在解析阶段建立关系。建议组合使用：

```text
1. 页面阅读顺序
2. bbox 空间距离
3. caption 识别
4. 正文引用匹配，例如“如下图”“例3-2”
5. VLM 输出与附近 OCR 文本的实体匹配
```

图文关系分强弱：

```text
HAS_CAPTION：强关系
REFERS_TO：强关系
NEAR：中等关系
IN_SECTION：中等关系
SEMANTIC_MATCH：中到强关系，取决于置信度
```

## 10. 第一阶段落地任务

建议第一阶段只处理这一本教材和现有 mathrock 乐谱样本，不要一开始就做大而全系统。

### 任务 A：教材页面解析

- 将 PDF 渲染为每页 PNG。
- 使用 MinerU 跑 OCR 和 layout。
- 输出每页 JSON 和整书 Markdown。
- 抽取并保存局部 block 图片。
- 随机抽查 5 页解析质量。

### 任务 B：图像块分类

- 将 figure/unknown block 分类为：
  - fretboard_diagram
  - chord_diagram
  - tablature
  - music_staff
  - exercise_image
  - decorative_or_unknown
- 只对音乐相关 block 调用 VLM。

### 任务 C：文本知识抽取

- 从 title/paragraph/caption/exercise 中抽取概念和关系。
- 每条知识必须带 page/block 证据。
- 对中文术语做规范化，例如“大调音阶”“Major Scale”对齐。

### 任务 D：乐谱特征抽取

- 解析 `data/scores/mathrock/*.mid` 和 `*.gp5`。
- 抽取 tempo、拍号、和弦、旋律轮廓、重复动机、节奏密度。
- 与教材中的概念建立弱关联，例如音阶、把位、节奏型、技法。

### 任务 E：知识图谱 MVP

- 先用 JSONL 或 SQLite 保存图谱边和节点。
- 后续再迁移到 Neo4j、Kuzu、DuckDB 或 RDF。
- MVP 阶段重点是 schema 稳定和证据可追溯。

## 11. 建议技术栈

本地处理优先：

```text
OCR/Layout：MinerU，Docling
PDF 渲染：pypdfium2 或 PyMuPDF
图像处理：Pillow / OpenCV
VLM：本地多模态模型或可替换 API adapter
音乐解析：pretty_midi / music21 / guitarpro
中间存储：JSONL + SQLite
图谱存储：Kuzu 或 Neo4j
检索：BM25 + embedding hybrid search
```

注意：PyMuPDF/PyMuPDF4LLM 涉及 AGPL/商业许可，若项目后续闭源或商用，需要提前评估许可证。

## 12. 后续开发入口

建议下一步建立这些脚本：

```text
scripts/
  inspect_pdf.py
  render_pdf_pages.py
  run_mineru.py
  normalize_layout.py
  classify_blocks.py
  extract_text_knowledge.py
  extract_score_features.py
  build_graph.py
```

推荐先做 `inspect_pdf.py` 和 `render_pdf_pages.py`，因为当前教材是扫描版，页面图像是后续所有 OCR/Layout/VLM 的基础。

## 13. 当前关键结论

这本教材的最佳路线不是“PDF 转 Markdown”，而是：

```text
扫描 PDF
  -> 页面图像
  -> OCR + 版面切块
  -> JSON 结构化保存
  -> Markdown 人工校对
  -> 文本/图片分别抽知识
  -> 知识图谱入库
```

Markdown 是项目沟通和校对层；JSON/Graph 才是 Agent 的长期记忆层。

## 14. OCR 清洗入口

当前已提供 OCR 清洗脚本：

```text
scripts/clean_ocr_blocks.py
```

输入 MinerU 的 `*_content_list.json`，输出：

```text
clean_blocks.jsonl  # 保留 ocr_text / clean_text / edits / page / bbox / raw
clean.md            # 供人工检查的清洗版 Markdown
clean_report.json   # 清洗统计
images/             # 从 MinerU 输出中复制过来的图片资产
```

保守规则清洗示例：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\clean_ocr_blocks.py `
  -i "data\processed\mineru_test\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)\ocr\吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)_content_list.json" `
  -o data\processed\mineru_test\cleaned `
  --source-page-offset 8
```

注意：简单中文错字、漏字、普通短语补全默认交给中文原生 LLM 处理，不建议沉淀为规则。规则层只保留确定性强、跨页复用、误伤风险低的结构/格式/版面伪影类规则。

LLM 清洗示例：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\clean_ocr_blocks.py `
  -i "path\to\*_content_list.json" `
  -o data\processed\books\some_book\cleaned `
  --source-page-offset 0 `
  --use-llm
```

让 LLM 审核并提出候选规则：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\clean_ocr_blocks.py `
  -i "path\to\*_content_list.json" `
  -o data\processed\books\some_book\rule_review `
  --source-page-offset 0 `
  --suggest-rules `
  --max-suggest-blocks 40
```

该模式会输出：

```text
suggested_rules.json
```

候选规则默认不会自动生效。审核后，将低风险规则合并到：

```text
config/ocr_cleaning_rules.json
```

规则格式：

```json
{
  "id": "music_literal_001",
  "enabled": true,
  "type": "literal",
  "from": "对于阶和琶",
  "to": "对于音阶和琶音",
  "reason": "music term completion"
}
```

候选规则筛选原则：

```text
保留：页眉页脚、练习编号、列表符号、图注格式、反复出现的扫描噪声、确定的格式归一化
丢弃：普通中文错字、上下文相关漏字、单页才出现的短语补全、可能误伤正常文本的宽泛替换
```

LLM 接口配置在 `.env` 中，使用 OpenAI-compatible Chat Completions：

```text
LLM_API_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=
LLM_MODEL=gpt-4.1-mini
```

清洗原则：LLM 只作为可追踪校正层，不能覆盖原始 OCR 证据。入库时应同时保留 `ocr_text`、`clean_text`、`edits`、`confidence`、`needs_review`、`page` 和 `bbox`。

## 15. 教材到编曲知识图谱抽取

当前已提供图谱抽取脚本：

```text
scripts/extract_arrangement_kg.py
```

这个脚本不做 OCR 拼写清洗。中文原生 LLM 会直接容忍普通 OCR 噪声，prompt 的重点是过滤教材噪音：

```text
拒绝基础定义
拒绝练习指令
拒绝无证据谱例
只保留色彩映射、吉他指板语汇、编曲避坑
```

本地预览 chunk，不调用 API：

```powershell
$env:PYTHONIOENCODING='utf-8'
.\.venv-mineru\Scripts\python.exe scripts\extract_arrangement_kg.py `
  -i "path\to\book.md" `
  -o data\processed\books\some_book\kg_extract `
  --max-chunks 2 `
  --dry-run
```

真实调用 API：

```powershell
$env:PYTHONIOENCODING='utf-8'
.\.venv-mineru\Scripts\python.exe scripts\extract_arrangement_kg.py `
  -i "path\to\book.md" `
  -o data\processed\books\some_book\kg_extract `
  --max-chars 1800
```

输出：

```text
arrangement_kg_edges.jsonl
arrangement_kg_report.json
chunks.json
```

注意：真实调用 API 会把教材片段发送到 `.env` 中配置的外部或本地 OpenAI-compatible 接口。若使用外部 API，应确认版权、隐私和数据保留策略。

## 16. 本地 Chroma 教材证据库

当前采用 Neo4j + Chroma 分层：

```text
Neo4j：存审核后的知识关系、节点网络、编配规则
Chroma：存教材原文 chunk、谱例/图片说明、可追溯证据
data：保留原始 PDF、课程文本、MinerU Markdown、图片文件
```

已建立本地 Chroma 文本 collection：

```text
CHROMA_PATH=data/chroma
CHROMA_TEXT_COLLECTION=guitar_text_chunks
```

教材来源索引：

```text
data/sources/catalog.json
```

当前已导入：

```text
mathrock_text_course：7 chunks
cory_wong_funk_core：10 chunks
fretboard_handbook_mineru：18 chunks
```

当前文本证据库已切换为 API embedding：

```text
EMBEDDING_PROVIDER=api
EMBEDDING_MODEL=text-embedding-v4
EMBEDDING_DIMENSIONS=1024
```

重建文本 collection：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\ingest_text_chunks_to_chroma.py --reset
```

文本检索测试：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\ingest_text_chunks_to_chroma.py `
  --query "funk sixteenth note muted chuck bubble rhythm guitar" `
  --n-results 4
```

视觉证据测试 collection：

```text
CHROMA_VISUAL_COLLECTION=guitar_visual_chunks
VL_EMBEDDING_MODEL=qwen3-vl-embedding
VL_EMBEDDING_DIMENSIONS=1024
```

视觉 smoke test：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\smoke_qwen_vl_embedding.py `
  --reset `
  --image "data\练习解答（图片）\练习52.png" `
  --image "data\练习解答（图片）\练习28-29.png" `
  --image "data\练习解答（图片）\练习1-练习5.png"
```

视觉检索测试：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\smoke_qwen_vl_embedding.py `
  --query "guitar exercise answer diagram fretboard notes" `
  --n-results 3
```

测试结论：

```text
text-embedding-v4 对 mathrock/DADGAD 查询召回稳定，前 5 条均为 mathrock 教程。
funk 查询第一名正确，但后续会混入 mathrock；生产检索应增加 Neo4j 风格/任务过滤或 reranker。
qwen3-vl-embedding 已能用文本 query 召回本地练习答案图，适合后续 PDF 图页/谱例页证据库。
```

## 17. 收紧后的检索层

裸向量检索会出现风格串台，因此当前检索入口改为：

```text
query / GP5 features
  -> 推断 style_tags / source_id / kg_node / gp5_feature
  -> Chroma 先召回较多候选
  -> 本地按 metadata 后过滤
  -> 可选 Neo4j 返回相关风格边作为解释上下文
```

脚本：

```text
scripts/retrieve_guitar_evidence.py
```

示例：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\retrieve_guitar_evidence.py `
  --query "funk rhythm guitar sixteenth note muted chuck bubble groove" `
  --top-k 5
```

GP5 特征式检索可以显式传入：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\retrieve_guitar_evidence.py `
  --query "DADGAD open string tapping riff" `
  --style-tag math_rock `
  --gp5-feature open_string_sustain_overlap `
  --gp5-feature tapping `
  --top-k 5
```

简单评测：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\retrieve_guitar_evidence.py --eval
```

评测文件：

```text
data/eval/retrieval_smoke_tests.json
```

## 18. 指板手册视觉层

指板手册的图片不只是教材装饰，而是指板/把位/指型/和弦图证据。当前策略是：

```text
局部图片块 -> qwen3-vl-embedding -> guitar_visual_chunks
图片附近文字/页码/优先级 -> metadata
后续少量关键页 -> VLM caption -> text Chroma / KG 审核
```

第一轮优先页：

```text
P0: page 14 根音五种指型
P1: page 35-40 五声音阶、音程、同度/八度
P2: page 45-62 三和弦/七和弦/延伸和弦/变化和弦、琶音
P3: page 67-69 其他常用音阶/和弦
```

生成 manifest 并入视觉 Chroma：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\ingest_fretboard_visuals_to_chroma.py
```

只生成清单、不调用 API：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\ingest_fretboard_visuals_to_chroma.py --manifest-only
```

视觉检索：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\query_visual_evidence.py `
  --query "大三和弦 琶音 指型 根音" `
  --source-id fretboard_handbook_mineru `
  --n-results 5
```
