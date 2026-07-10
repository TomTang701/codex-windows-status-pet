---
document_id: TESTING
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/quality/TESTING.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 90
---
# 测试

## 必需层级

按需使用Unit、Contract、Integration、UI-contract、Platform、Physical、Packaging和Soak测试。模拟通过不得记录为实体证据。

## 命令

```powershell
$py = "<bundled-python>"
& $py scripts/check_doc_parity.py
& $py -m unittest discover -s tests -q
& $py scripts/run_release_checks.py
```

UI变更需要确定性的适配器测试和Windows人工证据。显示/DPI变更需要几何测试和实体兼容矩阵。安全边界变更需要负向及脱敏测试。

实体记录必须包含日期、commit、Windows build、显示器拓扑、DPI、任务栏位置、结果和安全证据。除明确标记为manual外，测试不得依赖真实Codex账户。

## 最低矩阵

| 变更 | 最低证据 |
|---|---|
| 纯策略或parser | Unit和contract fixture，包含损坏输入 |
| 跨模块状态流 | 使用注入transport/时间/文件系统的Integration测试 |
| Tk或托盘适配器 | UI-contract测试及针对性实体交互 |
| 显示、DPI、任务栏 | 几何测试及带日期Windows实体记录 |
| 打包或启动器 | Package smoke、重复启动检查、干净机器记录 |
| 安全边界 | 负向、脱敏、注入和敏感文件检查 |

Fixture必须合成、最小且无凭据。自动化禁用真实账户；手工账户测试需要明确范围，只能记录安全派生状态。

## 并发、关闭和soak

Race测试覆盖重复刷新、过期generation、文件stat变化、托盘重启、重复close以及关闭期间到达的callback。8小时soak记录内存/进程稳定、刷新连续性、app-server恢复、托盘动作、隐藏/显示、收缩转换、设置修改和最终干净关闭。模拟运行只能标为自动或平台证据，不得标为Physical pass。

## 实体记录模板

每个场景新建 `docs/quality/test-records/YYYY-MM-DD-<scenario>.md`，包含Date、Commit、App version、Windows version/build、显示器拓扑、DPI、任务栏、步骤、预期、实际、结果、限制和安全证据。已有记录是append-only证据，不得覆盖。
