"""
cv_service.py — CV Generation Service  (SRP / DIP)
====================================================
Orchestrates the entire PDF generation pipeline.
The GUI depends on this abstraction; it never imports
reportlab or builders directly — Dependency Inversion.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

# Ensure project root is importable regardless of working dir
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from core.builders import CVStoryBuilder
from core.pdf_writer import PDFWriter
from core.styles import get_cv_styles
from languages.dynamic import DynamicCVContent


@dataclass(frozen=True)
class GenerationResult:
    """Value object returned after attempting to generate a CV."""
    success: bool
    output_path: str
    message: str


class CVGenerationService:
    """
    Generates a PDF CV from a plain data dict.

    Parameters
    ----------
    progress_callback : callable, optional
        Called with a human-readable status string at each step.
        Signature: ``callback(message: str) -> None``
    """

    def __init__(self, progress_callback: Optional[Callable[[str], None]] = None) -> None:
        self._log = progress_callback or (lambda msg: None)

    # ── Public API ────────────────────────────────────────────────────────────
    def generate(
        self,
        data: Dict[str, Any],
        photo_path: Optional[str],
        output_dir: str,
    ) -> GenerationResult:
        """
        Generate the CV PDF.

        Parameters
        ----------
        data        : form data dict (see DynamicCVContent for shape)
        photo_path  : absolute path to profile photo, or None
        output_dir  : directory where the PDF will be saved
        """
        try:
            self._log("Building content provider…")
            provider = DynamicCVContent(data)

            self._log("Applying document styles…")
            styles = get_cv_styles()

            self._log("Assembling CV structure…")
            story = CVStoryBuilder.build_cv_story(provider, styles, photo_path)

            # Determine output filename
            personal = data.get("personal", {})
            raw_name = personal.get("name", "CV").strip().replace(" ", "_")
            suffix = provider.get_filename_suffix()
            filename = f"CV_{raw_name}{suffix}.pdf"
            output_path = os.path.join(output_dir, filename)

            os.makedirs(output_dir, exist_ok=True)

            self._log(f"Writing PDF → {output_path}")
            success = PDFWriter.compile_pdf(output_path, story)

            if success:
                # Merge certificates if any
                certs = provider.get_certificates()
                if certs:
                    self._log("Anexando certificados...")
                    try:
                        from pypdf import PdfWriter as PyPdfWriter, PdfReader
                        merger = PyPdfWriter()
                        merger.append(output_path)
                        for cert in certs:
                            if os.path.exists(cert) and cert.lower().endswith(".pdf"):
                                merger.append(cert)
                        merger.write(output_path)
                        merger.close()
                    except Exception as e:
                        self._log(f"[WARN] No se pudieron anexar los certificados: {e}")

                self._log(f"Done! Saved to: {output_path}")
                return GenerationResult(
                    success=True,
                    output_path=output_path,
                    message=f"CV saved to:\n{output_path}",
                )
            return GenerationResult(
                success=False,
                output_path="",
                message="PDF compilation failed. Check console for details.",
            )

        except Exception as exc:
            return GenerationResult(
                success=False,
                output_path="",
                message=str(exc),
            )
