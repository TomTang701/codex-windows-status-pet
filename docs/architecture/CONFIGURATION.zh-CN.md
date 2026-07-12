# 配置

English: [English version](CONFIGURATION.md)

## 位置和schema

设置保存在 `%USERPROFILE%\.codex\codex-windows-status-pet.json`，当前使用schema版本 `1`。没有 `schema_version` 的旧文件按版本化前格式读取并在内存中规范化；保存时会写入当前schema。

上一个有效文件保存在 `%USERPROFILE%\.codex\codex-windows-status-pet.json.bak`。配置 API 可以先校验该副本，再原子恢复；缺失或损坏的备份会被忽略。右键菜单不提供恢复入口。

未来 schema、不可读、损坏、非对象以及字段无效的源文件在常规运行期间为只读。拖动、隐藏、切换、窗口恢复、退出和普通“保存”都不能覆盖它们。若要有意替换受保护源，请在设置窗口先选择 **恢复默认值**，再选择 **保存**。

```json
{
  "schema_version": 1,
  "alpha": 0.35,
  "font_color": "#e5e7eb",
  "font_size": 10,
  "background_color": "#000000",
  "topmost": true,
  "locked": true,
  "x": 4151,
  "y": 1248,
  "window_scale_percent": 100,
  "window_width": 330,
  "window_height": 138,
  "scale_mode": "proportional",
  "refresh_interval_seconds": 5,
  "language": "en",
  "compact": false
}
```

`language` 只接受 `en` 和 `zh-CN`，默认值为英文。`compact` 是唯一可持久化的 Compact 状态来源。旧的 `compact_when_idle` 输入会被忽略，因此不能再自动进入 Compact。设置语言选择器在 Apply 时预览，在 Close 时回滚，在 Save 时持久化。

`window_scale_percent` 是展开状态尺寸的规范来源。它会限制在 80–200%，按 5% 步长量化，默认值为 100%。窗口宽高、文字字体、爪印字体、换行长度和必要间距都由同一个纯 Window Scale API 结果推导。

为了保持 schema 1 的降级兼容性，“保存”还会写入派生的 `font_size`、`window_width`、`window_height` 和 `scale_mode: "proportional"`。v0.3.2 会忽略未知的规范字段，并读取这些可用的派生值。

没有 `window_scale_percent` 的有效旧文件会在内存中使用几何平均面积推断迁移：`sqrt((old_width * old_height) / (330 * 138))`，然后限制范围并量化。旧字体大小和缩放模式不再是独立来源。迁移保留位置、透明度、颜色、刷新间隔、置顶、锁定和 Compact 偏好；用户保存前不会写入磁盘。

`x` 和 `y` 是虚拟桌面坐标，可以为负数或超过主显示器。坐标、透明度、颜色、布尔值、刷新间隔、规范缩放和旧迁移输入在使用前都会规范化。

## 设置事务

设置界面区分持久化、当前运行、草稿和打开时快照：

- **Apply：** 预览有效草稿，不持久化，也不关闭窗口。
- **Save：** 应用并持久化有效草稿。
- **Restore Defaults：** 替换草稿，并明确授权下一次“保存”替换受保护源。
- **Close：** 对未保存的变更恢复打开时快照。
- 保存失败时保留上一个有效设置文件。

打开或关闭设置后，主悬浮窗必须恢复可见。隐藏只将透明度设为0，不覆盖已保存位置。

设置窗口只提供一个“窗口大小”滑块。移动滑块只改变草稿；“应用”推导并预览完整指标，“保存”持久化规范字段和兼容字段，“关闭”恢复打开时的缩放，“恢复默认值”将缩放重置为 100%。

## 校验和恢复

可编辑值必须经过候选值、提交和加载三层校验。损坏配置按字段回退。坐标必须保留合法副屏和负坐标；屏幕外窗口恢复到可见工作区。
