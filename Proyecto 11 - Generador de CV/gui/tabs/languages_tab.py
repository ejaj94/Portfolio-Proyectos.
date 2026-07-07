"""
languages_tab.py — Languages Tab  (SRP)
========================================
Simple two-column list: language name + proficiency level.
"""
from __future__ import annotations

import customtkinter as ctk
from typing import List, Tuple

from gui.components.entry_list import EntryList
from gui.theme import Palette, Fonts
from services.i18n import I18nService

class LanguagesTab(ctk.CTkScrollableFrame):
    def __init__(self, parent: ctk.CTkFrame, i18n: I18nService) -> None:
        super().__init__(parent, fg_color="transparent")
        self._i18n = i18n
        self.entry_list = EntryList(self, self._i18n.t("add_lang"), self._create_item)
        self.entry_list.pack(fill="both", expand=True)

    def _create_item(self, parent: ctk.CTkFrame, remove_cb) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(parent, fg_color=Palette.SURFACE, corner_radius=8)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        LANGUAGES = self._i18n.t("lang_options").split(",")
        LEVELS = self._i18n.t("lang_levels").split(",")

        lang_var = ctk.StringVar(value=LANGUAGES[0])
        opt_lang = ctk.CTkOptionMenu(frame, values=LANGUAGES, variable=lang_var, font=Fonts.label(), fg_color=Palette.ENTRY_BG, button_color=Palette.SURFACE2, button_hover_color=Palette.ACCENT_HOVER, text_color=Palette.TEXT)
        opt_lang.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        level_var = ctk.StringVar(value=LEVELS[0])
        opt_level = ctk.CTkOptionMenu(frame, values=LEVELS, variable=level_var, font=Fonts.label(), fg_color=Palette.ENTRY_BG, button_color=Palette.SURFACE2, button_hover_color=Palette.ACCENT_HOVER, text_color=Palette.TEXT)
        opt_level.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        btn_rm = ctk.CTkButton(frame, text="X", width=40, font=Fonts.button(), fg_color=Palette.ERROR, hover_color="#991B1B", command=remove_cb)
        btn_rm.grid(row=0, column=2, padx=10, pady=10)

        def get_data() -> Tuple[str, str]:
            return (lang_var.get(), level_var.get())
            
        frame.get_data = get_data
        return frame

    def update_labels(self) -> None:
        self.entry_list.update_labels(self._i18n.t("add_lang"))

    def get_data(self) -> List[Tuple[str, str]]:
        return self.entry_list.get_data()
