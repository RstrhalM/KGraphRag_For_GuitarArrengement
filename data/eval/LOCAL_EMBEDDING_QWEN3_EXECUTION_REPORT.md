# 本地 Qwen3 Embedding 接入与评测执行报告

执行时间：2026-06-02

本次目标是在不破坏现有 API embedding / 视觉 embedding 流程的前提下，为项目接入本地文本 embedding，并用现有小批量 RAG 评测验证效果。

## 1. 结论摘要

已完成：

- 下载本地模型：`Qwen/Qwen3-Embedding-0.6B`
- 本地模型路径：`models/embedding/qwen3-embedding-0.6b`
- 模型目录体量：约 1.21 GB
- 新增本地文本 collection：`guitar_text_chunks_qwen3_06b`
- 恢复并保留 API 文本 baseline collection：`guitar_text_chunks`
- 保留视觉 collection：`guitar_visual_chunks`
- 本地 Qwen3 小批量评测通过：
  - Math Rock PDF source_focus：3/3
  - 全项目 global：4/4

当前 Chroma collection 计数：

| Collection | 数量 | 说明 |
| --- | ---: | --- |
| `guitar_text_chunks` | 68 | API `text-embedding-v4` baseline |
| `guitar_text_chunks_qwen3_06b` | 68 | 本地 Qwen3 文本库 |
| `guitar_visual_chunks` | 504 | qwen3-vl-embedding 视觉库 |

## 2. 新增/修改文件

### 新增

| 文件 | 作用 |
| --- | --- |
| `scripts/local_text_embedding.py` | 本地 Transformers embedding backend |
| `data/sources/catalog_local_embedding.json` | 本地文本库构建用 catalog，统一指向现役 chunks |
| `data/chroma/guitar_text_chunks_qwen3_06b.embedding_metadata.json` | 本地 collection 的模型元数据 |
| `data/eval/mathrock_pdf_query_report_small_qwen3_local_source_focus.md/json` | 本地 Qwen3 Math Rock PDF 首轮评测 |
| `data/eval/mathrock_pdf_query_report_small_qwen3_local_source_focus_cache_hit.md/json` | 本地 Qwen3 Math Rock PDF 缓存命中评测 |
| `data/eval/full_project_query_report_small_qwen3_local.md/json` | 本地 Qwen3 全项目首轮评测 |
| `data/eval/full_project_query_report_small_qwen3_local_cache_hit.md/json` | 本地 Qwen3 全项目缓存命中评测 |

### 修改

| 文件 | 修改 |
| --- | --- |
| `scripts/ingest_text_chunks_to_chroma.py` | 增加 `local_qwen3` embedding provider；修复 CLI 参数优先级 |
| `scripts/eval_retrieval_bundle.py` | 增加 `--text-embedding-provider local_qwen3` |
| `PROJECT_FRAMEWORK.md` | 增加本地 embedding 架构说明 |

## 3. 新增函数与类

### `scripts/local_text_embedding.py`

#### `LocalTransformerEmbedder`

作用：用本地 Transformers 模型生成文本 embedding。

关键参数：

- `model_name_or_path`：模型名或本地路径，当前使用 `models/embedding/qwen3-embedding-0.6b`
- `device`：`auto/cuda/cpu`
- `max_length`：当前设置 2048
- `normalize`：默认 `true`，输出单位向量

核心方法：

- `embed(texts, batch_size=8)`  
  批量生成文本向量，返回 `list[list[float]]`。

- `metadata()`  
  返回模型、设备、维度、加载耗时等元数据。

内部策略：

- 使用 `AutoTokenizer.from_pretrained`
- 使用 `AutoModel.from_pretrained`
- 用 attention mask 做 mean pooling
- 用 L2 normalize 对齐 cosine 检索

#### `write_model_metadata(path, metadata)`

作用：把本地 collection 的模型信息写入 JSON，方便复现。

输出示例：

```json
{
  "collection": "guitar_text_chunks_qwen3_06b",
  "embedding_provider": "local_qwen3",
  "provider": "local_transformers",
  "model": "models/embedding/qwen3-embedding-0.6b",
  "device": "cuda",
  "max_length": 2048,
  "normalize": true,
  "dimensions": 1024
}
```

### `scripts/ingest_text_chunks_to_chroma.py`

#### `LocalEmbedder`

作用：把 `LocalTransformerEmbedder` 适配成原入库脚本需要的 `embed(list[str])` 接口。

核心方法：

- `embed(texts)`
- `metadata()`

#### `make_embedder(provider, batch_size)`

新增 provider：

```text
local_qwen3
```

现在支持：

```text
hash
api
local_qwen3
```

### `scripts/eval_retrieval_bundle.py`

#### `LocalEmbeddingClient`

作用：评测阶段用本地 Qwen3 生成 query embedding，并写入 SQLite 缓存。

核心方法：

- `embed_text(text)`

缓存 key：

```text
provider = local_transformers
model = models/embedding/qwen3-embedding-0.6b
input_type = local_text
```

新增 CLI：

```text
--text-embedding-provider api|local_qwen3
--text-model models/embedding/qwen3-embedding-0.6b
--text-collection guitar_text_chunks_qwen3_06b
```

## 4. 模型加载 smoke test

命令：

```powershell
$env:LOCAL_EMBEDDING_MODEL='models/embedding/qwen3-embedding-0.6b'
$env:LOCAL_EMBEDDING_DEVICE='auto'
$env:LOCAL_EMBEDDING_MAX_LENGTH='2048'
.\.venv-mineru\Scripts\python.exe -c "..."
```

结果：

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

说明：

- CUDA 可用。
- 输出维度为 1024，适合与当前 API baseline 对照。
- 向量已归一化，适合 Chroma cosine 检索。

## 5. 本地文本库构建

命令：

```powershell
$env:LOCAL_EMBEDDING_MODEL='models/embedding/qwen3-embedding-0.6b'
$env:LOCAL_EMBEDDING_DEVICE='auto'
$env:LOCAL_EMBEDDING_MAX_LENGTH='2048'
.\.venv-mineru\Scripts\python.exe scripts\ingest_text_chunks_to_chroma.py `
  --catalog data\sources\catalog_local_embedding.json `
  --collection guitar_text_chunks_qwen3_06b `
  --embedding-provider local_qwen3 `
  --batch-size 8 `
  --markdown-max-chars 3500 `
  --reset
```

结果：

```json
{
  "chroma_path": "data\\chroma",
  "collection": "guitar_text_chunks_qwen3_06b",
  "embedding_provider": "local_qwen3",
  "documents": 68,
  "collection_count": 68,
  "embedding": {
    "provider": "local_transformers",
    "model": "models/embedding/qwen3-embedding-0.6b",
    "device": "cuda",
    "max_length": 2048,
    "normalize": true,
    "dimensions": 1024,
    "load_seconds": 1.8360
  }
}
```

## 6. API baseline 恢复说明

构建过程中发现 `.env` 中的 `CHROMA_TEXT_COLLECTION` 覆盖了 CLI 的 `--collection`，导致第一次本地构建误写入默认 `guitar_text_chunks`。

已修复：

- `scripts/ingest_text_chunks_to_chroma.py` 现在 CLI 参数优先。
- 已重新构建 `guitar_text_chunks_qwen3_06b`。
- 已用 API provider 恢复默认 `guitar_text_chunks` baseline。

恢复命令：

```powershell
.\.venv-mineru\Scripts\python.exe scripts\ingest_text_chunks_to_chroma.py `
  --catalog data\sources\catalog_local_embedding.json `
  --collection guitar_text_chunks `
  --embedding-provider api `
  --batch-size 10 `
  --markdown-max-chars 3500 `
  --reset
```

恢复结果：

```json
{
  "collection": "guitar_text_chunks",
  "embedding_provider": "api",
  "documents": 68,
  "collection_count": 68
}
```

## 7. 本地 Qwen3 RAG 评测结果

### Math Rock PDF source_focus

命令要点：

```text
--tests-file data/eval/mathrock_pdf_query_tests_small.json
--retrieval-mode source_focus
--primary-source mathrock_pdf_steve_h
--text-embedding-provider local_qwen3
--text-model models/embedding/qwen3-embedding-0.6b
--text-collection guitar_text_chunks_qwen3_06b
```

首轮结果：

| 指标 | 结果 |
| --- | ---: |
| tests | 3 |
| bundle pass | 3/3 |
| text Top1 | 100% |
| text Recall@5 | 100% |
| visual Top1 | 100% |
| visual Recall@5 | 100% |
| KG hit rate | 100% |
| avg seconds | 2.91s |

缓存命中结果：

| 指标 | 结果 |
| --- | ---: |
| tests | 3 |
| bundle pass | 3/3 |
| avg seconds | 0.21s |
| text avg seconds | 0.03s |
| visual avg seconds | 0.03s |
| KG avg seconds | 0.15s |

报告：

- `data/eval/mathrock_pdf_query_report_small_qwen3_local_source_focus.md`
- `data/eval/mathrock_pdf_query_report_small_qwen3_local_source_focus_cache_hit.md`

### 全项目 global

命令要点：

```text
--tests-file data/eval/full_project_query_tests_small.json
--text-embedding-provider local_qwen3
--text-model models/embedding/qwen3-embedding-0.6b
--text-collection guitar_text_chunks_qwen3_06b
```

首轮结果：

| 指标 | 结果 |
| --- | ---: |
| tests | 4 |
| bundle pass | 4/4 |
| text Top1 | 100% |
| text Recall@5 | 100% |
| text Precision@5 avg | 0.90 |
| visual Top1 | 100% |
| visual Recall@5 | 100% |
| KG hit rate | 100% |
| avg seconds | 1.44s |

缓存命中结果：

| 指标 | 结果 |
| --- | ---: |
| tests | 4 |
| bundle pass | 4/4 |
| avg seconds | 0.17s |
| text avg seconds | 0.02s |
| visual avg seconds | 0.05s |
| KG avg seconds | 0.12s |

报告：

- `data/eval/full_project_query_report_small_qwen3_local.md`
- `data/eval/full_project_query_report_small_qwen3_local_cache_hit.md`

## 8. 与 API baseline 的小样本对比

| 测试 | API baseline | 本地 Qwen3 | 说明 |
| --- | ---: | ---: | --- |
| Math Rock PDF source_focus | 3/3 | 3/3 | 两者都满分 |
| 全项目 global | 4/4 | 4/4 | 两者都满分 |
| 全项目文本 Top1 | 75% | 100% | 小样本下本地 Qwen3 更稳 |
| 缓存命中平均耗时 | 0.16-0.22s | 0.17-0.21s | 缓存后接近 |

注意：

- 当前样本只有 7 条，不能得出最终模型优劣。
- 本地 Qwen3 首轮耗时主要包含模型加载和首次 query embedding。
- 缓存命中后，本地和 API 的差异主要不在速度，而在是否依赖外部 API。

## 9. 当前架构状态

```text
文本 API baseline:
  collection = guitar_text_chunks
  provider = text-embedding-v4

文本本地 baseline:
  collection = guitar_text_chunks_qwen3_06b
  provider = local_transformers
  model = models/embedding/qwen3-embedding-0.6b

视觉:
  collection = guitar_visual_chunks
  provider = qwen3-vl-embedding API

图谱:
  Neo4j

缓存:
  data/cache/embeddings.sqlite
```

## 10. 风险与后续建议

### 风险

1. 当前本地 embedding 使用 mean pooling，未额外使用模型官方 instruction/prompt 模板。
2. 小样本太少，不能证明大规模鲁棒性。
3. 视觉 embedding 仍走 API，尚未本地化。
4. 本地模型目录约 1.21GB，后续需要在项目说明中标注。

### 建议

1. 用 30 条扩容评测正式比较：
   - `text-embedding-v4`
   - `Qwen3-Embedding-0.6B`
2. 增加 source/style/diagnostic 三类模式的分项指标。
3. 如果 Qwen3 本地在 30 条集上接近或超过 API baseline，就把它设为默认文本 embedding。
4. 后续再接本地 reranker，不急着本地化视觉 embedding。

## 11. 面试展示价值

本次接入后，项目可以明确展示：

- API embedding baseline
- 本地 embedding backend
- 同一套 RAG eval 横向对比
- Chroma 多 collection 隔离
- SQLite embedding cache
- Neo4j + Chroma + 视觉证据融合
- 成本/延迟/离线能力权衡

这比单纯调用 API 更像一个完整、可评测、可部署的 RAG 工程项目。
