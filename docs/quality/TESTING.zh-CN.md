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
