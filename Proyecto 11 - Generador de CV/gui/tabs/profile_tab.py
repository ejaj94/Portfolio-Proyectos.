"""
profile_tab.py — Professional Profile Tab  (SRP)
=================================================
Free-text area for the professional summary paragraph.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from gui.theme import Palette, Fonts, Spacing
from services.i18n import I18nService


class ProfileTab(tk.Frame):

    def __init__(self, parent: tk.Widget, i18n: I18nService) -> None:
        super().__init__(parent, bg=Palette.SURFACE)
        self._i18n = i18n
        self._build()

    def _build(self) -> None:
        container = tk.Frame(self, bg=Palette.SURFACE)
        container.pack(fill="both", expand=True,
                       padx=Spacing.PAD_LG, pady=Spacing.PAD_LG)

        self._lbl = tk.Label(container,
                             text=self._i18n.t("lbl_profile_text"),
                             font=Fonts.HEADING,
                             bg=Palette.SURFACE, fg=Palette.TEXT)
        self._lbl.pack(anchor="w", pady=(0, Spacing.PAD_SM))

        # Scrollable text area
        txt_frame = tk.Frame(container, bg=Palette.BORDER, bd=1)
        txt_frame.pack(fill="both", expand=True)

        self._text = tk.Text(
            txt_frame,
            bg=Palette.ENTRY_BG, fg=Palette.ENTRY_FG,
            insertbackground=Palette.ACCENT_LIGHT,
            font=Fonts.ENTRY, relief="flat",
            wrap="word", padx=10, pady=8,
            highlightthickness=0,
        )
        scroll = ttk.Scrollbar(txt_frame, orient="vertical",
                               command=self._text.yview)
        self._text.configure(yscrollcommand=scroll.set)

        scroll.pack(side="right", fill="y")
        self._text.pack(side="left", fill="both", expand=True)

        # Tip label
        self._tip = tk.Label(container,
                             text=self._i18n.t("ph_profile"),
                             font=(Fonts.FAMILY, 9, "italic"),
                             bg=Palette.SURFACE, fg=Palette.TEXT_DIM,
                             wraplength=500, justify="left")
        self._tip.pack(anchor="w", pady=(Spacing.PAD_SM, 0))

    def refresh_labels(self) -> None:
        self._lbl.configure(text=self._i18n.t("lbl_profile_text"))
        self._tip.configure(text=self._i18n.t("ph_profile"))

    def get_data(self) -> str:
        return self._text.get("1.0", "end-1c").strip()
