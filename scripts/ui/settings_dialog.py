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
    from ui.theme import COLORS, FONT_FAMILY
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
    from scripts.ui.theme import COLORS, FONT_FAMILY


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
    dialog.configure(bg=COLORS["background"])
    settings_session = SettingsSession(owner.settings)
    reset_authorized = False
    owner._settings_session = settings_session
    draft = settings_session.draft_settings
    ui_language = draft["language"]
    draft_changed = False
    draft_tracking_enabled = False
    preview_status = None

    def text(key):
        return translate(ui_language, key)

    def lifecycle_status(applied=False, changed=None):
        if changed is None:
            changed = draft_changed
        if changed:
            return "\u8349\u7a3f\u5df2\u53d8\u66f4 \u00b7 \u70b9\u51fb\u5e94\u7528\u66f4\u65b0" if ui_language == "zh-CN" else "Draft changed \u00b7 Apply to update"
        if ui_language == "zh-CN":
            return "预览草稿 · 点击应用更新" if not applied else "预览已更新 · 保存后持久化"
        return "Draft only · Apply to update" if not applied else "Preview updated · Save to persist"
    shell = tk.Frame(dialog, bg=COLORS["background"], padx=10, pady=10)
    shell.pack(fill="both", expand=True)
    navigation = tk.Frame(shell, bg=COLORS["surface"], padx=8, pady=8, width=132)
    navigation.pack(side="left", fill="y", padx=(0, 10))
    navigation.pack_propagate(False)
    tk.Label(
        navigation,
        text="Codex Status Pet",
        bg=COLORS["surface"],
        fg=COLORS["text"],
        font=(FONT_FAMILY, 11, "bold"),
        anchor="w",
    ).pack(fill="x", pady=(2, 14))
    navigation_section_labels = []
    section_texts = {
        "en": ("General", "Appearance", "Quota display", "Behavior", "Advanced"),
        "zh-CN": ("\u901a\u7528", "\u5916\u89c2", "\u989d\u5ea6\u663e\u793a", "\u884c\u4e3a", "\u9ad8\u7ea7"),
    }
    for index, section in enumerate(section_texts[ui_language]):
        navigation_label = tk.Button(
            navigation,
            text=section,
            bg=COLORS["surface_alt"] if index == 0 else COLORS["surface"],
            fg=COLORS["accent"] if index == 0 else COLORS["muted"],
            font=(FONT_FAMILY, 9, "bold" if index == 0 else "normal"),
            anchor="w",
            padx=8,
            pady=7,
            relief="flat",
            bd=0,
            activebackground=COLORS["surface_alt"],
            activeforeground=COLORS["accent"],
            highlightthickness=0,
        )
        navigation_label.pack(fill="x", pady=1)
        navigation_section_labels.append(navigation_label)
    body = tk.Frame(shell, bg=COLORS["background"], padx=4, pady=2)
    body.pack(side="left", fill="both", expand=True)
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
    translated_widgets = []

    def translated(widget, key):
        translated_widgets.append((widget, key))
        return widget

    def themed_label(parent, value, **kwargs):
        return tk.Label(
            parent,
            text=value,
            bg=kwargs.pop("bg", COLORS["background"]),
            fg=kwargs.pop("fg", COLORS["text"]),
            font=kwargs.pop("font", (FONT_FAMILY, 9)),
            **kwargs,
        )

    def themed_checkbutton(parent, value, variable, command=None):
        options = {
            "text": value,
            "variable": variable,
            "bg": COLORS["background"],
            "fg": COLORS["text"],
            "activebackground": COLORS["background"],
            "activeforeground": COLORS["accent"],
            "selectcolor": COLORS["surface_alt"],
            "font": (FONT_FAMILY, 9),
        }
        if command is not None:
            options["command"] = command
        return tk.Checkbutton(parent, **options)

    def themed_scale(parent, **kwargs):
        return tk.Scale(
            parent,
            bg=COLORS["background"],
            fg=COLORS["muted"],
            troughcolor=COLORS["surface_alt"],
            activebackground=COLORS["accent"],
            highlightthickness=0,
            bd=0,
            font=(FONT_FAMILY, 8),
            **kwargs,
        )

    def themed_entry(parent, **kwargs):
        entry = tk.Entry(
            parent,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            insertbackground=COLORS["accent"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["accent"],
            **kwargs,
        )
        return entry

    def themed_button(parent, value, command, *, primary=False, width=None):
        options = {
            "text": value,
            "command": command,
            "font": (FONT_FAMILY, 9, "bold" if primary else "normal"),
            "fg": COLORS["background"] if primary else COLORS["text"],
            "bg": COLORS["accent"] if primary else COLORS["surface"],
            "activeforeground": COLORS["background"] if primary else COLORS["accent"],
            "activebackground": COLORS["accent_alt"] if primary else COLORS["surface_alt"],
            "relief": "flat",
            "bd": 0,
            "padx": 10,
            "pady": 5,
        }
        if width is not None:
            options["width"] = width
        return tk.Button(parent, **options)

    translated(themed_label(body, text("opacity")), "opacity").grid(row=0, column=0, sticky="w")
    opacity_scale = themed_scale(body, from_=0.25, to=1.0, resolution=0.05, orient="horizontal", length=230, variable=alpha, command=lambda value: refresh_preview(alpha_value=value))
    opacity_scale.grid(row=0, column=1)
    translated(themed_label(body, text("window_size")), "window_size").grid(row=1, column=0, sticky="w")
    window_scale_control = themed_scale(
        body,
        from_=MIN_WINDOW_SCALE_PERCENT,
        to=MAX_WINDOW_SCALE_PERCENT,
        resolution=WINDOW_SCALE_STEP,
        orient="horizontal",
        length=230,
        variable=window_scale,
        label="%",
        command=lambda value: refresh_preview(window_scale_value=value),
    )
    window_scale_control.grid(row=1, column=1)
    translated(themed_label(body, text("default_position")), "default_position").grid(row=2, column=0, sticky="w")
    position = tk.Frame(body, bg=COLORS["background"])
    position.grid(row=2, column=1, sticky="w")
    digit_or_signed = (owner.register(is_signed_integer_candidate), "%P")
    digits_only = (owner.register(is_unsigned_integer_candidate), "%P")
    themed_entry(position, textvariable=position_x, width=8, validate="key", validatecommand=digit_or_signed).pack(side="left")
    themed_label(position, ", ", fg=COLORS["muted"], font=(FONT_FAMILY, 9)).pack(side="left")
    themed_entry(position, textvariable=position_y, width=8, validate="key", validatecommand=digit_or_signed).pack(side="left")
    translated(themed_label(body, text("refresh_interval")), "refresh_interval").grid(row=3, column=0, sticky="w")
    refresh_interval_entry = themed_entry(body, textvariable=refresh_interval, width=8, validate="key", validatecommand=digits_only)
    refresh_interval_entry.grid(row=3, column=1, sticky="w")
    topmost_checkbutton = themed_checkbutton(body, text("always_on_top"), topmost)
    translated(topmost_checkbutton, "always_on_top").grid(row=4, column=0, sticky="w")
    translated(themed_checkbutton(body, text("lock_position"), locked), "lock_position").grid(row=4, column=1, sticky="w")
    quota_group_divider = tk.Frame(body, bg=COLORS["border"], height=1)
    quota_group_divider.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(8, 6))
    translated(themed_label(body, text("battery_content")), "battery_content").grid(row=6, column=0, sticky="w")
    source_control = tk.Frame(body, bg=COLORS["background"])
    source_control.grid(row=6, column=1, sticky="w")
    battery_source_scale = themed_scale(
        source_control,
        from_=0,
        to=1,
        resolution=1,
        orient="horizontal",
        showvalue=False,
        length=140,
        variable=battery_source,
    )
    battery_source_scale.grid(row=0, column=0, columnspan=2)
    translated(themed_label(source_control, text("five_hour"), fg=COLORS["muted"]), "five_hour").grid(row=1, column=0, sticky="w")
    translated(themed_label(source_control, text("weekly"), fg=COLORS["muted"]), "weekly").grid(row=1, column=1, sticky="e")
    translated(themed_label(body, text("language")), "language").grid(row=7, column=0, sticky="w")
    combo_style = ttk.Style(dialog)
    combo_style.configure(
        "HUD.TCombobox",
        fieldbackground=COLORS["surface"],
        background=COLORS["surface_alt"],
        foreground=COLORS["text"],
        bordercolor=COLORS["border"],
        lightcolor=COLORS["border"],
        darkcolor=COLORS["border"],
        arrowcolor=COLORS["accent"],
    )
    combo_style.map(
        "HUD.TCombobox",
        fieldbackground=[("readonly", COLORS["surface"])],
        foreground=[("readonly", COLORS["text"])],
        selectbackground=[("readonly", COLORS["surface_alt"])],
        selectforeground=[("readonly", COLORS["text"])],
    )
    language_combo = ttk.Combobox(body, textvariable=language, values=tuple(language_labels.values()), state="readonly", width=18, style="HUD.TCombobox")
    language_combo.grid(row=7, column=1, sticky="w")
    row_visibility_title = tk.Label(
        body,
        text="Row visibility",
        bg=COLORS["background"],
        fg=COLORS["accent"],
        font=(FONT_FAMILY, 10, "bold"),
    )
    row_visibility_title.grid(row=8, column=0, columnspan=2, sticky="w", pady=(8, 2))
    translated(themed_checkbutton(body, text("show_five_hour"), show_primary_5h, command=lambda: refresh_preview()), "show_five_hour").grid(row=10, column=0, sticky="w")
    translated(themed_checkbutton(body, text("show_weekly"), show_weekly, command=lambda: refresh_preview()), "show_weekly").grid(row=10, column=1, sticky="w")
    translated(themed_checkbutton(body, text("show_reset_credit"), show_reset_credit, command=lambda: refresh_preview()), "show_reset_credit").grid(row=11, column=0, sticky="w")

    preview = tk.LabelFrame(
        body,
        text="Live preview" if ui_language == "en" else "\u9884\u89c8",
        bg=COLORS["surface"],
        fg=COLORS["accent"],
        padx=10,
        pady=8,
        font=(FONT_FAMILY, 10, "bold"),
    )
    preview.grid(row=0, column=2, rowspan=12, padx=(18, 0), sticky="nsew")
    preview_card = tk.Frame(preview, bg=COLORS["background"], padx=10, pady=10, width=190, height=145)
    preview_card.pack(fill="both", expand=True)
    preview_card.pack_propagate(False)
    tk.Label(preview_card, text="●  Codex Outputting", bg=COLORS["background"], fg=COLORS["success"], anchor="w", font=(FONT_FAMILY, 10, "bold")).pack(fill="x")
    tk.Label(preview_card, text="Active conversations  1", bg=COLORS["background"], fg=COLORS["muted"], anchor="w").pack(fill="x", pady=(5, 8))
    preview_source = tk.Label(preview_card, text="", bg=COLORS["background"], fg=COLORS["muted"], anchor="w", font=(FONT_FAMILY, 8))
    preview_source.pack(fill="x", pady=(0, 4))
    preview_rows = {}
    for row_id, label, color in (("five_hour", "5-hour quota   -- / --", COLORS["accent"]), ("weekly", "Weekly quota   88%", COLORS["accent_alt"]), ("reset_credit", "Reset Credit   4 times", COLORS["warning"])):
        preview_rows[row_id] = tk.Label(preview_card, text=label, bg=COLORS["background"], fg=color, anchor="w")
        preview_rows[row_id].pack(fill="x", pady=2)
    preview_meta = tk.Label(preview_card, text="", bg=COLORS["background"], fg=COLORS["muted"], anchor="w", font=(FONT_FAMILY, 8))
    preview_meta.pack(fill="x", pady=(6, 0))
    preview_activity = preview_card.winfo_children()[0]
    preview_conversations = preview_card.winfo_children()[1]
    preview_row_keys = (
        ("five_hour", "preview_five_hour_quota"),
        ("weekly", "preview_weekly_quota"),
        ("reset_credit", "preview_reset_credit"),
    )
    source_labels = {
        0: source_control.winfo_children()[1],
        1: source_control.winfo_children()[2],
    }

    def refresh_preview(window_scale_value=None, alpha_value=None):
        preview_activity.configure(text=translate(ui_language, "preview_output"))
        preview_conversations.configure(text=translate(ui_language, "preview_active_conversations"))
        for row_id, text_key in preview_row_keys:
            preview_rows[row_id].configure(text=translate(ui_language, text_key))
        selected_source = int(battery_source.get())
        for source_index, label in source_labels.items():
            label.configure(
                fg=COLORS["accent"] if source_index == selected_source else COLORS["muted"]
            )
        for row_id, variable in (("five_hour", show_primary_5h), ("weekly", show_weekly), ("reset_credit", show_reset_credit)):
            row = preview_rows[row_id]
            if variable.get():
                if row.winfo_manager() == "":
                    row.pack(fill="x", pady=2)
            else:
                row.pack_forget()
        metrics = derive_window_metrics(window_scale_value if window_scale_value is not None else window_scale.get())
        topmost_state = ("置顶" if topmost.get() else "普通") if ui_language == "zh-CN" else ("topmost" if topmost.get() else "normal")
        opacity_value = alpha_value if alpha_value is not None else alpha.get()
        preview_prefix = "预览" if ui_language == "zh-CN" else "Preview"
        source_prefix = "数据源" if ui_language == "zh-CN" else "Source"
        source_name = ("5 小时" if ui_language == "zh-CN" else "5-hour") if battery_source.get() == 0 else ("每周" if ui_language == "zh-CN" else "Weekly")
        preview_source.configure(text=f"{source_prefix}: {source_name}")
        preview_meta.configure(
            text=f"{preview_prefix} · {metrics.scale_percent}% · opacity {round(float(opacity_value) * 100)}% · {topmost_state}"
        )

        mark_draft_changed()

    def mark_draft_changed():
        nonlocal draft_changed
        if not draft_tracking_enabled:
            return
        draft_changed = True
        if preview_status is not None:
            preview_status.configure(text=lifecycle_status(changed=True))

    window_scale.trace_add("write", lambda *_args: refresh_preview())
    alpha.trace_add("write", lambda *_args: refresh_preview())
    battery_source.trace_add("write", lambda *_args: refresh_preview())
    refresh_preview()

    focus_targets = (
        opacity_scale,
        window_scale_control,
        battery_source_scale,
        topmost_checkbutton,
        refresh_interval_entry,
    )

    def focus_section(index):
        for button_index, button in enumerate(navigation_section_labels):
            active = button_index == index
            button.configure(
                bg=COLORS["surface_alt"] if active else COLORS["surface"],
                fg=COLORS["accent"] if active else COLORS["muted"],
                font=(FONT_FAMILY, 9, "bold" if active else "normal"),
            )
        for target in focus_targets:
            target.configure(
                highlightthickness=0,
                highlightbackground=COLORS["border"],
                highlightcolor=COLORS["border"],
            )
        target = focus_targets[index]
        target.configure(
            highlightthickness=1,
            highlightbackground=COLORS["accent"],
            highlightcolor=COLORS["accent"],
        )
        target.focus_set()

    for index, button in enumerate(navigation_section_labels):
        button.configure(command=lambda index=index: focus_section(index))

    def choose_font():
        chosen = colorchooser.askcolor(color=draft["font_color"], parent=dialog)[1]
        if chosen:
            draft["font_color"] = chosen

    def choose_background():
        chosen = colorchooser.askcolor(color=draft["background_color"], parent=dialog)[1]
        if chosen:
            draft["background_color"] = chosen

    translated(themed_button(body, text("font_color"), choose_font), "font_color").grid(row=9, column=0, pady=(8, 0), sticky="w")
    translated(themed_button(body, text("background_color"), choose_background), "background_color").grid(row=9, column=1, pady=(8, 0), sticky="w")

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
            messagebox.showerror(
                text("invalid_settings_title"),
                text("invalid_settings_message"),
                parent=dialog,
            )
            return False
        return True

    def refresh_language_widgets(selected_language):
        nonlocal ui_language, language_labels, language_by_label
        ui_language = selected_language
        dialog.title(text("settings_title"))
        for widget, key in translated_widgets:
            widget.configure(text=text(key))
        for widget, label in zip(navigation_section_labels, section_texts[selected_language]):
            widget.configure(text=label)
        row_visibility_title.configure(
            text="行可见性" if selected_language == "zh-CN" else "Row visibility"
        )
        preview.configure(text="预览" if selected_language == "zh-CN" else "Live preview")
        preview_status.configure(text=lifecycle_status(applied=False))
        language_labels = {
            "en": text("english"),
            "zh-CN": text("simplified_chinese"),
        }
        language_by_label = {
            label: code for code, label in language_labels.items()
        }
        language_combo.configure(values=tuple(language_labels.values()))
        language.set(language_labels[draft["language"]])
        refresh_preview()

    def apply_draft():
        nonlocal draft_changed
        if not sync_draft():
            return False
        owner.apply_settings(settings_session.apply())
        draft_changed = False
        refresh_language_widgets(draft["language"])
        draft_changed = False
        preview_status.configure(text=lifecycle_status(applied=True))
        return True

    def save_and_close():
        nonlocal reset_authorized
        if not apply_draft():
            return
        if not owner.save_settings(allow_unsafe_overwrite=reset_authorized):
            messagebox.showwarning(
                text("protected_settings_title"),
                text("protected_settings_message"),
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
        refresh_language_widgets(draft["language"])
        show_primary_5h.set(draft["show_primary_5h"])
        show_weekly.set(draft["show_weekly"])
        show_reset_credit.set(draft["show_reset_credit"])
        battery_source.set(
            0 if draft["battery_quota_source"] == "primary_5h" else 1
        )
        refresh_preview()

    preview_status = tk.Label(
        body,
        text=lifecycle_status(),
        bg=COLORS["background"],
        fg=COLORS["muted"],
        font=(FONT_FAMILY, 8),
        anchor="w",
    )
    preview_status.grid(row=12, column=0, columnspan=3, sticky="w", pady=(10, 0))
    buttons = tk.Frame(body, bg=COLORS["background"])
    buttons.grid(row=13, column=0, columnspan=3, pady=(8, 0))
    translated(themed_button(buttons, text("save"), save_and_close, primary=True, width=8), "save").pack(side="left", padx=3)
    translated(themed_button(buttons, text("apply"), apply_draft, width=8), "apply").pack(side="left", padx=3)
    translated(themed_button(buttons, text("restore_defaults"), restore_defaults, width=12), "restore_defaults").pack(side="left", padx=3)
    translated(themed_button(buttons, text("close"), lambda: owner.close_settings(dialog), width=8), "close").pack(side="left", padx=3)
    dialog.bind("<Alt-a>", lambda _event: (apply_draft(), "break")[1])
    dialog.bind("<Alt-s>", lambda _event: (save_and_close(), "break")[1])
    dialog.bind("<Escape>", lambda _event: (owner.close_settings(dialog), "break")[1])
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

    def initialize_dialog_focus():
        nonlocal draft_changed, draft_tracking_enabled
        focus_section(0)
        draft_changed = False
        draft_tracking_enabled = True
        preview_status.configure(text=lifecycle_status())

    dialog.after_idle(initialize_dialog_focus)
    owner.after_idle(owner.ensure_visible)
