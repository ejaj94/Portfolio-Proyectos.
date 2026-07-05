"""
skills_tab.py — Technical Skills Tab  (SRP)
============================================
Each row = one skill group (e.g. "Languages: Python, SQL, JS").
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import List, Tuple

from gui.components.entry_list import EntryList
from gui.theme import Palette, Spacing
from services.i18n import I18nService


class SkillsTab(tk.Frame):

    def __init__(self, parent: tk.Widget, i18n: I18nService) -> None:
        super().__init__(parent, bg=Palette.SURFACE)
        self._i18n = i18n
        self._build()

    def _fields(self) -> list:
        return [
            ("group", self._i18n.t("lbl_skill_group")),
            ("items", self._i18n.t("lbl_skill_items")),
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

    def get_data(self) -> List[Tuple[str, str]]:
        return [
            (row.get("group", ""), row.get("items", ""))
            for row in self._list.get_all_data()
            if row.get("group") or row.get("items")
        ]
