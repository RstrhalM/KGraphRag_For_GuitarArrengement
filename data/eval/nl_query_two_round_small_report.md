# 自然语言 Query 小批量双轮评测

评测时间：2026-06-02

本轮按旧的 retrieval bundle 结构测试：

1. 单独针对新导入的 Math Rock PDF。
2. 结合整个项目已有知识库。

检索链路包括：

- 文本 Chroma：`guitar_text_chunks`
- 视觉 Chroma：`guitar_visual_chunks`
- Neo4j KG：已导入图谱节点和关系
- SQLite embedding 缓存：`data/cache/embeddings.sqlite`

## 测试文件

| 轮次 | 测试集 | 首次报告 | 缓存命中报告 |
| --- | --- | --- | --- |
| Math Rock PDF 专项 | `data/eval/mathrock_pdf_query_tests_small.json` | `data/eval/mathrock_pdf_query_report_small.md` | `data/eval/mathrock_pdf_query_report_small_cache_hit.md` |
| 全项目混合 | `data/eval/full_project_query_tests_small.json` | `data/eval/full_project_query_report_small.md` | `data/eval/full_project_query_report_small_cache_hit.md` |

## 结果总览

| 轮次 | 用例数 | Bundle 通过率 | 文本 Top1 | 文本 Recall@5 | 视觉 Top1 | 视觉 Recall@5 | KG 命中率 | 首次平均耗时 | 缓存命中平均耗时 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Math Rock PDF 专项 | 3 | 2/3 | 33.3% | 66.7% | 100% | 100% | 100% | 85.44s | 0.19s |
| 全项目混合 | 4 | 4/4 | 75.0% | 100% | 100% | 100% | 100% | 63.87s | 0.16s |

新增 `source_focus` 对照：

| 轮次 | 模式 | Primary source | 用例数 | Bundle 通过率 | 文本 Top1 | 文本 Recall@5 | 视觉 Top1 | 视觉 Recall@5 | KG 命中率 | 平均耗时 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Math Rock PDF 专项 | `source_focus` | `mathrock_pdf_steve_h` | 3 | 3/3 | 100% | 100% | 100% | 100% | 100% | 0.22s |

报告文件：

- `data/eval/mathrock_pdf_query_report_small_source_focus.md`
- `data/eval/mathrock_pdf_query_report_small_source_focus.json`

## Math Rock PDF 专项观察

### `pdf_tapping_simultaneous_rhythm_lead`

- Bundle：通过
- 文本：Recall@5 通过，但 Top1 被 `mathrock_text_course` 抢走。
- 视觉：命中 `mathrock_pdf_steve_h`
- KG：命中 `technique:two_hand_tapping`、`guitar_idiom:simultaneous_rhythm_lead`、`guitar_idiom:solo_guitar_arrangement`

说明：该 query 的语义非常接近之前的 Math Rock 文本课程，因此文本 Chroma 会优先返回文本课程；但 PDF 证据仍在 Top5，图谱和视觉层稳定。

### `pdf_facgce_open_string_voicing`

- Bundle：通过
- 文本：Top1 通过
- 视觉：通过
- KG：命中 `tuning:FACGCE`、`chord:open_Fmaj9`、`pattern:movable_barre_shapes_root_6`

说明：这是本轮最干净的 PDF 专项 case。FACGCE 是 PDF 视觉补抽中的强特征，文本、视觉、图谱三层一致。

### `pdf_clean_maj9_ambient_texture`

- Bundle：未通过
- 文本：Top5 未命中 PDF，全部返回 `mathrock_text_course`
- 视觉：通过
- KG：命中 `chord:maj9`、`color:lush_ambient_texture`、`voicing:open_string_maj9_cluster`

说明：失败点只在文本 Chroma。`clean/open string/maj9/lush/ambient` 这类词与 Math Rock 文本课程中的开放弦、调弦、氛围描述高度相似，文本检索被课程文本吸走。视觉和 KG 已能支撑答案，但当前 bundle 规则要求文本也命中预期源，因此判为未通过。

## 全项目混合观察

### `whole_funk_muted_chuck_space`

- Bundle：通过
- 文本：Top5 全部是 `cory_wong_funk_core`
- KG：命中 muted chuck、sixteenth undercurrent、leave space

说明：Funk 课程的语义边界很清楚，召回稳定。

### `whole_mathrock_open_string_tapping`

- Bundle：通过
- 文本：Top5 全部是 `mathrock_text_course`
- 视觉：命中 `mathrock_pdf_steve_h`
- KG：命中 open string、two hand tapping、wide interval

说明：这个 case 体现了组合检索的价值：文本层偏向课程文本，视觉层补到 PDF 图示，KG 层连接两者。

### `whole_fretboard_triad_arpeggio`

- Bundle：通过
- 文本：Top5 全部是 `fretboard_handbook_mineru`
- 视觉：命中 `P2_arpeggios_chords`
- KG：命中三和弦/琶音相关节点

说明：指板手册的文本与视觉层都稳定，适合作为基础知识类 query 的基准。

### `whole_arrangement_diagnosis_muddy_dense`

- Bundle：通过
- 文本：Recall@5 通过，但 Top1 是 `mathrock_text_course`
- KG：命中 `heuristic:leave_space_for_band`、`voicing:sparse_funk_voicing`、`caution:low_string_sympathetic_resonance`

说明：这是开放式诊断 query，文本源天然会跨 Funk/Math Rock。Top1 不一定等于失败，只要 Top5 能覆盖多源证据，反而符合最终 agent 的使用方式。

## 结论

1. Neo4j 图谱命中稳定：两轮 KG 命中率均为 100%。
2. 视觉 Chroma 很稳：涉及视觉的 5 个 case 全部 Top1/Recall@5 命中。
3. 文本 Chroma 的主要问题不是“找不到”，而是相近 Math Rock 来源之间互相抢 Top1。
4. 对于全项目 agent，跨来源召回是优点；但对“单教材专项评测”，需要更强的 source filter 或 source-aware rerank。
5. 首次运行慢来自 embedding API；缓存命中后，两轮都降到 0.2s 以内单条平均耗时。
6. `source_focus` 能把“专项评测”的 primary source 边界拉清楚，同时保留 support pool 展示跨源辅助证据。

## 下一步建议

1. 专项评测使用 `source_focus`，避免 Math Rock PDF 专项被文本课程抢占。
2. 为全项目评测保留当前宽松召回模式，因为真实用户 query 本来就会跨教材、跨风格。
3. 新增 NLP query 分层：
   - 单源精确检索
   - 多源融合检索
   - 诊断建议类检索
   - 视觉证据强依赖检索
4. GP5 接入后，把 GP5 特征 query 和自然语言 query 放在同一个评测报告里对照。
