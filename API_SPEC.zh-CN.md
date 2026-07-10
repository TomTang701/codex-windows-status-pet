# API 与测试边界规范

## 目的

将 Windows 伴侣拆成多个可独立测试的 API，使配置、会话状态、单实例和诊断问题可以在不启动 Tk 或托盘的情况下单独调试。

| API | 模块 | 职责 | 测试边界 |
|---|---|---|---|
| 配置 API | `scripts/api/config_api.py` | 校验、规范化、读取和原子保存设置。 | 临时 JSON 文件，不启动 Tk。 |
| 活动状态 API | `scripts/api/activity_api.py` | 读取 Codex JSONL 会话并计算活动/完成状态，对未变化文件使用缓存。 | 合成 JSONL 目录，可注入时间和缓存。 |
| 运行时 API | `scripts/api/runtime_api.py` | 管理 Windows 命名单实例互斥体。 | Windows 互斥体申请和释放。 |
| 诊断 API | `scripts/api/diagnostics_api.py` | 在 `pythonw.exe` 隐藏控制台时记录未捕获异常。 | 临时日志和合成异常。 |
| 显示 API | `scripts/api/display_api.py` | 查询虚拟桌面范围/DPI，并在不限制合法多屏坐标的前提下测试位置相交。 | 模拟 96/144/192 DPI 和虚拟桌面范围。 |
| 输入校验 API | `scripts/api/config_api.py` | 校验带符号坐标、有限窗口尺寸、缩放模式和 1–10 秒刷新间隔。 | 类型化和损坏 JSON 固件；Tk 按键校验回调。 |
| 弹出菜单几何 API | `scripts/api/display_api.py` | 选择显示器工作区并将弹出菜单完整放入其中。 | 四个角、副屏幕、负坐标和任务栏工作区。 |
| 额度格式化 API | `scripts/api/quota_format_api.py` | 选择未来最近的额度到期时间，并格式化本地 `HH:MM M/D` 文本。 | 非法/过去的到期值、缺失日期和不补前导零。 |
| 额度状态 API | `scripts/api/quota_status_api.py` | 将有效额度窗口分类为健康、警告、危险或不可用。 | 百分比边界和损坏窗口。 |
| 显示模式 API | `scripts/api/display_mode_api.py` | 决定是否启用空闲收缩并计算收缩尺寸。 | 启用、活动、悬停和非法尺寸场景。 |
| 窗口尺寸 API | `scripts/api/window_size_api.py` | 在边界内计算自由或等比例的宽高变化。 | 自由、等比例、边界和非法因子场景。 |
| 额度数据源 API | `scripts/api/quota_provider_api.py` | 规范化已获取的本地 app-server 数据，不读取认证信息，也不发起网络请求。 | 有效、损坏和带凭据字段的响应测试。 |
| 托盘生命周期 API | `scripts/api/tray_lifecycle_api.py` | 校验托盘动作，并保证只请求一次恢复重建。 | 动作白名单、可见性策略、重复故障和关闭场景。 |
| 刷新调度 API | `scripts/api/refresh_scheduler_api.py` | 使用已校验的间隔，并保证同时只有一个刷新工作线程。 | 重复刷新调用和间隔限制测试。 |
| Codex 通信 API | `AppServer` | 启动本机 app-server、执行 JSON-RPC 并报告协议错误。 | 模拟子进程和响应矩阵。 |
| UI/托盘适配层 | `Pet` 与 `TrayIcon3` | 将 API 结果转换为 Tk 和托盘动作。 | Windows 界面和人工交互测试。 |

## 不变量

- 配置 API 遇到错误 JSON 不得崩溃，应返回默认值和警告。
- 配置 API 必须兼容常见 Windows 编辑器生成的 UTF-8 和 UTF-8-BOM JSON。
- 配置写入必须使用同目录临时文件和原子替换。
- 活动状态 API 使用最新会话事件作为超时依据，而不是只使用任务开始时间。
- 运行时 API 不得为了取得互斥体而杀死无关进程。
- Tk 线程不得执行阻塞的 app-server 或文件系统工作。
- 主界面只显示活动对话数量，不显示计划步骤文本。
- 弹出菜单矩形必须完全位于所选显示器工作区内。
- 坐标允许为负数；窗口尺寸限制为宽 180–1200、高 80–800；刷新间隔限制为 1–10 秒。
- 额度日期使用本地时区和不补前导零的 `M/D`；数据源缺失时不得臆造。
- 默认额度数据源只接受本地 app-server 结果；不得读取认证文件、发送令牌或持久化凭据。
- 重大行为或性能变化必须同时更新更新日志、规范和回归测试。

## 测试命令

```powershell
$py = "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
& $py -m unittest discover -s .\tests -v
$api = Get-ChildItem .\scripts\api -Filter *.py | ForEach-Object FullName
& $py -m py_compile .\scripts\codex_status_pet.py $api
# 伴侣可见时运行 Windows 显示器探测
& $py .\scripts\probe_display.py
& $py .\scripts\check_doc_parity.py
# 可重复的自动化发布门禁（不能替代实体测试）
& $py .\scripts\run_release_checks.py
```

连接不同 Windows 缩放比例的显示器后必须重新运行现场探测并保存 JSON 输出；不能用模拟值推断混合 DPI 结论。

## Windows 显示器现场证据

伴侣可见时运行 `python .\scripts\probe_display.py`，并将输出保存到测试记录中。

## 变更分类

- **重大行为：** 菜单、可见性、托盘、单实例、设置语义或状态显示变化；必须有专项回归测试和 Windows 手工检查。
- **性能变化：** 会话扫描耗时、刷新间隔、线程数量或磁盘写入频率变化；必须有基准/边界测试并记录到更新日志。
- **文档变化：** 仍需检查中英文规范是否一致。

## Git 变更门禁

较大变更必须通过自动发布检查和 `git diff --check`，同步更新中英文文档，使用有明确范围的提交，并推送到已核验的仓库所有者。必须通过 `.githooks` 保持本地 pre-push 保护启用。

现场显示器证据：伴侣可见时运行 `python .\scripts\probe_display.py`，保存 JSON 输出；连接不同 Windows 缩放比例的显示器后必须重新运行，不能用模拟值代替混合 DPI 结论。
