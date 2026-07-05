"""
dynamic.py — Dynamic CV Content Provider  (OCP / LSP / DIP)
=============================================================
Implements CVContentProvider using a plain dict received from the GUI.
This decouples the presentation layer from the PDF generation engine:
the GUI only needs to build a dict; this class handles the contract.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from core.models import CVContentProvider


class DynamicCVContent(CVContentProvider):
    """
    Concrete CVContentProvider that derives all content from a data dict.

    Expected dict shape (all keys optional — sensible defaults applied):
    {
        "personal": {
            "name": str, "title": str, "phone": str, "email": str,
            "address": str, "github": str, "linkedin": str
        },
        "profile_title": str,
        "profile_text":  str,
        "experience_title": str,
        "experience": [
            {"title": str, "subtitle": str, "date": str, "bullets": [str, ...]}
        ],
        "skills_title": str,
        "skills": [("Group label", "item1, item2, ..."), ...],
        "education_title": str,
        "education": [
            {"title": str, "subtitle": str, "date": str, "bullets": [str, ...]}
        ],
        "certificates_subtitle": str,
        "certificates": [str, ...],
        "languages_title": str,
        "languages": [("Language", "Level"), ...],
        "output_lang": str,          # "es" | "en" | "pt"
    }
    """

    # ── Default section labels per output language ───────────────────────────
    _DEFAULTS: Dict[str, Dict[str, str]] = {
        "en": {
            "profile_title":       "Professional Profile",
            "experience_title":    "Work Experience",
            "skills_title":        "Technical Skills",
            "education_title":     "Education & Certifications",
            "certificates_subtitle": "Training Certificates",
            "languages_title":     "Languages",
        },
        "es": {
            "profile_title":       "Perfil Profesional",
            "experience_title":    "Experiencia Laboral",
            "skills_title":        "Habilidades Técnicas",
            "education_title":     "Educación y Certificados",
            "certificates_subtitle": "Certificados de Formación",
            "languages_title":     "Idiomas",
        },
        "pt": {
            "profile_title":       "Perfil Profissional",
            "experience_title":    "Experiência Profissional",
            "skills_title":        "Competências Técnicas",
            "education_title":     "Formação e Certificados",
            "certificates_subtitle": "Certificados de Formação",
            "languages_title":     "Idiomas",
        },
    }

    def __init__(self, data: Dict[str, Any]) -> None:
        self._data = data
        lang = data.get("output_lang", "en")
        self._defaults = self._DEFAULTS.get(lang, self._DEFAULTS["en"])

    # ── Helpers ──────────────────────────────────────────────────────────────
    def _get(self, key: str, fallback: Any = "") -> Any:
        return self._data.get(key) or self._defaults.get(key, fallback)

    # ── CVContentProvider contract ────────────────────────────────────────────
    def get_personal_info(self) -> Dict[str, str]:
        p = self._data.get("personal", {})
        return {
            "name":     p.get("name",     ""),
            "title":    p.get("title",    ""),
            "phone":    p.get("phone",    ""),
            "email":    p.get("email",    ""),
            "address":  p.get("address",  ""),
            "github":   p.get("github",   ""),
            "linkedin": p.get("linkedin", ""),
        }

    def get_profile_title(self) -> str:
        return self._get("profile_title")

    def get_profile_text(self) -> str:
        return self._get("profile_text")

    def get_experience_section_title(self) -> str:
        return self._get("experience_title")

    def get_experience(self) -> List[Dict[str, Any]]:
        return self._data.get("experience", [])

    def get_skills_section_title(self) -> str:
        return self._get("skills_title")

    def get_skills(self) -> List[Tuple[str, str]]:
        return self._data.get("skills", [])

    def get_education_section_title(self) -> str:
        return self._get("education_title")

    def get_education(self) -> List[Dict[str, Any]]:
        return self._data.get("education", [])

    def get_certificates_subtitle(self) -> str:
        return self._get("certificates_subtitle")

    def get_certificates(self) -> List[str]:
        return self._data.get("certificates", [])

    def get_languages_section_title(self) -> str:
        return self._get("languages_title")

    def get_languages(self) -> List[Tuple[str, str]]:
        return self._data.get("languages", [])

    def get_filename_suffix(self) -> str:
        lang = self._data.get("output_lang", "en").upper()
        return f"_{lang}" if lang != "ES" else ""

    def has_cover_letter(self) -> bool:
        return False

    def get_cover_letter_filename(self) -> str:
        return ""

    def get_cover_letter_content(self) -> Dict[str, Any]:
        return {}
