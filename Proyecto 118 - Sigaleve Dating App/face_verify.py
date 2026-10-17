# -*- coding: utf-8 -*-
"""
face_verify.py — Verificação de perfis por selfie (Sigaleve).

Fluxo (100% local na VPS — nenhum dado biométrico sai do servidor):
  1. Utilizador tira uma selfie na câmara do app.
  2. POST /api/v1/verify/selfie → deteta o rosto, gera embedding 128-d
     e compara com as fotos de perfil do utilizador.
  3. Se distância euclidiana < LIMIAR → marca is_verified=True.
  4. A selfie é processada em memória e APAGADA de imediato.
     Persiste apenas um booleano no perfil (nunca o embedding, nunca a foto).

Privacidade (RGPD Art. 9 — dados de categoria especial):
  - Nenhum dado biométrico é armazenado; apenas o resultado (verificado sim/não).
  - Nenhuma API externa é chamada.

Fallback: se a biblioteca face_recognition não estiver disponível
(ex.: dlib não compilado), o endpoint responde 503 explicativo em vez
de fingir verificação.
"""
import base64
import io
import threading

import numpy as numpy  # usado apenas quando face_recognition está disponível

# ── Configuração ─────────────────────────────────────────────────────────────
MATCH_TOLERANCE = 0.60   # distância euclidiana máxima para considerar o mesmo rosto
MIN_FACE_SIZE = 80       # tamanho mínimo do rosto em px para aceitar

_LOCK = threading.Lock()
_face_rec = None
_STATUS = {"available": False, "reason": "não inicializado"}

def _try_import():
    """Importa face_recognition uma única vez (dlib demora a carregar ~2s)."""
    global _face_rec, _STATUS
    with _LOCK:
        if _face_rec is not None or _STATUS.get("initialized"):
            return
        _STATUS["initialized"] = True
        try:
            import face_recognition as fr
            _face_rec = fr
            _STATUS["available"] = True
            _STATUS["reason"] = "ok"
            print("[FACE_VERIFY] face_recognition carregada.")
        except Exception as e:
            _STATUS["available"] = False
            _STATUS["reason"] = str(e)
            print(f"[FACE_VERIFY] face_recognition indisponível: {e}")

def is_available():
    _try_import()
    return _STATUS["available"]

def status_reason():
    _try_import()
    return _STATUS["reason"]


def _decode_image(data_url_or_b64):
    """Converte data URL/base64 em imagem numpy."""
    import numpy as np
    from PIL import Image
    s = data_url_or_b64.strip()
    if "," in s[:140] and s.strip()[:5] in ("data:", "data:"):
        s = s.split(",", 1)[1]
    raw = base64.b64decode(s)
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    return np.array(img)


def _best_face_encoding(image_arr):
    """Devolve o encoding do maior rosto detetado (ou None)."""
    fr = _face_rec
    locations = fr.face_locations(image_arr)
    if not locations:
        return None, "Nenhum rosto detetado na selfie. Certifica-te de que o teu rosto está visível e bem iluminado."
    # maior rosto = mais perto (provável rosto principal)
    (top, right, bottom, left) = max(locations, key=lambda l: (l[2]-l[0])*(l[1]-l[3]))
    if (right - left) < MIN_FACE_SIZE or (bottom - top) < MIN_FACE_SIZE:
        return None, "Rosto detetado demasiado pequeno. Aproxima a câmara do teu rosto."
    encodings = fr.face_encodings(image_arr, known_face_locations=[(top, right, bottom, left)])
    if not encodings:
        return None, "Não foi possível analisar o rosto. Tenta noutra posição ou com mais luz."
    return encodings[0], None


def _url_to_image(url):
    """Descarrega uma foto de perfil (http/https ou data URL) para numpy array."""
    import urllib.request
    import numpy as np
    from PIL import Image
    s = str(url).strip()
    if not s:
        return None
    if s.startswith("data:image"):
        return _decode_image(s)
    req = urllib.request.Request(s, headers={"User-Agent": "Mozilla/5.0 SigaleveFaceVerify"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read()
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    return np.array(img)


def verify_selfie_vs_profile(selfie_b64, profile_photo_urls):
    """
    Compara a selfie com as fotos de perfil.
    Devolve (sucesso: bool, mensagem: str, detalhe: dict).
    A selfie nunca é guardada.
    """
    if not is_available():
        return False, "Verificação por selfie indisponível neste momento. Tenta novamente mais tarde.", {"available": False}

    try:
        selfie_arr = _decode_image(selfie_b64)
    except Exception:
        return False, "Não foi possível ler a imagem da selfie. Tenta capturar outra foto.", {"available": True}

    try:
        selfie_enc, err = _best_face_encoding(selfie_arr)
    except Exception:
        return False, "Erro ao analisar a selfie. Tenta novamente.", {"available": True}
    if selfie_enc is None:
        return False, err, {"available": True}

    # Compara com cada foto de perfil (máx. 6)
    best = None
    errors = 0
    for url in (profile_photo_urls or [])[:6]:
        try:
            arr = _url_to_image(url)
            if arr is None:
                continue
            encs = _face_rec.face_encodings(arr)
            if not encs:
                continue
            for enc in encs:
                dist = float(numpy.linalg.norm(selfie_enc - enc))
                if best is None or dist < best:
                    best = dist
        except Exception:
            errors += 1
            continue

    if best is None:
        msg = "Não foi possível comparar com as tuas fotos de perfil. Adiciona pelo menos uma foto de rosto claro."
        if errors:
            msg += f" ({errors} foto(s) não puderam ser carregadas)"
        return False, msg, {"available": True}

    if best <= MATCH_TOLERANCE:
        return True, "Perfil verificado com sucesso! O teu selo de verificação já está ativo.", {
            "available": True, "distance": round(best, 3), "tolerance": MATCH_TOLERANCE,
        }
    return False, "A selfie não corresponde às tuas fotos de perfil. Certifica-te de que és tu nas fotos do perfil e tenta de novo.", {
        "available": True, "distance": round(best, 3), "tolerance": MATCH_TOLERANCE,
    }
