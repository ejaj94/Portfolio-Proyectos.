"""
education_tab.py — Education & Certificates Tab  (SRP)
=======================================================
Two sections: degree entries + free-text certificates list.
"""
from __future__ import annotations

import os
import customtkinter as ctk
from tkinter import filedialog
from typing import Dict, Any, List

from gui.components.entry_list import EntryList
from gui.components.date_picker import DateRangeField
from gui.theme import Palette, Fonts
from services.i18n import I18nService

class EducationTab(ctk.CTkScrollableFrame):
    def __init__(self, parent: ctk.CTkFrame, i18n: I18nService) -> None:
        super().__init__(parent, fg_color="transparent")
        self._i18n = i18n
        
        # Degrees
        self._lbl_edu = ctk.CTkLabel(self, text=self._i18n.t("edu_heading"), font=Fonts.heading(), text_color=Palette.TEXT)
        self._lbl_edu.pack(anchor="w", pady=(10, 10))
        
        self.entry_list = EntryList(self, self._i18n.t("add_edu"), self._create_item)
        self.entry_list.pack(fill="x")

        # Certificates
        self._lbl_cert = ctk.CTkLabel(self, text=self._i18n.t("cert_heading"), font=Fonts.heading(), text_color=Palette.TEXT)
        self._lbl_cert.pack(anchor="w", pady=(20, 10))
        
        self._cert_paths = []
        
        self.btn_add_cert = ctk.CTkButton(
            self, text="+ Upload PDFs", font=Fonts.button(), fg_color=Palette.ACCENT, hover_color=Palette.ACCENT_HOVER,
            command=self._select_pdfs
        )
        self.btn_add_cert.pack(anchor="w", pady=(0, 10))
        
        self._lbl_cert_files = ctk.CTkLabel(self, text="Ningún archivo seleccionado", font=Fonts.label(), text_color=Palette.TEXT_MUTED, justify="left")
        self._lbl_cert_files.pack(anchor="w", pady=(0, 20))

    def _create_item(self, parent: ctk.CTkFrame, remove_cb) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(parent, fg_color=Palette.SURFACE, corner_radius=12, border_width=1, border_color=Palette.BORDER)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        fields = [
            ("degree", "edu_degree"),
            ("school", "edu_school"),
            ("dates", "edu_dates")
        ]
        
        entries = {}
        lbls = []
        for idx, (key, lang_key) in enumerate(fields):
            lbl = ctk.CTkLabel(frame, text=self._i18n.t(lang_key), font=Fonts.label_bold(), text_color=Palette.TEXT)
            lbl.grid(row=idx*2, column=0, columnspan=2, sticky="w", padx=15, pady=(10 if idx==0 else 5, 0))
            lbls.append((lbl, lang_key))
            
            if key == "dates":
                entry = DateRangeField(frame, self._i18n, current_label_key="date_current_edu")
                entry.grid(row=idx*2+1, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 5))
            else:
                entry = ctk.CTkEntry(frame, font=Fonts.label(), fg_color=Palette.ENTRY_BG, border_color=Palette.BORDER, height=36)
                entry.grid(row=idx*2+1, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 5))
            entries[key] = entry

        # Remove button
        btn_rm = ctk.CTkButton(
            frame, text=self._i18n.t("remove"), 
            font=Fonts.button(), fg_color=Palette.ERROR, hover_color="#991B1B", 
            command=remove_cb, width=100
        )
        btn_rm.grid(row=6, column=1, sticky="e", padx=15, pady=(10, 15))

        def update_labels():
            for l, l_k in lbls:
                l.configure(text=self._i18n.t(l_k))
            btn_rm.configure(text=self._i18n.t("remove"))
            if "dates" in entries and hasattr(entries["dates"], "update_labels"):
                entries["dates"].update_labels()
        
        frame.update_labels = update_labels

        def get_data() -> Dict[str, str]:
            return {
                "degree": entries["degree"].get().strip(),
                "school": entries["school"].get().strip(),
                "date": entries["dates"].get_data().strip()
            }
            
        frame.get_data = get_data
        return frame

    def _select_pdfs(self):
        paths = filedialog.askopenfilenames(
            title="Seleccionar Certificados (PDF)",
            filetypes=[("PDF files", "*.pdf")]
        )
        if paths:
            self._cert_paths = list(paths)
            filenames = [os.path.basename(p) for p in self._cert_paths]
            self._lbl_cert_files.configure(text="\n".join(filenames))

    def update_labels(self) -> None:
        self._lbl_edu.configure(text=self._i18n.t("edu_heading"))
        self._lbl_cert.configure(text=self._i18n.t("cert_heading"))
        self.entry_list.update_labels(self._i18n.t("add_edu"))

    def get_data(self) -> Dict[str, Any]:
        return {
            "degrees": self.entry_list.get_data(),
            "certificates": self._cert_paths
        }
