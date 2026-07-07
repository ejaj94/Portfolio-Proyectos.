"""
photo_picker.py — Profile Photo Widget (SRP)
==============================================
Uses CustomTkinter for rounded buttons and modern UI.
"""
from __future__ import annotations

import os
import tkinter as tk
from tkinter import filedialog
from typing import Optional

import customtkinter as ctk

try:
    from PIL import Image, ImageTk, ImageDraw
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

from gui.theme import Palette, Fonts


class PhotoPicker(ctk.CTkFrame):

    def __init__(self, parent: ctk.CTkFrame, pick_label: str, no_photo_label: str) -> None:
        super().__init__(parent, fg_color=Palette.SURFACE)
        self._photo_path: Optional[str] = None
        self._photo_img: Optional[ImageTk.PhotoImage] = None

        # Build UI
        self._preview_lbl = ctk.CTkLabel(
            self,
            text=no_photo_label if HAS_PIL else "Pillow no instalado",
            width=120, height=120,
            corner_radius=60,
            fg_color=Palette.ENTRY_BG,
            text_color=Palette.TEXT_MUTED,
            font=Fonts.label()
        )
        self._preview_lbl.pack(pady=(0, 10))

        self._btn = ctk.CTkButton(
            self,
            text=pick_label,
            font=Fonts.button(),
            fg_color=Palette.ACCENT,
            hover_color=Palette.ACCENT_HOVER,
            command=self._on_pick
        )
        self._btn.pack(fill="x")

    def update_labels(self, pick_label: str, no_photo_label: str) -> None:
        self._btn.configure(text=pick_label)
        if not self._photo_path:
            self._preview_lbl.configure(
                text=no_photo_label if HAS_PIL else "Pillow no instalado"
            )

    def get_photo_path(self) -> Optional[str]:
        return self._photo_path

    def _on_pick(self) -> None:
        path = filedialog.askopenfilename(
            title="Seleccionar Foto",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        if path:
            self._photo_path = path
            self._update_preview(path)

    def _update_preview(self, path: str) -> None:
        if not HAS_PIL:
            self._preview_lbl.configure(text=os.path.basename(path))
            return

        try:
            img = Image.open(path).convert("RGBA")
            # Create a circular mask for preview
            size = min(img.size)
            img = img.crop((0, 0, size, size)).resize((120, 120), Image.Resampling.LANCZOS)
            
            mask = Image.new("L", (120, 120), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 120, 120), fill=255)
            
            circular_img = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
            circular_img.paste(img, (0, 0), mask)
            
            ctk_img = ctk.CTkImage(light_image=circular_img, dark_image=circular_img, size=(120, 120))
            self._preview_lbl.configure(image=ctk_img, text="")
            self._photo_img = ctk_img # Keep reference
        except Exception:
            self._preview_lbl.configure(text="Error loading")
