import os
from datetime import datetime
from typing import Dict

try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except Exception:
    OCR_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except Exception:
    REQUESTS_AVAILABLE = False


def _check_expiry_from_filename(path: str):
    name = os.path.basename(path)
    parts = name.split('_')
    for p in parts:
        if p.startswith('exp') and len(p) > 3:
            try:
                date_str = p[3:].lstrip('-')
                d = datetime.fromisoformat(date_str).date()
                return d >= datetime.utcnow().date()
            except Exception:
                continue
    return None


def _ocr_text(path: str) -> str:
    # Prefer local OCR if available
    if OCR_AVAILABLE:
        try:
            img = Image.open(path)
            text = pytesseract.image_to_string(img)
            return text
        except Exception:
            pass

    # Fallback to external OCR if configured
    api_key = os.environ.get('OCR_SPACE_API_KEY')
    if api_key and REQUESTS_AVAILABLE:
        try:
            with open(path, 'rb') as f:
                files = {'file': f}
                data = {'apikey': api_key, 'language': 'eng'}
                resp = requests.post('https://api.ocr.space/parse/image', files=files, data=data, timeout=30)
            j = resp.json()
            if j.get('IsErroredOnProcessing') is False:
                parsed = j.get('ParsedResults') or []
                texts = [p.get('ParsedText','') for p in parsed]
                return '\n'.join(texts)
        except Exception:
            pass

    return ""


def verify_documents(files: Dict[str, str]) -> Dict[str, Dict]:
    """
    Verificador mejorado:
    - Si OCR disponible extrae texto y busca fechas y palabras clave
    - Si no, intenta inferir expiración por nombre de archivo
    Devuelve: {doc_key: {status: 'valid'|'invalid'|'missing', reason: str, text: str}}
    """
    results = {}
    for key, path in files.items():
        info = {"status": "unknown", "reason": "", "text": ""}
        if not path or not os.path.exists(path):
            info["status"] = "missing"
            info["reason"] = "file not found"
            results[key] = info
            continue

        ext = os.path.splitext(path)[1].lower().lstrip('.')
        if ext not in ("png", "jpg", "jpeg", "pdf"):
            info["status"] = "invalid"
            info["reason"] = "unsupported file type"
            results[key] = info
            continue

        text = _ocr_text(path)
        info["text"] = text

        expiry_ok = _check_expiry_from_filename(path)
        if expiry_ok is True:
            info["status"] = "valid"
            info["reason"] = "expiry inferred from filename"
        elif expiry_ok is False:
            info["status"] = "invalid"
            info["reason"] = "expired (inferred)"
        else:
            # Try find year-like dates in OCR text
            if text:
                # naive search for YYYY or YYYY-MM-DD
                found = None
                for token in text.split():
                    t = token.strip('.,')
                    try:
                        if len(t) == 10 and t.count('-') == 2:
                            d = datetime.fromisoformat(t).date()
                            found = d
                            break
                        if len(t) == 4 and t.isdigit():
                            y = int(t)
                            if 1900 < y < 2100:
                                found = datetime(y,1,1).date()
                                break
                    except Exception:
                        continue
                if found:
                    info["reason"] = f"date found in text: {found.isoformat()}"
                    info["status"] = "valid" if found >= datetime.utcnow().date() else "invalid"
                else:
                    info["status"] = "valid"
                    info["reason"] = "no expiry inferred — manual review recommended"
            else:
                info["status"] = "valid"
                info["reason"] = "no OCR available and no expiry inferred — manual review recommended"

        results[key] = info

    return results
