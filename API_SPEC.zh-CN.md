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
| 输入校验 API | `scripts/api/input_validation_api.py` | 校验设置字段中的带符号/无符号整数候选值和提交值。 | 空值、负号中间态、非法粘贴、损坏和范围限制整数固件。 |
| 设置会话 API | `scripts/api/settings_session_api.py` | 在应用、保存、关闭和恢复默认值之间区分已保存、运行时、草稿和打开时快照。 | 不启动 Tk 的应用/保存/关闭事务测试。 |
| 弹出菜单几何 API | `scripts/api/display_api.py` | 选择显示器工作区并将弹出菜单完整放入其中。 | 四个角、副屏幕、负坐标和任务栏工作区。 |
| 额度格式化 API | `scripts/api/quota_format_api.py` | 选择未来最近的额度到期时间，并格式化本地 `HH:MM M/D` 文本。 | 非法/过去的到期值、缺失日期和不补前导零。 |
| 额度状态 API | `scripts/api/quota_status_api.py` | 将有效额度窗口分类为健康、警告、危险或不可用。 | 百分比边界和损坏窗口。 |
| 显示模式 API | `scripts/api/display_mode_api.py` | 决定是否启用空闲收缩并计算收缩尺寸。 | 启用、活动、悬停和非法尺寸场景。 |
| 收缩状态 API | `scripts/api/compact_state_api.py` | 延迟空闲收缩，在活动/悬停时展开，并保持边缘锚点。 | 空闲延迟、活动、悬停、阻塞和边缘几何测试。 |
| 窗口恢复 API | `scripts/api/window_recovery_api.py` | 保留合法显示器坐标，并将离屏窗口恢复到最近工作区。 | 负坐标/副屏坐标、断开显示器和边界限制测试。 |
| 窗口尺寸 API | `scripts/api/window_size_api.py` | 在边界内计算自由或等比例的宽高变化。 | 自由、等比例、边界和非法因子场景。 |
| 缩放会话 API | `scripts/api/resize_session_api.py` | 基于打开时尺寸应用可逆的百分比缩放。 | 加减精确对称和边界尺寸测试。 |
| 额度数据源 API | `scripts/api/quota_provider_api.py` | 规范化已获取的本地 app-server 数据，不读取认证信息，也不发起网络请求。 | 有效、损坏和带凭据字段的响应测试。 |
| 额度解析 API | `scripts/api/quota_parse_api.py` | 只规范化批准的额度字段及明确的 camelCase/snake_case 别名。 | 未知字段、非法数字、别名和缺失字段测试。 |
| 额度状态 API | `scripts/api/quota_state_api.py` | 保留最近成功数据，并分类 loading、ok、stale 和明确错误。 | 成功恢复、短暂失败、过期超时和无数据失败测试。 |
| 领域模型 API | `scripts/api/models_api.py` | 定义类型化的额度窗口、重置额度和额度快照值。 | 数据类构造和类型边界测试。 |
| 托盘生命周期 API | `scripts/api/tray_lifecycle_api.py` | 校验托盘动作，并保证只请求一次恢复重建。 | 动作白名单、可见性策略、重复故障和关闭场景。 |
| 刷新调度 API | `scripts/api/refresh_scheduler_api.py` | 使用已校验的间隔，并保证同时只有一个刷新工作线程。 | 重复刷新调用和间隔限制测试。 |
| 刷新控制器 API | `scripts/api/refresh_controller_api.py` | 使用 generation、取消和关闭保护，让 Activity 与 Quota 通道彼此独立。 | 独立 single-flight 通道、过期 generation 和关闭回调测试。 |
| Codex 通信 API | `AppServer` | 启动本机 app-server、执行 JSON-RPC 并报告协议错误。 | 模拟子进程和响应矩阵。 |
| UI/托盘适配层 | `Pet` 与 `TrayIcon3` | 将 API 结果转换为 Tk 和托盘动作。 | Windows 界面和人工交互测试。 |
| 右键菜单 UI | `scripts/ui/context_menu.py` | 管理首次点击安全的弹出菜单构造、定位、命令分发和关闭。 | 现有首次点击/设置弹窗集成测试和实体角落检查。 |
| 设置窗口 UI | `scripts/ui/settings_dialog.py` | 管理设置控件、校验绑定、事务动作和可到达窗口定位。 | 设置会话测试和 Windows 副屏交互检查。 |
| 托盘 UI | `scripts/ui/tray_adapter.py` | 管理图标构造、pystray 回调、托盘线程和停止处理；动作通过队列返回。 | 托盘故障、动作白名单、重复启动和实体显示/隐藏检查。 |
| Codex 通信 API | `scripts/api/codex_transport_api.py` | 发现本机 Codex CLI 并执行 app-server stdio JSON-RPC，不承担 UI 职责。 | 配置路径发现、停止进程拒绝和模拟通信边界测试。 |
| 诊断摘要 API | `scripts/api/diagnostic_summary_api.py` | 生成可复制运行诊断，同时排除凭据、提示词、回答、会话内容和原始额度。 | 状态/路径格式化和敏感数据排除测试。 |
| 状态快照 API | `scripts/api/status_snapshot_api.py` | 在不依赖 Tk 的情况下，将批准的活动/额度状态转换为显示文字、颜色和活动数量。 | 真实格式化、stale 颜色和原始字段排除测试。 |

## 不变量

- 配置 API 遇到错误 JSON 不得崩溃，应返回默认值和警告。
- 配置 API 必须兼容常见 Windows 编辑器生成的 UTF-8 和 UTF-8-BOM JSON。
- 配置写入必须使用同目录临时文件和原子替换。
- 活动状态 API 使用最新会话事件作为超时依据，而不是只使用任务开始时间。
- 运行时 API 不得为了取得互斥体而杀死无关进程。
- 设置中的“应用”只改变运行时预览；只有“保存”改变持久化设置。
- 设置“关闭”恢复打开时快照，包括已经应用过预览的情况。
- 坐标输入允许逐键输入临时的 `-`，但提交时拒绝非法带符号整数。
- 缩放按钮对宽高应用相同比例，并且围绕会话基准尺寸可逆。
- Tk 线程不得执行阻塞的 app-server 或文件系统工作。
- 主界面只显示活动对话数量，不显示计划步骤文本。
- 弹出菜单矩形必须完全位于所选显示器工作区内。
- 坐标允许为负数；窗口尺寸限制为宽 180–1200、高 80–800；刷新间隔限制为 1–10 秒。
- 额度日期使用本地时区和不补前导零的 `M/D`；数据源缺失时不得臆造。
- 默认额度数据源只接受本地 app-server 结果；不得读取认证文件、发送令牌或持久化凭据。
- 重大行为或性能变化必须同时更新更新日志、规范和回归测试。
- 右键菜单只能保留一条可到达的弹出路径；无条件 return 后不得保留废弃的原生菜单代码。
- 诊断摘要可以包含路径和运行状态，但不得包含令牌、提示词、回答、会话内容或原始额度响应。

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
& $py .\scripts\package_smoke_test.py
& $py .\scripts\check_release_readiness.py
```

连接不同 Windows 缩放比例的显示器后必须重新运行现场探测并保存 JSON 输出；不能用模拟值推断混合 DPI 结论。

打包 smoke 测试会检查 manifest/应用版本一致性、已核验作者元数据、启动器和文档是否存在，并创建非正式发布 ZIP。GitHub Actions 会在 Windows 上运行这些检查。
`check_release_readiness.py` 默认只报告仍阻止 v0.3.0 发布的实体兼容性行，不会误使日常门禁失败；发布决策时使用 `--strict`。

## Windows 显示器现场证据

伴侣可见时运行 `python .\scripts\probe_display.py`，并将输出保存到测试记录中。

## 变更分类

- **重大行为：** 菜单、可见性、托盘、单实例、设置语义或状态显示变化；必须有专项回归测试和 Windows 手工检查。
- **性能变化：** 会话扫描耗时、刷新间隔、线程数量或磁盘写入频率变化；必须有基准/边界测试并记录到更新日志。
- **文档变化：** 仍需检查中英文规范是否一致。

## Git 变更门禁

较大变更必须通过自动发布检查和 `git diff --check`，同步更新中英文文档，使用有明确范围的提交，并推送到已核验的仓库所有者。必须通过 `.githooks` 保持本地 pre-push 保护启用。

现场显示器证据：伴侣可见时运行 `python .\scripts\probe_display.py`，保存 JSON 输出；连接不同 Windows 缩放比例的显示器后必须重新运行，不能用模拟值代替混合 DPI 结论。
