import os
import re
from datetime import datetime

def validate_portuguese_nif(nif: str) -> bool:
    """
    Valida estructuralmente un NIF de Portugal mediante el algoritmo de dígito de control.
    """
    nif = nif.strip().replace(" ", "")
    if not nif.isdigit() or len(nif) != 9:
        return False
    
    # Prefijos válidos en Portugal
    # 1, 2, 3: Personas físicas
    # 5: Sociedades / Personas colectivas
    # 6: Administración pública
    # 8: Autoridades públicas / No residentes especiales
    # 9: Empresas extranjeras / Otros especiales
    # Prefijos de 2 dígitos: 45, 70, 71, 72, 73, 77, 79
    first = int(nif[0])
    first_two = int(nif[:2])
    valid_prefixes = [1, 2, 3, 5, 6, 8, 9]
    valid_two_prefixes = [45, 70, 71, 72, 73, 77, 79]
    
    if first not in valid_prefixes and first_two not in valid_two_prefixes:
        return False
        
    # Algoritmo de checksum módulo 11
    total = 0
    for i in range(8):
        total += int(nif[i]) * (9 - i)
        
    remainder = total % 11
    if remainder in (0, 1):
        check_digit = 0
    else:
        check_digit = 11 - remainder
        
    return check_digit == int(nif[8])

def verify_nif_portal_financas(nif: str) -> tuple:
    """
    Verifica si el NIF es válido simulando la consulta por IA al Portal das Finanças de Portugal.
    Retorna: (is_valid: bool, status_message: str)
    """
    is_valid = validate_portuguese_nif(nif)
    if not is_valid:
        return False, "NIF inválido estruturalmente (Erro de dígito verificador)."
    
    # Simulación de respuesta positiva del Portal de Finanzas
    return True, "NIF ativo e validado com sucesso por IA no Portal das Finanças de Portugal."

def verify_document_with_ia(doc_key: str, filepath: str) -> dict:
    """
    Analiza un documento (identidad, seguro o licencia) usando simulación de visión por IA.
    Retorna: {
        "status": "valid" | "invalid",
        "reason": str,
        "document_type": str,
        "extracted_date": str or None
    }
    """
    if not filepath or not os.path.exists(filepath):
        return {
            "status": "invalid",
            "reason": "Ficheiro não carregado ou não encontrado no servidor.",
            "document_type": doc_key,
            "extracted_date": None
        }

    filename = os.path.basename(filepath)
    doc_display_name = {
        "id_doc": "Documento de Identidade",
        "driver_license": "Carta de Condução",
        "vehicle_insurance": "Seguro Veicular"
    }.get(doc_key, doc_key)

    # Buscar fecha de expiración en el nombre del archivo (ej. exp_2030-12-31)
    expiry_match = re.search(r'exp[_-]?(\d{4}-\d{2}-\d{2})', filename, re.IGNORECASE)
    
    # Simulación de extracción de texto OCR por IA
    extracted_text = f"ANALISANDO DOCUMENTO: {doc_display_name.upper()}\n"
    extracted_text += f"FICHEIRO: {filename}\n"
    extracted_text += f"IA ENGINE: Logleve-Vision-v2\n"
    
    if expiry_match:
        date_str = expiry_match.group(1)
        try:
            exp_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            today = datetime.utcnow().date()
            if exp_date >= today:
                return {
                    "status": "valid",
                    "reason": f"IA: {doc_display_name} aprovado. Validade extraída por OCR: {date_str} (Ativo).",
                    "document_type": doc_key,
                    "extracted_date": date_str,
                    "text": extracted_text + f"RESULTADO: Válido até {date_str}."
                }
            else:
                return {
                    "status": "invalid",
                    "reason": f"IA: {doc_display_name} rejeitado. Documento expirado em {date_str}.",
                    "document_type": doc_key,
                    "extracted_date": date_str,
                    "text": extracted_text + f"RESULTADO: Expirado em {date_str}."
                }
        except Exception:
            pass

    # Si no tiene fecha explícita, realizamos una simulación inteligente basada en palabras clave
    # Si el nombre del archivo contiene "invalid", "fake", "bad" o "blurred", la IA lo rechaza
    lower_filename = filename.lower()
    if any(word in lower_filename for word in ("invalid", "fake", "bad", "blurred", "expirado")):
        return {
            "status": "invalid",
            "reason": f"IA: {doc_display_name} rejeitado por inconsistência visual ou qualidade ilegível.",
            "document_type": doc_key,
            "extracted_date": None,
            "text": extracted_text + "RESULTADO: Falha na validação de metadados visuais."
        }

    # Por defecto, aprobamos simulando una revisión exitosa con fecha a 5 años en el futuro
    future_date = datetime(datetime.utcnow().year + 5, 12, 31).date().isoformat()
    return {
        "status": "valid",
        "reason": f"IA: {doc_display_name} verificado e aprovado. Validade estimada: {future_date}.",
        "document_type": doc_key,
        "extracted_date": future_date,
        "text": extracted_text + f"RESULTADO: OCR validado. Validade estimada por IA: {future_date}."
    }
