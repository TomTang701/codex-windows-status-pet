# 文件规范

## 仓库结构

| 路径 | 用途 |
|---|---|
| `.codex-plugin/plugin.json` | Codex 插件清单和缓存破坏版本号。 |
| `scripts/codex_status_pet.py` | Windows 悬浮窗、托盘、app-server 客户端、活动监视和设置界面。 |
| `scripts/ui/context_menu.py` | 独立的首次点击安全右键菜单 Tk 适配层。 |
| `scripts/ui/settings_dialog.py` | 独立的事务化设置窗口 Tk 适配层。 |
| `scripts/ui/tray_adapter.py` | 独立的通知区域图标和回调适配层。 |
| `scripts/start_pet.ps1` | 允许 PowerShell 的环境下使用的启动脚本。 |
| `start_codex_status_pet.cmd` | 推荐双击启动程序，使用 `pythonw.exe`。 |
| `skills/codex-windows-status-pet/SKILL.md` | Codex 使用该伴侣工具的技能说明。 |
| `README.md` | 主文档，英文版。 |
| `README.zh-CN.md` | 中文快速阅读和维护副本。 |
| `FILE_SPEC.md` | 主文件和配置规范，英文版。 |
| `FILE_SPEC.zh-CN.md` | 中文文件规范。 |
| `CHANGELOG.md` | 主更新日志，英文版。 |
| `CHANGELOG.zh-CN.md` | 中文更新日志。 |
| `API_SPEC.md` / `API_SPEC.zh-CN.md` | API 边界、测试契约和变更分类。 |
| `PRODUCT_REVIEW.md` / `PRODUCT_REVIEW.zh-CN.md` | 英文产品评审及中文翻译副本。 |
| `DEVELOPMENT_PLAN.md` | 英文主开发路线图。 |
| `DEVELOPMENT_PLAN.zh-CN.md` | 开发路线图的中文翻译副本。 |
| `requirements.txt` | 回退 Python 环境的运行时依赖下限。 |
| `tests/` | 无界面 API 和 UI 适配层回归测试。 |
| `scripts/api/quota_format_api.py` | 与 UI 无关的额度/日期格式化 API。 |
| `scripts/api/quota_status_api.py` | 与 UI 无关的额度健康状态分类 API。 |
| `scripts/api/display_mode_api.py` | 与 UI 无关的收缩/展开显示模式 API。 |
| `scripts/api/window_size_api.py` | 与 UI 无关的自由/等比例窗口尺寸 API。 |
| `scripts/api/quota_provider_api.py` | 仅限本地的数据源响应规范化 API，不负责认证或网络。 |
| `COMPATIBILITY_MATRIX.md` / `COMPATIBILITY_MATRIX.zh-CN.md` | 持续维护的 Windows 兼容性和发布门槛记录。 |
| `scripts/api/tray_lifecycle_api.py` | 与 UI 无关的托盘动作和恢复策略 API。 |
| `scripts/api/refresh_scheduler_api.py` | 与 UI 无关的单实例刷新调度 API。 |
| `scripts/check_doc_parity.py` | 英文/中文文档副本结构一致性检查器。 |
| `scripts/run_release_checks.py` | 可重复的自动化发布门禁；实体测试保持独立。 |
| `scripts/package_smoke_test.py` | 校验打包元数据并创建非正式发布 smoke ZIP。 |
| `.github/workflows/ci.yml` | Windows GitHub Actions 质量门禁和 smoke 制品工作流。 |
| `scripts/api/compact_state_api.py` | 与 UI 无关的定时收缩/展开状态和边缘几何 API。 |
| `scripts/api/window_recovery_api.py` | 与 UI 无关的离屏恢复和最近工作区选择 API。 |
| `scripts/api/refresh_controller_api.py` | Activity/Quota 独立刷新通道生命周期 API。 |
| `scripts/api/quota_parse_api.py` | 严格批准字段的额度响应解析 API。 |
| `scripts/api/quota_state_api.py` | 最近成功、过期和明确额度错误状态 API。 |
| `scripts/api/models_api.py` | 类型化额度领域数据类。 |
| `scripts/api/codex_transport_api.py` | 本地 Codex CLI 发现和 app-server stdio JSON-RPC 通信。 |

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
  "y": 1248,
  "window_width": 330,
  "window_height": 138,
  "scale_mode": "free",
  "refresh_interval_seconds": 5,
  "compact_when_idle": false
}
```

`x` 和 `y` 是虚拟桌面坐标，可以指向任意连接的显示器，包括负坐标或超过主显示器范围的坐标。

## 运行不变量

- 同时只允许一个伴侣进程运行。
- 隐藏只把透明度设为 0，不覆盖已保存的位置。
- 打开或关闭设置后，主悬浮窗必须恢复可见。
- 菜单命令只执行一次，命令执行后关闭右键菜单。
- 后台线程不能直接调用 Tk API，界面调度必须留在 Tk 主线程。
- 较大变更在自动发布门禁通过后必须及时提交；远程所有者和作者身份由本地 Git 配置及 pre-push 钩子核验。
