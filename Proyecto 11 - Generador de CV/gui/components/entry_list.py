"""
entry_list.py — Reusable Dynamic List Widget  (SRP / OCP)
===========================================================
A scrollable container that lets users add/remove structured entries
(e.g. work experience, education).  The fields for each entry are
passed in at construction time → fully reusable, no duplication.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Dict, List, Tuple

from gui.theme import Palette, Fonts, Spacing


class EntryCard(tk.Frame):
    """
    A single data-entry card inside an EntryList.
    Renders one row of fields + a Remove button.
    """

    def __init__(
        self,
        parent: tk.Widget,
        fields: List[Tuple[str, str]],   # [(field_key, label_text), ...]
        on_remove: Callable[[], None],
        remove_label: str = "− Remove",
    ) -> None:
        super().__init__(parent, bg=Palette.SURFACE2,
                         highlightbackground=Palette.BORDER,
                         highlightthickness=1)

        self._vars: Dict[str, tk.StringVar] = {}

        # ── Fields ────────────────────────────────────────────────────────────
        fields_frame = tk.Frame(self, bg=Palette.SURFACE2)
        fields_frame.pack(fill="x", padx=Spacing.PAD_MD, pady=(Spacing.PAD_SM, 0))

        for key, label_text in fields:
            row = tk.Frame(fields_frame, bg=Palette.SURFACE2)
            row.pack(fill="x", pady=Spacing.PAD_XS)

            tk.Label(row, text=label_text, font=Fonts.LABEL_BOLD,
                     bg=Palette.SURFACE2, fg=Palette.ACCENT_LIGHT,
                     width=18, anchor="w").pack(side="left", padx=(0, 8))

            var = tk.StringVar()
            self._vars[key] = var

            # Multi-line fields use a Text widget, single-line use Entry
            if key.endswith("_bullets") or key.endswith("_text"):
                txt = tk.Text(row, height=3,
                              bg=Palette.ENTRY_BG, fg=Palette.ENTRY_FG,
                              insertbackground=Palette.ACCENT_LIGHT,
                              font=Fonts.ENTRY, relief="flat",
                              highlightbackground=Palette.BORDER,
                              highlightthickness=1, bd=0,
                              wrap="word", padx=6, pady=4)
                txt.pack(fill="x", expand=True)
                # Bind Text content to the StringVar via a helper
                self._vars[key] = txt   # type: ignore[assignment]
            else:
                entry = ttk.Entry(row, textvariable=var, style="TEntry")
                entry.pack(fill="x", expand=True, ipady=2)

        # ── Remove button ─────────────────────────────────────────────────────
        btn_row = tk.Frame(self, bg=Palette.SURFACE2)
        btn_row.pack(fill="x", padx=Spacing.PAD_MD,
                     pady=(Spacing.PAD_XS, Spacing.PAD_SM))

        ttk.Button(btn_row, text=remove_label, style="Danger.TButton",
                   command=on_remove).pack(side="right")

        ttk.Separator(self, orient="horizontal").pack(
            fill="x", padx=Spacing.PAD_MD, pady=(0, Spacing.PAD_XS))

    # ── Public API ────────────────────────────────────────────────────────────
    def get_data(self) -> Dict[str, Any]:
        """Return current field values as a plain dict."""
        result = {}
        for key, var in self._vars.items():
            if isinstance(var, tk.Text):
                result[key] = var.get("1.0", "end-1c").strip()
            else:
                result[key] = var.get().strip()
        return result

    def set_data(self, data: Dict[str, Any]) -> None:
        """Populate fields from a dict (e.g. for loading saved data)."""
        for key, var in self._vars.items():
            value = data.get(key, "")
            if isinstance(var, tk.Text):
                var.delete("1.0", "end")
                var.insert("1.0", value)
            else:
                var.set(str(value))


class EntryList(tk.Frame):
    """
    Scrollable list of EntryCards with Add/Remove functionality.

    Parameters
    ----------
    parent          : parent widget
    fields          : list of (field_key, label_text) tuples for each card
    add_label       : text for the Add button
    remove_label    : text for each card's Remove button
    """

    def __init__(
        self,
        parent: tk.Widget,
        fields: List[Tuple[str, str]],
        add_label: str = "+ Add",
        remove_label: str = "− Remove",
    ) -> None:
        super().__init__(parent, bg=Palette.SURFACE)
        self._fields = fields
        self._remove_label = remove_label
        self._cards: List[EntryCard] = []

        # ── Add button ────────────────────────────────────────────────────────
        btn_bar = tk.Frame(self, bg=Palette.SURFACE)
        btn_bar.pack(fill="x", pady=(0, Spacing.PAD_SM))
        self._add_btn = ttk.Button(btn_bar, text=add_label,
                                   style="Secondary.TButton",
                                   command=self._add_card)
        self._add_btn.pack(side="left")

        # ── Scrollable canvas ─────────────────────────────────────────────────
        canvas_frame = tk.Frame(self, bg=Palette.SURFACE)
        canvas_frame.pack(fill="both", expand=True)

        self._canvas = tk.Canvas(canvas_frame, bg=Palette.SURFACE,
                                 highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical",
                                  command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self._scroll_frame = tk.Frame(self._canvas, bg=Palette.SURFACE)
        self._window = self._canvas.create_window(
            (0, 0), window=self._scroll_frame, anchor="nw")

        self._scroll_frame.bind("<Configure>", self._on_frame_configure)
        self._canvas.bind("<Configure>", self._on_canvas_configure)
        self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    # ── Event handlers ────────────────────────────────────────────────────────
    def _on_frame_configure(self, _event: tk.Event) -> None:
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_configure(self, event: tk.Event) -> None:
        self._canvas.itemconfig(self._window, width=event.width)

    def _on_mousewheel(self, event: tk.Event) -> None:
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ── Card management ───────────────────────────────────────────────────────
    def _add_card(self) -> None:
        card = EntryCard(
            self._scroll_frame,
            fields=self._fields,
            on_remove=lambda c=None: self._remove_card(len(self._cards) - 1),
            remove_label=self._remove_label,
        )
        card.pack(fill="x", padx=Spacing.PAD_SM,
                  pady=(0, Spacing.PAD_SM))
        self._cards.append(card)
        # Fix remove callback to capture correct index
        card._vars  # trigger layout
        self._rebind_remove_buttons()

    def _remove_card(self, index: int) -> None:
        if 0 <= index < len(self._cards):
            self._cards[index].destroy()
            self._cards.pop(index)
            self._rebind_remove_buttons()

    def _rebind_remove_buttons(self) -> None:
        """Rebind remove callbacks so each card removes itself."""
        for i, card in enumerate(self._cards):
            idx = i   # capture
            # Find the Danger button inside the card
            for child in card.winfo_children():
                if isinstance(child, tk.Frame):
                    for widget in child.winfo_children():
                        if isinstance(widget, ttk.Button):
                            widget.configure(command=lambda i=idx: self._remove_card(i))

    # ── Public API ────────────────────────────────────────────────────────────
    def update_labels(self, add_label: str, remove_label: str) -> None:
        """Live-update button labels on language change."""
        self._add_btn.configure(text=add_label)
        self._remove_label = remove_label

    def get_all_data(self) -> List[Dict[str, Any]]:
        """Return list of dicts, one per card."""
        return [card.get_data() for card in self._cards]

    def clear(self) -> None:
        for card in list(self._cards):
            card.destroy()
        self._cards.clear()
