# Codex Windows Status Pet 文档

这里是开发文档首页。英文是唯一事实来源；英文文件旁边的 `.zh-CN.md` 文件是对应的中文翻译。

## 从这里开始

| 读者 | 首先阅读 |
|---|---|
| 用户 | [根目录 README](../README.zh-CN.md) |
| 贡献者 | [工程开发总规范](governance/ENGINEERING_STANDARD.zh-CN.md)、[路线图](product/ROADMAP.zh-CN.md) |
| API或UI开发者 | [API规范](architecture/API_SPEC.zh-CN.md)、[仓库结构](architecture/REPOSITORY_STRUCTURE.zh-CN.md)、[配置](architecture/CONFIGURATION.zh-CN.md) |
| 测试或发布维护者 | [兼容性矩阵](quality/COMPATIBILITY_MATRIX.zh-CN.md)、[测试错误报告](archive/audits/2026-07-09-test-error-report.md) |

## 文档分类

- **规范类：** 定义必须遵守的行为或流程。
- **描述类：** 解释当前设计或产品。
- **证据类：** 记录自动化或实体测试结果。
- **历史类：** 保存已完成的审计或已被替代的计划。

仓库正在按照[文档结构优化方案](../Goal/codex-status-pet-documentation-structure-plan-zh.md)从根目录平铺结构迁移到分层结构。manifest会记录当前有效路径，并保持现有链接兼容。

## 唯一事实来源

英文文档是权威版本。中文翻译必须保留标题、标识符、表格、代码示例、版本和要求，并在英文发生实质变化的同一提交中更新。

机器可读的文档清单是 [`document_manifest.json`](document_manifest.json)。文档变更后应运行仓库发布检查。
