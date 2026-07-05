"""
experience_tab.py — Work Experience Tab  (SRP / OCP)
=====================================================
Delegates dynamic list management to EntryList (DIP).
"""
from __future__ import annotations

import tkinter as tk
from typing import Any, Dict, List

from gui.components.entry_list import EntryList
from gui.theme import Palette, Spacing
from services.i18n import I18nService


class ExperienceTab(tk.Frame):

    def __init__(self, parent: tk.Widget, i18n: I18nService) -> None:
        super().__init__(parent, bg=Palette.SURFACE)
        self._i18n = i18n
        self._build()

    def _fields(self) -> list:
        t = self._i18n.t
        return [
            ("title",    t("lbl_exp_role")),
            ("subtitle", t("lbl_exp_company")),
            ("date",     t("lbl_exp_date")),
            ("_bullets", t("lbl_exp_bullets")),
        ]

    def _build(self) -> None:
        self._list = EntryList(
            self,
            fields=self._fields(),
            add_label=self._i18n.t("btn_add_entry"),
            remove_label=self._i18n.t("btn_remove_entry"),
        )
        self._list.pack(fill="both", expand=True,
                        padx=Spacing.PAD_MD, pady=Spacing.PAD_MD)

    def refresh_labels(self) -> None:
        self._list.update_labels(
            self._i18n.t("btn_add_entry"),
            self._i18n.t("btn_remove_entry"),
        )

    def get_data(self) -> List[Dict[str, Any]]:
        entries = []
        for raw in self._list.get_all_data():
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
