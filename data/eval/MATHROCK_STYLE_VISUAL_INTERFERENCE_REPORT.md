# Math Rock 风格视觉混合库抗干扰报告
日期：2026-06-10

## 测试目标

验证 9 条 Math Rock 风格视觉 caption 加入现有指板视觉库后：

1. 风格查询能否优先命中新视觉证据。
2. 普通和弦、琶音和练习查询是否仍优先命中基础指板教材。
3. 规则 rerank 是否能执行调弦、风格模式和否定技法边界。

## 测试集合

- 基础视觉 caption：389 条
- Math Rock 风格 caption：9 条
- 混合集合：398 条
- 临时集合：`guitar_visual_mixed_mathrock_trial_qwen3_06b`
- 正式集合：未修改
- Embedding：本地 `Qwen3-Embedding-0.6B`
- 设备：CUDA
- 向量维度：1024

测试 query：

- Math Rock 正向：7 条
- 基础能力保持：7 条
- 合计：14 条

## 结果

| 方案 | Math Rock Hit@1 | 基础保持 Hit@1 | 总 Hit@1 | 总 Hit@5 |
|---|---:|---:|---:|---:|
| 原始基础库 rerank | - | 7/7 | 7/7 | 7/7 |
| 混合库无 rerank | 7/7 | 5/7 | 12/14 | 14/14 |
| 混合库旧 rerank | 7/7 | 5/7 | 12/14 | 13/14 |
| 混合库边界 rerank v2 | 7/7 | 7/7 | 14/14 | 14/14 |

最终 rerank v2：

- 平均总耗时：约 `0.078s`
- 中位总耗时：约 `0.046s`
- miss：0

## 干扰案例

### 普通 G7

Query：

`标准调弦 G7 属七和弦普通指型图`

无边界规则时，FACGCE 的 Math Rock G7 被推到 Top1。

加入标准调弦与基础意图约束后：

- Top1：`fretboard_answer_E51_8`
- 来源：`fretboard_handbook_question_answer`

### 基础 Cmaj7

Query：

`标准调弦 Cmaj7 大七和弦基础指型，不需要点弦谱例`

无边界规则时，Math Rock Cmaj7 点弦谱例被推到 Top1；旧 rerank 甚至使正确基础图掉出 Top5。

加入否定技法与基础意图约束后：

- Top1：`fretboard_answer_E51_10`
- 来源：`fretboard_handbook_question_answer`

## 新增边界规则

1. Query 明确包含 `Math Rock / 数摇 / 数学摇滚` 时，提高风格证据层权重。
2. Query 包含 `普通 / 基础 / 常规` 且未指定风格时，降低风格专用证据权重。
3. Query 指定标准调弦时：
   - 明确 `tuning=standard` 的证据加分。
   - 明确为 FACGCE 等特殊调弦的证据强惩罚。
4. Query 包含 `不需要点弦 / 不要点弦 / 非点弦` 时，点弦证据强惩罚。
5. 同类规则已为琶音、开放弦否定表达预留。

## 结论

这 9 条 Math Rock 视觉数据已经通过小规模混合库抗干扰测试。

关键结论不是“向量模型自动解决了一切”，而是：

- 细粒度视觉裁切让风格证据具备独立召回能力。
- canonical terms 保证特殊调弦、和弦、技法和节拍可稳定匹配。
- Query 的调弦、风格模式和否定条件必须在 rerank 阶段执行。
- 只依赖向量相似度会让风格化谱例污染普通和弦查询。

## 后续建议

1. 暂不直接覆盖正式集合，先把混合集合接入前端 A/B 测试。
2. 收集更多自然语言表达，尤其是“不需要某技法”“只要基础指型”等负约束。
3. 扩展到 20-30 条 Math Rock 图后重复本测试。
4. 稳定后将边界规则迁移到正式 query plan / rerank 链路。
