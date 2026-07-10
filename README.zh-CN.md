# Codex Windows 状态宠物

这是一个非官方 Windows Codex 外部伴侣工具，提供桌面悬浮窗和任务栏通知区域图标，用于显示 Codex 活动状态、计划完成度、额度和重置次数。

## 功能

- 通过本机 `codex app-server --stdio` 的 JSON-RPC 接口读取额度。
- 通过本机会话 JSONL 文件判断是否有活动中的 Codex 对话。
- 只显示当前活动对话数量，不显示计划步骤详情。
- 支持多显示器，并保留用户填写的虚拟桌面坐标。
- 可配置透明度、字体大小、字体颜色、背景颜色、默认 X/Y 坐标、置顶和锁定位置。
- 设置操作包括保存、应用、恢复默认值和关闭。
- 托盘菜单支持显示、隐藏、打开设置和退出。
- 使用 `pythonw.exe`，不保留 CMD 控制台窗口。
- 通过 Windows 登录启动项自动启动。

## 快速启动

双击仓库中的 `start_codex_status_pet.cmd`，或使用工作区根目录的 `启动Codex状态宠物.cmd`。

启动器优先使用 Codex 捆绑 Python；找不到时回退到系统 PATH 中的 `pythonw.exe`。

## 数据与安全边界

工具只启动本机 Codex app-server，并读取本机 Codex 会话元数据；不读取 `auth.json`，不向第三方服务发送项目文件，也没有自建后端。网络活动仅来自官方本机 Codex app-server 进程。

本地设置保存于 `%USERPROFILE%\.codex\codex-windows-status-pet.json`。

## 开发检查

```powershell
python -m py_compile .\scripts\codex_status_pet.py
```

本工具刻意保持为外部伴侣。Codex 自定义宠物目前是静态 spritesheet 契约，因此动态文字显示在外部悬浮窗中，不注入内置宠物。

## 许可证

MIT。如果项目所有者添加许可证文件，请以 `LICENSE` 为准。
