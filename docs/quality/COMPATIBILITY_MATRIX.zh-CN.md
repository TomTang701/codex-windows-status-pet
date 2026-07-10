---
document_id: COMPATIBILITY-MATRIX
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/quality/COMPATIBILITY_MATRIX.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 30
---
# Windows 兼容性矩阵

**状态：** 持续维护的测试记录  
**规则：** 模拟测试或无界面测试不能替代实体 Windows 测试结果。

| ID | 范围 | 覆盖内容 | 状态 | 阻塞 | 证据/下一步 |
|---|---|---|---|---|---|
| WIN10-DEFERRED | Windows版本 | Windows 10 | Deferred | No | 不在当前发布范围，不宣称支持。 |
| WIN11-X64 | Windows版本 | Windows 11 Home x64 10.0.26200 | Physical pass | Yes | 2026-07-10主机探测及启动器/悬浮窗通过。 |
| DISPLAY-1 | 显示器 | 单显示器 | Partial | Yes | 几何测试通过；仍需单屏实体记录。 |
| DISPLAY-2 | 显示器 | 双显示器 | Physical pass | Yes | [2026-07-10拓扑记录](test-records/2026-07-10-win11-dual-monitor.md)；支持 `(4150,1248)`。 |
| COORD-NEGATIVE | 坐标 | 虚拟桌面负坐标 | Automated pass | No | Display API测试覆盖负坐标。 |
| COORD-LARGE | 坐标 | 大副屏坐标 `(4151,1248)` | Physical pass | No | 已在副屏观察悬浮窗和菜单。 |
| TASKBAR-BOTTOM | 菜单 | 正常Windows 11底部任务栏 | Physical pass | Yes | 已实体观察底部任务栏和角落定位。 |
| TASKBAR-ALT | 菜单 | 顶部/左侧/右侧几何 | Automated pass | No | 纯几何测试覆盖其他工作区；不要求不受支持的注册表修改。 |
| POPUP-FIRST-CLICK | 菜单 | 第一次点击 | Physical pass | No | 副屏测试第一次点击打开设置。 |
| SETTINGS-RESIZE | 设置 | 宽高及等比例缩放 | Automated pass | No | Window Size API覆盖自由、比例、边界和非法因子。 |
| INPUT-PASTE | 设置 | 数字输入和间隔1–10 | Automated pass | No | 校验fixture拒绝非法粘贴并限制边界。 |
| CONFIG-BOM | 设置 | UTF-8 BOM JSON | Automated pass | No | 配置API接受UTF-8和UTF-8-BOM fixture。 |
| QUOTA-DISPLAY | 额度显示 | 完整Reset Credit到期 | Physical pass | Yes | [2026-07-10状态行记录](test-records/2026-07-10-win11-reset-credit-status-rows.md)显示保存的330x138窗口内完整 `HH:MM M/D`。 |
| LIFECYCLE-HIDE | 生命周期 | 隐藏后继续运行 | Physical pass | No | 隐藏后 `pythonw.exe` 仍运行。 |
| TRAY-RESTORE | 生命周期 | 托盘隐藏后显示 | Physical pass | Yes | 隐藏再显示后恢复到副屏。 |
| DPI-MIXED | DPI | 混合缩放 | Deferred | No | 已有自动几何覆盖；混合DPI实体证据不在v0.3.0声明内。 |
| DISPLAY-RECONNECT | 显示器 | 断开并重连 | Partial | Yes | 在可用双屏主机上实际可行时验证。 |
| WORKAREA-RUNTIME | 任务栏 | 运行时工作区变化 | Automated pass | No | 恢复路径已有覆盖，不要求不受支持的任务栏布局。 |
| COMPACT-HOVER | 收缩模式 | 空闲收缩和悬停展开 | Partial | Yes | 纯状态测试通过；仍需实体记录。 |
| CLEAN-ENV | 依赖 | 全新本地Windows 11 venv | Automated pass | Yes | 2026-07-10新venv安装依赖、运行测试并通过package smoke。 |
| SOAK-8H | 可靠性 | 8小时soak | Deferred | No | 属于未来可靠性证据，不是v0.3.0实体要求。 |
| QUALITY-GATE | 自动门禁 | 文档、编译、测试和打包 | Automated pass | No | 日常Quality通过但不直接批准发布。 |
| SINGLE-INSTANCE | 启动器 | 重复启动 | Physical pass | Yes | 两次启动只产生一个悬浮窗进程且无常驻CMD。 |
| STARTUP-CLEAN | 启动项 | 旧快捷方式审计 | Physical pass | No | 启动项审计报告 `clean: true`。 |

## 发布门槛

在所有“待验证”项目获得实体 Windows 结果，或由维护者明确批准并记录环境限制之前，不得标记产品已达到发布就绪状态。
