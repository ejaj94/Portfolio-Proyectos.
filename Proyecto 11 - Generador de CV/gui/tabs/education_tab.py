"""
education_tab.py — Education & Certificates Tab  (SRP)
=======================================================
Two sections: degree entries (via EntryList) + a free-text certificates list.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, List

from gui.components.entry_list import EntryList
from gui.theme import Palette, Fonts, Spacing
from services.i18n import I18nService


class EducationTab(tk.Frame):

    def __init__(self, parent: tk.Widget, i18n: I18nService) -> None:
        super().__init__(parent, bg=Palette.SURFACE)
        self._i18n = i18n
        self._build()

    def _edu_fields(self) -> list:
        return [
            ("title",    self._i18n.t("lbl_edu_degree")),
            ("subtitle", self._i18n.t("lbl_edu_institution")),
            ("date",     self._i18n.t("lbl_edu_date")),
            ("_bullets", self._i18n.t("lbl_edu_bullets")),
        ]

    def _build(self) -> None:
        # ── Degrees section ───────────────────────────────────────────────────
        self._edu_list = EntryList(
            self,
            fields=self._edu_fields(),
            add_label=self._i18n.t("btn_add_entry"),
            remove_label=self._i18n.t("btn_remove_entry"),
        )
        self._edu_list.pack(fill="both", expand=True,
                            padx=Spacing.PAD_MD, pady=(Spacing.PAD_MD, 0))

        ttk.Separator(self, orient="horizontal").pack(
            fill="x", padx=Spacing.PAD_MD, pady=Spacing.PAD_MD)

        # ── Certificates section ──────────────────────────────────────────────
        cert_frame = tk.Frame(self, bg=Palette.SURFACE)
        cert_frame.pack(fill="x", padx=Spacing.PAD_MD,
                        pady=(0, Spacing.PAD_MD))

        self._cert_lbl = tk.Label(cert_frame,
                                  text=self._i18n.t("lbl_certificates"),
                                  font=Fonts.LABEL_BOLD,
                                  bg=Palette.SURFACE, fg=Palette.ACCENT_LIGHT)
        self._cert_lbl.pack(anchor="w", pady=(0, Spacing.PAD_XS))

        txt_frame = tk.Frame(cert_frame, bg=Palette.BORDER, bd=1)
        txt_frame.pack(fill="x")

        self._cert_text = tk.Text(
            txt_frame, height=5,
            bg=Palette.ENTRY_BG, fg=Palette.ENTRY_FG,
            insertbackground=Palette.ACCENT_LIGHT,
            font=Fonts.ENTRY, relief="flat",
            wrap="word", padx=8, pady=6,
            highlightthickness=0,
        )
        self._cert_text.pack(fill="x")

    def refresh_labels(self) -> None:
        self._edu_list.update_labels(
            self._i18n.t("btn_add_entry"),
            self._i18n.t("btn_remove_entry"),
        )
        self._cert_lbl.configure(text=self._i18n.t("lbl_certificates"))

    def get_education_data(self) -> List[Dict[str, Any]]:
        entries = []
        for raw in self._edu_list.get_all_data():
            bullets = [
                b.strip()
                for b in raw.get("_bullets", "").splitlines()
                if b.strip()
            ]
            entries.append({
                "title":    raw.get("title", ""),
                "subtitle": raw.get("subtitle", ""),
                "date":     raw.get("date", ""),
                "bullets":  bullets,
            })
        return entries

    def get_certificates(self) -> List[str]:
        raw = self._cert_text.get("1.0", "end-1c")
        return [c.strip() for c in raw.splitlines() if c.strip()]
