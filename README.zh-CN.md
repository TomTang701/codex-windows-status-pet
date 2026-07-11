# Codex Windows 状态宠物

这是一个非官方 Windows Codex 外部伴侣工具，提供小型桌面悬浮窗和通知区域图标，用于显示 Codex 活动、额度和重置次数。

受支持平台：Windows 11 x64。Windows 10 为延期、不声明支持、非阻塞；ARM64 和 32 位 Windows 不在声明范围内。

## 功能

- 通过本机 `codex app-server --stdio` JSON-RPC 接口读取额度。
- 从本机会话 JSONL 文件判断活动中的 Codex 会话。
- 将活动状态、活动会话数、5h 额度、周额度和 Reset Credit 渲染为五个独立稳定行，不暴露计划步骤详情。
- 支持多个显示器，并保留用户填写的虚拟桌面坐标。
- 右键菜单始终完整位于活动显示器工作区内，包括右下角边界。
- 设置包括透明度、一个 80–200% 的按比例“窗口大小”滑块、字体颜色、背景颜色、默认 X/Y 坐标、置顶、锁定位置，以及只能输入数字的 1–10 秒刷新间隔。
- 可选的空闲收缩会缩小悬浮窗并在悬停时展开，默认关闭。
- 周额度和最近未来 Reset Credit 到期时间使用本地 `HH:MM M/D` 格式，月和日不补前导零。
- 设置操作包括保存、应用、恢复默认值和关闭。
- 通知区域菜单支持显示、隐藏、打开设置和退出。
- 使用 `pythonw.exe`，无需保留命令提示符窗口。
- 仓库启动器按需启动伴侣，不会安装 Windows 登录自动启动项。

## 快速启动

双击仓库中的 `start_codex_status_pet.cmd`，或使用工作区根目录的 `启动Codex状态宠物.cmd`。

启动器优先使用 Codex 捆绑的 Python 运行时；不可用时回退到 `PATH` 中的 `pythonw.exe`。回退环境必须安装 `requirements.txt` 中列出的包。

## 数据与安全边界

伴侣只启动本机 Codex app-server，并读取本地 Codex 会话元数据。额度数据源只规范化已经获取的本地数据；不读取 `auth.json`、访问令牌或项目文件，不向第三方服务发送数据，也不维护自建后端。唯一网络活动来自官方本机 Codex app-server 进程。

本地设置保存在 `%USERPROFILE%\.codex\codex-windows-status-pet.json`。

参见 [ROADMAP](docs/product/ROADMAP.zh-CN.md) 了解分阶段路线图，参见 [API_SPEC](docs/architecture/API_SPEC.zh-CN.md) 了解测试边界。
参见 [COMPATIBILITY_MATRIX](docs/quality/COMPATIBILITY_MATRIX.zh-CN.md) 了解当前 Windows 证据和发布门禁。
参见[开发文档首页](docs/README.zh-CN.md)了解文档地图和迁移状态。

## 开发检查

```powershell
python -m py_compile .\scripts\codex_status_pet.py
$py = "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
& $py -m unittest discover -s .\tests -v
```

日常自动 Quality 命令是 `python scripts/run_quality_checks.py`；通过不代表发布批准。正式候选版本使用 `python scripts/run_release_candidate_checks.py`，它会严格执行 `docs/quality/COMPATIBILITY_MATRIX.zh-CN.md` 中的 Windows 阻塞项。
打包冒烟门禁是 `python scripts/package_smoke_test.py`；GitHub Actions 会在 Windows 上运行两组门禁。
使用 `python scripts/check_release_readiness.py` 检查当前兼容性阻塞项和明确延期的实体环境限制。仓库不会自动安装启动文件夹项目。
使用 `python scripts/startup_audit.py` 报告已知旧启动项；该命令只读，只有维护者明确批准后才可删除确认过的旧项目。

发布前，必须在本地仓库明确批准目标 GitHub 所有者。受跟踪的 `.githooks/pre-push` 会在未设置时拒绝推送，也会拒绝所有者不匹配的远程仓库：

```powershell
git config --local core.hooksPath .githooks
git config --local codex.expected-owner <你的-github-用户名>
git config --local user.name "你的 GitHub 显示名称"
git config --local user.email "你的 GitHub noreply 邮箱"
git config --local codex.expected-author-email "你的 GitHub noreply 邮箱"
```

钩子同时校验远程所有者和提交作者邮箱。这样 GitHub CLI 账号、凭据助手或全局 Git 身份不会静默决定发布位置或提交署名。

该应用刻意保持为外部伴侣。Codex 自定义宠物当前提供静态 spritesheet 契约，因此动态文字保留在外部悬浮窗中，不注入内置宠物。

## 许可证

MIT。如果项目所有者添加许可证文件，请以 `LICENSE` 为准。
