# Full Chain RAG Execution Report

## 目标

完成项目的最小闭环：

```text
用户 Query
-> LLM Query Normalizer
-> Text / Visual Caption / KG 多路召回
-> canonical + 规则 rerank
-> 可选 Qwen3 rerank
-> Evidence Bundle
-> LLM Answer Composer
-> 前端 Full Chain 测试模块展示
```

本阶段不追求答案完美，而是先让端到端链路可运行、可观察、可人工评测。

## 新增模块

### `scripts/answer_composer.py`

作用：

- 接收 evidence bundle。
- 只基于证据生成中文编曲建议。
- 强制引用 `evidence_id`。
- 输出结构化 JSON。

核心函数：

- `compose_answer(bundle, env_file)`
- `build_compose_payload(bundle)`
- `render_answer_markdown(answer)`

输出字段：

- `summary`
- `answer`
- `evidence_used`
- `fretboard_options`
- `style_arrangement_advice`
- `kg_reasoning`
- `theory_checks`
- `uncertainties`
- `next_steps`

特别加入：

- `theory_checks`：用于检查和弦构成、开放弦作为和弦音或 tension 的判断，降低乐理幻觉。

## 后端接入

文件：

- `backend/app.py`

接口：

- `POST /api/query/run`

新增请求字段：

```json
{
  "compose_answer": true
}
```

行为：

- `compose_answer=false`：保持原 evidence bundle 流程。
- `compose_answer=true`：在 bundle 完成后调用 Answer Composer。

返回中新增：

- `composed_answer`
- `answer_composer_error`

报告中新增：

- `## Composed Answer`
- `answer_composer_seconds`

## 前端接入

文件：

- `frontend/index.html`
- `frontend/app.js`
- `frontend/styles.css`

新增侧边栏入口：

- `Full Chain`

新增页面：

- `Full Chain Test`

默认流程：

- 使用 LLM Query Normalizer。
- 默认启用本地 Qwen3 reranker。
- 默认 `RERANK_WEIGHT=0.35`。
- 调用 Answer Composer 生成最终答案。

前端展示：

- 最终回答
- evidence used
- fretboard options
- arrangement advice
- theory checks
- uncertainties
- 答案引用到的视觉证据图片
- 文本证据中的 `image_refs` 图片代码/路径对照
- QueryPlan / Judgement
- Model Rerank 状态
- Text / Visual / KG evidence

### 图片证据侧栏

`Full Chain Result` 现在使用左右布局：

- 左侧：最终答案、QueryPlan、Judgement、Rerank 状态、Text/Visual/KG evidence。
- 右侧：`图片证据` 侧栏。

侧栏分为两块：

- `Answer Visuals`：显示答案引用到的 visual evidence 图片，例如 `visual_caption:fretboard_answer_E04_9` 对应的裁切指板图。
- `Text Image Refs`：显示文本 evidence 中保留的 `image_refs`，以 `img_1: 文件名` 的形式建立代码/路径对照，并可点击打开原图。

这样可以保留教材文本中的图片信息，同时让 Answer Composer 真正调用到的视觉证据可被人工审核。

## Smoke Test

测试 query：

```text
Fmaj7 做 math rock 开放弦 riff 怎么编配，给我可用的指型和节奏建议
```

运行方式：

- `use_normalizer=true`
- `compose_answer=true`
- `rerank_backend=local`
- `top_k=3`
- `kg_limit=5`

输出报告：

- `data/eval/manual_queries/manual_query_20260610_142028_753269dd36.md`
- `data/eval/manual_queries/manual_query_20260610_142028_753269dd36.json`

结果摘要：

- `ok=true`
- Answer Composer 成功返回。
- summary：

```text
在标准调弦下，利用 F 大调音阶指型与开放弦（特别是高音 E、B 弦）的结合，构建包含 Fmaj7 色彩（根音、三音、七音）的 Math Rock Riff，并采用切分节奏与延音技巧。
```

耗时：

```json
{
  "model_load_seconds": 9.553,
  "fretboard_text_seconds": 0.710,
  "style_text_seconds": 0.110,
  "visual_caption_seconds": 0.274,
  "kg_seconds": 0.869,
  "canonical_visual_seconds": 0.230,
  "model_rerank_seconds": 7.143,
  "total_seconds": 19.986,
  "answer_composer_seconds": 40.613
}
```

## 发现的问题与修正

第一次 smoke 暴露了一个典型 Answer Composer 问题：

- 模型把 B 空弦误说成 Fmaj7 的三音。
- 实际上 Fmaj7 的和弦内音是 F、A、C、E。
- B 在 Fmaj7 / F Lydian 语境下更适合解释为 `#11` 色彩音。

已修正：

- Answer Composer prompt 加入乐理自检约束。
- JSON schema 增加 `theory_checks` 字段。
- 前端 Full Chain 页面显示 `Theory Checks`。

重跑 Answer Composer 后验证：

- 输出 `B 音在 F 大调中为 #11 (Lydian 特征音)，在 Fmaj7 语境下可作为色彩音，不应被称为三音。`
- 输出 `Fmaj7 和弦内音为 F, A, C, E。`

重跑报告：

- `data/eval/answer_composer_theory_check_smoke.md`
- `data/eval/answer_composer_theory_check_smoke.json`

## 当前结论

全链路已经跑通：

```text
Normalizer -> RAG -> canonical/rule rerank -> Qwen rerank -> Answer Composer -> 前端展示
```

目前最值得继续评测的是：

- Answer 是否严格引用 evidence_id。
- Answer 是否有乐理错误。
- KG 是否提供有效编曲关系，而不是噪声。
- visual evidence 是否被正确当作指型/把位参考。
- Qwen rerank 是否改善最终答案，而不仅是改善候选排序。

## 后续建议

1. 在 `Full Chain` 页面先跑 10 条人工 query。
2. 对每条记录：
   - 答案是否可执行。
   - 是否引用了正确 evidence。
   - 是否有乐理错误。
   - 是否出现未由证据支持的幻觉。
3. 再决定是否：
   - 为 Full Chain 单独加“答案质量评分”表单。
   - 降低 Answer Composer 输入证据数量以减少耗时。
   - 将 Qwen rerank 默认只用于 text/visual，暂缓 KG。
