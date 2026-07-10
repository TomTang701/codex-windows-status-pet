# 文件规范

## 本次运行规范补充

- 启动时会结束窗口标题为 `Codex Windows Status Pet` 的旧 `python.exe`/`pythonw.exe` 伴侣进程，然后取得命名互斥体，避免重复测试产生多个悬浮窗和托盘图标。
- 检测到 Codex 计划时，主界面第二行显示 `活动对话 N 个（第 M/K 步）`；`M` 为已完成步骤数加一，并且不会超过 `K`。
- 主界面右键菜单第一次左键点击就执行命令，并在执行后关闭菜单。

## 仓库结构

| 路径 | 用途 |
|---|---|
| `.codex-plugin/plugin.json` | Codex 插件清单和缓存破坏版本号。 |
| `scripts/codex_status_pet.py` | Windows 悬浮窗、托盘、app-server 客户端、活动监视和设置界面。 |
| `scripts/start_pet.ps1` | 允许 PowerShell 的环境下使用的启动脚本。 |
| `start_codex_status_pet.cmd` | 推荐双击启动程序，使用 `pythonw.exe`。 |
| `skills/codex-windows-status-pet/SKILL.md` | Codex 使用该伴侣工具的技能说明。 |
| `README.md` | 主文档，英文版。 |
| `README.zh-CN.md` | 中文快速阅读和维护副本。 |
| `FILE_SPEC.md` | 主文件和配置规范，英文版。 |
| `FILE_SPEC.zh-CN.md` | 中文文件规范。 |
| `CHANGELOG.md` | 主更新日志，英文版。 |
| `CHANGELOG.zh-CN.md` | 中文更新日志。 |

## 运行时配置

`%USERPROFILE%\.codex\codex-windows-status-pet.json`

```json
{
  "alpha": 0.35,
  "font_color": "#e5e7eb",
  "font_size": 10,
  "background_color": "#000000",
  "topmost": true,
  "locked": true,
  "x": 4151,
  "y": 1248
}
```

`x` 和 `y` 是虚拟桌面坐标，可以指向任意连接的显示器，包括负坐标或超过主显示器范围的坐标。

## 运行不变量

- 同时只允许一个伴侣进程运行。
- 隐藏只把透明度设为 0，不覆盖已保存的位置。
- 打开或关闭设置后，主悬浮窗必须恢复可见。
- 菜单命令只执行一次，命令执行后关闭右键菜单。
- 后台线程不能直接调用 Tk API，界面调度必须留在 Tk 主线程。
