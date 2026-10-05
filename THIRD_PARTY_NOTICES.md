# 第三方许可说明（THIRD PARTY NOTICES）

本仓库在演化过程中使用了以下开源项目的工作流、模板、工具脚本或设计思路。
各项目的许可声明予以完整保留，**不被本仓库 LICENSE 替代或取消**。

---

## 1. 女娲 · Skill 造人术（nuwa-skill）— MIT

- 项目：<https://github.com/alchaincyf/nuwa-skill>
- 作者：花叔（Huashu）
- 许可：MIT，`Copyright (c) 2026 Huashu (花叔)`
- 在本仓库中的作用：**v1.0 / v2.0 的生成框架**——提供"把人物蒸馏为可运行视角技能"的工作流、模板与工具脚本，确立了六维调研结构与"心智模型 + 决策启发式"的组织方式。

## 2. book-to-skill — 用于 EPUB 提取

- 项目：<https://github.com/virgiliojr94/book-to-skill>
- 在本仓库中的作用：**v3.1 / v3.2 的语料提取流水线**。本仓库 `scripts/` 下 `extract_epub.py` 等脚本为其本地适配版本。

## 3. 设计借鉴（仅方法论参考，未包含其代码或文本）

以下项目为本仓库 v5.0 的定向优化提供了设计思路，本仓库**未复制其任何代码或原文内容**：

| 项目 | 许可 | 借鉴的设计 |
|---|---|---|
| [kangarooking/mao-selected-works-skill](https://github.com/kangarooking/mao-selected-works-skill) | MIT | RIA-TV++ 中的 **B 字段（边界与盲点）按单元独立构造**，而非全局共用一张表 |
| [hahadu4520/maoxuanwisdom](https://github.com/hahadu4520/maoxuanwisdom) | 见原仓库 | `type: 正论 / 警示` 论点分型；**"警示优先"**原则；引用可追溯字段（`path` / `location` / `derivation`） |
| [fyfyfy9314-stack/mao-zedong-perspective-skill](https://github.com/fyfyfy9314-stack/mao-zedong-perspective-skill) | MIT | **失效分析**（反右 / 大跃进 / 文革 / 个人崇拜）；**第五卷 1977 年版不与 1–4 卷无差别处理**的版本边界；`SOURCE-MANIFEST` 来源清单 |

---

## 关于原著著作权

- 本仓库**不收录**《毛泽东选集》《毛泽东传》的任何完整原文，仅含提炼后的框架、短引语与索引。
- 原始 EPUB 素材存放于 `references/sources/books/`，已被 `.gitignore` 排除，**不随仓库分发**。
