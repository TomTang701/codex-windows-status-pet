# 测试

English: [English version](TESTING.md)

## 必需层级

按需使用Unit、Contract、Integration、UI-contract、Platform、Physical、Packaging和Soak测试。模拟通过不得记录为实体证据。

## 命令

```powershell
$py = "<bundled-python>"
& $py scripts/check_doc_parity.py
& $py -m unittest discover -s tests -q
& $py scripts/run_quality_checks.py
# 唯一正式自动化发布候选命令。
& $py scripts/run_release_candidate_checks.py
```

机器可观察的 UI 事实必须使用确定性的适配层、Tk、Win32、进程、文件系统或 GitHub 证据。人工视觉确认不是常规门禁。实体证据只保留给不可用硬件/拓扑或真正主观的外观。显示/DPI 变更需要几何测试和真实的实体兼容性分类；安全边界变更需要负向测试和脱敏测试。

`verification-inventory.json` 分类每项发布事实并指定唯一权威检查。`AUTOMATABLE` 工作进入发布范围时必须转换；`PHYSICAL-ONLY` 限制只记录一次，不属于失败测试。`DUPLICATE` 和 `OBSOLETE` 项不得作为独立发布流程。

实体记录必须包含日期、commit、Windows build、显示器拓扑、DPI、任务栏位置、结果和安全证据。除明确标记为manual外，测试不得依赖真实Codex账户。
