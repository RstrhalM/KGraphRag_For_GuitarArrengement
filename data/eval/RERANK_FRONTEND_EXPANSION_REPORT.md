# Rerank Frontend Expansion Report

## 本次目标

把 Qwen reranker 的开关和参数接到前端人工 Query 工作台里，方便扩大人工 query 评测，不再需要每次手动改 `.env`。

## 前端新增控件

位置：

- `RAG Query -> Manual Query Collector`

新增字段：

- `Rerank`
  - `关闭`：本次 query 不启用模型 rerank。
  - `本地 Qwen3`：使用 `models/reranker/qwen3-reranker-0.6b`。
  - `使用环境变量`：不覆盖后端环境变量，适合临时命令行实验。
- `Weight`
  - 模型 rerank 分数加回 evidence 总分的权重。
  - 当前建议从 `0.35` 开始。
- `Batch`
  - reranker 每批处理候选数。
  - 当前建议 `4`，更大可能更快但更吃显存。
- `Max Len`
  - 每条 evidence 进入 reranker 的最大 token 长度。
  - 当前建议 `1024`。
- `Rerank Model`
  - 默认 `models/reranker/qwen3-reranker-0.6b`。

## 后端行为

接口：

- `POST /api/query/run`

新增请求字段：

```json
{
  "rerank_backend": "none | local | env",
  "rerank_model": "models/reranker/qwen3-reranker-0.6b",
  "rerank_weight": 0.35,
  "rerank_batch_size": 4,
  "rerank_max_length": 1024
}
```

后端只在本次请求期间临时设置：

- `RERANK_BACKEND`
- `RERANK_MODEL`
- `RERANK_WEIGHT`
- `RERANK_BATCH_SIZE`
- `RERANK_MAX_LENGTH`

请求结束后会恢复原环境变量，避免影响下一次 query。

## 结果展示

前端结果页会显示：

- 本次 `Rerank` 配置。
- `Model Rerank` 状态：
  - text / visual / kg 是否启用。
  - provider，例如 `qwen3_causal_lm`。
  - 参与 rerank 的候选数量。
  - `model_rerank_seconds` 耗时。
- evidence 卡片上会显示 `rerank +delta` badge。

人工 query 历史列表会显示：

- `rerank none`
- `rerank local`
- 或 `rerank env`

点击历史记录时会恢复当时的 rerank 参数。

## 推荐扩大评测方式

每条人工 query 至少跑两次：

1. `Rerank = 关闭`
2. `Rerank = 本地 Qwen3`

然后在反馈面板里重点记录：

- top1 是否变好。
- top5 是否减少明显误召。
- 是否把风格边界搞乱。
- visual caption 是否更贴近具体调性/和弦/指型。
- KG top evidence 是否更像“可用于编曲建议”的关系。
- `model_rerank_seconds` 是否可接受。

建议先固定：

```text
Top K = 5
KG Limit = 8
Weight = 0.35
Batch = 4
Max Len = 1024
```

当样本达到 30-50 条后，再考虑：

- 调整 `Weight = 0.25 / 0.35 / 0.45` 做对比。
- 只对 `text,visual_caption` 启用 rerank，暂缓 KG。
- 引入第二个轻量 reranker 做横向比较。

## 当前注意点

Qwen reranker 对中英文 query 的语义判断是可用的，但它仍然不是规则层替代品。当前项目更适合保持：

```text
Query Normalizer -> 多路召回 -> canonical/规则 rerank -> Qwen model rerank -> 人工反馈
```

也就是说，模型 rerank 是最后一层相关性裁判，而不是负责术语规范化、风格路由或图谱关系推理。
