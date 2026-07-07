"""
entry_list.py — Dynamic List Builder Widget (OCP / DIP)
=========================================================
Manages a list of dynamic sub-forms (e.g. Work Experience blocks).
"""
from __future__ import annotations

import customtkinter as ctk
from typing import List, Callable, Any

from gui.theme import Palette, Fonts


class EntryList(ctk.CTkFrame):
    """
    A dynamic list widget that manages multiple child forms (ItemFactory).
    """

    def __init__(
            self,
            parent: ctk.CTkFrame,
            add_button_text: str,
            item_factory: Callable[[ctk.CTkFrame, Callable[[], None]], ctk.CTkFrame]
    ) -> None:
        super().__init__(parent, fg_color="transparent")
        self._add_text = add_button_text
        self._factory = item_factory
        self._items: List[ctk.CTkFrame] = []

        # Container for the dynamic items
        self._container = ctk.CTkFrame(self, fg_color="transparent")
        self._container.pack(fill="x", expand=True, pady=(0, 15))

        # Add new item button
        self._btn_add = ctk.CTkButton(
            self,
            text=add_button_text,
            font=Fonts.button(),
            fg_color=Palette.SURFACE2,
            hover_color=Palette.BORDER,
            text_color=Palette.ACCENT_LIGHT,
            border_width=1,
            border_color=Palette.BORDER,
            command=self._on_add
        )
        self._btn_add.pack(anchor="w")

    def update_labels(self, add_button_text: str) -> None:
        self._add_text = add_button_text
        self._btn_add.configure(text=add_button_text)
        for item in self._items:
            if hasattr(item, "update_labels"):
                item.update_labels()

    def get_data(self) -> List[Any]:
        """Collects data from all child forms."""
        return [item.get_data() for item in self._items]

    def _on_add(self) -> None:
        """Instantiates a new form using the injected factory."""
        item = self._factory(self._container, lambda: self._on_remove(item))
        item.pack(fill="x", pady=(0, 15))
        self._items.append(item)

    def _on_remove(self, item: ctk.CTkFrame) -> None:
        """Destroys an item and removes it from the list."""
        item.destroy()
        self._items.remove(item)
