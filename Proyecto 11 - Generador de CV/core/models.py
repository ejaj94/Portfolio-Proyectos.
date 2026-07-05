from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any

class CVContentProvider(ABC):
    """
    Abstracción base para la definición de contenidos de CV en múltiples idiomas (OCP/LSP).
    Cada implementación concreta debe retornar sus traducciones y textos estructurados.
    """

    @abstractmethod
    def get_personal_info(self) -> Dict[str, str]:
        """
        Retorna la información personal (nombre, telemóvel, morada, email, github, linkedin).
        """
        pass

    @abstractmethod
    def get_profile_title(self) -> str:
        """
        Retorna el título de la sección de perfil profesional.
        """
        pass

    @abstractmethod
    def get_profile_text(self) -> str:
        """
        Retorna el párrafo descriptivo del perfil profesional.
        """
        pass

    @abstractmethod
    def get_experience_section_title(self) -> str:
        """
        Retorna el título de la sección de experiencia laboral.
        """
        pass

    @abstractmethod
    def get_experience(self) -> List[Dict[str, Any]]:
        """
        Retorna la lista de experiencias laborales estructuradas.
        Cada experiencia es un dict con:
        - title: Cargo
        - subtitle: Empresa/Ubicación
        - date: Periodo
        - bullets: Detalles (lista de strings)
        """
        pass

    @abstractmethod
    def get_skills_section_title(self) -> str:
        """
        Retorna el título de la sección de habilidades técnicas.
        """
        pass

    @abstractmethod
    def get_skills(self) -> List[Tuple[str, str]]:
        """
        Retorna la lista de habilidades técnicas organizadas por grupos: (nombre_grupo, elementos).
        """
        pass

    @abstractmethod
    def get_education_section_title(self) -> str:
        """
        Retorna el título de la sección de educación.
        """
        pass

    @abstractmethod
    def get_education(self) -> List[Dict[str, Any]]:
        """
        Retorna la formación académica. Cada item es un dict con:
        - title: Título
        - subtitle: Institución
        - date: Periodo
        - bullets: Detalles (lista de strings)
        """
        pass

    @abstractmethod
    def get_certificates_subtitle(self) -> str:
        """
        Retorna el subtítulo de la subsección de certificados (por ejemplo, "Certificados de Formación").
        """
        pass

    @abstractmethod
    def get_certificates(self) -> List[str]:
        """
        Retorna la lista de certificaciones obtenidas.
        """
        pass

    @abstractmethod
    def get_languages_section_title(self) -> str:
        """
        Retorna el título de la sección de idiomas.
        """
        pass

    @abstractmethod
    def get_languages(self) -> List[Tuple[str, str]]:
        """
        Retorna la lista de idiomas: (idioma, nivel).
        """
        pass

    @abstractmethod
    def get_filename_suffix(self) -> str:
        """
        Sufijo del archivo PDF generado (ej. '_PT', '_EN' o vació para español).
        """
        pass

    @abstractmethod
    def has_cover_letter(self) -> bool:
        """
        Indica si este idioma incluye carta de presentación.
        """
        pass

    @abstractmethod
    def get_cover_letter_filename(self) -> str:
        """
        Nombre del archivo PDF para la carta de presentación.
        """
        pass

    @abstractmethod
    def get_cover_letter_content(self) -> Dict[str, Any]:
        """
        Retorna el contenido estructurado de la carta de presentación:
        - date_location: Ubicación y fecha
        - salutation: Destinatario
        - paragraphs: Cuerpo de la carta (lista de strings)
        - signature: Nombre para la firma
        - signature_title: Título bajo la firma
        """
        pass
