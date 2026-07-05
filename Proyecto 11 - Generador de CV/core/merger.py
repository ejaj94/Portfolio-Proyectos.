import os
from pypdf import PdfReader, PdfWriter

class PDFMerger:
    """
    Clase responsable de la combinación de múltiples archivos PDF (SRP).
    Permite acoplar certificados en formato PDF al documento principal.
    """

    @staticmethod
    def merge_cv_with_certificates(
        base_pdf: str, 
        cert_dir: str, 
        cert_filenames: list, 
        final_pdf: str
    ) -> bool:
        """
        Une el PDF base del CV con los certificados PDF encontrados en cert_dir.
        """
        writer = PdfWriter()
        
        # 1. Leer y añadir las páginas del CV base
        if not os.path.exists(base_pdf):
            print(f"[ERROR] Archivo base del CV no encontrado: {base_pdf}")
            return False
            
        try:
            reader_cv = PdfReader(base_pdf)
            for page in reader_cv.pages:
                writer.add_page(page)
        except Exception as e:
            print(f"[ERROR] No se pudo leer el archivo base del CV: {e}")
            return False
            
        # 2. Leer y añadir los certificados PDF
        for filename in cert_filenames:
            filepath = os.path.join(cert_dir, filename)
            if os.path.exists(filepath):
                try:
                    reader_cert = PdfReader(filepath)
                    for page in reader_cert.pages:
                        writer.add_page(page)
                    print(f"[OK] Certificado anexado: {filename}")
                except Exception as e:
                    print(f"[ERROR] Error al anexar certificado {filename}: {e}")
            else:
                print(f"[WARN] Fichero de certificado no encontrado: {filepath}")
                
        # 3. Escribir el archivo final unificado
        try:
            with open(final_pdf, "wb") as f_out:
                writer.write(f_out)
            print(f"[SUCCESS] PDF final completo generado con éxito en: {final_pdf}")
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo escribir el PDF final en {final_pdf}: {e}")
            return False
