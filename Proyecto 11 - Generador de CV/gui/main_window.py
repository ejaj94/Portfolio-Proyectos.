"""
main_window.py — Application Orchestrator for CustomTkinter
=============================================================
Builds the top-level window, wires all components together and
delegates each concern to the appropriate service / widget.
"""
from __future__ import annotations

import os
import threading
from typing import Dict, Any, Type

import customtkinter as ctk

from core.models import CVContentProvider
from services.i18n import I18nService
from services.cv_service import CVGenerationService
from services.i18n import I18nService
from languages.dynamic import DynamicCVContent

# UI Components
from gui.theme import apply_theme, Palette, Fonts
from gui.tabs.personal_tab import PersonalTab
from gui.tabs.profile_tab import ProfileTab
from gui.tabs.experience_tab import ExperienceTab
from gui.tabs.skills_tab import SkillsTab
from gui.tabs.education_tab import EducationTab
from gui.tabs.languages_tab import LanguagesTab


class MainWindow(ctk.CTk):
    """
    Main Application Window.
    Follows DIP: Depends on abstractions (I18nProvider, CVContentProvider)
    rather than concretions where possible.
    """

    def __init__(self, i18n_svc: I18nService, cv_svc: CVGenerationService) -> None:
        super().__init__()

        self._i18n = i18n_svc
        self._cv_svc = cv_svc
        self._tabs: Dict[str, ctk.CTkFrame] = {}
        self._current_tab: str = "personal"

        # Window Setup
        self.title(self._i18n.t("window_title"))
        self.geometry("1100x700")
        self.minsize(900, 600)
        apply_theme()

        # Grid Layout: Sidebar (0) | Main Content (1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._build_sidebar()
        self._build_main_area()
        
        # Select first tab
        self._select_tab("personal")

    def _build_sidebar(self) -> None:
        """Creates the left navigation sidebar."""
        self.sidebar_frame = ctk.CTkFrame(self, fg_color=Palette.SURFACE, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1) # Spacer

        # Logo / Title
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="CV Maker", font=Fonts.title(), text_color=Palette.ACCENT)
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        # Navigation Buttons
        self.nav_buttons = {}
        nav_items = [
            ("personal", "tab_personal"),
            ("profile", "tab_profile"),
            ("experience", "tab_experience"),
            ("skills", "tab_skills"),
            ("education", "tab_education"),
            ("languages", "tab_languages")
        ]

        for i, (key, lang_key) in enumerate(nav_items):
            btn = ctk.CTkButton(
                self.sidebar_frame, 
                text=self._i18n.t(lang_key),
                font=Fonts.sidebar_btn(),
                fg_color="transparent",
                text_color=Palette.TEXT_MUTED,
                hover_color=Palette.SURFACE2,
                anchor="w",
                command=lambda k=key: self._select_tab(k)
            )
            btn.grid(row=i+1, column=0, padx=10, pady=5, sticky="ew")
            self.nav_buttons[key] = btn

        # Language switcher
        self.lang_var = ctk.StringVar(value=self._i18n.language.upper())
        self.lang_menu = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["ES", "EN", "PT"],
            command=self._on_language_change,
            font=Fonts.label_bold(),
            fg_color=Palette.ENTRY_BG,
            button_color=Palette.ACCENT,
            button_hover_color=Palette.ACCENT_HOVER
        )
        self.lang_menu.set(self.lang_var.get())
        self.lang_menu.grid(row=9, column=0, padx=20, pady=(10, 10), sticky="ew")

        # Generate Button
        self.btn_generate = ctk.CTkButton(
            self.sidebar_frame,
            text=self._i18n.t("btn_generate"),
            font=Fonts.button(),
            fg_color=Palette.ACCENT,
            hover_color=Palette.ACCENT_HOVER,
            command=self._on_generate
        )
        self.btn_generate.grid(row=10, column=0, padx=20, pady=(10, 20), sticky="ew")

    def _build_main_area(self) -> None:
        """Creates the central content area with a log bar at the bottom."""
        self.main_frame = ctk.CTkFrame(self, fg_color=Palette.BG, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Tab Container
        self.tab_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.tab_container.grid(row=0, column=0, sticky="nsew")
        self.tab_container.grid_rowconfigure(0, weight=1)
        self.tab_container.grid_columnconfigure(0, weight=1)

        # Initialize all tabs
        self._tabs["personal"] = PersonalTab(self.tab_container, self._i18n)
        self._tabs["profile"] = ProfileTab(self.tab_container, self._i18n)
        self._tabs["experience"] = ExperienceTab(self.tab_container, self._i18n)
        self._tabs["skills"] = SkillsTab(self.tab_container, self._i18n)
        self._tabs["education"] = EducationTab(self.tab_container, self._i18n)
        self._tabs["languages"] = LanguagesTab(self.tab_container, self._i18n)

        # Log Bar
        self.log_lbl = ctk.CTkLabel(
            self.main_frame, 
            text="Listo.", 
            font=Fonts.label(), 
            text_color=Palette.TEXT_MUTED,
            anchor="w"
        )
        self.log_lbl.grid(row=1, column=0, sticky="ew", pady=(10, 0))

    def _select_tab(self, tab_key: str) -> None:
        """Switches the visible tab and updates button styles."""
        # Hide current
        if self._current_tab in self._tabs:
            self._tabs[self._current_tab].grid_forget()
            self.nav_buttons[self._current_tab].configure(fg_color="transparent", text_color=Palette.TEXT_MUTED)
        
        # Show new
        self._current_tab = tab_key
        self._tabs[tab_key].grid(row=0, column=0, sticky="nsew")
        self.nav_buttons[tab_key].configure(fg_color=Palette.ACCENT, text_color=Palette.TEXT)

    def _on_language_change(self, code: str) -> None:
        self._i18n.set_language(code.lower())
        self._update_all_labels()
        self._log(f"Language changed to {code}", level="success")

    def _update_all_labels(self) -> None:
        self.title(self._i18n.t("app_title"))
        self.btn_generate.configure(text=self._i18n.t("btn_generate"))
        
        nav_keys = ["tab_personal", "tab_profile", "tab_experience", "tab_skills", "tab_education", "tab_languages"]
        for key, lang_key in zip(self.nav_buttons.keys(), nav_keys):
            self.nav_buttons[key].configure(text=self._i18n.t(lang_key))

        for tab in self._tabs.values():
            if hasattr(tab, "update_labels"):
                tab.update_labels()

    def _log(self, message: str, level: str = "info") -> None:
        color = Palette.TEXT_MUTED
        if level == "error": color = Palette.ERROR
        elif level == "success": color = Palette.SUCCESS
        self.log_lbl.configure(text=message, text_color=color)

    def _on_generate(self) -> None:
        # 1. Collect Data
        raw_data = {
            "personal": self._tabs["personal"].get_data(),
            "profile": self._tabs["profile"].get_data(),
            "experience": self._tabs["experience"].get_data(),
            "skills": self._tabs["skills"].get_data(),
            "education": self._tabs["education"].get_data(),
            "languages": self._tabs["languages"].get_data(),
            "output_lang": self.lang_menu.get().lower()
        }

        # 2. Validation: All fields must be filled
        personal = raw_data["personal"]
        for key, val in personal.items():
            if key != "photo" and not val:
                self._log("Todos los campos de Información Personal son obligatorios", "error")
                return
                
        if not raw_data["profile"]:
            self._log("El Perfil Profesional es obligatorio", "error")
            return
            
        for exp in raw_data["experience"]:
            if not exp.get("title") or not exp.get("company") or not exp.get("date"):
                self._log("Completa todos los campos en cada Experiencia", "error")
                return
                
        for edu in raw_data["education"].get("degrees", []):
            if not edu.get("degree") or not edu.get("school") or not edu.get("date"):
                self._log("Completa todos los campos en cada Educación", "error")
                return
                
        for skill in raw_data["skills"]:
            if not skill[1]:
                self._log("No dejes habilidades vacías", "error")
                return

        # 3. Create Provider
        provider: CVContentProvider = DynamicCVContent(raw_data)

        # 4. Generate Async
        self.btn_generate.configure(state="disabled")
        self._log("Generando PDF...", "info")

        def worker() -> None:
            try:
                out_dir = os.path.join(os.path.expanduser("~"), "Desktop")
                photo_path = raw_data["personal"].get("photo")
                
                result = self._cv_svc.generate(raw_data, photo_path, out_dir)
                if result.success:
                    self.after(0, lambda: self._on_generation_success(result.output_path))
                else:
                    self.after(0, lambda: self._on_generation_error(Exception(result.message)))
            except Exception as e:
                self.after(0, lambda err=e: self._on_generation_error(err))

        threading.Thread(target=worker, daemon=True).start()

    def _on_generation_success(self, path: str) -> None:
        self.btn_generate.configure(state="normal")
        self._log(f"✅ ¡CV generado exitosamente! -> {path}", "success")

    def _on_generation_error(self, err: Exception) -> None:
        self.btn_generate.configure(state="normal")
        self._log(f"Error: {err}", "error")
