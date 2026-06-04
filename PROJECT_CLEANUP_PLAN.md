# 项目瘦身与 GP5 工作流接入计划

本文件用于在接入 GP5 识别/分析工作流前，说明当前项目文件的作用、基本结构、可保留资产与可归档中间产物。原则是：先归档、再收口，不直接删除可追溯数据。

## 1. 当前项目定位

项目目标是构建一个吉他编配分析助手：

1. 从吉他教材中抽取编曲知识，形成 Neo4j 知识图谱。
2. 将教材文本、谱例图、和弦图、指板图写入 Chroma，作为可检索证据库。
3. 将 GP5/MIDI/音频等乐谱特征转为结构化输入，例如节奏型、BPM、和声进行、调性、riff 特征。
4. 用 Neo4j + Chroma 检索相关知识和证据，再交给 LLM 给出编配分析和建议。

当前项目已经完成了教材侧的主要验证：指板手册、Funk 课程、Math Rock 文本课程、Math Rock PDF 文本与视觉补抽。

## 2. 当前目录职责

### `data/book`

原始教材与课程文本。

当前主要文件：

- `吉他指板手册 ... .pdf`：指板体系、指型、和弦/音阶/练习来源。
- `cory wong funk吉他大师课.txt`：Funk 节奏吉他课程文本。
- `mathrock教学课.txt`：Math Rock 文本课程。
- `Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans.pdf`：Math Rock PDF 教材。

处理建议：长期保留。它们是知识抽取和误差回溯的源文件。

### `data/processed`

处理过程产物，当前体量最大。

主要子目录：

- `mineru_full_gpu`：指板手册的 MinerU 转换结果、分块抽取、视觉补抽、审核文件。
- `mathrock`：Math Rock PDF 的 MinerU 转换、整页图、视觉密度报告、Chroma 视觉 manifest、多模态 KG 补抽结果。
- `style_rhythm`：Funk 课程抽取与审核结果。
- `fretboard_handbook`：指板手册视觉层 manifest。
- `mineru_test` / `mineru_full`：早期测试或空目录。

处理建议：只保留当前可追溯链路的关键文件，其余移动到 `data/archive/processed_runs`。

### `data/knowledge`

已经审核并可入库的知识图谱边文件。

每个知识包通常包含：

- `edges.jsonl`：最终入库边，最核心。
- `accepted_edges.jsonl`：审核通过边。
- `revised_edges.jsonl`：LLM 根据人工 revise 修正后的边。
- `rejected_review_items.jsonl`：拒绝项。
- `pending_review_items.jsonl`：未处理项。
- `curation_report.json`：整理报告。
- `import.cypher`：Neo4j Browser 可执行导入文件。

当前知识包：

- `arrangement_kg`：指板手册早期核心片段。
- `arrangement_kg_chunks_006_010`：指板手册 chunk 006-010。
- `arrangement_kg_integrated_chunks_011_015`：指板手册综合补抽 011-015。
- `arrangement_kg_visual_answer_chunks_002_010`：指板手册练习答案视觉补抽。
- `arrangement_kg_cory_wong_funk_core`：Funk 节奏吉他核心知识。
- `arrangement_kg_mathrock_text`：Math Rock 文本课程知识。
- `mathrock_pdf_kg`：Math Rock PDF 文字知识。
- `mathrock_pdf_visual_supplement_kg`：Math Rock PDF 多模态视觉补充知识。

处理建议：全部保留。后续可以新增 `data/knowledge/manifest.json` 记录每个知识包是否已导入 Neo4j。

### `data/chroma`

本地 Chroma 向量库。

当前作用：

- `guitar_text_chunks`：教材文本块检索。
- `guitar_visual_chunks`：教材图片/谱例/和弦图/指板图检索。

处理建议：保留。它是 RAG 运行时资产，不应归档。

### `data/cache`

缓存目录。

当前核心文件：

- `embeddings.sqlite`：文本/视觉 query 的 embedding 缓存，减少重复 API 调用。

处理建议：保留。若后续切换 embedding 模型，可新建带模型名的缓存表或新 sqlite。

### `data/eval`

检索评测结果。

主要文件：

- `retrieval_smoke_tests.json`：小规模检索测试用例。
- `retrieval_bundle_report*.md/json`：不同阶段检索评测报告。

处理建议：保留最新报告和基准测试；旧报告可归档。

### `data/scores`

乐谱测试样本。

当前包含 Math Rock 示例：

- `.gp5`：待接入的 Guitar Pro 文件。
- `.mid`：可能由 GP5 导出或辅助分析的 MIDI 文件。

处理建议：保留并扩展。后续 GP5 工作流的测试入口应从这里开始。

### `scripts`

当前脚本数量约 30 个，已经混合了正式流程、调试脚本和一次性迁移脚本。

建议重组为：

- `scripts/kg_pipeline`
  - `extract_arrangement_kg.py`
  - `extract_style_rhythm_kg.py`
  - `extract_multimodal_kg_supplement.py`
  - `curate_reviewed_kg.py`
  - `render_kg_review_md.py`
  - `sync_kg_review_md.py`
  - `export_kg_to_neo4j_cypher.py`
  - `import_kg_to_neo4j.py`
  - `check_kg_import_duplicates.py`

- `scripts/retrieval`
  - `ingest_text_chunks_to_chroma.py`
  - `ingest_visuals_to_chroma.py`
  - `retrieve_guitar_evidence.py`
  - `query_visual_evidence.py`
  - `embedding_cache.py`
  - `eval_retrieval_bundle.py`

- `scripts/pdf_processing`
  - `render_pdf_visual_pages.py`
  - `inspect_pdf_visual_density.py`
  - `build_pdf_visual_review_list.py`
  - `build_multimodal_kg_pairings.py`

- `scripts/dev`
  - `smoke_qwen_vision.py`
  - `smoke_qwen_vl_embedding.py`
  - `check_neo4j_kg.py`
  - `check_mathrock_pdf_neo4j.py`

- `scripts/archive`
  - 早期一次性脚本、过期实验脚本。

处理建议：先移动重组，不改脚本逻辑；移动后统一修正运行文档。

### `config`

配置文件。

- `mineru.json`：MinerU 配置。
- `ocr_cleaning_rules.json`：早期 OCR 清理规则。

处理建议：保留。后续如果不再走正则清洗，可以把 OCR rules 标记为 legacy。

## 3. 当前体量观察

按目录估算：

| 目录 | 文件数 | 体量 |
| --- | ---: | ---: |
| `data` | 1316 | 276.98 MB |
| `data/book` | 4 | 45.21 MB |
| `data/processed` | 1199 | 201.24 MB |
| `data/knowledge` | 57 | 0.88 MB |
| `data/chroma` | 13 | 10.89 MB |
| `data/cache` | 1 | 6.46 MB |
| `data/eval` | 11 | 1.06 MB |
| `data/scores` | 6 | 0.01 MB |
| `scripts` | 60 | 0.72 MB |

结论：真正占空间的是 `data/processed`，尤其是 PDF/MinerU 图片和中间产物。知识库本身很轻，不是瘦身重点。

## 4. 建议保留的核心资产

### 必须保留

- `data/book`
- `data/knowledge`
- `data/chroma`
- `data/cache/embeddings.sqlite`
- `data/scores`
- `PROJECT_FRAMEWORK.md`
- `PROJECT_GUIDE.md`
- `.env` / `.env.example`

### 建议保留但可整理

- `data/eval`
- `data/sources`
- `data/processed/*/arrangement_kg_review.synced.jsonl`
- `data/processed/*/arrangement_kg_review.md`
- `data/processed/*/chunks.json`
- 视觉 manifest：
  - `data/processed/fretboard_handbook/visual_layer`
  - `data/processed/mathrock/visual_layer`

### 可归档

- MinerU 的 `_model.json`、`_middle.json`、`_span.pdf`、`_layout.pdf`
- 早期 dry-run 目录
- 已完成阶段的临时 pairings/report
- 旧版评测报告
- 过期的未同步 review 草稿

### 暂不建议删除

- 原始 PDF/文本
- 已导入知识包
- Chroma 数据库
- embedding 缓存
- 已审核 synced JSONL

## 5. 建议目标结构

```text
data/
  book/                    # 原始教材
  scores/                  # GP5/MIDI/音频测试样本
  knowledge/               # 已审核、可入库 KG
  chroma/                  # 本地向量库
  cache/                   # embedding / query 缓存
  sources/                 # 教材 catalog / source manifest
  eval/                    # 检索与工作流评测
  processed/
    current/               # 当前仍在活跃处理的产物
    manifests/             # 文本/视觉 manifest
  archive/
    processed_runs/        # 旧 MinerU、dry-run、中间实验

scripts/
  kg_pipeline/
  retrieval/
  pdf_processing/
  gp5_pipeline/
  dev/
  archive/
```

## 6. GP5 工作流接入建议

建议新增 `scripts/gp5_pipeline`，先做最小可用链路：

```text
GP5 文件
  -> 结构化解析
  -> score_features.json
  -> Neo4j + Chroma 检索
  -> retrieval_bundle.json
  -> LLM 编配分析
  -> analysis_report.md/json
```

### 第一阶段：GP5 解析

目标输出：

```json
{
  "file": "data/scores/mathrock/song_1.gp5",
  "tempo": 120,
  "time_signatures": ["4/4", "7/8"],
  "key_candidates": ["E minor"],
  "sections": [],
  "tracks": [],
  "riffs": [],
  "chord_events": [],
  "rhythm_patterns": [],
  "techniques": [],
  "style_feature_hints": []
}
```

### 第二阶段：检索桥接

把 GP5 特征映射成检索 query：

- 节奏：odd meter、syncopation、16th-note funk、displaced accents。
- riff：pedal tone、string skipping、tapping riff、open-string ostinato。
- 和弦：shell voicing、add9、sus2、open voicing、spread triads。
- 技法：palm mute、let ring、slide、hammer-on、pull-off、hybrid picking。

检索应同时查：

- Neo4j：规则、因果、风格知识。
- Chroma text：教材文字证据。
- Chroma visual：谱例/和弦图/指板图证据。

### 第三阶段：报告生成

输出建议：

- `data/outputs/gp5_analysis/<song_id>/score_features.json`
- `data/outputs/gp5_analysis/<song_id>/retrieval_bundle.json`
- `data/outputs/gp5_analysis/<song_id>/analysis_report.md`

## 7. 瘦身执行顺序

### Step 1：只建 manifest，不移动

生成：

- `data/manifest_current_assets.json`
- `data/manifest_archive_candidates.json`

目的：先看清楚哪些文件会被移动。

### Step 2：建立归档目录

新增：

```text
data/archive/processed_runs/
data/archive/eval_reports/
scripts/archive/
```

### Step 3：移动明显中间产物

优先移动：

- `data/processed/mineru_test`
- `data/processed/mineru_full`
- 早期 dry-run 目录
- 未使用的旧 report

### Step 4：脚本分组

先移动脚本，不改逻辑；移动后更新 `PROJECT_FRAMEWORK.md` 里的路径说明。

### Step 5：接入 GP5 最小链路

新增：

- `scripts/gp5_pipeline/parse_gp5.py`
- `scripts/gp5_pipeline/build_score_features.py`
- `scripts/gp5_pipeline/run_gp5_rag_analysis.py`

## 8. 当前建议

在开始 GP5 前，建议只执行 Step 1 和 Step 2：

1. 生成 manifest。
2. 建立 archive 目录。
3. 暂不移动核心文件。

这样可以让项目视野变清楚，同时不影响已经跑通的 KG、Chroma、Neo4j 流程。
