import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Localizamos y cargamos el archivo .env para seguridad de credenciales
dotenv_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path)

# 2. Obtenemos las variables de entorno (si no existen, usa valores por defecto)
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
DATABASE_USER = os.getenv("DATABASE_USER", "root")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "3306")
DATABASE_NAME = os.getenv("DATABASE_NAME", "Clase1")

# 3. Construimos la URL de conexión dinámicamente según si hay password o no
if DATABASE_PASSWORD:
    DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
else:
    DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# 4. El Engine es el "motor" que se comunica directamente con MySQL
# echo=True permite ver en consola las consultas SQL reales que se ejecutan
engine = create_engine(DATABASE_URL, echo=True)

# 5. SessionLocal es la "fábrica" de sesiones para realizar consultas
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# 6. Base es la clase de la cual heredarán todos nuestros modelos (tablas)
Base = declarative_base()

# 7. Función generadora para obtener una sesión de DB y cerrarla automáticamente
def get_db():
    db = SessionLocal()
    try:
        yield db  # Entrega la sesión para ser usada
    finally:
        db.close() # Se asegura de cerrar la conexión al terminar
