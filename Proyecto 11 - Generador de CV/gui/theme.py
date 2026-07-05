"""
theme.py — Visual Design System  (SRP)
========================================
Single source of truth for every colour, font size, padding and
widget style used by the application.  No magic numbers anywhere else.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk


# ── Colour Palette (dark-mode, indigo accent) ─────────────────────────────────
class Palette:
    BG          = "#0f0f1a"   # main window background
    SURFACE     = "#1a1a2e"   # card / frame background
    SURFACE2    = "#16213e"   # slightly elevated surface
    BORDER      = "#2a2a4a"   # dividers, borders
    ACCENT      = "#7c3aed"   # indigo-600 — primary action
    ACCENT_HOVER= "#6d28d9"   # indigo-700
    ACCENT_LIGHT= "#a78bfa"   # indigo-300 — secondary text
    SUCCESS     = "#10b981"   # green-500
    ERROR       = "#ef4444"   # red-500
    WARNING     = "#f59e0b"   # amber-500
    TEXT        = "#e2e8f0"   # slate-200 — primary text
    TEXT_MUTED  = "#94a3b8"   # slate-400 — secondary text
    TEXT_DIM    = "#475569"   # slate-600 — placeholder / disabled
    ENTRY_BG    = "#1e1e35"   # text input background
    ENTRY_FG    = "#e2e8f0"
    TAB_ACTIVE  = "#7c3aed"
    TAB_INACTIVE= "#1a1a2e"
    SCROLLBAR   = "#2a2a4a"
    BTN_DANGER  = "#7f1d1d"


# ── Typography ────────────────────────────────────────────────────────────────
class Fonts:
    FAMILY      = "Segoe UI"
    FAMILY_MONO = "Consolas"

    TITLE       = (FAMILY, 22, "bold")
    SUBTITLE    = (FAMILY, 11)
    HEADING     = (FAMILY, 13, "bold")
    LABEL       = (FAMILY, 10)
    LABEL_BOLD  = (FAMILY, 10, "bold")
    ENTRY       = (FAMILY, 10)
    BUTTON      = (FAMILY, 11, "bold")
    BUTTON_SM   = (FAMILY, 9, "bold")
    LOG         = (FAMILY_MONO, 9)
    TAB         = (FAMILY, 10, "bold")


# ── Spacing ────────────────────────────────────────────────────────────────────
class Spacing:
    PAD_LG  = 20
    PAD_MD  = 12
    PAD_SM  = 6
    PAD_XS  = 3
    RADIUS  = 8    # conceptual — used in docs/notes (tk has no border-radius)


# ── ttk Style factory ─────────────────────────────────────────────────────────
def apply_theme(root: tk.Tk) -> ttk.Style:
    """
    Apply the dark-indigo theme to all ttk widgets.
    Returns the configured Style instance.
    """
    style = ttk.Style(root)
    style.theme_use("clam")

    p = Palette
    f = Fonts

    # ── Frame ─────────────────────────────────────────────────────────────────
    style.configure("TFrame",       background=p.SURFACE)
    style.configure("Card.TFrame",  background=p.SURFACE2)
    style.configure("BG.TFrame",    background=p.BG)

    # ── Label ─────────────────────────────────────────────────────────────────
    style.configure("TLabel",
                    background=p.SURFACE, foreground=p.TEXT,
                    font=f.LABEL)
    style.configure("BG.TLabel",
                    background=p.BG,      foreground=p.TEXT,
                    font=f.LABEL)
    style.configure("Heading.TLabel",
                    background=p.SURFACE, foreground=p.TEXT,
                    font=f.HEADING)
    style.configure("Muted.TLabel",
                    background=p.SURFACE, foreground=p.TEXT_MUTED,
                    font=f.LABEL)
    style.configure("Accent.TLabel",
                    background=p.SURFACE, foreground=p.ACCENT_LIGHT,
                    font=f.LABEL_BOLD)
    style.configure("Success.TLabel",
                    background=p.BG,      foreground=p.SUCCESS,
                    font=f.LABEL_BOLD)
    style.configure("Error.TLabel",
                    background=p.BG,      foreground=p.ERROR,
                    font=f.LABEL_BOLD)

    # ── Entry ─────────────────────────────────────────────────────────────────
    style.configure("TEntry",
                    fieldbackground=p.ENTRY_BG,
                    foreground=p.ENTRY_FG,
                    insertcolor=p.ACCENT_LIGHT,
                    bordercolor=p.BORDER,
                    lightcolor=p.BORDER,
                    darkcolor=p.BORDER,
                    relief="flat",
                    font=f.ENTRY,
                    padding=6)
    style.map("TEntry",
              bordercolor=[("focus", p.ACCENT)],
              lightcolor=[("focus", p.ACCENT)],
              darkcolor=[("focus", p.ACCENT)])

    # ── Button — Primary ──────────────────────────────────────────────────────
    style.configure("Primary.TButton",
                    background=p.ACCENT,
                    foreground=p.TEXT,
                    font=f.BUTTON,
                    borderwidth=0,
                    relief="flat",
                    padding=(16, 10))
    style.map("Primary.TButton",
              background=[("active", p.ACCENT_HOVER),
                          ("pressed", p.ACCENT_HOVER)],
              foreground=[("active", p.TEXT)])

    # ── Button — Secondary ────────────────────────────────────────────────────
    style.configure("Secondary.TButton",
                    background=p.SURFACE2,
                    foreground=p.ACCENT_LIGHT,
                    font=f.BUTTON_SM,
                    borderwidth=1,
                    relief="flat",
                    padding=(10, 6))
    style.map("Secondary.TButton",
              background=[("active", p.BORDER)],
              foreground=[("active", p.TEXT)])

    # ── Button — Danger ───────────────────────────────────────────────────────
    style.configure("Danger.TButton",
                    background=p.BTN_DANGER,
                    foreground=p.ERROR,
                    font=f.BUTTON_SM,
                    borderwidth=0,
                    relief="flat",
                    padding=(8, 5))
    style.map("Danger.TButton",
              background=[("active", "#991b1b")])

    # ── Notebook (tabs) ───────────────────────────────────────────────────────
    style.configure("TNotebook",
                    background=p.BG,
                    borderwidth=0,
                    tabmargins=[0, 0, 0, 0])
    style.configure("TNotebook.Tab",
                    background=p.SURFACE2,
                    foreground=p.TEXT_MUTED,
                    font=f.TAB,
                    padding=[14, 8],
                    borderwidth=0)
    style.map("TNotebook.Tab",
              background=[("selected", p.ACCENT)],
              foreground=[("selected", p.TEXT)])

    # ── Scrollbar ─────────────────────────────────────────────────────────────
    style.configure("TScrollbar",
                    background=p.SCROLLBAR,
                    troughcolor=p.SURFACE,
                    borderwidth=0,
                    arrowsize=12)

    # ── Combobox ─────────────────────────────────────────────────────────────
    style.configure("TCombobox",
                    fieldbackground=p.ENTRY_BG,
                    background=p.SURFACE2,
                    foreground=p.ENTRY_FG,
                    selectbackground=p.ACCENT,
                    selectforeground=p.TEXT,
                    bordercolor=p.BORDER,
                    arrowcolor=p.ACCENT_LIGHT,
                    font=f.ENTRY,
                    padding=6)
    style.map("TCombobox",
              fieldbackground=[("readonly", p.ENTRY_BG)],
              foreground=[("readonly", p.ENTRY_FG)])

    # ── Separator ─────────────────────────────────────────────────────────────
    style.configure("TSeparator", background=p.BORDER)

    # ── LabelFrame ────────────────────────────────────────────────────────────
    style.configure("TLabelframe",
                    background=p.SURFACE,
                    bordercolor=p.BORDER,
                    relief="flat")
    style.configure("TLabelframe.Label",
                    background=p.SURFACE,
                    foreground=p.ACCENT_LIGHT,
                    font=f.LABEL_BOLD)

    root.configure(bg=p.BG)
    return style
