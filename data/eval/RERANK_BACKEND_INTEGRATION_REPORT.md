# Rerank Backend Integration Report

## 目标

在现有规则召回已经稳定的基础上，加入一个可选的本地 rerank 二阶段排序层。默认不开启，避免影响当前 RAG 结果；需要做 A/B 评测时再通过 `.env` 打开。

## 当前接入方式

新增模块：

- `scripts/rerank_backend.py`

核心函数：

- `RerankConfig.from_env()`：从环境变量读取 rerank 配置。
- `evidence_text_for_rerank(item)`：把 text / visual_caption / kg 证据统一压成“查询-文档对”中的文档文本。
- `apply_model_rerank(query, items, config)`：对候选证据打模型分，并把模型分按权重加回 `EvidenceItem.score`。

主链路接入点：

- `scripts/query_rag_bundle.py`
- 执行顺序为：
  1. Chroma / KG / canonical visual 多路召回
  2. `merge_evidence`
  3. `apply_domain_rerank` 规则重排
  4. `apply_model_rerank` 可选模型重排
  5. `judge_bundle`
  6. 输出 Markdown / JSON 报告

这样保留了当前规则层的主导权，rerank 模型只负责在候选内部微调顺序。

## 配置项

已写入 `.env.example`：

```env
RERANK_BACKEND=none
RERANK_MODEL=models/reranker/qwen3-reranker-0.6b
RERANK_DEVICE=auto
RERANK_BATCH_SIZE=8
RERANK_MAX_LENGTH=1024
RERANK_WEIGHT=0.45
RERANK_ENABLED_TYPES=text,visual_caption,kg
```

说明：

- `RERANK_BACKEND=none`：默认关闭。
- `RERANK_BACKEND=local`：启用本地模型。
- `RERANK_MODEL`：本地模型目录，默认预留给 `Qwen3-Reranker-0.6B` 一类模型。
- `RERANK_WEIGHT`：模型分数加回证据总分的权重。当前建议 0.3-0.45 起步。
- `RERANK_ENABLED_TYPES`：控制哪些证据参与模型重排。

## 模型加载策略

当前实现优先尝试：

1. `sentence_transformers.CrossEncoder`
2. `transformers.AutoModelForSequenceClassification`

如果本地模型不存在、依赖缺失或模型结构不兼容，会自动降级为 no-op，并在 `answer_seed.model_rerank` 中记录：

```json
{
  "enabled": false,
  "provider": "none",
  "reason": "backend_unavailable"
}
```

## 输出变化

每条被模型重排的证据会写入：

```json
"model_rerank": {
  "provider": "...",
  "model": "...",
  "raw_score": 0.0,
  "normalized_score": 0.0,
  "weight": 0.45,
  "delta": 0.0
}
```

整体报告会在 `answer_seed.model_rerank` 中记录 text / visual / kg 三组状态，并在 `timings.model_rerank_seconds` 中记录耗时。

## 已完成验证

编译检查：

```powershell
.\.venv-mineru\Scripts\python.exe -m py_compile scripts\rerank_backend.py scripts\query_rag_bundle.py
```

结果：通过。

默认关闭烟测：

```powershell
$env:RERANK_BACKEND='none'
.\.venv-mineru\Scripts\python.exe scripts\query_rag_bundle.py `
  --query "给出G小调的吉他指型参考" `
  --context-json <canonical_visual_gminor_context.json> `
  --top-k 5 `
  --report-md data\eval\rerank_backend_none_smoke.md `
  --report-json data\eval\rerank_backend_none_smoke.json
```

结果摘要：

- `judgement.sufficient = true`
- `confidence = 0.71`
- `text = 10`
- `visual = 5`
- `kg = 0`
- `model_rerank_seconds ≈ 0.00003s`
- top visual 仍命中 `G 小调指型 4 (Bb 大调指型 3)` 等 canonical visual 证据。

这说明默认关闭时不会额外加载模型，也没有破坏现有召回规则。

## 下一步评测建议

本地模型已下载到：

```text
models/reranker/qwen3-reranker-0.6b
```

当前 backend 已支持 Qwen3 causal-LM reranker 的官方 yes/no 打分方式。

启用设置：

```env
RERANK_BACKEND=local
RERANK_WEIGHT=0.35
```

已完成小规模 A/B：

- 报告：`data/eval/qwen_reranker_smoke_ab_report.md`
- JSON：`data/eval/qwen_reranker_smoke_ab_report.json`

测试 query：

- `给出G小调的吉他指型参考`
- `funk 十六分闷音 groove 伴奏怎么编`
- `Fmaj7 做 mathrock riff 怎么结合开放弦和高把位指型`

初步结果：

- `G 小调视觉召回`：top visual 保持 `fretboard_answer_E14_6`，没有破坏 canonical visual 的强规则命中。
- `funk groove`：top text 从 `chunk_0008` 变为 `chunk_0009`，需要人工比较哪条更贴近“十六分闷音 groove 伴奏”。
- `mathrock Fmaj7`：top text 与 top visual 保持稳定；KG top1 有变化，后续需要扩大样本看是否更合理。
- local rerank 阶段耗时约 `2.1s-4.6s`，取决于候选数量和 evidence 类型数量。

后续建议继续用同一批人工 query 做 A/B：

   - A：`RERANK_BACKEND=none`
   - B：`RERANK_BACKEND=local`

比较：

   - top1 是否更贴近问题
   - top5 是否减少风格/调性误召回
   - visual caption 是否更少被“视觉相似但语义不匹配”的结果挤上来
   - 单次 query 增加耗时是否可接受

建议不要马上把 rerank 权重拉太高。当前规则层已经比较稳，模型 rerank 更适合作为“相关性裁判”，不是替代规则层。
