# 架构

English: [English version](ARCHITECTURE.md)

## 分层

```text
Windows/Tk适配层 -> 应用控制层 -> 领域服务/状态 -> 纯模型/策略
```

领域和纯API不得导入Tkinter或pystray。UI适配层只渲染已校验状态并绑定动作；传输适配层返回规范化值，不得修改UI。后台worker通过队列或主线程调度回调与Tk通信。

状态展示以五个命名行跨越纯逻辑/UI 边界。纯快照拥有顺序和兼容文字；Tk 适配层拥有五个持久 Label，并在原位更新。

应用、状态展示、设置持久化和窗口生命周期控制器拥有协调状态，但不拥有控件。`Pet` 负责组合它们，并把决定转换为 Tk 动作。

## 运行时边界

- Activity和Quota刷新通道彼此独立，具备single-flight、generation安全、可取消和shutdown感知能力。
- Tk调用保留在Tk主线程；传输和文件系统工作离开该线程。
- 创建UI前先获取命名mutex。第二次启动不得杀死其他进程而应退出。
- Shutdown必须幂等，并阻止callback安排新任务。
- 本地app-server是额度传输边界；不得访问token或 `auth.json`。

详细公开契约见 [`API_SPEC.md`](API_SPEC.zh-CN.md)；配置事务见 [`CONFIGURATION.md`](CONFIGURATION.zh-CN.md)。
