"""
skills_tab.py — Technical Skills Tab  (SRP)
============================================
Each row = one skill group. Uses CTk.
"""
from __future__ import annotations

import customtkinter as ctk
from typing import List, Tuple

from gui.components.entry_list import EntryList
from gui.theme import Palette, Fonts
from services.i18n import I18nService

class SkillsTab(ctk.CTkScrollableFrame):
    def __init__(self, parent: ctk.CTkFrame, i18n: I18nService) -> None:
        super().__init__(parent, fg_color="transparent")
        self._i18n = i18n
        self.entry_list = EntryList(self, self._i18n.t("add_skill"), self._create_item)
        self.entry_list.pack(fill="both", expand=True)

    def _create_item(self, parent: ctk.CTkFrame, remove_cb) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(parent, fg_color=Palette.SURFACE, corner_radius=8)
        frame.grid_columnconfigure(0, weight=1)

        ent_items = ctk.CTkEntry(frame, placeholder_text=self._i18n.t("skill_items_ph"), font=Fonts.label(), fg_color=Palette.ENTRY_BG)
        ent_items.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        btn_rm = ctk.CTkButton(frame, text=self._i18n.t("remove"), width=40, font=Fonts.button(), fg_color=Palette.ERROR, hover_color="#991B1B", command=remove_cb)
        btn_rm.grid(row=0, column=1, padx=10, pady=10)

        def update_labels():
            ent_items.configure(placeholder_text=self._i18n.t("skill_items_ph"))
            btn_rm.configure(text=self._i18n.t("remove"))
            
        frame.update_labels = update_labels

        def get_data() -> Tuple[str, str]:
            items_str = ent_items.get().strip()
            return ("", items_str)
            
        frame.get_data = get_data
        return frame

    def update_labels(self) -> None:
        self.entry_list.update_labels(self._i18n.t("add_skill"))

    def get_data(self) -> List[Tuple[str, str]]:
        return self.entry_list.get_data()
