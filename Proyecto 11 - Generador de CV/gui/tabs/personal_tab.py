"""
personal_tab.py — Personal Information Tab  (SRP)
==================================================
Collects name, title, contact details and social links.
"""
from __future__ import annotations

import customtkinter as ctk
from typing import Dict, Any

from gui.components.photo_picker import PhotoPicker
from gui.theme import Palette, Fonts
from services.i18n import I18nService


class PersonalTab(ctk.CTkScrollableFrame):
    def __init__(self, parent: ctk.CTkFrame, i18n: I18nService) -> None:
        super().__init__(parent, fg_color="transparent")
        self._i18n = i18n
        self._entries: Dict[str, ctk.CTkEntry] = {}

        # Two-column layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Photo Picker (Top center)
        photo_frame = ctk.CTkFrame(self, fg_color="transparent")
        photo_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        self.photo_picker = PhotoPicker(
            photo_frame,
            self._i18n.t("btn_photo"),
            self._i18n.t("lbl_no_photo")
        )
        self.photo_picker.pack()

        # Fields definitions
        self._fields = [
            ("name", "lbl_full_name"),
            ("title", "lbl_job_title"),
            ("email", "lbl_email"),
            ("phone", "lbl_phone"),
            ("location", "lbl_address"),
            ("linkedin", "lbl_linkedin"),
            ("github", "lbl_github")
        ]

        row = 1
        col = 0
        for key, lang_key in self._fields:
            lbl = ctk.CTkLabel(self, text=self._i18n.t(lang_key), font=Fonts.label_bold(), text_color=Palette.TEXT)
            lbl.grid(row=row, column=col, sticky="w", padx=10, pady=(10, 0))
            # Store label reference for dynamic updates
            setattr(self, f"lbl_{key}", lbl)

            entry = ctk.CTkEntry(
                self, 
                font=Fonts.label(), 
                fg_color=Palette.ENTRY_BG, 
                border_color=Palette.BORDER,
                height=36,
                corner_radius=8
            )
            entry.grid(row=row+1, column=col, sticky="ew", padx=10, pady=(5, 10))
            self._entries[key] = entry

            col += 1
            if col > 1:
                col = 0
                row += 2

    def update_labels(self) -> None:
        self.photo_picker.update_labels(
            self._i18n.t("btn_photo"),
            self._i18n.t("lbl_no_photo")
        )
        for key, lang_key in self._fields:
            lbl: ctk.CTkLabel = getattr(self, f"lbl_{key}")
            lbl.configure(text=self._i18n.t(lang_key))

    def get_data(self) -> Dict[str, Any]:
        data = {k: v.get().strip() for k, v in self._entries.items()}
        data["photo"] = self.photo_picker.get_photo_path()
        return data
