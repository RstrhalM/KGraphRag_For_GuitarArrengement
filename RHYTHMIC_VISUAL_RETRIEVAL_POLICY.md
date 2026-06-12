# Rhythmic Visual Retrieval Policy

日期：2026-06-10

本文固定项目中“节奏 / 拍号 / riff / 谱例”类视觉证据的 caption 与召回规则。该策略适用于 Math Rock，也预留给后续 Prog Metal、Funk、Fusion、Emo、Post Rock 等风格教材。

## 1. 目标

当用户询问：

- 某个节拍或拍号下的 riff；
- 非常规节拍、混合拍、节奏分组；
- 带 TAB / 谱例 / 具体演奏片段的问题；
- 某风格的 riff 写法和节奏组织；

视觉层应优先返回“谱例图 / TAB 片段 / riff tab”，而不是普通和弦图、音阶图或指板练习图。

## 2. 适用 Query

典型 query：

```text
给我一个6/8转9/8的I-IV数摇riff
Math Rock 里 7/8 的开放弦 riff 怎么写
给我一个 5/8 + 7/8 的 prog metal riff 谱例
Funk 里 16分切分 groove 有没有谱例
```

触发关键词：

```text
riff
谱例
tab
节拍
拍号
节奏型
groove
odd meter
irregular meter
polymeter
metric modulation
```

## 3. Caption 规范

这类视觉 caption 必须尽量包含：

```text
visual_type: tab_excerpt
visual_subtype: riff_tab
style: math_rock / funk / metal / fusion / ...
tuning: standard / facgce / drop_d / ...
meter: 6_8 / 9_8 / 5_8 / 7_8 / ...
rhythm_grouping: 3_3_3 / 2_2_3 / 3_4 / ...
technique: irregular_meter
technique: accent_displacement
technique: rapid_chord_changes
technique: open_string
concept: riff_composition
```

可选字段：

```text
chord:c_maj7
chord:f_maj7
root:c
root:f
chord_quality:maj7
fret_range: open-15
visible_notation: tab / staff / rhythmic_slashes
```

不要把节奏谱例只标成：

```text
visual_type: chord_diagram
visual_type: scale_pattern
```

除非图片本身确实只是和弦图或音阶图。

## 4. Query 术语抽取

RAG 侧会从 query 中抽取：

```text
6/8 -> meter:6_8
9/8 -> meter:9_8
5/8 -> meter:5_8
7/8 -> meter:7_8
```

当 query 同时包含 `riff / 谱例 / tab / 节拍 / 拍号` 时，会自动加入：

```text
visual_type:tab_excerpt
visual_subtype:riff_tab
technique:riff
concept:riff_composition
```

当 query 明确包含风格词，例如 `math rock / mathrock / 数摇 / 数学摇滚`，会加入：

```text
style:math_rock
```

## 5. 召回优先级

节奏谱例类 query 的视觉排序优先级：

1. 同时命中 `meter:*`、`style:*`、`visual_type:tab_excerpt` 的谱例图。
2. 命中风格和谱例类型，但缺少具体拍号的同风格谱例。
3. 命中节奏或 riff 语义，但不是同风格的谱例。
4. 普通和弦图 / 普通音阶图 / 普通指板图。

对于 `给我一个6/8转9/8的I-IV数摇riff`：

```text
Top1 应为 mr_style_015
matched:
  meter:6_8
  meter:9_8
  style:math_rock
  tuning:standard
  visual_type:tab_excerpt
```

## 6. 边界规则

### 6.1 不把 I-IV 泛化成普通大三和弦图

`I-IV` 可以提示和声框架，但不能让 `chord_quality:maj` 抢占节奏谱例召回。
节奏谱例 query 中，普通 `chord_quality:maj` 只作为弱信号，不作为视觉 required term。

### 6.2 不让基础指板图抢占风格谱例

当 query 明确要求 `riff / 谱例 / 节拍` 时：

- `scale_pattern` 降权；
- `chord_diagram` 降权，除非用户问的是和弦指型；
- `tab_excerpt` 加权；
- `riff_tab` 加权。

### 6.3 调弦仍是硬边界

如果用户没有指明特殊调弦：

```text
target_tuning: standard
required_terms: tuning:standard
```

非标准调弦谱例只能作为后置扩展。

如果用户明确指定 FACGCE / DADGAD / Drop D：

```text
target_tuning: facgce / dadgad / drop_d
```

对应调弦必须优先。

## 7. 当前实现位置

当前已在以下位置实现基础规则：

```text
scripts/query_rag_bundle.py
```

相关函数：

```text
meter_terms_from_query()
is_riff_tab_request()
refine_visual_query_terms()
search_canonical_visual_all()
```

当前已接入：

- 指板手册 canonical sidecar；
- Math Rock style visual canonical sidecar；
- 混合视觉库 `guitar_visual_mixed_mathrock_trial_qwen3_06b`。

## 8. 已验证样例

### Math Rock 6/8 -> 9/8

Query：

```text
给我一个6/8转9/8的I-IV数摇riff
```

期望：

```text
visual_caption:mr_style_015
```

验证结果：

```text
Top1: visual_caption:mr_style_015
image: data/processed/mathrock/style_visual_caption_trial/batch_001_visual_crops/crops/mr_style_015.png
matched:
  meter:6_8
  meter:9_8
  style:math_rock
  tuning:standard
  visual_type:tab_excerpt
```

报告：

```text
data/eval/query_rag_bundle_mathrock_6_8_9_8_after_riff_fix.md
data/eval/query_rag_bundle_mathrock_6_8_9_8_after_riff_fix.json
```

## 9. 后续扩展

后续风格教材 caption 中如出现以下信息，应统一进入 canonical terms：

```text
rhythm_grouping:3_3_3
rhythm_grouping:2_2_3
rhythm_grouping:3_4
concept:polymeter
concept:metric_modulation
technique:accent_displacement
technique:syncopation
technique:ghost_note_groove
technique:odd_meter_riff
```

这会让“节拍型 query”可以跨风格复用同一套召回策略，而不是为每个教材单独写补丁。
