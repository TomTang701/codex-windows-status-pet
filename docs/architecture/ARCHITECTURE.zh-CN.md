---
document_id: ARCHITECTURE
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/architecture/ARCHITECTURE.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 90
---
# 架构

## 分层

```text
Windows/Tk适配层 -> 应用控制层 -> 领域服务/状态 -> 纯模型/策略
```

领域和纯API不得导入Tkinter或pystray。UI适配层只渲染已校验状态并绑定动作；传输适配层返回规范化值，不得修改UI。后台worker通过队列或主线程调度回调与Tk通信。

## 运行时边界

- Activity和Quota刷新通道彼此独立，具备single-flight、generation安全、可取消和shutdown感知能力。
- Tk调用保留在Tk主线程；传输和文件系统工作离开该线程。
- 创建UI前先获取命名mutex。第二次启动不得杀死其他进程而应退出。
- Shutdown必须幂等，并阻止callback安排新任务。
- 本地app-server是额度传输边界；不得访问token或 `auth.json`。

详细公开契约见 [`API_SPEC.md`](API_SPEC.md)；配置事务见 [`CONFIGURATION.md`](CONFIGURATION.md)。

## 组件和依赖方向

```text
启动器 -> 运行时保护 -> Tk主窗口
Tk主窗口 -> UI适配器 -> 纯API策略
后台Activity worker -> queue -> Tk轮询/渲染
后台Quota worker -> 本地app-server -> 规范化快照 -> queue -> Tk轮询/渲染
托盘线程 -> 动作queue -> Tk动作分发
```

依赖向内：UI和transport适配器可以调用API策略，但纯API模块不得导入Tk、pystray或具体窗口对象。Queue payload只包含channel、generation、批准的活动/额度结果或脱敏错误；原始provider对象不得进入展示层。

展开悬浮窗渲染五个稳定Label（`activity`、`progress`、`primary_5h`、`weekly`和`reset_credit`）。Compact模式可以隐藏整组，但展开会恢复每一行，不重建或截断展示文本。

## 启动和关闭顺序

启动依次配置日志和DPI awareness、申请命名mutex、加载并分类设置、创建Tk状态、启动托盘适配器，然后调度独立Activity和Quota刷新。Quota只能从后台worker启动本地app-server。

关闭先标记closing、取消刷新generation、阻止新callback、按可写状态保存设置、幂等停止托盘和app-server、销毁Tk并释放mutex。重复关闭请求无害。

## 状态生命周期和恢复

设置在持久化、打开快照、草稿和运行时状态间转换。未来或损坏配置保持只读，直到明确重置。Activity和Quota保持独立generation及失败状态；Quota通信失败可使用近期last-good快照，但必须明确显示stale。显示拓扑定期重评估，只移动真正不可达的窗口。托盘故障最多调度一次重启；app-server故障只影响Quota，不停止Activity。

## 决策记录

当前架构决策记录在 [`adr/`](adr/)，包括本地provider、Tkinter、仅本地安全边界、独立刷新channel和带schema版本的设置。
