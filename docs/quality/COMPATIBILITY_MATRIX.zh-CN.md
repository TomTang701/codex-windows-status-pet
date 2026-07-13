# Windows 兼容性矩阵

English: [English version](COMPATIBILITY_MATRIX.md)

## v0.8.0 调整后的发布证据

Windows Sandbox、独立干净 Windows 11 VM 和跨 Windows 用户桌面自动化在当前环境不可用，已获批准作为**非阻塞环境限制**；它们不是已通过的证据，也不会为 v0.8.0 新增 VM 或跨用户自动化基础设施。真实打包 EXE 生命周期仍以当前 Windows 主机为客户端证据；GitHub Windows runner 的安装生命周期结果属于干净 runner 自动化证据，除非独立验证运行器操作系统，否则不声明为实体 Windows 11 客户端证据。正式 README 证据为英文和简体中文各三张真实打包 EXE 截图：主悬浮窗、右键菜单和设置窗口。

## v0.9.0 分发与生命周期证据

| 范围 | 覆盖内容 | 状态 | 证据/下一步 |
|---|---|---|---|
| v0.9.0 ZIP 直接使用 | 解压完整 onedir ZIP，并在没有源运行时的情况下运行 `CodexStatusPet.exe` | 自动化 Windows 主机通过 | 隔离的打包运行时 smoke 在移除 `PYTHONPATH` 后通过，且没有创建安装状态或开始菜单快捷方式。 |
| v0.9.0 已认证部署 | 历史私有 GitHub Release 解析、ZIP/SHA 获取和 installer 委托 | 历史通过 | 已由 v0.9.1 公开 REST bootstrap 修正替代；v0.9.0 历史保持不变。 |
| v0.9.0 已安装生命周期 | 从 v0.8.0 升级、修复安装、回滚、普通卸载和彻底卸载 | 实体 Windows 主机及 GitHub Windows CI 通过 | 聚焦生命周期 smoke 保留 settings 字节和无关 `.codex` 数据，清理测试残留，并在本地和 PR #40 exact-head CI 通过。 |
| v0.9.0 发布 | 合并后 main RC、带注释标签、Release ZIP 和 SHA-256 sidecar | 通过 | RC 在 `bdae1942856ffa00677e64c63142457d0f79efce` 通过；标签与公开 GitHub Release 指向同一提交。 |

## v0.9.1 公开分发修正

v0.9.1 使用公开 REST Release 元数据和精确 `browser_download_url` 资产，替代需要认证的 `gh` 获取路径。
完成打包、发布，并从公开 latest 与固定版本 bootstrap 路径验证后，发布门已通过。

| 区域 | 覆盖范围 | 状态 | 证据 / 下一步 |
|---|---|---|---|
| v0.9.1 公开分发 | 公开 latest/固定版本 bootstrap、精确产品 ZIP/SHA/install 资产和现有安装器委托 | 通过 | PR #43 exact-head Windows CI 通过；合并 main `821d58a`；tag/Release `v0.9.1`；公开 latest 安装生命周期通过；产品 ZIP SHA-256 为 `706f24bab7bc3054dd2bd410ab3ff60144972a20690796e0036568f8211ec338`。 |

**状态：** 持续维护的测试记录  
**规则：** 模拟测试或无界面测试不能替代实体 Windows 测试结果。

| 范围 | 覆盖内容 | 状态 | 证据/下一步 |
|---|---|---|---|
| Windows 版本 | Windows 10 | 延后 / 不声明支持 / 非阻塞 | 不在当前 Windows 11 x64 支持声明内；未来证据可以扩展支持范围，但不阻塞当前发布。 |
| Windows 版本 | Windows 11 Home 10.0.26200（构建 26200） | 实体通过 | 2026-07-10 通过 `Win32_OperatingSystem` 探测主机；启动器和悬浮窗已手动启动。 |
| 显示器 | 单显示器 | 实体通过 | 2026-07-10 维护者授权并确认单显示器实体运行通过。`DisplaySwitch.exe /internal` 报告一块 `2048x1152` 显示器，工作区为 `(0,0)-(2048,1104)`；根启动器稳定为一个项目进程；测试后已恢复扩展双显示器模式。 |
| 显示器 | 双显示器 | 实体通过 | [2026-07-10拓扑记录](test-records/2026-07-10-win11-dual-monitor.md)；已完成 `DISPLAY1`/`DISPLAY2` 探测；虚拟桌面为 `0,0-4480,1434`，工作区为 `0,0-2048,1104` 和 `2560,354-4480,1386`；副屏坐标 `(4150,1248)` 仍受支持。 |
| 坐标 | 虚拟桌面负坐标 | 自动化 | `Display API` 相交和定位测试覆盖负坐标。 |
| 坐标 | 大副屏坐标 `(4151,1248)` | 实体通过 | 已在副屏观察到悬浮窗和右键菜单。 |
| 菜单 | 底部任务栏和显示器工作区 | 实体通过 | 2026-07-10 实体探测显示主任务栏位于底部（`0,1380-2560,1440`）；悬浮窗和菜单保持在探测到的双显示器工作区内。 |
| 菜单 | 顶部、左侧和右侧任务栏边缘 | 延后 / 不声明支持 / 非阻塞 | 这些任务栏位置不属于 v0.4.0 的实体支持声明；几何 API 测试仅作为回归证据。 |
| 菜单 | 第一次点击 | 实体通过 | 副屏测试中第一次点击设置即可打开设置窗口。 |
| 设置 | 规范缩放和降级几何 | 自动化 | `Window Scale API` 和配置测试覆盖 80–200% 等比例指标、非法值、旧版推断、边界和 schema-1 降级字段。 |
| 设置 | 只允许数字和间隔 1–10 | 自动化 | 输入校验、配置和调度测试覆盖逐键/粘贴候选、非法值和边界。 |
| 设置 | Windows 编辑器生成的 UTF-8 BOM JSON | 自动化通过 | 配置 API 接受 UTF-8 和 UTF-8-BOM 测试文件，不会丢失坐标。 |
| 生命周期 | 隐藏后进程继续运行 | 实体通过 | 隐藏动作移除悬浮窗，同时 `pythonw.exe` 仍然运行。 |
| 生命周期 | 隐藏后托盘显示 | 实体通过 | 使用 Windows 键盘通知区域路径（`Win+B` → Apps）打开托盘菜单；执行隐藏再显示后，悬浮窗恢复到副屏坐标 `(4150,1248)`。 |
| DPI | 100% / 125% / 150% / 200% | 已批准限制 / 非阻塞 | 实体主机的两块显示器均为 96 DPI，模拟 96/120/144/192 DPI 路径通过。本环境无法进行混合 DPI 实体认证，v0.4.0 不声明已完成该认证。 |
| 收缩模式 | 空闲收缩和悬停展开 | 实体通过 | 2026-07-10 维护者确认运行中的应用可真实空闲收缩并在鼠标悬停时展开；纯模式 API 回归测试也通过。 |
| 窗口缩放 | 80% / 100% / 150% / 200% 统一几何和字体 | Windows 主机运行通过 | [2026-07-10 v0.4.0缩放记录](test-records/2026-07-10-v0.4.0-window-scale-validation.md)；四档真实 Tk 几何/字体/换行/间距、五行、重置额度日期、菜单、拖动/锁定、隐藏/恢复、收缩/展开和临时文件重启持久化均通过。 |
| v0.4.1 内容与错误 | 全部 25 个缩放档位；托盘/额度失败路径 | 通过 | [2026-07-11 v0.4.1正确性记录](test-records/2026-07-11-v0.4.1-correctness-validation.md)保留已失效的 96-DPI 结果，重现生产 120-DPI 失败，并记录替代生产顺序探针通过全部 25 档。错误路径集成保持绿色。 |
| v0.4.2 发布验证 | Quality、RC、兼容性、CI 和宿主事实分类 | 通过 | [2026-07-11 v0.4.2验证记录](test-records/2026-07-11-v0.4.2-autonomous-verification.md)；23 项事实均指定唯一权威检查，重复 CI/本地门禁已合并，UTF-8 安全输出受回归保护，162 项测试和正式 RC 通过且零阻塞。 |
| v0.5.0 精简核心 | 过时兼容边界和额度解析路径 | 通过 | [2026-07-11 v0.5.0精简核心记录](test-records/2026-07-11-v0.5.0-lean-core.md)；删除四个生产模块，额度隐私/损坏行为转移到解析器权威契约，159 项行为/发布测试和正式 RC 通过且零阻塞。 |
| v0.5.1 运行时几何 | 长生命周期设置/生命周期转换；DPI 96/120 下 80-200% | Windows 主机自动化通过 | [2026-07-11 v0.5.1 调查记录](test-records/2026-07-11-v0.5.1-runtime-geometry-investigation.md)；v0.5.0 的冷启动适配/运行时裁切转换已固化为 RED，统一的已定位 HWND DPI 权威使 50 个 DPI/缩放组合和 15 类生命周期转换中的五行内容全部适配。 |
| v0.5.3 Shell 身份 | 桌面/托盘可见且没有普通应用窗口身份 | Windows 主机自动化通过 | [2026-07-11 v0.5.3 调查记录](test-records/2026-07-11-v0.5.3-shell-identity-investigation.md)；真实 root HWND RED/GREEN 证明 `WS_EX_TOOLWINDOW=true`、`WS_EX_APPWINDOW=false`、owner 为 `0`，并在生命周期中保持。启动器仍只有一个进程，Windows 应用清单不会将覆盖层枚举为普通应用窗口。 |
| v0.5.5 混合 DPI 启动恢复 | 125% 主屏 / 100% 副屏下合法边缘位置的重启保留 | Windows 主机自动化通过 | [2026-07-12 v0.5.5 调查记录](test-records/2026-07-12-v0.5.5-mixed-dpi-startup-position-investigation.md)；生产等价 RED 将第一处错误夹紧追踪到 bootstrap 120-DPI 恢复尺寸，GREEN 保留副屏右边缘、下边缘、右下角和内部坐标，同时保留无效位置恢复。 |
| v0.6.0 电池与布局 | 五行文字加 2×5 / 十格电池；compact 完整电池；80–200% 与 DPI 96/120 内容适配 | Windows 主机自动化通过 | v0.6.0 PR #25 的展示语义与 BatteryView RED/GREEN、全部 25 个缩放档、DPI 探针、生命周期回归、正式 RC 和 exact-head Windows CI 均通过。电池与 `primary_5h` 文字消费同一权威的剩余额度展示结果。 |
| 依赖 | 捆绑运行时和回退依赖 | 已批准限制 / 非阻塞 | 全新 Python 3.12 venv 仅安装 `requirements.txt`，通过 127 项测试、Quality、打包 smoke 和重复启动 smoke；Windows CI 也通过。当前没有独立干净 Windows 机器，因此不声明已完成该实体测试。 |
| 自动化 Quality | 文档一致性、编译和单元测试 | 通过 | `scripts/run_quality_checks.py` 已通过；Quality 明确不做发布就绪决定。 |
| 启动器 | 根目录 `start_codex_status_pet.cmd`，重复启动 | 实体通过 | 2026-07-10 连续启动两次只产生一个实际 `pythonw.exe` 悬浮窗进程，没有常驻 CMD 窗口；进程计数已排除命令行自匹配。 |
| 启动项清理 | 旧 `Codex Status Pet.lnk` | 实体通过 | 2026-07-10 检查启动文件夹和快捷方式目标；已删除指向旧 `.agents\plugins\plugins\codex-windows-status-pet` 副本的快捷方式；`startup_audit.py` 当前报告 `clean: true`，没有本项目启动项。 |
| v0.8.0 打包 | PyInstaller onedir EXE、清单、声明、SHA-256 和排除清单 | 自动通过 | `python scripts/build_release.py` 和 `python scripts/package_smoke_test.py` 已生成并验证版本化 EXE ZIP。 |
| v0.8.0 打包生命周期 | GUI EXE 首次启动、重复实例保持和正常关闭 | 自动化 Windows 主机通过 | `python scripts/packaged_runtime_smoke.py` 已针对真实版本化 EXE ZIP 通过；没有源代码进程替代该 artifact。 |
| v0.8.0 已安装生命周期 | 全新安装、开始菜单条目、测试创建的重装、普通卸载保留设置和清除安全性 | 实体 Windows 主机通过 | 2026-07-12 真实 artifact 在独立 PowerShell supervisor 下完成，子进程 `ExitCode = 0`，smoke 结构化结果为 `passed: true`；最终检查没有已安装 EXE、mutex、安装根或快捷方式，且原 settings 的 SHA-256 未变化。未来 GitHub runner 的结果属于干净生命周期自动化；除非独立验证其操作系统，否则不是实体 Windows 11 客户端证据。 |
| v0.8.0 干净 VM/Sandbox/跨用户 | 独立干净 Windows 11 VM、Sandbox 或跨用户桌面自动化 | 已批准限制 / 非阻塞 | 这些环境在当前执行上下文中不可用，未通过也不作声明；不会仅为 v0.8.0 新增 VM 或跨用户自动化基础设施。 |
| v0.8.0 README 证据 | 三张打包英文和三张打包简体中文产品视图 | 实体 Windows 主机通过 | 维护者提供的真实打包 EXE 截图展示了两种语言下已规范化的展开主悬浮窗、主悬浮窗右键菜单和设置窗口；`python scripts/check_readme_screenshots.py` 验证准确六个文件及 README 语言映射。 |

## 发布门槛

Windows 11 x64 是受支持平台。在每个具有阻塞性的“待验证”或“部分完成”项目获得实体 Windows 结果，或由维护者明确批准并记录环境限制之前，不得标记产品已达到发布就绪状态。明确标记为“非阻塞”的项目仍会报告，但不进入可执行阻塞项集合。
