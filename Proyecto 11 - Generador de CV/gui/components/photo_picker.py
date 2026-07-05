"""
photo_picker.py — Photo Picker & Preview Widget  (SRP)
=======================================================
Encapsulates all photo-picking logic: file dialog, image loading,
thumbnail generation and preview rendering.  The rest of the UI
only calls get_photo_path() to retrieve the selected file.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, ttk
from typing import Optional

try:
    from PIL import Image, ImageTk, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from gui.theme import Palette, Fonts, Spacing


class PhotoPicker(tk.Frame):
    """
    Self-contained widget that shows a circular avatar preview and
    a button to pick a new photo from the filesystem.
    """

    THUMB_SIZE = (110, 110)

    def __init__(self, parent: tk.Widget, pick_label: str = "📷  Choose Photo",
                 no_photo_label: str = "No photo selected") -> None:
        super().__init__(parent, bg=Palette.SURFACE)

        self._photo_path: Optional[str] = None
        self._tk_image: Optional[ImageTk.PhotoImage] = None  # type: ignore[name-defined]
        self._pick_label = pick_label
        self._no_photo_label = no_photo_label

        self._build()

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build(self) -> None:
        # Canvas for circular avatar
        self._canvas = tk.Canvas(self, width=self.THUMB_SIZE[0] + 10,
                                 height=self.THUMB_SIZE[1] + 10,
                                 bg=Palette.SURFACE, highlightthickness=0)
        self._canvas.pack(pady=(0, Spacing.PAD_SM))
        self._draw_placeholder()

        # Status label
        self._status_lbl = tk.Label(self, text=self._no_photo_label,
                                    font=Fonts.LABEL, bg=Palette.SURFACE,
                                    fg=Palette.TEXT_MUTED,
                                    wraplength=160, justify="center")
        self._status_lbl.pack()

        # Pick button
        self._btn = ttk.Button(self, text=self._pick_label,
                               style="Secondary.TButton",
                               command=self._pick_photo)
        self._btn.pack(pady=(Spacing.PAD_SM, 0))

    # ── Private helpers ───────────────────────────────────────────────────────
    def _draw_placeholder(self) -> None:
        cx = cy = self.THUMB_SIZE[0] // 2 + 5
        r = self.THUMB_SIZE[0] // 2
        self._canvas.delete("all")
        self._canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                 fill=Palette.SURFACE2,
                                 outline=Palette.ACCENT, width=2)
        self._canvas.create_text(cx, cy, text="👤",
                                 font=(Fonts.FAMILY, 30),
                                 fill=Palette.TEXT_DIM)

    def _render_photo(self, path: str) -> None:
        if not PIL_AVAILABLE:
            self._status_lbl.configure(
                text="Install Pillow for photo preview.\npip install pillow",
                fg=Palette.WARNING)
            return

        try:
            img = Image.open(path).convert("RGBA")
            img.thumbnail(self.THUMB_SIZE, Image.LANCZOS)

            # Create circular mask
            mask = Image.new("L", img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, *img.size), fill=255)

            circular = Image.new("RGBA", img.size, (0, 0, 0, 0))
            circular.paste(img, mask=mask)

            self._tk_image = ImageTk.PhotoImage(circular)
            cx = cy = self.THUMB_SIZE[0] // 2 + 5
            r = self.THUMB_SIZE[0] // 2
            self._canvas.delete("all")
            self._canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                     fill=Palette.SURFACE2,
                                     outline=Palette.ACCENT, width=2)
            self._canvas.create_image(cx, cy, image=self._tk_image)
        except Exception as exc:
            self._status_lbl.configure(
                text=f"Preview error: {exc}", fg=Palette.ERROR)

    def _pick_photo(self) -> None:
        path = filedialog.askopenfilename(
            title="Select profile photo",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif"),
                       ("All files", "*.*")]
        )
        if path:
            self._photo_path = path
            short = path.split("/")[-1].split("\\")[-1]
            self._status_lbl.configure(text=short, fg=Palette.SUCCESS)
            self._render_photo(path)

    # ── Public API ────────────────────────────────────────────────────────────
    def get_photo_path(self) -> Optional[str]:
        return self._photo_path

    def update_labels(self, pick_label: str, no_photo_label: str) -> None:
        self._pick_label = pick_label
        self._no_photo_label = no_photo_label
        self._btn.configure(text=pick_label)
        if not self._photo_path:
            self._status_lbl.configure(text=no_photo_label)
