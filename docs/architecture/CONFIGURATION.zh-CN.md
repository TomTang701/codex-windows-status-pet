# 配置

## 位置和schema

设置保存在 `%USERPROFILE%\.codex\codex-windows-status-pet.json`。当前文件早于带schema版本的迁移机制；在引入破坏性配置变更前，必须先补充schema版本。

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

`x`和`y`是虚拟桌面坐标，可以为负数或超过主显示器。宽度、高度、透明度、字体大小、颜色、布尔值、缩放模式和刷新间隔在使用前必须通过输入校验API规范化。

## 设置事务

设置界面区分持久化、当前运行、草稿和打开时快照：

- **Apply：** 预览有效草稿，不持久化，也不关闭窗口。
- **Save：** 应用并持久化有效草稿。
- **Restore Defaults：** 先替换草稿。
- **Close：** 对未保存的变更恢复打开时快照。
- 保存失败时保留上一个有效设置文件。

打开或关闭设置后，主悬浮窗必须恢复可见。隐藏只将透明度设为0，不覆盖已保存位置。

## 校验和恢复

可编辑值必须经过候选值、提交和加载三层校验。损坏配置按字段回退。坐标必须保留合法副屏和负坐标；屏幕外窗口恢复到可见工作区。
