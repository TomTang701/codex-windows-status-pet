# Codex Windows 状态宠物

这是一个非官方 Windows Codex 外部伴侣工具，提供桌面悬浮窗和任务栏通知区域图标，用于显示 Codex 活动状态、额度和重置次数。

受支持平台：Windows 11 x64。Windows 10 为延后、不声明支持、非阻塞；ARM64 和 32 位 Windows 不声明支持。

## 功能

- 通过本机 `codex app-server --stdio` 的 JSON-RPC 接口读取额度。
- 通过本机会话 JSONL 文件判断是否有活动中的 Codex 对话。
- 将活动状态、活动对话数量、5h 额度、周额度和重置额度渲染为五个独立稳定行，不显示计划步骤详情。
- 支持多显示器，并保留用户填写的虚拟桌面坐标。
- 右键菜单始终完整位于当前显示器工作区内，包括右下角边界。
- 可配置透明度、字体大小、字体颜色、背景颜色、默认 X/Y 坐标、置顶和锁定位置。
- 可配置窗口宽度、高度、等比例缩放和 1–10 秒刷新间隔。
- 可选的空闲收缩会缩小悬浮窗并在悬停时展开，默认关闭。
- 周额度和最近未来的重置额度到期时间使用本地 `HH:MM M/D` 格式，月份和日期不补前导零。
- 设置操作包括保存、应用、恢复默认值和关闭。
- 托盘菜单支持显示、隐藏、打开设置和退出。
- 使用 `pythonw.exe`，不保留 CMD 控制台窗口。
- 通过 Windows 登录启动项自动启动。

## 快速启动

双击仓库中的 `start_codex_status_pet.cmd`，或使用工作区根目录的 `启动Codex状态宠物.cmd`。

启动器优先使用 Codex 捆绑 Python；找不到时回退到系统 PATH 中的 `pythonw.exe`。

## 数据与安全边界

工具只启动本机 Codex app-server，并读取本机 Codex 会话元数据。额度数据源只规范化已经获取的本地数据；不读取 `auth.json`、访问令牌或项目文件，不向第三方服务发送数据，也没有自建后端。网络活动仅来自官方本机 Codex app-server 进程。

本地设置保存于 `%USERPROFILE%\.codex\codex-windows-status-pet.json`。

参见 [ROADMAP](docs/product/ROADMAP.zh-CN.md) 了解分阶段路线，并参见 [API_SPEC](docs/architecture/API_SPEC.zh-CN.md) 了解测试边界。
参见 [COMPATIBILITY_MATRIX](docs/quality/COMPATIBILITY_MATRIX.zh-CN.md) 了解当前 Windows 证据和发布门槛。
参见[开发文档首页](docs/README.zh-CN.md)了解文档地图和迁移状态。

## 开发检查

```powershell
python -m py_compile .\scripts\codex_status_pet.py
```

日常自动化 Quality 命令是 `python scripts/run_quality_checks.py`，通过不代表发布批准。正式候选版本使用 `python scripts/run_release_candidate_checks.py`，它会严格执行 `docs/quality/COMPATIBILITY_MATRIX.zh-CN.md` 中的实体 Windows 阻塞项。
打包 smoke 门禁命令是 `python scripts/package_smoke_test.py`；GitHub Actions 会在 Windows 上运行两组门禁。
使用 `python scripts/check_release_readiness.py` 查看实体兼容性证据是否仍阻止 v0.3.0 发布。当前仓库不会自动安装启动文件夹项目。
使用 `python scripts/startup_audit.py` 报告已知旧版启动项；该命令只读，只有维护者明确确认后才删除旧项目。

发布前必须在本地仓库中明确批准目标 GitHub 所有者。受跟踪的 `.githooks/pre-push` 会在未设置时拒绝推送，也会拒绝所有者不匹配的远程仓库：

```powershell
git config --local core.hooksPath .githooks
git config --local codex.expected-owner <你的 GitHub 用户名>
git config --local user.name "你的 GitHub 显示名称"
git config --local user.email "你的 GitHub noreply 邮箱"
git config --local codex.expected-author-email "你的 GitHub noreply 邮箱"
```

钩子会同时校验远程仓库所有者和提交作者邮箱，避免机器级 GitHub CLI 账号、凭据助手或全局 Git 身份无声地决定发布位置或提交署名。

本工具刻意保持为外部伴侣。Codex 自定义宠物目前是静态 spritesheet 契约，因此动态文字显示在外部悬浮窗中，不注入内置宠物。

## 许可证

MIT。如果项目所有者添加许可证文件，请以 `LICENSE` 为准。
