import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Localizamos y cargamos el archivo .env para seguridad de credenciales
dotenv_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path)

# 2. Obtenemos las variables de entorno (si no existen, usa valores por defecto)
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
DATABASE_USER = os.getenv("DATABASE_USER", "root")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "3306")
DATABASE_NAME = os.getenv("DATABASE_NAME", "Clase1")

# 3. Base para modelos ORM
Base = declarative_base()

# Global variables for Engine and Session status
CURRENT_DB_TYPE = "MySQL"

def _init_engine():
    global CURRENT_DB_TYPE
    # Intentamos primero la conexión a MySQL
    if DATABASE_PASSWORD:
        mysql_url = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    else:
        mysql_url = f"mysql+pymysql://{DATABASE_USER}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    
    try:
        eng = create_engine(mysql_url, echo=False, connect_args={"connect_timeout": 3})
        # Prueba de vida de conexión
        with eng.connect() as conn:
            conn.execute(text("SELECT 1"))
        CURRENT_DB_TYPE = "MySQL"
        print("[OK] Conectado exitosamente a MySQL")
        return eng
    except Exception as e:
        print(f"[!] No se pudo conectar a MySQL. Conmutando a SQLite local...")
        sqlite_file = Path(__file__).resolve().parent / "gestor_pro.db"
        sqlite_url = f"sqlite:///{sqlite_file}"
        eng = create_engine(sqlite_url, echo=False, connect_args={"check_same_thread": False})
        CURRENT_DB_TYPE = "SQLite (Local)"
        print(f"[OK] Conectado a SQLite local: {sqlite_file}")
        return eng

engine = _init_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db_type():
    """Retorna el tipo de base de datos actualmente activa (MySQL o SQLite)."""
    return CURRENT_DB_TYPE

def get_db():
    """Función generadora para obtener una sesión de DB y cerrarla automáticamente."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

