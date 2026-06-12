# 项目前后端接口与页面设计报告

日期：2026-06-11

本文固定当前 Guitar Arrangement Inspiration Agent 的本地前后端形态：前端如何组织页面、浏览器如何调用后端、后端如何连接本地知识库 / Chroma / Neo4j / LLM API，以及后续 Agentic RAG 模块如何继续扩展。

## 0. 后续前后端扩展计划（固定版）

当前前端已经从只读浏览器升级为可运行 Query Normalizer、RAG Bundle、Full Chain Answer Composer、人工评分和图片证据查看的研发 Workbench。后续前后端建设的重点，是把 Agentic RAG 的多 Agent 协作、Prompt 版本、记忆反馈和评测闭环显式展示出来。

### 0.0 当前运行约定

- 本地后端统一运行在 `http://127.0.0.1:8765`。
- 8000 端口实例已经停用，前端、接口测试和文档均以 8765 为准。
- 正式指板视觉库为 `guitar_fretboard_answer_captions_qwen3_06b`，当前 389 条。
- 混合视觉试验库为 `guitar_visual_mixed_mathrock_trial_qwen3_06b`，当前 398 条，包含 9 条 Math Rock 风格谱例。
- 选择混合视觉库时，后端会同步启用指板答案与 Math Rock 风格两套 canonical sidecar。

### 0.1 已完成的关键交互

- 人工 query 输入与保存。
- “只规范化”按钮：单独测试 Query Normalizer。
- Full Chain：Normalizer -> Retrieval -> Rerank -> Composer。
- 混合视觉库选择：正式库 / Math Rock trial mixed 库。
- Qwen reranker 开关与 TopK 参数。
- 答案侧边栏展示视觉图片证据和文本证据中的 image refs。
- QueryPlan / Evidence Bundle / Answer / Feedback 分区展示。
- Prompt version 显示：记录 normalizer 与 composer 使用的 prompt 版本。
- 节奏谱例视觉召回：当 query 包含 riff / 谱例 / 节拍 / 拍号时，后端按 `RHYTHMIC_VISUAL_RETRIEVAL_POLICY.md` 优先返回 tab/riff 图。
- 点弦谱例视觉召回：当 query 明确包含点弦、琶音或谱例需求时，优先返回对应 `tab_excerpt`，并检查精确和弦与调弦。
- Math Rock 裁图展示：支持从 canonical sidecar 的嵌套 `source_metadata.image_path` 解析并展示原始裁图。

### 0.1.1 已通过的前端全链路视觉用例

| 人工 Query | 预期视觉证据 | 当前结果 |
|---|---|---|
| `给我一个Cmaj7两手点弦琶音谱例` | Cmaj7 点弦 tab | Top1 `mr_style_010` |
| `给我一个6/8转9/8的I-IV数摇riff` | 6/8、9/8 数摇 riff tab | Top1 `mr_style_015` |

这两条用例同时验证了 Query Normalizer、视觉任务路由、canonical branch、规则 rerank、图片路径解析和前端证据侧栏。

### 0.2 下一批后端接口

| 接口 | 状态 | 用途 |
|---|---|---|
| `GET /api/prompts/versions` | 已完成 | 返回当前 active prompt versions |
| `POST /api/answer/verify` | 计划中 | 独立调用 Verifier / Critic Agent |
| `POST /api/query/run?verify=true` | 计划中 | Full Chain 后自动追加 Verifier 结果 |
| `GET /api/session/state` | 计划中 | 读取当前会话已确认约束和偏好 |
| `POST /api/session/state` | 计划中 | 写入用户确认的风格、调弦、难度、禁用项 |
| `GET /api/golden-answers` | 计划中 | 浏览高分人工问答样例 |
| `POST /api/golden-answers/accept` | 计划中 | 将某次高分结果加入动态 few-shot 候选 |
| `POST /api/fewshot/select` | 计划中 | 根据 QueryPlan 选择 composer few-shot 示例 |
| `POST /api/prompts/ab-run` | 计划中 | 对同一 query 使用不同 prompt 版本进行 A/B 测试 |

### 0.3 Verifier 接口草案

请求：

```json
{
  "query": "Fmaj7 想做数摇式开放和弦",
  "query_plan": {},
  "evidence_bundle": {},
  "answer": {},
  "prompt_versions": {
    "query_normalizer": "query_normalizer_v1.1",
    "answer_composer": "answer_composer_v1.0"
  }
}
```

响应：

```json
{
  "passed": true,
  "risk_level": "low",
  "issues": [],
  "rewrite_required": false,
  "suggested_fix": "",
  "verifier_prompt_version": "answer_verifier_v0.1"
}
```

### 0.4 前端新增页面/面板

- Verifier 面板：显示 pass/fail、risk、issues、suggested_fix。
- Evidence Conflict 面板：展示调弦冲突、风格冲突、文本/视觉证据冲突。
- Session State 侧栏：显示当前会话已确认的风格、调弦、偏好和禁用项。
- Prompt Version 面板：展示本次 query 使用的 prompt 版本，并支持 A/B 选择。
- Golden Answer 面板：将高分人工反馈结果收进 few-shot 候选库。
- Bad Case 面板：把低分 query、召回结果、Verifier issue 和人工备注汇总为优化任务。

### 0.5 前后端调用目标形态

```text
Browser
  -> POST /api/query/run
  -> Query Normalizer
  -> Session State 合并约束
  -> Retrieval Orchestrator
  -> Rule Rerank + Qwen Rerank
  -> Evidence Bundle Builder
  -> Dynamic Few-Shot Selector
  -> Answer Composer
  -> Answer Verifier
  -> Session Memory / Feedback Log
  -> Frontend 分面展示 answer / evidence / verifier / feedback
```

其中，视觉证据分流已经固定三类：

- 和弦/voicing 问题：优先 `chord_diagram`。
- 调性/音阶/指板问题：优先 `scale_pattern` / `fretboard_diagram`。
- riff/谱例/节拍问题：优先 `tab_excerpt` / `riff_tab`，并匹配 `meter:*`、`rhythm_grouping:*`。

## 1. 当前定位

当前前后端不是最终产品化应用，而是一个面向研发和评测的本地 Workbench。它的核心目标是让项目进入可观察、可调试、可评测的状态：

- 能浏览教材文本分块、视觉证据、图谱和评测报告。
- 能在前端输入人工 query，收集真实问题。
- 能单独测试 Query Normalizer，也能跑完整 RAG 链路。
- 能展示文本证据、视觉证据、KG 匹配、rerank 结果和最终 LLM 生成答案。
- 能保存人工 query、反馈、报告，作为后续评测集和 Agent 策略优化数据。

## 2. 技术结构

当前采用轻量本地架构：

- 后端：FastAPI，入口为 `backend/app.py`。
- 前端：静态 HTML / CSS / JavaScript，入口为 `frontend/index.html`、`frontend/app.js`、`frontend/styles.css`。
- 页面托管：FastAPI 直接服务前端静态文件。
- 本地知识数据：`data/processed`、`data/knowledge`、`data/eval`。
- 向量库：本地 Chroma。
- 图谱库：本地 Neo4j。
- 本地模型：embedding / reranker 可走本地模型目录。
- 外部 LLM API：用于 Query Normalizer、KG 抽取、视觉 caption、Answer Composer 等需要语言推理的模块。

浏览器与后端之间主要通过 JSON API 通信。后端内部再访问本地文件、Chroma、Neo4j、本地模型和外部 LLM API。

## 3. 网络调用链路

### 3.1 页面加载

用户访问本地服务根路径：

```text
Browser -> GET / -> frontend/index.html
Browser -> GET /static/app.js
Browser -> GET /static/styles.css
```

前端加载后，根据不同页面发起 `/api/...` 请求。

### 3.2 普通数据浏览

```text
Browser
  -> FastAPI /api/books 或 /api/chunks
  -> Backend 读取 data/processed 下的 Markdown / JSON / manifest
  -> 返回 JSON
  -> Frontend 渲染教材、分块、图片引用
```

### 3.3 图片访问

```text
Browser
  -> GET /api/file?path=<workspace-relative-image-path>
  -> Backend 校验路径仍在 workspace 内
  -> 返回本地图片文件
  -> Frontend 在 chunks / visual evidence / full chain 侧边栏展示图片
```

这个设计让前端可以展示本地教材切图，但不会直接暴露任意磁盘路径。

### 3.4 RAG 查询

```text
Browser
  -> POST /api/query/run
  -> Backend 可选调用 Query Normalizer
  -> Backend 调用 scripts/query_rag_bundle.py 的检索链路
  -> 查询 Chroma 文本库 / 视觉 caption 库 / Neo4j KG
  -> 规则 rerank 或 Qwen reranker 重排
  -> 可选调用 Answer Composer 生成最终答案
  -> 写入 data/eval/manual_queries
  -> 返回 bundle / answer / image evidence / timing
```

### 3.5 Query Normalizer

```text
Browser
  -> POST /api/query/normalize
  -> Backend 读取规范化 prompt
  -> 调用已配置 LLM API
  -> 返回 query_plan / normalized_query / canonical_terms / retrieval_intent
```

Query Normalizer 当前作为 Agentic RAG 的第一个子 Agent：负责把用户自然语言问题转成更适合库内召回的结构化查询计划。

### 3.6 Full Chain

Full Chain 是当前端到端链路验证模块：

```text
用户 query
  -> Query Normalizer
  -> Text RAG + Visual Caption RAG + KG
  -> Rule Rerank / Qwen Rerank
  -> Evidence Bundle
  -> Answer Composer
  -> Theory Checks
  -> 前端展示答案、证据、图片侧边栏、调试信息
```

它不是只看最终答案，而是把“答案用了哪些证据、图片来自哪里、理论检查有没有发现风险”都展示出来。

## 4. 后端接口清单

### 4.1 基础状态

| 方法 | 路径 | 作用 |
|---|---|---|
| `GET` | `/api/health` | 服务健康检查，确认后端可访问 |
| `GET` | `/api/dashboard` | 返回项目数据概览，用于首页仪表盘 |

### 4.2 教材与分块浏览

| 方法 | 路径 | 作用 |
|---|---|---|
| `GET` | `/api/sources` | 返回已接入的数据源 / 教材来源 |
| `GET` | `/api/books` | 返回可浏览的课本母目录 |
| `GET` | `/api/chunks` | 按课本 / 类型返回分块列表 |
| `GET` | `/api/chunk` | 返回单个 chunk 的正文、metadata、图片引用 |
| `GET` | `/api/visuals` | 返回视觉 caption / 视觉证据条目 |
| `GET` | `/api/file` | 读取本地图片或文件，用于前端展示 |

### 4.3 Neo4j 图谱

| 方法 | 路径 | 作用 |
|---|---|---|
| `GET` | `/api/graph/summary` | 图谱节点、关系、标签等概览 |
| `GET` | `/api/graph/filters` | 返回图谱筛选项 |
| `GET` | `/api/graph/search` | 搜索图谱节点 / 关系 |
| `GET` | `/api/graph/neighborhood` | 查询某个节点的邻域关系 |

### 4.4 Query Workbench

| 方法 | 路径 | 作用 |
|---|---|---|
| `GET` | `/api/query/prompts` | 返回 query 输入提示和测试建议 |
| `GET` | `/api/query/logs` | 返回人工 query 历史 |
| `GET` | `/api/query/feedback` | 返回人工反馈记录 |
| `POST` | `/api/query/feedback` | 保存本次 query / RAG 结果的人工评分 |
| `POST` | `/api/query/save` | 保存人工输入 query，不一定运行 RAG |
| `POST` | `/api/query/normalize` | 只运行 Query Normalizer，返回 query plan |
| `POST` | `/api/query/run` | 运行 RAG 或 Full Chain |

### 4.5 报告阅读

| 方法 | 路径 | 作用 |
|---|---|---|
| `GET` | `/api/reports` | 列出可读的评测 / 执行报告 |
| `GET` | `/api/report` | 读取指定 Markdown 报告 |

## 5. 核心请求模型

### 5.1 QueryRunRequest

`POST /api/query/run` 是当前最重要的接口。它承载普通 RAG、rerank 测试、Full Chain 答案生成。

主要字段：

| 字段 | 作用 |
|---|---|
| `query` | 用户原始问题 |
| `notes` | 人工备注，用于评测记录 |
| `tags` | 人工标签，例如 funk、mathrock、fretboard |
| `context` | 额外上下文 |
| `top_k` | 文本 / 视觉召回数量 |
| `kg_limit` | KG 返回上限 |
| `use_normalizer` | 是否先调用 Query Normalizer |
| `rerank_backend` | rerank 后端，例如 rule 或 qwen |
| `rerank_model` | rerank 模型路径或名称 |
| `rerank_weight` | rerank 权重 |
| `rerank_batch_size` | rerank 批大小 |
| `rerank_max_length` | rerank 输入截断长度 |
| `compose_answer` | 是否调用 Answer Composer 生成最终回答 |

### 5.2 QueryNormalizeRequest

用于只测试规范化效果，不跑完整 RAG。

主要字段：

- `query`
- `context`
- `tags`

返回内容应包含规范化后的查询表达、意图、风格约束、乐理实体、检索策略等。

### 5.3 QueryFeedbackRequest

用于把前端人工评分保存为评测数据。

建议反馈维度：

- Query Normalizer 是否理解正确。
- 文本召回是否相关。
- 视觉证据是否可用。
- KG 是否命中合理。
- rerank 排序是否优于原始召回。
- 最终答案是否可执行。
- 是否存在乐理错误或过度推断。

## 6. 前端页面设计

### 6.1 Dashboard

首页仪表盘展示项目状态：

- 已接入数据源数量。
- 文本 / 视觉 / KG 数据概览。
- 最近报告。
- 当前系统运行状态。

它的作用是快速判断项目是否处在可测试状态。

### 6.2 Datasets

数据源页面用于浏览当前已接入教材：

- 吉他指板手册。
- Funk 节奏吉他课程。
- Math Rock 文本课程。
- Math Rock PDF。
- 后续新增风格教材。

这个页面帮助确认每本教材是否已经完成文本层、视觉层、KG 层或评测层处理。

### 6.3 Chunks

分块页面按“课本母目录 -> chunk”组织：

- 先选择教材。
- 再选择该教材下的分块。
- 展示 Markdown 正文、metadata、图片引用。
- 对新版指板练习答案整合块，也放在指板教材母目录下浏览。

这个页面主要用于人工确认分块质量，尤其是教材 OCR、答案对照、图片路径是否正确。

### 6.4 Visual Evidence

视觉证据页面展示视觉 caption 层：

- 图片切块。
- 视觉 caption。
- canonical terms。
- 关联练习 / 题号 / 小题号。
- 本地图片预览。

当前设计重点是“视觉证据层作为 RAG 可召回材料”，不急于把练习 caption 全部导入 Neo4j 主 KG。

### 6.5 RAG Query

RAG Query 页面用于人工 query 评测：

- 输入用户自然语言问题。
- 可选择只保存 query。
- 可选择只运行 Query Normalizer。
- 可运行 RAG bundle。
- 可选择 top_k、kg_limit、rerank backend 等参数。
- 显示文本召回、视觉召回、KG 匹配、rerank 结果。
- 保存人工反馈评分。

这个页面是后续构建真实评测集的入口。

### 6.6 Full Chain

Full Chain 页面用于验证完整 Agentic RAG 雏形：

- 输入一个面向吉他编曲的真实问题。
- 运行 Query Normalizer。
- 运行混合检索。
- 运行 rerank。
- 调用 Answer Composer。
- 展示最终答案。
- 展示理论检查结果。
- 在侧边栏展示答案调取的图片证据。
- 保留文本证据中的图片引用代码对照。

当前它是最接近最终产品体验的页面。

### 6.7 Graph

图谱页面用于查看 Neo4j 知识图谱：

- 图谱概览。
- 节点搜索。
- 邻域关系查询。
- 过滤节点类型和关系类型。

当前 KG 更适合承载结构化概念、风格技法、编配关系；视觉练习答案优先作为 caption RAG 证据层存在。

### 6.8 Eval Reports

报告页面读取本地 Markdown：

- query 评测报告。
- rerank A/B 报告。
- full chain 执行报告。
- caption 处理报告。
- 项目框架文档。

这个页面让项目的评测和开发过程可追溯。

## 7. 当前已形成的页面能力

当前前端已经不是纯展示页，而是一个研发闭环工具：

- 数据浏览：能看教材、分块、图片。
- 知识观察：能看视觉 caption、KG、报告。
- Query 收集：能记录人工 query。
- Normalizer 测试：能单独看 query plan。
- RAG 测试：能看召回和重排。
- Full Chain 测试：能看最终答案和证据图片。
- 人工反馈：能逐步积累 query 质量评价数据。

这为后续 Agentic RAG 提供了一个很重要的基础：不是凭感觉改 prompt，而是用前端收集的 query 和反馈驱动迭代。

## 8. 当前边界

### 8.1 不是公开 Web 服务

当前应用默认面向本地开发，不设计公网部署。原因：

- 教材材料涉及版权边界。
- `.env` 中有 API key。
- 本地 Chroma / Neo4j / 模型路径依赖开发机环境。

### 8.2 不把所有视觉 caption 都塞进主 KG

目前判断是：

- 主 KG 适合存稳定概念和关系。
- 视觉 caption 更适合作为证据层。
- 指板练习答案图主要用于“可视化指型推荐”和“答案证据”，不必全部变成 KG 节点。

### 8.3 Query Normalizer 不是最终 Agent

它只是 Agentic RAG 的第一个子 Agent。完整 Agent 还需要：

- Evidence Planner。
- Retrieval Controller。
- Answer Composer。
- Answer Verifier。
- Revision Agent。
- Session Manager。

## 9. 后续接口扩展计划

### 9.1 Answer Verifier

新增接口建议：

```text
POST /api/query/verify
```

作用：

- 输入 query、answer、evidence bundle。
- 检查答案是否引用证据。
- 检查乐理推断是否可能错误。
- 标记“证据不足”“调性不一致”“和弦音解释错误”等风险。

### 9.2 Answer Revision

新增接口建议：

```text
POST /api/query/revise
```

作用：

- 基于 verifier 的问题清单修正答案。
- 保留原证据编号。
- 输出更保守、更可验证的版本。

### 9.3 A/B Rerank Compare

新增接口建议：

```text
POST /api/query/compare-rerank
```

作用：

- 同一个 query 同时跑 rule rerank 和 Qwen rerank。
- 前端并排展示 Top N。
- 人工选择哪边更好。

### 9.4 Session Manager

新增接口建议：

```text
POST /api/session/create
GET /api/session/{id}
POST /api/session/{id}/query
```

作用：

- 支持多轮编曲讨论。
- 保存用户目标、风格、调性、谱例分析结果、历史证据。

### 9.5 GP5 / 乐谱分析

新增接口建议：

```text
POST /api/score/upload
POST /api/score/analyze
GET /api/score/{id}/features
POST /api/score/{id}/rag
```

作用：

- 导入 `.gp5` 或其他谱面文件。
- 提取 BPM、调性、和声进行、riff、节奏型。
- 把乐谱特征转成 query plan。
- 调用当前 RAG 系统生成编配建议。

## 10. 推荐开发顺序

1. 先稳定 Full Chain 页面：保证 query、证据、图片、答案都能顺畅展示。
2. 加 Answer Verifier：把“答案对不对”从人工感觉变成结构化检查。
3. 加 Rerank A/B 前端对比：让人工 query 评测可以稳定积累。
4. 加 Session Manager：让系统从单问答变成编曲协作流程。
5. 再接 GP5 分析：把乐谱特征作为 Agentic RAG 的上游输入。

这个顺序比较稳，因为它先把 RAG 的可解释性和评测闭环做好，再把乐谱分析接进来。否则 GP5 分析即使做出来，也很难判断后面的建议到底是检索问题、重排问题，还是生成问题。
# Prompt Version Interface Update

新增接口：

```text
GET /api/prompts/versions
```

用途：查看当前 Query Normalizer、Answer Composer、Answer Verifier 的 prompt registry。

`POST /api/query/run` 返回的 `bundle.prompt_versions` 会在前端 Query / Full Chain 结果面板展示。
