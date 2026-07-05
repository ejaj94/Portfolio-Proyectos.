"""
main_window.py — Application Orchestrator  (SRP / DIP / OCP)
=============================================================
Builds the top-level window, wires all components together and
delegates each concern to the appropriate service / widget.

Dependency graph (all arrows point inward → DIP satisfied):
  MainWindow ──► I18nService
              ──► CVGenerationService
              ──► PersonalTab, ProfileTab, ExperienceTab,
                  SkillsTab, EducationTab, LanguagesTab
              ──► PhotoPicker
"""
from __future__ import annotations

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from gui.components.photo_picker import PhotoPicker
from gui.tabs.education_tab import EducationTab
from gui.tabs.experience_tab import ExperienceTab
from gui.tabs.languages_tab import LanguagesTab
from gui.tabs.personal_tab import PersonalTab
from gui.tabs.profile_tab import ProfileTab
from gui.tabs.skills_tab import SkillsTab
from gui.theme import Fonts, Palette, Spacing, apply_theme
from services.cv_service import CVGenerationService
from services.i18n import I18nService


class MainWindow:
    """Root application window."""

    _WIN_W  = 1100
    _WIN_H  = 760
    _MIN_W  = 900
    _MIN_H  = 640

    _PDF_LANG_OPTIONS = [
        ("English",    "en"),
        ("Español",    "es"),
        ("Português",  "pt"),
    ]

    def __init__(self) -> None:
        self._i18n = I18nService("en")

        self._root = tk.Tk()
        self._root.title(self._i18n.t("app_title"))
        self._root.geometry(f"{self._WIN_W}x{self._WIN_H}")
        self._root.minsize(self._MIN_W, self._MIN_H)

        apply_theme(self._root)

        self._output_dir: str = os.path.join(os.path.expanduser("~"), "Desktop")
        self._pdf_lang_var  = tk.StringVar(value="en")
        self._ui_lang_var   = tk.StringVar(value="en")

        self._build_layout()

    # ── Layout builders ───────────────────────────────────────────────────────
    def _build_layout(self) -> None:
        """Assemble the full window in three vertical sections."""
        self._build_header()

        # Central pane: left (form) + right (sidebar)
        center = tk.Frame(self._root, bg=Palette.BG)
        center.pack(fill="both", expand=True,
                    padx=Spacing.PAD_LG, pady=(0, Spacing.PAD_MD))

        self._build_form(center)
        self._build_sidebar(center)

        self._build_log_bar()

    def _build_header(self) -> None:
        hdr = tk.Frame(self._root, bg=Palette.SURFACE2)
        hdr.pack(fill="x")

        inner = tk.Frame(hdr, bg=Palette.SURFACE2)
        inner.pack(padx=Spacing.PAD_LG, pady=Spacing.PAD_MD)

        # Accent stripe
        stripe = tk.Frame(self._root, bg=Palette.ACCENT, height=3)
        stripe.pack(fill="x")

        self._title_lbl = tk.Label(inner,
                                   text=self._i18n.t("app_title"),
                                   font=Fonts.TITLE,
                                   bg=Palette.SURFACE2, fg=Palette.TEXT)
        self._title_lbl.pack(side="left")

        self._subtitle_lbl = tk.Label(inner,
                                      text=self._i18n.t("app_subtitle"),
                                      font=Fonts.SUBTITLE,
                                      bg=Palette.SURFACE2,
                                      fg=Palette.TEXT_MUTED)
        self._subtitle_lbl.pack(side="left", padx=(Spacing.PAD_MD, 0))

        # UI language selector (top-right)
        lang_frame = tk.Frame(inner, bg=Palette.SURFACE2)
        lang_frame.pack(side="right")

        self._ui_lang_lbl = tk.Label(lang_frame,
                                     text=self._i18n.t("lbl_ui_lang"),
                                     font=Fonts.LABEL,
                                     bg=Palette.SURFACE2, fg=Palette.TEXT_MUTED)
        self._ui_lang_lbl.pack(side="left", padx=(0, Spacing.PAD_SM))

        ui_combo = ttk.Combobox(lang_frame, textvariable=self._ui_lang_var,
                                values=["en", "es", "pt"],
                                state="readonly", width=5)
        ui_combo.pack(side="left")
        ui_combo.bind("<<ComboboxSelected>>", self._on_ui_lang_change)

    def _build_form(self, parent: tk.Widget) -> None:
        """Left pane: tabbed form."""
        form_frame = tk.Frame(parent, bg=Palette.SURFACE,
                              highlightbackground=Palette.BORDER,
                              highlightthickness=1)
        form_frame.pack(side="left", fill="both", expand=True,
                        padx=(0, Spacing.PAD_MD))

        self._notebook = ttk.Notebook(form_frame)
        self._notebook.pack(fill="both", expand=True,
                            padx=Spacing.PAD_SM, pady=Spacing.PAD_SM)

        # Instantiate tabs
        self._tab_personal   = PersonalTab(self._notebook,  self._i18n)
        self._tab_profile    = ProfileTab(self._notebook,   self._i18n)
        self._tab_experience = ExperienceTab(self._notebook, self._i18n)
        self._tab_skills     = SkillsTab(self._notebook,    self._i18n)
        self._tab_education  = EducationTab(self._notebook, self._i18n)
        self._tab_languages  = LanguagesTab(self._notebook, self._i18n)

        self._tabs = [
            (self._tab_personal,   "tab_personal"),
            (self._tab_profile,    "tab_profile"),
            (self._tab_experience, "tab_experience"),
            (self._tab_skills,     "tab_skills"),
            (self._tab_education,  "tab_education"),
            (self._tab_languages,  "tab_languages"),
        ]

        for widget, i18n_key in self._tabs:
            self._notebook.add(widget, text=f"  {self._i18n.t(i18n_key)}  ")

    def _build_sidebar(self, parent: tk.Widget) -> None:
        """Right sidebar: photo, options, generate button."""
        sidebar = tk.Frame(parent, bg=Palette.SURFACE,
                           width=230,
                           highlightbackground=Palette.BORDER,
                           highlightthickness=1)
        sidebar.pack(side="right", fill="y")
        sidebar.pack_propagate(False)

        inner = tk.Frame(sidebar, bg=Palette.SURFACE)
        inner.pack(fill="both", expand=True,
                   padx=Spacing.PAD_MD, pady=Spacing.PAD_MD)

        # Photo picker
        self._photo_picker = PhotoPicker(
            inner,
            pick_label=self._i18n.t("btn_photo"),
            no_photo_label=self._i18n.t("lbl_no_photo"),
        )
        self._photo_picker.pack(fill="x", pady=(0, Spacing.PAD_MD))

        ttk.Separator(inner, orient="horizontal").pack(fill="x",
                                                       pady=Spacing.PAD_SM)

        # PDF language selector
        self._pdf_lang_lbl = tk.Label(inner,
                                      text=self._i18n.t("lbl_pdf_lang"),
                                      font=Fonts.LABEL_BOLD,
                                      bg=Palette.SURFACE, fg=Palette.ACCENT_LIGHT)
        self._pdf_lang_lbl.pack(anchor="w")

        pdf_combo = ttk.Combobox(inner, textvariable=self._pdf_lang_var,
                                 values=["en", "es", "pt"],
                                 state="readonly", width=10)
        pdf_combo.pack(fill="x", pady=(Spacing.PAD_XS, Spacing.PAD_MD))

        # Output folder selector
        self._out_lbl = tk.Label(inner,
                                 text=self._i18n.t("lbl_output_dir"),
                                 font=Fonts.LABEL_BOLD,
                                 bg=Palette.SURFACE, fg=Palette.ACCENT_LIGHT)
        self._out_lbl.pack(anchor="w")

        self._out_dir_lbl = tk.Label(inner,
                                     text=self._output_dir,
                                     font=(Fonts.FAMILY, 8),
                                     bg=Palette.SURFACE, fg=Palette.TEXT_MUTED,
                                     wraplength=200, justify="left")
        self._out_dir_lbl.pack(anchor="w")

        ttk.Button(inner,
                   text=self._i18n.t("btn_output"),
                   style="Secondary.TButton",
                   command=self._pick_output_dir).pack(
                       fill="x", pady=(Spacing.PAD_XS, Spacing.PAD_MD))

        ttk.Separator(inner, orient="horizontal").pack(fill="x",
                                                       pady=Spacing.PAD_SM)

        # Generate button (hero CTA)
        self._gen_btn = ttk.Button(inner,
                                   text=self._i18n.t("btn_generate"),
                                   style="Primary.TButton",
                                   command=self._on_generate)
        self._gen_btn.pack(fill="x", ipady=6, pady=(Spacing.PAD_MD, 0))

    def _build_log_bar(self) -> None:
        """Bottom status bar with scrollable log."""
        bar = tk.Frame(self._root, bg=Palette.SURFACE2, height=80)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)

        self._log_text = tk.Text(
            bar,
            bg=Palette.SURFACE2, fg=Palette.TEXT_MUTED,
            font=Fonts.LOG,
            height=4, relief="flat",
            state="disabled",
            padx=Spacing.PAD_MD, pady=Spacing.PAD_SM,
            wrap="word", highlightthickness=0,
        )
        self._log_text.pack(fill="both", expand=True)
        self._log(self._i18n.t("log_ready"))

    # ── Event handlers ────────────────────────────────────────────────────────
    def _on_ui_lang_change(self, _event: tk.Event) -> None:
        lang = self._ui_lang_var.get()
        self._i18n.set_language(lang)
        self._refresh_all_labels()

    def _refresh_all_labels(self) -> None:
        """Push new translations to every widget without rebuilding the UI."""
        t = self._i18n.t
        self._root.title(t("app_title"))
        self._title_lbl.configure(text=t("app_title"))
        self._subtitle_lbl.configure(text=t("app_subtitle"))
        self._ui_lang_lbl.configure(text=t("lbl_ui_lang"))
        self._pdf_lang_lbl.configure(text=t("lbl_pdf_lang"))
        self._out_lbl.configure(text=t("lbl_output_dir"))
        self._gen_btn.configure(text=t("btn_generate"))
        self._photo_picker.update_labels(t("btn_photo"), t("lbl_no_photo"))

        # Refresh tab titles
        for i, (_, i18n_key) in enumerate(self._tabs):
            self._notebook.tab(i, text=f"  {t(i18n_key)}  ")

        # Refresh tab internals
        for widget, _ in self._tabs:
            if hasattr(widget, "refresh_labels"):
                widget.refresh_labels()

        self._log(t("log_ready"))

    def _pick_output_dir(self) -> None:
        path = filedialog.askdirectory(title="Select output folder",
                                       initialdir=self._output_dir)
        if path:
            self._output_dir = path
            self._out_dir_lbl.configure(text=path)

    def _on_generate(self) -> None:
        """Validate, collect data and run generation in a background thread."""
        data = self._collect_form_data()
        errors = self._validate(data)
        if errors:
            messagebox.showerror("Validation", "\n".join(errors))
            return

        self._gen_btn.configure(state="disabled")
        self._log(self._i18n.t("log_generating"))

        def _worker() -> None:
            service = CVGenerationService(progress_callback=self._log)
            result = service.generate(
                data=data,
                photo_path=self._photo_picker.get_photo_path(),
                output_dir=self._output_dir,
            )
            self._root.after(0, lambda: self._on_generation_done(result))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_generation_done(self, result) -> None:
        self._gen_btn.configure(state="normal")
        if result.success:
            self._log(self._i18n.t("log_success"))
            if messagebox.askyesno(
                self._i18n.t("app_title"),
                f"{result.message}\n\n{self._i18n.t('log_open_folder')}?",
            ):
                os.startfile(os.path.dirname(result.output_path))
        else:
            self._log(self._i18n.t("log_error", msg=result.message))
            messagebox.showerror("Error", result.message)

    # ── Data collection & validation ──────────────────────────────────────────
    def _collect_form_data(self) -> dict:
        return {
            "personal":    self._tab_personal.get_data(),
            "profile_text": self._tab_profile.get_data(),
            "experience":  self._tab_experience.get_data(),
            "skills":      self._tab_skills.get_data(),
            "education":   self._tab_education.get_education_data(),
            "certificates": self._tab_education.get_certificates(),
            "languages":   self._tab_languages.get_data(),
            "output_lang": self._pdf_lang_var.get(),
        }

    def _validate(self, data: dict) -> list[str]:
        errors = []
        if not data["personal"].get("name"):
            errors.append(self._i18n.t("val_name_required"))
        if not data["profile_text"]:
            errors.append(self._i18n.t("val_profile_required"))
        return errors

    # ── Log helper ────────────────────────────────────────────────────────────
    def _log(self, message: str) -> None:
        self._log_text.configure(state="normal")
        self._log_text.insert("end", f"{message}\n")
        self._log_text.see("end")
        self._log_text.configure(state="disabled")

    # ── Entry point ───────────────────────────────────────────────────────────
    def run(self) -> None:
        self._root.mainloop()
