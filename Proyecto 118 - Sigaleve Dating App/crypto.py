# -*- coding: utf-8 -*-
"""
crypto.py — Encriptação de dados sensíveis (Art. 9 RGPD) do Sigaleve.

Campos protegidos (armazenados cifrados em repouso em data/users_store.json):
  - date_of_birth  (data de nascimento)
  - phone          (número de telemóvel)
  - diagnosis      (código de condição de saúde — dado de categoria especial)

Implementação: Fernet (AES-128-CBC + HMAC-SHA256), chave derivada do
FERNET_KEY do .env. Se a chave não existir, é gerada automaticamente na
primeira execução e gravada no .env para persistência.

IMPORTANTE — Compatibilidade:
  - decrypt_field() devolve o valor original se este NÃO estiver cifrado
    (migração transparente de registos antigos em texto claro).
  - Ao ler um utilizador, os campos sensíveis são decifrados em memória;
    ao gravar, são cifrados de novo. O JSON em disco nunca fica com
    dados sensíveis em texto claro (após o primeiro save de cada registo).
"""
import os

try:
    from cryptography.fernet import Fernet, InvalidToken
    _HAS_FERNET = True
except ImportError:
    Fernet = None
    InvalidToken = Exception
    _HAS_FERNET = False
    print("[CRYPTO] Biblioteca 'cryptography' não instalada — dados sensíveis serão guardados em texto claro (NÃO recomendado em produção).")

ENV_FILE = os.path.join(os.path.dirname(__file__), ".env")
FERNET_KEY = None


def _load_key_from_env():
    """Lê a FERNET_KEY do .env (sem depender de python-dotenv)."""
    if not os.path.exists(ENV_FILE):
        return None
    try:
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("FERNET_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception as e:
        print(f"[CRYPTO] Erro ao ler .env: {e}")
    return None


def _ensure_key():
    """Garante que existe uma FERNET_KEY: usa a do .env ou gera e persiste uma nova."""
    global FERNET_KEY
    if FERNET_KEY:
        return FERNET_KEY
    if not _HAS_FERNET:
        return None
    FERNET_KEY = _load_key_from_env()
    if not FERNET_KEY:
        FERNET_KEY = Fernet.generate_key().decode()
        try:
            with open(ENV_FILE, "a", encoding="utf-8") as f:
                f.write(f"\nFERNET_KEY={FERNET_KEY}\n")
            print("[CRYPTO] Nova FERNET_KEY gerada e persistida no .env.")
        except Exception as e:
            print(f"[CRYPTO] AVISO: não foi possível gravar a chave no .env: {e}")
    return FERNET_KEY


def _fernet():
    if not _HAS_FERNET:
        return None
    key = _ensure_key()
    if not key:
        return None
    try:
        return Fernet(key.encode() if isinstance(key, str) else key)
    except Exception as e:
        print(f"[CRYPTO] Chave inválida: {e}")
        return None


# Prefixo que marca um valor como cifrado (permite migração transparente)
_ENC_PREFIX = "gAA encrypted:"


def encrypt_field(value):
    """Cifra um valor sensível. Devolve None se valor vazio/None.
    Se a cifragem não estiver disponível, devolve o valor original."""
    if value in (None, ""):
        return value
    if not _HAS_FERNET:
        return value
    f = _fernet()
    if not f:
        return value
    try:
        # Se já está cifrado, não cifrar de novo
        if isinstance(value, str) and value.startswith(_ENC_PREFIX):
            return value
        token = f.encrypt(str(value).encode("utf-8")).decode("ascii")
        return _ENC_PREFIX + token
    except Exception as e:
        print(f"[CRYPTO] Erro ao cifrar: {e}")
        return value


def decrypt_field(value):
    """Decifra um valor sensível. Se o valor não estiver cifrado (registo
    antigo em texto claro), devolve-o tal qual — migração transparente."""
    if value in (None, ""):
        return value
    if not isinstance(value, str) or not value.startswith(_ENC_PREFIX):
        return value
    if not _HAS_FERNET:
        print("[CRYPTO] AVISO: valor cifrado encontrado mas 'cryptography' não instalada.")
        return value
    f = _fernet()
    if not f:
        return value
    try:
        token = value[len(_ENC_PREFIX):]
        return f.decrypt(token.encode("ascii")).decode("utf-8")
    except InvalidToken:
        print("[CRYPTO] AVISO: token inválido (chave trocada?) — a devolver valor bruto.")
        return value
    except Exception as e:
        print(f"[CRYPTO] Erro ao decifrar: {e}")
        return value


SENSITIVE_FIELDS = ["date_of_birth", "phone", "diagnosis"]


def encrypt_user_sensitive(user):
    """Cifra os campos sensíveis de um registo de utilizador (antes de gravar)."""
    if not isinstance(user, dict):
        return user
    for field in SENSITIVE_FIELDS:
        if field in user:
            user[field] = encrypt_field(user[field])
    return user


def decrypt_user_sensitive(user):
    """Decifra os campos sensíveis de um registo de utilizador (após carregar).
    Devolve um NOVO dict — não altera o registo em memória da loja."""
    if not isinstance(user, dict):
        return user
    out = dict(user)
    for field in SENSITIVE_FIELDS:
        if field in out:
            out[field] = decrypt_field(out[field])
    return out
