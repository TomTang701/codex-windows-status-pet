"""Static, Tk-independent text for the supported runtime languages."""

from __future__ import annotations


SUPPORTED_LANGUAGES = ("en", "zh-CN")

_TEXT = {
    "en": {
        "idle": "Idle",
        "activity": "Codex {detail}",
        "quota_unavailable": "Quota unavailable",
        "week": "Week",
        "stale": "(quota stale)",
        "tray_error": "Tray icon error",
        "settings_title": "Codex Status Pet Settings",
        "language": "Language",
        "english": "English",
        "simplified_chinese": "Simplified Chinese",
        "opacity": "Opacity",
        "window_size": "Window size",
        "default_position": "Default position (X, Y)",
        "refresh_interval": "Refresh interval (seconds)",
        "always_on_top": "Always on top",
        "lock_position": "Lock position",
        "battery_content": "Battery display content",
        "five_hour": "5-hour",
        "weekly": "Weekly",
        "show_five_hour": "Show 5-hour quota",
        "show_weekly": "Show weekly quota",
        "show_reset_credit": "Show reset credit",
        "font_color": "Font color...",
        "background_color": "Background color...",
        "save": "Save",
        "apply": "Apply",
        "restore_defaults": "Restore Defaults",
        "close": "Close",
    },
    "zh-CN": {
        "idle": "空闲",
        "activity": "Codex {detail}",
        "quota_unavailable": "额度暂不可用",
        "week": "周",
        "stale": "（额度过期）",
        "tray_error": "托盘图标异常",
        "settings_title": "Codex 宠物设置",
        "language": "语言",
        "english": "English",
        "simplified_chinese": "简体中文",
        "opacity": "透明度",
        "window_size": "窗口大小",
        "default_position": "默认位置 (X, Y)",
        "refresh_interval": "刷新间隔 (秒)",
        "always_on_top": "置顶",
        "lock_position": "锁定位置",
        "battery_content": "电池显示内容",
        "five_hour": "5小时",
        "weekly": "每周",
        "show_five_hour": "显示 5 小时额度",
        "show_weekly": "显示周额度",
        "show_reset_credit": "显示重置次数",
        "font_color": "字体颜色...",
        "background_color": "背景颜色...",
        "save": "保存",
        "apply": "应用",
        "restore_defaults": "恢复默认值",
        "close": "关闭",
    },
}


def normalize_language(value):
    """Return a supported code and an optional normalization warning."""
    if value in SUPPORTED_LANGUAGES:
        return value, None
    if value is None:
        return "en", None
    return "en", "language is invalid; English retained"


def translate(language, key, **format_values):
    """Return one translated user-facing string or fail visibly for a bad key."""
    normalized, _warning = normalize_language(language)
    return _TEXT[normalized][key].format(**format_values)
