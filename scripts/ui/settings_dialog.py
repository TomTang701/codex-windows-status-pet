"""Transactional settings dialog adapter."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser, messagebox

try:
    from api.config_api import DEFAULT_SETTINGS
    from api.display_api import place_popup, work_area_for_point
    from api.input_validation_api import (
        is_signed_integer_candidate,
        is_unsigned_integer_candidate,
        parse_signed_integer,
        parse_unsigned_integer,
    )
    from api.settings_session_api import SettingsSession
    from api.localization_api import translate
    from api.window_scale_api import (
        MAX_WINDOW_SCALE_PERCENT,
        MIN_WINDOW_SCALE_PERCENT,
        WINDOW_SCALE_STEP,
        derive_window_metrics,
    )
except ModuleNotFoundError:
    from scripts.api.config_api import DEFAULT_SETTINGS
    from scripts.api.display_api import place_popup, work_area_for_point
    from scripts.api.input_validation_api import (
        is_signed_integer_candidate,
        is_unsigned_integer_candidate,
        parse_signed_integer,
        parse_unsigned_integer,
    )
    from scripts.api.settings_session_api import SettingsSession
    from scripts.api.localization_api import translate
    from scripts.api.window_scale_api import (
        MAX_WINDOW_SCALE_PERCENT,
        MIN_WINDOW_SCALE_PERCENT,
        WINDOW_SCALE_STEP,
        derive_window_metrics,
    )


def show_settings_dialog(owner):
    if owner.settings_dialog is not None and owner.settings_dialog.winfo_exists():
        owner.show_window()
        owner.settings_dialog.deiconify()
        owner.settings_dialog.lift()
        owner.settings_dialog.focus_force()
        return

    owner.show_window()
    dialog = tk.Toplevel(owner)
    owner.settings_dialog = dialog
    dialog.title("Codex 宠物设置")
    dialog.resizable(False, False)
    dialog.attributes("-topmost", True)
    settings_session = SettingsSession(owner.settings)
    reset_authorized = False
    owner._settings_session = settings_session
    draft = settings_session.draft_settings
    ui_language = draft["language"]
    text = lambda key: translate(ui_language, key)
    body = tk.Frame(dialog, padx=14, pady=12)
    body.pack(fill="both", expand=True)
    alpha = tk.DoubleVar(value=draft["alpha"])
    window_scale = tk.IntVar(value=draft["window_scale_percent"])
    position_x = tk.StringVar(value=str(draft["x"]))
    position_y = tk.StringVar(value=str(draft["y"]))
    refresh_interval = tk.StringVar(value=str(draft["refresh_interval_seconds"]))
    topmost = tk.BooleanVar(value=draft["topmost"])
    locked = tk.BooleanVar(value=draft["locked"])
    language_labels = {
        "en": translate(ui_language, "english"),
        "zh-CN": translate(ui_language, "simplified_chinese"),
    }
    language_by_label = {label: code for code, label in language_labels.items()}
    language = tk.StringVar(value=language_labels[draft["language"]])
    show_primary_5h = tk.BooleanVar(value=draft["show_primary_5h"])
    show_weekly = tk.BooleanVar(value=draft["show_weekly"])
    show_reset_credit = tk.BooleanVar(value=draft["show_reset_credit"])
    battery_source = tk.IntVar(
        value=0 if draft["battery_quota_source"] == "primary_5h" else 1
    )

    dialog.title(text("settings_title"))
    tk.Label(body, text=text("opacity")).grid(row=0, column=0, sticky="w")
    tk.Scale(body, from_=0.25, to=1.0, resolution=0.05, orient="horizontal", length=230, variable=alpha).grid(row=0, column=1)
    tk.Label(body, text=text("window_size")).grid(row=1, column=0, sticky="w")
    tk.Scale(
        body,
        from_=MIN_WINDOW_SCALE_PERCENT,
        to=MAX_WINDOW_SCALE_PERCENT,
        resolution=WINDOW_SCALE_STEP,
        orient="horizontal",
        length=230,
        variable=window_scale,
        label="%",
    ).grid(row=1, column=1)
    tk.Label(body, text=text("default_position")).grid(row=2, column=0, sticky="w")
    position = tk.Frame(body)
    position.grid(row=2, column=1, sticky="w")
    digit_or_signed = (owner.register(is_signed_integer_candidate), "%P")
    digits_only = (owner.register(is_unsigned_integer_candidate), "%P")
    tk.Entry(position, textvariable=position_x, width=8, validate="key", validatecommand=digit_or_signed).pack(side="left")
    tk.Label(position, text=", ").pack(side="left")
    tk.Entry(position, textvariable=position_y, width=8, validate="key", validatecommand=digit_or_signed).pack(side="left")
    tk.Label(body, text=text("refresh_interval")).grid(row=3, column=0, sticky="w")
    tk.Entry(body, textvariable=refresh_interval, width=8, validate="key", validatecommand=digits_only).grid(row=3, column=1, sticky="w")
    tk.Checkbutton(body, text=text("always_on_top"), variable=topmost).grid(row=4, column=0, sticky="w")
    tk.Checkbutton(body, text=text("lock_position"), variable=locked).grid(row=4, column=1, sticky="w")
    tk.Label(body, text=text("battery_content")).grid(row=6, column=0, sticky="w")
    source_control = tk.Frame(body)
    source_control.grid(row=6, column=1, sticky="w")
    tk.Scale(
        source_control,
        from_=0,
        to=1,
        resolution=1,
        orient="horizontal",
        showvalue=False,
        length=140,
        variable=battery_source,
    ).grid(row=0, column=0, columnspan=2)
    tk.Label(source_control, text=text("five_hour")).grid(row=1, column=0, sticky="w")
    tk.Label(source_control, text=text("weekly")).grid(row=1, column=1, sticky="e")
    tk.Label(body, text=text("language")).grid(row=7, column=0, sticky="w")
    ttk.Combobox(body, textvariable=language, values=tuple(language_labels.values()), state="readonly", width=18).grid(row=7, column=1, sticky="w")
    tk.Checkbutton(body, text=text("show_five_hour"), variable=show_primary_5h).grid(row=10, column=0, sticky="w")
    tk.Checkbutton(body, text=text("show_weekly"), variable=show_weekly).grid(row=10, column=1, sticky="w")
    tk.Checkbutton(body, text=text("show_reset_credit"), variable=show_reset_credit).grid(row=11, column=0, sticky="w")

    def choose_font():
        chosen = colorchooser.askcolor(color=draft["font_color"], parent=dialog)[1]
        if chosen:
            draft["font_color"] = chosen

    def choose_background():
        chosen = colorchooser.askcolor(color=draft["background_color"], parent=dialog)[1]
        if chosen:
            draft["background_color"] = chosen

    tk.Button(body, text=text("font_color"), command=choose_font).grid(row=9, column=0, pady=(8, 0), sticky="w")
    tk.Button(body, text=text("background_color"), command=choose_background).grid(row=9, column=1, pady=(8, 0), sticky="w")

    def sync_draft():
        try:
            draft["alpha"] = float(alpha.get())
            draft["x"] = parse_signed_integer(position_x.get())
            draft["y"] = parse_signed_integer(position_y.get())
            draft["refresh_interval_seconds"] = parse_unsigned_integer(refresh_interval.get(), 1, 10)
            draft["topmost"] = bool(topmost.get())
            draft["locked"] = bool(locked.get())
            draft["language"] = language_by_label[language.get()]
            draft["show_primary_5h"] = bool(show_primary_5h.get())
            draft["show_weekly"] = bool(show_weekly.get())
            draft["show_reset_credit"] = bool(show_reset_credit.get())
            draft["battery_quota_source"] = (
                "primary_5h" if battery_source.get() == 0 else "weekly"
            )
            metrics = derive_window_metrics(window_scale.get())
            draft["window_scale_percent"] = metrics.scale_percent
            draft["font_size"] = metrics.text_font_size
            draft["window_width"] = metrics.width
            draft["window_height"] = metrics.height
            draft["scale_mode"] = "proportional"
        except (TypeError, ValueError):
            messagebox.showerror("设置无效", "坐标和刷新间隔必须填写合法数字。", parent=dialog)
            return False
        return True

    def apply_draft():
        if not sync_draft():
            return False
        owner.apply_settings(settings_session.apply())
        return True

    def save_and_close():
        nonlocal reset_authorized
        if not apply_draft():
            return
        if not owner.save_settings(allow_unsafe_overwrite=reset_authorized):
            messagebox.showwarning(
                "配置受保护",
                "原配置不兼容或已损坏。若要替换它，请先选择“恢复默认值”，再保存。",
                parent=dialog,
            )
            return
        owner.settings = settings_session.save()
        owner.apply_settings(owner.settings)
        reset_authorized = False
        owner.close_settings(dialog)

    def restore_defaults():
        nonlocal reset_authorized
        reset_authorized = True
        settings_session.restore_defaults(DEFAULT_SETTINGS)
        draft.clear()
        draft.update(settings_session.draft_settings)
        alpha.set(draft["alpha"])
        window_scale.set(draft["window_scale_percent"])
        position_x.set(draft["x"])
        position_y.set(draft["y"])
        refresh_interval.set(draft["refresh_interval_seconds"])
        topmost.set(draft["topmost"])
        locked.set(draft["locked"])
        language.set(language_labels[draft["language"]])
        show_primary_5h.set(draft["show_primary_5h"])
        show_weekly.set(draft["show_weekly"])
        show_reset_credit.set(draft["show_reset_credit"])
        battery_source.set(
            0 if draft["battery_quota_source"] == "primary_5h" else 1
        )

    buttons = tk.Frame(body)
    buttons.grid(row=12, column=0, columnspan=2, pady=(14, 0))
    tk.Button(buttons, text=text("save"), width=8, command=save_and_close).pack(side="left", padx=3)
    tk.Button(buttons, text=text("apply"), width=8, command=apply_draft).pack(side="left", padx=3)
    tk.Button(buttons, text=text("restore_defaults"), width=12, command=restore_defaults).pack(side="left", padx=3)
    tk.Button(buttons, text=text("close"), width=8, command=lambda: owner.close_settings(dialog)).pack(side="left", padx=3)
    dialog.protocol("WM_DELETE_WINDOW", lambda: owner.close_settings(dialog))
    dialog.update_idletasks()
    dialog_work_area = work_area_for_point(owner.winfo_rootx(), owner.winfo_rooty())
    dialog_x, dialog_y = place_popup(
        owner.winfo_rootx(), owner.winfo_rooty(), dialog.winfo_reqwidth(), dialog.winfo_reqheight(), dialog_work_area
    )
    dialog.geometry(f"+{dialog_x}+{dialog_y}")
    dialog.deiconify()
    dialog.lift()
    dialog.focus_force()
    owner.after_idle(owner.ensure_visible)
