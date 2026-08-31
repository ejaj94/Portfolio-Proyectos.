"""
dynamic.py — Dynamic CV Content Provider  (OCP / LSP / DIP)
=============================================================
Implements CVContentProvider using a plain dict received from the GUI/Web API.
This decouples the presentation layer from the PDF generation engine.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple
from core.models import CVContentProvider


class DynamicCVContent(CVContentProvider):
    """
    Concrete CVContentProvider that derives all content from a data dict.
    Supports both legacy dict shapes and web app JSON payloads.
    """

    _DEFAULTS: Dict[str, Dict[str, str]] = {
        "en": {
            "profile_title":       "Professional Profile",
            "experience_title":    "Work Experience",
            "skills_title":        "Technical Skills",
            "education_title":     "Education & Qualifications",
            "certificates_subtitle": "Training Certificates",
            "languages_title":     "Languages",
        },
        "es": {
            "profile_title":       "Perfil Profesional",
            "experience_title":    "Experiencia Laboral",
            "skills_title":        "Habilidades Técnicas",
            "education_title":     "Educación y Titulaciones",
            "certificates_subtitle": "Certificados de Formación",
            "languages_title":     "Idiomas",
        },
        "pt": {
            "profile_title":       "Perfil Profissional",
            "experience_title":    "Experiência Profissional",
            "skills_title":        "Competências Técnicas",
            "education_title":     "Formação Académica",
            "certificates_subtitle": "Certificados de Formação",
            "languages_title":     "Idiomas",
        },
    }

    def __init__(self, data: Dict[str, Any]) -> None:
        self._data = data
        lang = data.get("lang") or data.get("output_lang") or "pt"
        self._defaults = self._DEFAULTS.get(lang.lower(), self._DEFAULTS["pt"])

    def _get(self, key: str, fallback: Any = "") -> Any:
        return self._data.get(key) or self._defaults.get(key, fallback)

    def get_personal_info(self) -> Dict[str, str]:
        p = self._data.get("personal", {})
        return {
            "name":     p.get("name",     "Enmanuel Jimenez"),
            "title":    p.get("title",    "Engenheiro de Software"),
            "phone":    p.get("phone",    ""),
            "email":    p.get("email",    ""),
            "address":  p.get("location", p.get("address", "")),
            "github":   p.get("github",   ""),
            "linkedin": p.get("website",  p.get("linkedin", "")),
        }

    def get_profile_title(self) -> str:
        return self._get("profile_title")

    def get_profile_text(self) -> str:
        p = self._data.get("personal", {})
        return p.get("summary") or self._data.get("profile_text") or self._data.get("profile") or ""

    def get_experience_section_title(self) -> str:
        return self._get("experience_title")

    def get_experience(self) -> List[Dict[str, Any]]:
        raw = self._data.get("experience", [])
        result = []
        for r in raw:
            if isinstance(r, dict):
                title = r.get("title", "")
                subtitle = r.get("company") or r.get("subtitle", "")
                date = r.get("dates") or r.get("date", "")
                desc = r.get("desc") or r.get("bullets", [])
                
                bullets = [desc] if isinstance(desc, str) and desc.strip() else (desc if isinstance(desc, list) else [])
                result.append({
                    "title": title,
                    "subtitle": subtitle,
                    "date": date,
                    "bullets": bullets
                })
        return result

    def get_skills_section_title(self) -> str:
        return self._get("skills_title")

    def get_skills(self) -> List[Tuple[str, str]]:
        raw = self._data.get("skills", [])
        if not raw:
            return []
        
        # If raw is a list of strings ["Python", "Flask", ...]
        if isinstance(raw, list) and len(raw) > 0 and isinstance(raw[0], str):
            skills_str = ", ".join(raw)
            return [(self._get("skills_title"), skills_str)]
        
        # If raw is a list of tuples [("Group", "Items")]
        result = []
        for item in raw:
            if isinstance(item, (tuple, list)) and len(item) >= 2:
                result.append((str(item[0]), str(item[1])))
            elif isinstance(item, str):
                result.append((self._get("skills_title"), item))
        return result

    def get_education_section_title(self) -> str:
        return self._get("education_title")

    def get_education(self) -> List[Dict[str, Any]]:
        edu_data = self._data.get("education", [])
        raw = edu_data.get("degrees", []) if isinstance(edu_data, dict) else edu_data
        result = []
        if isinstance(raw, list):
            for r in raw:
                if isinstance(r, dict):
                    title = r.get("degree") or r.get("title", "")
                    subtitle = r.get("institution") or r.get("school") or r.get("subtitle", "")
                    date = r.get("dates") or r.get("date", "")
                    bullets = r.get("bullets", [])
                    if isinstance(bullets, str):
                        bullets = [bullets]
                    result.append({
                        "title": title,
                        "subtitle": subtitle,
                        "date": date,
                        "bullets": bullets
                    })
        return result

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
        result = []
        
        for item in raw:
            if isinstance(item, (tuple, list)) and len(item) >= 2:
                result.append((str(item[0]), str(item[1])))
            elif isinstance(item, str):
                if "(" in item and ")" in item:
                    parts = item.split("(")
                    lang_name = parts[0].strip()
                    level = parts[1].replace(")", "").strip()
                    result.append((lang_name, level))
                else:
                    result.append((item.strip(), "Fluente/Nativo"))
        return result

    def get_filename_suffix(self) -> str:
        lang = (self._data.get("lang") or self._data.get("output_lang") or "PT").upper()
        return f"_{lang}"

    def has_cover_letter(self) -> bool:
        return False

    def get_cover_letter_filename(self) -> str:
        return ""

    def get_cover_letter_content(self) -> Dict[str, Any]:
        return {}
