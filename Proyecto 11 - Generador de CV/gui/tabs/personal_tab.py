"""
personal_tab.py — Personal Information Tab  (SRP)
==================================================
Collects name, title, contact details and social links.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Dict

from gui.theme import Palette, Fonts, Spacing
from services.i18n import I18nService


class PersonalTab(tk.Frame):

    _FIELDS = [
        ("name",     "lbl_full_name"),
        ("title",    "lbl_job_title"),
        ("phone",    "lbl_phone"),
        ("email",    "lbl_email"),
        ("address",  "lbl_address"),
        ("github",   "lbl_github"),
        ("linkedin", "lbl_linkedin"),
    ]

    def __init__(self, parent: tk.Widget, i18n: I18nService) -> None:
        super().__init__(parent, bg=Palette.SURFACE)
        self._i18n = i18n
        self._vars: Dict[str, tk.StringVar] = {k: tk.StringVar() for k, _ in self._FIELDS}
        self._labels: Dict[str, tk.Label] = {}
        self._build()

    def _build(self) -> None:
        container = tk.Frame(self, bg=Palette.SURFACE)
        container.pack(fill="both", expand=True,
                       padx=Spacing.PAD_LG, pady=Spacing.PAD_LG)

        for key, i18n_key in self._FIELDS:
            row = tk.Frame(container, bg=Palette.SURFACE)
            row.pack(fill="x", pady=Spacing.PAD_SM)

            lbl = tk.Label(row, text=self._i18n.t(i18n_key),
                           font=Fonts.LABEL_BOLD,
                           bg=Palette.SURFACE, fg=Palette.ACCENT_LIGHT,
                           width=20, anchor="w")
            lbl.pack(side="left")
            self._labels[key] = lbl

            entry = ttk.Entry(row, textvariable=self._vars[key], style="TEntry")
            entry.pack(side="left", fill="x", expand=True, ipady=3)

    def refresh_labels(self) -> None:
        for key, i18n_key in self._FIELDS:
            if key in self._labels:
                self._labels[key].configure(text=self._i18n.t(i18n_key))

    def get_data(self) -> Dict[str, str]:
        return {k: v.get().strip() for k, v in self._vars.items()}
