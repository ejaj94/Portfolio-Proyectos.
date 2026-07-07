"""
experience_tab.py — Work Experience Tab  (SRP / OCP)
=====================================================
Delegates dynamic list management to EntryList.
"""
from __future__ import annotations

import customtkinter as ctk
from typing import List, Dict, Any

from gui.components.entry_list import EntryList
from gui.components.date_picker import DateRangeField
from gui.theme import Palette, Fonts
from services.i18n import I18nService

class ExperienceTab(ctk.CTkScrollableFrame):
    def __init__(self, parent: ctk.CTkFrame, i18n: I18nService) -> None:
        super().__init__(parent, fg_color="transparent")
        self._i18n = i18n
        self.entry_list = EntryList(self, self._i18n.t("add_exp"), self._create_item)
        self.entry_list.pack(fill="both", expand=True)

    def _create_item(self, parent: ctk.CTkFrame, remove_cb) -> ctk.CTkFrame:
        # We use a Card for each experience item
        frame = ctk.CTkFrame(parent, fg_color=Palette.SURFACE, corner_radius=12, border_width=1, border_color=Palette.BORDER)
        
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        fields = [
            ("title", "exp_title"),
            ("company", "exp_company"),
            ("dates", "exp_dates")
        ]
        
        entries = {}
        lbls = []
        for idx, (key, lang_key) in enumerate(fields):
            lbl = ctk.CTkLabel(frame, text=self._i18n.t(lang_key), font=Fonts.label_bold(), text_color=Palette.TEXT)
            lbl.grid(row=idx*2, column=0, columnspan=2, sticky="w", padx=15, pady=(10 if idx==0 else 5, 0))
            lbls.append((lbl, lang_key))
            
            if key == "dates":
                entry = DateRangeField(frame, self._i18n)
                entry.grid(row=idx*2+1, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 5))
            else:
                entry = ctk.CTkEntry(frame, font=Fonts.label(), fg_color=Palette.ENTRY_BG, border_color=Palette.BORDER, height=36)
                entry.grid(row=idx*2+1, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 5))
            entries[key] = entry
            
        lbl_desc = ctk.CTkLabel(frame, text=self._i18n.t("exp_desc"), font=Fonts.label_bold(), text_color=Palette.TEXT)
        lbl_desc.grid(row=6, column=0, columnspan=2, sticky="w", padx=15, pady=(5, 0))
        txt_desc = ctk.CTkTextbox(frame, font=Fonts.label(), fg_color=Palette.ENTRY_BG, border_color=Palette.BORDER, border_width=1, height=80)
        txt_desc.grid(row=7, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 10))
        entries["desc"] = txt_desc
        
        btn_rm = ctk.CTkButton(frame, text=self._i18n.t("remove"), width=80, font=Fonts.button(), fg_color=Palette.ERROR, hover_color="#991B1B", command=remove_cb)
        btn_rm.grid(row=8, column=1, sticky="e", padx=15, pady=(0, 15))

        def update_labels():
            for l, l_k in lbls:
                l.configure(text=self._i18n.t(l_k))
            lbl_desc.configure(text=self._i18n.t("exp_desc"))
            btn_rm.configure(text=self._i18n.t("remove"))
            if "dates" in entries and hasattr(entries["dates"], "update_labels"):
                entries["dates"].update_labels()
        
        frame.update_labels = update_labels

        def get_data() -> Dict[str, Any]:
            desc_text = entries["desc"].get("1.0", "end-1c").strip()
            desc_list = [line.lstrip("- *").strip() for line in desc_text.split("\n") if line.strip()]
            return {
                "title": entries["title"].get().strip(),
                "company": entries["company"].get().strip(),
                "date": entries["dates"].get_data().strip(),
                "description": desc_list
            }
            
        frame.get_data = get_data
        
        return frame

    def update_labels(self) -> None:
        self.entry_list.update_labels(self._i18n.t("add_exp"))

    def get_data(self) -> List[Dict[str, Any]]:
        return self.entry_list.get_data()
