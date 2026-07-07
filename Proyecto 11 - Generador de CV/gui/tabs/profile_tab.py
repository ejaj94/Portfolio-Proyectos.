"""
profile_tab.py — Professional Profile Tab  (SRP)
=================================================
Free-text area for the professional summary paragraph.
"""
from __future__ import annotations

import customtkinter as ctk
from gui.theme import Palette, Fonts
from services.i18n import I18nService

class ProfileTab(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, i18n: I18nService) -> None:
        super().__init__(parent, fg_color="transparent")
        self._i18n = i18n

        self._lbl = ctk.CTkLabel(
            self, 
            text=self._i18n.t("lbl_profile_text"), 
            font=Fonts.heading(), 
            text_color=Palette.TEXT
        )
        self._lbl.pack(anchor="w", pady=(10, 5))

        self._tip = ctk.CTkLabel(
            self, 
            text=self._i18n.t("ph_profile"), 
            font=Fonts.label(), 
            text_color=Palette.TEXT_MUTED
        )
        self._tip.pack(anchor="w", pady=(0, 15))

        self._text = ctk.CTkTextbox(
            self,
            font=Fonts.label(),
            fg_color=Palette.ENTRY_BG,
            border_color=Palette.BORDER,
            border_width=1,
            corner_radius=8
        )
        self._text.pack(fill="both", expand=True)

    def update_labels(self) -> None:
        self._lbl.configure(text=self._i18n.t("lbl_profile_text"))
        self._tip.configure(text=self._i18n.t("ph_profile"))

    def get_data(self) -> str:
        return self._text.get("1.0", "end-1c").strip()
