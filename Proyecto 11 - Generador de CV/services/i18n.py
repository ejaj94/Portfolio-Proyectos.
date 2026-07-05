"""
i18n.py — UI Internationalisation Service  (SRP / OCP)
========================================================
Provides translated UI strings for the application in
Spanish (es), English (en) and Portuguese (pt).

Usage:
    i18n = I18nService("en")
    label_text = i18n.t("tab_personal")
"""
from __future__ import annotations

from typing import Dict

# ── Translation catalogue ─────────────────────────────────────────────────────
_CATALOGUE: Dict[str, Dict[str, str]] = {
    # ── English ──────────────────────────────────────────────────────────────
    "en": {
        # Window / general
        "app_title":           "CV Generator Pro",
        "app_subtitle":        "Build your professional résumé in seconds",
        "btn_generate":        "⚡  Generate CV",
        "btn_photo":           "📷  Choose Photo",
        "btn_output":          "📁  Output Folder",
        "lbl_output_dir":      "Output folder:",
        "lbl_pdf_lang":        "PDF Language:",
        "lbl_ui_lang":         "Interface Language:",
        "lbl_photo_preview":   "Photo Preview",
        "lbl_no_photo":        "No photo selected",
        "log_ready":           "Ready. Fill in your details and click Generate CV.",
        "log_generating":      "Generating your CV…",
        "log_success":         "✅  CV generated successfully!",
        "log_error":           "❌  Error: {msg}",
        "log_open_folder":     "📂  Open output folder",

        # Tabs
        "tab_personal":        "Personal",
        "tab_profile":         "Profile",
        "tab_experience":      "Experience",
        "tab_skills":          "Skills",
        "tab_education":       "Education",
        "tab_languages":       "Languages",

        # Personal tab
        "lbl_full_name":       "Full Name",
        "lbl_job_title":       "Job Title",
        "lbl_phone":           "Phone",
        "lbl_email":           "E-mail",
        "lbl_address":         "Address",
        "lbl_github":          "GitHub URL",
        "lbl_linkedin":        "LinkedIn URL",

        # Profile tab
        "lbl_profile_text":    "Professional Summary",
        "ph_profile":          "Describe your professional profile in 3-5 sentences…",

        # Experience tab
        "lbl_exp_role":        "Role / Position",
        "lbl_exp_company":     "Company & Location",
        "lbl_exp_date":        "Date Range",
        "lbl_exp_bullets":     "Responsibilities (one per line)",
        "btn_add_entry":       "+ Add",
        "btn_remove_entry":    "− Remove",

        # Skills tab
        "lbl_skill_group":     "Group (e.g. Languages)",
        "lbl_skill_items":     "Skills (comma-separated)",

        # Education tab
        "lbl_edu_degree":      "Degree / Course",
        "lbl_edu_institution": "Institution",
        "lbl_edu_date":        "Date Range",
        "lbl_edu_bullets":     "Details (one per line)",
        "lbl_certificates":    "Certificates (one per line)",

        # Languages tab
        "lbl_lang_name":       "Language",
        "lbl_lang_level":      "Level",

        # Validation
        "val_name_required":   "Full name is required.",
        "val_profile_required":"Professional summary cannot be empty.",
    },

    # ── Spanish ───────────────────────────────────────────────────────────────
    "es": {
        "app_title":           "Generador de CV Pro",
        "app_subtitle":        "Crea tu currículum profesional en segundos",
        "btn_generate":        "⚡  Generar CV",
        "btn_photo":           "📷  Elegir Foto",
        "btn_output":          "📁  Carpeta de Salida",
        "lbl_output_dir":      "Carpeta de salida:",
        "lbl_pdf_lang":        "Idioma del PDF:",
        "lbl_ui_lang":         "Idioma de la interfaz:",
        "lbl_photo_preview":   "Vista previa de foto",
        "lbl_no_photo":        "Sin foto seleccionada",
        "log_ready":           "Listo. Completa tus datos y pulsa Generar CV.",
        "log_generating":      "Generando tu CV…",
        "log_success":         "✅  ¡CV generado con éxito!",
        "log_error":           "❌  Error: {msg}",
        "log_open_folder":     "📂  Abrir carpeta de salida",

        "tab_personal":        "Personal",
        "tab_profile":         "Perfil",
        "tab_experience":      "Experiencia",
        "tab_skills":          "Habilidades",
        "tab_education":       "Educación",
        "tab_languages":       "Idiomas",

        "lbl_full_name":       "Nombre Completo",
        "lbl_job_title":       "Título Profesional",
        "lbl_phone":           "Teléfono",
        "lbl_email":           "Correo Electrónico",
        "lbl_address":         "Dirección",
        "lbl_github":          "URL de GitHub",
        "lbl_linkedin":        "URL de LinkedIn",

        "lbl_profile_text":    "Perfil Profesional",
        "ph_profile":          "Describe tu perfil profesional en 3-5 frases…",

        "lbl_exp_role":        "Cargo / Puesto",
        "lbl_exp_company":     "Empresa y Ubicación",
        "lbl_exp_date":        "Periodo",
        "lbl_exp_bullets":     "Responsabilidades (una por línea)",
        "btn_add_entry":       "+ Añadir",
        "btn_remove_entry":    "− Eliminar",

        "lbl_skill_group":     "Grupo (ej. Lenguajes)",
        "lbl_skill_items":     "Habilidades (separadas por coma)",

        "lbl_edu_degree":      "Título / Curso",
        "lbl_edu_institution": "Institución",
        "lbl_edu_date":        "Periodo",
        "lbl_edu_bullets":     "Detalles (uno por línea)",
        "lbl_certificates":    "Certificados (uno por línea)",

        "lbl_lang_name":       "Idioma",
        "lbl_lang_level":      "Nivel",

        "val_name_required":   "El nombre completo es obligatorio.",
        "val_profile_required":"El perfil profesional no puede estar vacío.",
    },

    # ── Portuguese ────────────────────────────────────────────────────────────
    "pt": {
        "app_title":           "Gerador de CV Pro",
        "app_subtitle":        "Crie o seu currículo profissional em segundos",
        "btn_generate":        "⚡  Gerar CV",
        "btn_photo":           "📷  Escolher Foto",
        "btn_output":          "📁  Pasta de Saída",
        "lbl_output_dir":      "Pasta de saída:",
        "lbl_pdf_lang":        "Idioma do PDF:",
        "lbl_ui_lang":         "Idioma da interface:",
        "lbl_photo_preview":   "Pré-visualização",
        "lbl_no_photo":        "Sem foto selecionada",
        "log_ready":           "Pronto. Preencha os seus dados e clique em Gerar CV.",
        "log_generating":      "A gerar o seu CV…",
        "log_success":         "✅  CV gerado com sucesso!",
        "log_error":           "❌  Erro: {msg}",
        "log_open_folder":     "📂  Abrir pasta de saída",

        "tab_personal":        "Pessoal",
        "tab_profile":         "Perfil",
        "tab_experience":      "Experiência",
        "tab_skills":          "Competências",
        "tab_education":       "Formação",
        "tab_languages":       "Idiomas",

        "lbl_full_name":       "Nome Completo",
        "lbl_job_title":       "Título Profissional",
        "lbl_phone":           "Telemóvel",
        "lbl_email":           "E-mail",
        "lbl_address":         "Morada",
        "lbl_github":          "URL do GitHub",
        "lbl_linkedin":        "URL do LinkedIn",

        "lbl_profile_text":    "Perfil Profissional",
        "ph_profile":          "Descreva o seu perfil profissional em 3-5 frases…",

        "lbl_exp_role":        "Cargo / Função",
        "lbl_exp_company":     "Empresa e Localização",
        "lbl_exp_date":        "Período",
        "lbl_exp_bullets":     "Responsabilidades (uma por linha)",
        "btn_add_entry":       "+ Adicionar",
        "btn_remove_entry":    "− Remover",

        "lbl_skill_group":     "Grupo (ex. Linguagens)",
        "lbl_skill_items":     "Competências (separadas por vírgula)",

        "lbl_edu_degree":      "Grau / Curso",
        "lbl_edu_institution": "Instituição",
        "lbl_edu_date":        "Período",
        "lbl_edu_bullets":     "Detalhes (um por linha)",
        "lbl_certificates":    "Certificados (um por linha)",

        "lbl_lang_name":       "Idioma",
        "lbl_lang_level":      "Nível",

        "val_name_required":   "O nome completo é obrigatório.",
        "val_profile_required":"O perfil profissional não pode estar vazio.",
    },
}


class I18nService:
    """
    Single-responsibility service for UI text translation.
    Switching language only requires calling set_language(); no restarts needed.
    """

    SUPPORTED: tuple[str, ...] = ("en", "es", "pt")

    def __init__(self, language: str = "en") -> None:
        self._lang = language if language in self.SUPPORTED else "en"

    # ── Public API ────────────────────────────────────────────────────────────
    @property
    def language(self) -> str:
        return self._lang

    def set_language(self, language: str) -> None:
        if language not in self.SUPPORTED:
            raise ValueError(f"Unsupported language '{language}'. Choose from {self.SUPPORTED}.")
        self._lang = language

    def t(self, key: str, **kwargs: str) -> str:
        """Return the translated string for *key*, with optional format kwargs."""
        text = _CATALOGUE.get(self._lang, {}).get(key, key)
        return text.format(**kwargs) if kwargs else text
