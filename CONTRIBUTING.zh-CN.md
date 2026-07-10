---
document_id: CONTRIBUTING
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: CONTRIBUTING.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 90
---
# 贡献

当前生效的[工程开发总规范](docs/governance/ENGINEERING_STANDARD.zh-CN.md)是所有贡献的最高层级依据；本文仅补充贡献流程，不得覆盖总规范。

重大工作使用短期分支，并保持 `main` 可发布。变更应有需求、API/文件归属、测试、兼容性影响、安全影响、回滚计划；适用时同步更新中英文文档。

提交前运行相关测试、`scripts/check_doc_parity.py`、`scripts/run_release_checks.py` 和 `git diff --check`。每个提交只包含一个连贯变化并使用祈使语气，同时核验远程所有者和作者身份。不得混入无关用户改动。

## 分支、变更和review规则

重大工作使用短期分支和聚焦提交；不得把无关重大变化直接堆入 `main`。每项变化分类为行为、API、配置schema、UI、性能、安全、文档、打包或实体证据。新行为需要明确API归属、负向和兼容测试、英文原版、同提交中文翻译、Changelog和回滚说明。

每个重大提交前运行 `scripts/run_quality_checks.py` 和 `git diff --check`，检查staged路径，并核验作者/远程owner。正式发布还运行 `scripts/run_release_candidate_checks.py`；预期的严格实体失败必须保持可见，不得绕过。

PR说明需求、root cause、用户影响、安全/隐私影响、兼容证据、测试、文档和回滚。Review必须拒绝隐藏provider变化、Tk阻塞I/O、UI原始dict解析、凭据访问、重复日期/版本逻辑、覆盖不支持schema，或仅凭模拟声明实体通过。
