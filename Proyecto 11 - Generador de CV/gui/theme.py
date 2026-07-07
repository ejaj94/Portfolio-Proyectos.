"""
theme.py — Visual Design System for CustomTkinter (SRP)
=========================================================
Defines the Dark Neon palette and typography for the UI.
"""
import customtkinter as ctk

class Palette:
    BG          = "#13131A"   # Deep space dark
    SURFACE     = "#1C1C26"   # Elevated card background
    SURFACE2    = "#252533"   # Active/hover states
    BORDER      = "#3A3A4D"   # Subtle borders
    ACCENT      = "#7C3AED"   # Vibrant Indigo
    ACCENT_HOVER= "#6D28D9"   # Indigo hover
    ACCENT_LIGHT= "#A78BFA"   # Indigo light for text
    CYAN        = "#06B6D4"   # Secondary accent
    SUCCESS     = "#10B981"
    ERROR       = "#EF4444"
    TEXT        = "#F8FAFC"   # Primary text
    TEXT_MUTED  = "#94A3B8"   # Secondary text
    ENTRY_BG    = "#16161E"   # Darker input fields

class Fonts:
    FAMILY = "Segoe UI"
    
    @classmethod
    def title(cls) -> tuple: return (cls.FAMILY, 24, "bold")
    
    @classmethod
    def subtitle(cls) -> tuple: return (cls.FAMILY, 14)
    
    @classmethod
    def heading(cls) -> tuple: return (cls.FAMILY, 16, "bold")
    
    @classmethod
    def label(cls) -> tuple: return (cls.FAMILY, 12)
    
    @classmethod
    def label_bold(cls) -> tuple: return (cls.FAMILY, 12, "bold")
    
    @classmethod
    def button(cls) -> tuple: return (cls.FAMILY, 13, "bold")
    
    @classmethod
    def sidebar_btn(cls) -> tuple: return (cls.FAMILY, 14, "bold")

def apply_theme():
    """Initializes global CustomTkinter settings."""
    ctk.set_appearance_mode("dark")
    # We use our own colors mostly, but dark-blue provides good defaults
    ctk.set_default_color_theme("dark-blue")
