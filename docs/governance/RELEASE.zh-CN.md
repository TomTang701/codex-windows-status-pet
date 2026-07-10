---
document_id: RELEASE
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/governance/RELEASE.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 90
---
# 发布

当前生效的[工程开发总规范](ENGINEERING_STANDARD.zh-CN.md)是本发布流程的最高层级依据。

## 门禁

`scripts/run_quality_checks.py` 是日常 push/PR 门禁，执行manifest和链接、版本/敏感文件/依赖/双语检查、递归编译 `scripts` 下全部Python文件、测试、启动项审计、非严格就绪报告和package smoke。旧名称 `run_release_checks.py` 保留为兼容入口。

`scripts/run_release_candidate_checks.py` 是正式手工/tag门禁，在Quality基础上还要求严格实体就绪、tag触发时版本匹配、正式更新日志版本、回滚说明、非空制品和SHA-256 checksum。日常Quality通过不等于批准发布。

发布前必须完成自动检查、必需实体矩阵、版本来源一致性、双语一致性、敏感文件扫描、干净环境启动、更新日志、已知问题和回滚说明。当前实体阻塞项由 `scripts/check_release_readiness.py --strict` 报告。

运行时依赖策略在 `requirements.txt` 中使用最低兼容版本。发布门禁会检查每项声明已安装、满足最低版本并且可以导入；当前已验证环境为 Pillow 12.2.0 和 pystray 0.19.5。

## 支持的运行时声明

- 支持系统：Windows 11 x64 已完成实体测试；Windows 10 仍待实体验证。
- Python/运行时：CI基线为Python 3.11；本地已验证Python 3.12.13。回退运行时必须提供 `pythonw.exe` 并安装 `requirements.txt`。
- 架构：已测试架构为x64 Windows；不宣称支持ARM64或32位Windows。
- 未签名行为：项目不提供已签名二进制；打包发布时可能出现Windows SmartScreen或策略警告，必须记录。

## 版本和回滚

采用Semantic Versioning。应用、manifest、更新日志、包、制品和诊断中的版本必须一致。记录上一个稳定版本、配置兼容性、重装路径、降级限制和备份/恢复路径。

重大变更使用聚焦提交，且只有在 `scripts/run_quality_checks.py` 和 `git diff --check` 通过后推送。正式候选还必须通过 `scripts/run_release_candidate_checks.py`。远程所有者必须保持为 `TomTang701`。

## 候选和tag流程

1. 选择canonical版本，并一起更新runtime、plugin manifest、Changelog、诊断和package版本来源。
2. 运行Quality、完成所有阻塞实体记录，再运行严格Release Candidate套件。
3. 检查ZIP内容、checksum、依赖列表、未签名状态、干净机器证据、known issues和配置降级限制。
4. 只从已验证commit创建 `v<version>` tag；tag workflow必须复现相同制品检查。
5. 同时发布制品和 `.sha256`，并附支持的Windows/runtime范围及回滚说明。

## 回滚流程

停止托盘进程，保留当前设置和 `.bak`，重新安装上一已知良好制品，并通过根启动器重启。如果当前配置schema高于旧应用支持范围，不得让旧版本直接使用它；保留文件并恢复兼容backup，或经用户确认后明确重置。记录撤回的commit/tag、制品checksum、原因、用户影响和替代版本。不得重写旧证据或静默移动release tag。
