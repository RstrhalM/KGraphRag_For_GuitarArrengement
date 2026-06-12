# A2A 联动方案：Music Fact Agent × Guitar Arrangement Agent

日期：2026-06-10

本文设计当前项目 `KGraphRag2` 与上一级项目 `Cross-Platform Music Fact-Checking & Media MCP Pipeline` 的 Agent-to-Agent 联动方式。

## 1. 两个项目的职责边界

### 1.1 Music Fact MCP Pipeline

上一级项目定位为“外部事实雷达”：

- 核查 `{title, artist}` 歌曲候选是否真实存在。
- 通过 `netease / tencent / kugou / kuwo` 等平台聚合证据。
- 输出 `verified_candidate_pool` 与 `rejected_candidates`。
- 可选拉取 SongBPM 证据：`BPM / key / mode / time_signature / duration`。
- 可选下载或探测媒体链接。
- 以 MCP stdio 暴露工具：
  - `verify_song_candidates`
  - `verify_song_candidates_real`
  - `verify_song_candidates_hybrid`
  - `song_probe`
  - `download_verified_media`
  - `health`

它擅长回答：

```text
这首歌是否真实存在？
标准歌名 / 艺人名是什么？
跨平台是否能互相验证？
BPM / 调性 / 拍号等外部网页证据是什么？
试听链接或媒体资源是否可用？
```

### 1.2 Guitar Arrangement Agent

当前项目定位为“吉他编曲知识与谱例 RAG”：

- 解析用户编曲 query。
- 检索教材文本、视觉 caption、Neo4j KG。
- 返回指型、voicing、riff、节奏、风格迁移建议。
- 使用 Answer Composer 生成结构化回答。
- 前端支持证据可视化和人工评分。

它擅长回答：

```text
这个和弦/调性在吉他上怎么编？
某风格 riff 怎么设计？
有哪些教材证据、指板图、谱例图可参考？
如何把某个乐理/风格概念转成吉他编配建议？
```

## 2. A2A 总体架构

推荐不要把两个项目合并，也不要把 Music Fact 的结果直接灌进 Neo4j。
更稳的做法是：把 Music Fact 项目作为外部 Agent / Tool Agent 调用。

```text
User Query
  -> Guitar Query Normalizer
  -> 判断是否需要现实歌曲事实
  -> Music Fact Agent / MCP song_probe
  -> 返回 SongFactBundle
  -> 转成 Guitar QueryPlan context
  -> Text / Visual / KG RAG
  -> Answer Composer
  -> Answer Verifier
  -> Frontend 展示
```

## 3. 触发条件与实施边界

Music Fact Agent 不进入当前主 RAG 必选链路。它作为后置子模块，在 Agentic RAG 的 Verifier、Memory、Few-shot 等核心模块完善后再接入。

触发条件只保留两类：

1. 用户明确提到某首真实歌曲、艺人、乐队或曲目引用。
2. 用户要求系统推荐参考歌曲、相似歌曲、风格参考曲或可分析曲目。

典型 query：

```text
分析 CHON - Rosewood 的数摇吉他编配思路
Fluffy 这种 CHON 风格 riff 可以怎么写
Periphery - Marigold 的节奏/调性对吉他编配有什么启发
帮我找一首 Polyphia 风格的 riff 作为参考
这首歌 BPM 和调性是什么，再给我编配建议
推荐几首适合学习 Math Rock 点弦的参考歌曲
给我几首 Funk 节奏吉他可以扒的歌
```

Normalizer 可以增加字段：

```json
{
  "needs_song_fact_agent": true,
  "song_fact_trigger": "mentioned_song | recommendation_request",
  "song_candidates": [
    {
      "title": "Rosewood",
      "artist": "CHON",
      "reason_hint": "用户要求基于真实歌曲做风格分析",
      "source": "user_query"
    }
  ]
}
```

不触发场景：

```text
给我一个Cmaj7两手点弦琶音谱例
FACGCE下Am add11开放弦voicing
给我一个6/8转9/8的I-IV数摇riff
Funk C7#9 低把位怎么按
```

这些问题只需要本项目教材 RAG / KG / 视觉 caption，不需要现实歌曲事实核查。

## 4. A2A 消息契约

### 4.1 Guitar -> Music Fact

调用 `song_probe(request)`：

```json
{
  "title": "Rosewood",
  "artist": "CHON",
  "check_media_links": false,
  "fetch_external_evidence": true,
  "evidence_layers": {
    "songbpm": true
  }
}
```

或者批量候选核查：

```json
{
  "candidates": [
    {
      "candidate_id": "song-001",
      "title": "Rosewood",
      "artist": "CHON",
      "reason_hint": "用户指定真实歌曲作为编曲参考",
      "candidate_type": "reference_song",
      "source": "guitar_agent_query"
    }
  ],
  "platforms": ["netease", "tencent", "kugou", "kuwo"]
}
```

### 4.2 Music Fact -> Guitar

本项目建议抽象为 `SongFactBundle`：

```json
{
  "status": "verified",
  "canonical_title": "Rosewood",
  "canonical_artist": "CHON",
  "evidence_level": "multi_source",
  "matched_platform_count": 2,
  "matched_platforms": ["kugou", "kuwo"],
  "bpm": 110.0,
  "key": "G#/Ab",
  "mode": "minor",
  "time_signature": 4,
  "duration_ms": 220000,
  "warnings": [
    "SongBPM is parsed from a public web page, not an official API."
  ],
  "raw": {}
}
```

进入 Guitar RAG 时，转成 QueryPlan context：

```json
{
  "external_song_facts": {
    "title": "Rosewood",
    "artist": "CHON",
    "bpm": 110.0,
    "key_or_tonality": "G#/Ab minor",
    "meter_or_rhythm": "4/4",
    "evidence_level": "multi_source"
  },
  "style_hints": ["mathrock"],
  "retrieval_bias": {
    "needs_style_text": true,
    "needs_rhythm_visual": true,
    "needs_kg": true
  }
}
```

## 5. 三种接入方式

### 5.1 Phase 1：CLI 子进程桥接

最快可跑通方式：本项目后端通过 `subprocess` 调用 sibling 项目的 CLI。

示例：

```powershell
..\Cross-Platform Music Fact-Checking & Media MCP Pipeline\.venv\Scripts\python.exe `
  ..\Cross-Platform Music Fact-Checking & Media MCP Pipeline\mcp_server.py `
  --probe-json '{"title":"Rosewood","artist":"CHON","check_media_links":false,"fetch_external_evidence":true,"evidence_layers":{"songbpm":true}}'
```

优点：

- 不需要先写 MCP client。
- 低风险，可快速 smoke test。
- 便于把 JSON 结果保存到本项目 `data/eval/song_fact_agent/`。

缺点：

- 启动开销较大。
- 不适合高频前端调用。

适合作为第一个实验版本。

### 5.2 Phase 2：MCP stdio client

本项目实现一个轻量 MCP client，启动 sibling 项目的：

```powershell
.\.venv\Scripts\python.exe mcp_server.py --stdio
```

然后调用：

```text
tools/list
tools/call song_probe
```

优点：

- 更接近真正 A2A / Tool Agent 架构。
- 可以复用 sibling 项目的 MCP 工具列表。
- 便于以后接入更多外部 MCP Agent。

缺点：

- 需要管理子进程生命周期、stdio JSON-RPC、超时、错误恢复。

### 5.3 Phase 3：HTTP Wrapper

如果后续两个项目都要长期运行，可以给 Music Fact 项目加 FastAPI wrapper：

```text
POST /api/song/probe
POST /api/song/verify
GET  /api/health
```

本项目通过 HTTP 调用。

优点：

- 前后端、日志、超时、并发更清晰。
- 更适合演示和部署。

缺点：

- 需要改 sibling 项目。

## 6. 本项目新增模块建议

建议新增：

```text
backend/agent_tools/music_fact_agent.py
```

职责：

- 识别 sibling 项目路径。
- 调用 CLI 或 MCP stdio。
- 将 Music Fact 输出归一化成 `SongFactBundle`。
- 写入本地缓存。
- 将错误转成可解释 warning，不阻断主 RAG。

建议新增缓存：

```text
data/eval/song_fact_agent/song_fact_cache.jsonl
```

缓存 key：

```text
normalized_artist + normalized_title + evidence_layers
```

## 7. 前端设计

Full Chain 增加一个可选开关：

```text
[ ] 使用 Music Fact Agent 核查真实歌曲信息
```

如果开启并命中歌曲实体，页面展示：

- Song Fact 状态：verified / rejected / uncertain。
- 标准歌名、艺人名。
- 平台证据数量。
- BPM / Key / Mode / Time Signature。
- warnings。
- 原始 JSON 折叠面板。

Evidence Bundle 新增一类：

```text
external_song_fact
```

Composer 回答中可以引用：

```text
[song_fact:Rosewood_CHON]
```

## 8. 对 Agentic RAG 的价值

这条 A2A 联动会让项目更像真实 Agent 系统：

- Query Normalizer 负责判断任务是否需要外部事实。
- Music Fact Agent 负责现实歌曲核查与参考曲候选验证。
- Guitar RAG Agent 负责教材知识和编曲建议。
- Composer 负责综合证据。
- Verifier 负责检查事实边界和证据引用。

面试表达可以是：

```text
我把系统拆成两个自治 Agent：一个是 Music Fact Agent，负责现实歌曲实体核查和外部证据；另一个是 Guitar Arrangement Agent，负责教材知识、视觉谱例和图谱推理。两个 Agent 通过标准 JSON contract / MCP tool call 进行 A2A 通信。这样可以避免主 RAG 把 LLM 猜测的歌曲信息当事实，同时让编曲建议能够基于真实歌曲的 BPM、调性和拍号进行检索增强。
```

## 9. 推荐实施顺序

该模块不抢当前主线，排在 Agentic 核心模块之后：

```text
Phase A: Answer Verifier / Critic Agent
Phase B: Session Memory 与多轮对话
Phase C: Dynamic Few-Shot / Golden Answers
Phase D: Prompt A/B 与回归评测
Phase E: Music Fact Agent A2A 子模块
```

到 Phase E 时再按以下步骤落地：

1. 写 `music_fact_agent.py`，先用 CLI 子进程桥接。
2. 做 “提及真实歌曲” smoke test：`Rosewood / CHON`、`Fluffy / CHON`。
3. 做 “推荐参考曲” smoke test：让 Composer 先提出候选，再交给 Music Fact Agent 验证。
4. 将 `SongFactBundle` 注入 QueryPlan context。
5. 前端 Full Chain 增加开关和 Song Fact 面板。
6. Composer 支持引用 `external_song_fact`。
7. Verifier 增加外部事实一致性检查。
8. 稳定后再升级为 MCP stdio client 或 HTTP wrapper。

## 10. 风险与边界

- SongBPM 是网页解析证据，不是官方 API，应标记为 `soft_web_evidence`。
- 外部平台搜索可能失败，失败不能阻断主 RAG，只能降级为 warning。
- 现实歌曲事实不能直接写入长期 KG，除非经过人工确认和版权/来源边界评估。
- 媒体下载不是当前本项目主线，应先只使用 metadata，不自动下载音频。
- 若用户只问通用编曲问题，不应触发 Music Fact Agent。
