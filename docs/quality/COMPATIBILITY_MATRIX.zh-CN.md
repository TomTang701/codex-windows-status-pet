# Windows 兼容性矩阵

**状态：** 持续维护的测试记录  
**规则：** 模拟测试或无界面测试不能替代实体 Windows 测试结果。

| ID | 范围 | 覆盖内容 | 状态 | 证据/下一步 | 阻塞 |
|---|---|---|---|---|---|
| WIN-10 | Windows版本 | Windows 10 | Pending | 在Windows 10机器运行启动器和完整UI smoke。 | Yes |
| WIN-11 | Windows版本 | Windows 11 Home 10.0.26200（build 26200） | Physical pass | 2026-07-10通过 `Win32_OperatingSystem` 探测；已手动启动悬浮窗。 | No |
| DISPLAY-1 | 显示器 | 单显示器 | Partial | 几何API测试通过；仍需带日期的单屏实体记录。 | Yes |
| DISPLAY-2 | 显示器 | 双显示器 | Physical pass | [2026-07-10拓扑记录](test-records/2026-07-10-win11-dual-monitor.md)；副屏坐标 `(4150,1248)` 受支持。 | No |
| COORD-NEGATIVE | 坐标 | 虚拟桌面负坐标 | Automated pass | `Display API` 相交和定位测试覆盖负坐标。 | No |
| COORD-LARGE | 坐标 | 大副屏坐标 `(4151,1248)` | Physical pass | 已在副屏观察到悬浮窗和右键菜单。 | No |
| TASKBAR-EDGES | 菜单 | 四角和任务栏工作区 | Partial | 底部任务栏已实测且几何测试通过；顶部/左侧/右侧仍待完成。 | Yes |
| POPUP-FIRST-CLICK | 菜单 | 第一次点击 | Physical pass | 副屏测试第一次点击即可打开设置。 | No |
| SETTINGS-RESIZE | 设置 | 宽高及等比例缩放 | Automated pass | `Window Size API` 覆盖自由、等比例、边界和非法因子。 | No |
| INPUT-PASTE | 设置 | 只允许数字和间隔1–10 | Partial | 自动非法/边界fixture通过；手动非法粘贴证据仍待完成。 | Yes |
| CONFIG-BOM | 设置 | Windows编辑器UTF-8 BOM JSON | Automated pass | 配置API接受UTF-8和UTF-8-BOM fixture，不丢失坐标。 | No |
| QUOTA-DISPLAY | 额度显示 | 主要、周额度和Reset Credit到期契约 | Partial | 自动格式/parser/快照测试通过；展开模式实体可见性仍待完成。 | Yes |
| LIFECYCLE-HIDE | 生命周期 | 隐藏后进程继续运行 | Physical pass | 隐藏悬浮窗后 `pythonw.exe` 仍运行。 | No |
| TRAY-RESTORE | 生命周期 | 隐藏后托盘显示 | Physical pass | 隐藏再显示后恢复到副屏坐标 `(4150,1248)`。 | No |
| DPI-MIXED | DPI | 100% / 125% / 150% / 200% | Partial | 模拟DPI路径通过；实体混合DPI仍待完成。 | Yes |
| COMPACT-HOVER | 收缩模式 | 空闲收缩和悬停展开 | Partial | 纯状态测试通过；实体空闲收缩/悬停展开仍待完成。 | Yes |
| CLEAN-MACHINE | 依赖 | 捆绑运行时和回退依赖 | Partial | 临时venv和Windows CI通过；独立干净Windows启动仍待完成。 | Yes |
| QUALITY-GATE | 自动门禁 | 文档、编译、测试和打包 | Automated pass | `scripts/run_quality_checks.py` 通过且明确不批准发布。 | No |
| SINGLE-INSTANCE | 启动器 | 根启动器及重复启动 | Physical pass | 连续启动两次只产生一个悬浮窗进程且无常驻CMD。 | No |
| STARTUP-CLEAN | 启动项清理 | 旧快捷方式 | Physical pass | 启动项审计报告 `clean: true`；不存在当前项目启动项。 | No |

## 发布门槛

在所有“待验证”项目获得实体 Windows 结果，或由维护者明确批准并记录环境限制之前，不得标记产品已达到发布就绪状态。
