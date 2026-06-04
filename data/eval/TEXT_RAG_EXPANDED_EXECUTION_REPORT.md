# Text RAG Expanded Execution Report

日期：2026-06-03

## 目标

收紧文本 RAG 主干，确认本地 Qwen3 文本 embedding 库能稳定召回：

- Cory Wong Funk 吉他课程
- Math Rock 文本课程
- Math Rock PDF 文本
- 吉他指板手册
- 跨来源综合 query

本轮不调用 LLM API，不导入 Neo4j，只测试本地 embedding + Chroma。

## 当前文本库

```text
collection：guitar_text_chunks_qwen3_06b
embedding：Qwen3-Embedding-0.6B
device：CUDA
dimensions：1024
docs：68
```

来源分布：

```text
mathrock_text_course：7
cory_wong_funk_core：14
fretboard_handbook_mineru：37
mathrock_pdf_steve_h：10
```

## 新增脚本

```text
scripts/eval_text_retrieval.py
```

作用：

- 从 Chroma 文本 collection 召回 TopK 文本证据。
- 使用本地 Qwen3 embedding 生成 query 向量。
- 统计 source 命中和关键词命中。
- 支持轻量 rerank。
- 输出 Markdown + JSON 报告。

Rerank 规则：

```text
Chroma 先取更宽候选池，例如 Top25
  -> 保留向量距离
  -> query token 命中加分
  -> 根据 query 推断 source/style intent 加分
  -> 压低作者介绍、如何应用本书等泛化块
  -> 重排回 TopK
```

## 测试集

```text
data/eval/text_rag_expanded_tests.json
```

测试数量：40

覆盖：

- funk rhythm guitar
- muted chuck / ghost note / sixteenth feel
- DADGAD / open string drone / tapping
- Math Rock PDF tapping / shell voicing / alternate tuning
- 指板手册三和弦、七和弦、琶音、加九/六九
- GP5 未来特征映射 query
- 跨来源编配建议 query

## 运行结果

无 rerank：

```text
tests：40
pass_all：33/40
source_hit_at_k：34/40
keyword_hit_at_k：37/40
source_hit_at_1：19/40
keyword_hit_at_1：21/40
avg latency：0.047s/query
```

启用 rerank：

```text
tests：40
pass_all：40/40
source_hit_at_k：40/40
keyword_hit_at_k：40/40
source_hit_at_1：39/40
keyword_hit_at_1：33/40
avg latency：0.048s/query
median latency：0.038s/query
```

Rerank 收益：

```text
pass_all：33/40 -> 40/40
source_hit_at_1：19/40 -> 39/40
source_hit_at_k：34/40 -> 40/40
```

## 输出文件

```text
data/eval/text_rag_expanded_rerank_report.md
data/eval/text_rag_expanded_rerank_report.json
data/eval/text_rag_expanded_no_rerank_report.md
data/eval/text_rag_expanded_no_rerank_report.json
```

## 观察

文本 RAG 主干已经可用。当前最大问题不是 embedding 速度或模型能力，而是：

```text
1. 文本 chunk 偏粗，PDF 与课程转写里一个 chunk 包含大量主题。
2. 一些泛化文本块容易被原始向量召回排到前面。
3. 具体和弦图例更适合由 visual caption 层承担，而不是强求文本 chunk 命中精确和弦名。
```

本轮 rerank 已经显著缓解 2；后续若继续优化，应优先做更细粒度文本 chunk，而不是马上导入 Neo4j。
