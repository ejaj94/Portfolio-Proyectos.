import os
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4

class PDFWriter:
    """
    Clase responsable de instanciar la plantilla física y compilar el archivo PDF (SRP).
    """

    @staticmethod
    def compile_pdf(output_path: str, story: list, margins: tuple = (36, 36, 36, 36)) -> bool:
        """
        Compila una historia de flowables a un archivo PDF.
        margins: (leftMargin, rightMargin, topMargin, bottomMargin)
        """
        left, right, top, bottom = margins
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                leftMargin=left,
                rightMargin=right,
                topMargin=top,
                bottomMargin=bottom
            )
            doc.build(story)
            print(f"[OK] PDF generado correctamente: {output_path}")
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo compilar el PDF en {output_path}: {e}")
            return False
