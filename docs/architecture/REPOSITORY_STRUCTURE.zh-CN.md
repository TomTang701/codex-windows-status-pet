# 仓库结构

本文档说明项目文件的归属。配置值属于 `CONFIGURATION.md`；运行时API契约属于 `API_SPEC.md`。

## 顶层结构

| 路径 | 用途 |
|---|---|
| `.codex-plugin/plugin.json` | Codex插件清单和缓存破坏版本号。 |
| `scripts/codex_status_pet.py` | Windows悬浮窗、托盘、app-server客户端、活动监视和设置界面。 |
| `scripts/ui/main_window.py` | Tk主窗口生命周期、渲染、恢复、刷新编排和UI组装。 |
| `scripts/api/` | 与UI无关的领域、传输、校验、刷新、额度、几何和诊断API。 |
| `scripts/ui/` | Tk和通知区域适配层。 |
| `start_codex_status_pet.cmd` | 推荐使用 `pythonw.exe` 的双击启动程序。 |
| `skills/codex-windows-status-pet/SKILL.md` | Codex技能说明。 |
| `tests/` | 无界面API和UI适配层回归测试。 |
| `docs/` | 分层项目文档和测试证据。 |
| `.github/workflows/ci.yml` | Windows CI质量门禁和smoke制品流程。 |
| `requirements.txt` | 回退Python环境的运行时依赖下限。 |

## 文件放置规则

- 新的纯逻辑放入 `scripts/api/`，并配套确定性测试。
- Windows或Tk调用放入平台/UI适配层，不得成为领域层依赖。
- 安装和故障排除放入 `docs/operations/`。
- 治理规范放入 `docs/governance/`。
- 架构和配置契约放入 `docs/architecture/`。
- 兼容性结果放入 `docs/quality/`；一次性审计放入 `docs/archive/audits/`。
- 生成的smoke包、probe输出、日志和本地设置不得提交。

## 运行时归属不变量

- 同时只允许一个伴侣实例；第二次启动不杀死已有进程而直接退出。
- 后台worker不得直接调用Tk API；UI调度必须在Tk主线程。
- 菜单命令第一次点击执行一次，执行后关闭右键菜单。
- 自动发布门禁通过后应提交重大变更，并由本地Git配置和pre-push钩子核验远程所有者及作者身份。
