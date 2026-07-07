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
            "address":  p.get("location", ""),
            "github":   p.get("github",   ""),
            "linkedin": p.get("linkedin", ""),
        }

    def get_profile_title(self) -> str:
        return self._get("profile_title")

    def get_profile_text(self) -> str:
        return self._data.get("profile", "")

    def get_experience_section_title(self) -> str:
        return self._get("experience_title")

    def get_experience(self) -> List[Dict[str, Any]]:
        raw = self._data.get("experience", [])
        return [
            {
                "title": r.get("title", ""),
                "subtitle": r.get("company", ""),
                "date": r.get("date", ""),
                "bullets": r.get("description", [])
            } for r in raw
        ]

    def get_skills_section_title(self) -> str:
        return self._get("skills_title")

    def get_skills(self) -> List[Tuple[str, str]]:
        return self._data.get("skills", [])

    def get_education_section_title(self) -> str:
        return self._get("education_title")

    def get_education(self) -> List[Dict[str, Any]]:
        edu_data = self._data.get("education", {})
        raw = edu_data.get("degrees", []) if isinstance(edu_data, dict) else edu_data
        return [
            {
                "title": r.get("degree", ""),
                "subtitle": r.get("school", ""),
                "date": r.get("date", ""),
                "bullets": []
            } for r in raw
        ]

    def get_certificates_subtitle(self) -> str:
        return self._get("certificates_subtitle")

    def get_certificates(self) -> List[str]:
        edu_data = self._data.get("education", {})
        if isinstance(edu_data, dict):
            return edu_data.get("certificates", [])
        return self._data.get("certificates", [])

    def get_languages_section_title(self) -> str:
        return self._get("languages_title")

    def get_languages(self) -> List[Tuple[str, str]]:
        raw = self._data.get("languages", [])
        target = self._data.get("output_lang", "en").lower()
        
        lang_map = {
            "inglés": {"en": "English", "es": "Inglés", "pt": "Inglês"},
            "english": {"en": "English", "es": "Inglés", "pt": "Inglês"},
            "inglês": {"en": "English", "es": "Inglés", "pt": "Inglês"},
            "español": {"en": "Spanish", "es": "Español", "pt": "Espanhol"},
            "spanish": {"en": "Spanish", "es": "Español", "pt": "Espanhol"},
            "espanhol": {"en": "Spanish", "es": "Español", "pt": "Espanhol"},
            "francés": {"en": "French", "es": "Francés", "pt": "Francês"},
            "french": {"en": "French", "es": "Francés", "pt": "Francês"},
            "francês": {"en": "French", "es": "Francés", "pt": "Francês"},
            "alemán": {"en": "German", "es": "Alemán", "pt": "Alemão"},
            "german": {"en": "German", "es": "Alemán", "pt": "Alemão"},
            "alemão": {"en": "German", "es": "Alemán", "pt": "Alemão"},
            "portugués": {"en": "Portuguese", "es": "Portugués", "pt": "Português"},
            "portuguese": {"en": "Portuguese", "es": "Portugués", "pt": "Português"},
            "português": {"en": "Portuguese", "es": "Portugués", "pt": "Português"},
            "italiano": {"en": "Italian", "es": "Italiano", "pt": "Italiano"},
            "italian": {"en": "Italian", "es": "Italiano", "pt": "Italiano"},
            "chino": {"en": "Chinese", "es": "Chino", "pt": "Chinês"},
            "chinese": {"en": "Chinese", "es": "Chino", "pt": "Chinês"},
            "chinês": {"en": "Chinese", "es": "Chino", "pt": "Chinês"},
            "japonés": {"en": "Japanese", "es": "Japonés", "pt": "Japonês"},
            "japanese": {"en": "Japanese", "es": "Japonés", "pt": "Japonês"},
            "japonês": {"en": "Japanese", "es": "Japonés", "pt": "Japonês"},
            "ruso": {"en": "Russian", "es": "Ruso", "pt": "Russo"},
            "russian": {"en": "Russian", "es": "Ruso", "pt": "Russo"},
            "russo": {"en": "Russian", "es": "Ruso", "pt": "Russo"},
        }
        
        level_map = {
            "básico": {"en": "Basic", "es": "Básico", "pt": "Básico"},
            "basic": {"en": "Basic", "es": "Básico", "pt": "Básico"},
            "intermedio": {"en": "Intermediate", "es": "Intermedio", "pt": "Intermediário"},
            "intermediate": {"en": "Intermediate", "es": "Intermedio", "pt": "Intermediário"},
            "intermediário": {"en": "Intermediate", "es": "Intermedio", "pt": "Intermediário"},
            "avanzado": {"en": "Advanced", "es": "Avanzado", "pt": "Avançado"},
            "advanced": {"en": "Advanced", "es": "Avanzado", "pt": "Avançado"},
            "avançado": {"en": "Advanced", "es": "Avanzado", "pt": "Avançado"},
            "profesional/nativo": {"en": "Native/Bilingual", "es": "Profesional/Nativo", "pt": "Nativo/Bilingue"},
            "native/bilingual": {"en": "Native/Bilingual", "es": "Profesional/Nativo", "pt": "Nativo/Bilingue"},
            "nativo/bilingue": {"en": "Native/Bilingual", "es": "Profesional/Nativo", "pt": "Nativo/Bilingue"},
        }
        
        translated_langs = []
        for l, lev in raw:
            tl = lang_map.get(l.lower(), {}).get(target, l)
            tlev = level_map.get(lev.lower(), {}).get(target, lev)
            translated_langs.append((tl, tlev))
            
        return translated_langs

    def get_filename_suffix(self) -> str:
        lang = self._data.get("output_lang", "en").upper()
        return f"_{lang}" if lang != "ES" else ""

    def has_cover_letter(self) -> bool:
        return False

    def get_cover_letter_filename(self) -> str:
        return ""

    def get_cover_letter_content(self) -> Dict[str, Any]:
        return {}
