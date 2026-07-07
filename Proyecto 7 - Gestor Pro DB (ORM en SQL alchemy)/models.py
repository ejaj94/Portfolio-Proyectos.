from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

# Definición de la clase User que representa la tabla en MySQL
class User(Base):
    # Nombre exacto de la tabla en la base de datos
    __tablename__ = "users"

    # Columna ID: Clave primaria, autoincremental y con índice para búsquedas rápidas
    id = Column(Integer, primary_key=True, index=True)
    
    # Columnas de texto con límite de 50 caracteres
    name = Column(String(50))
    last_name = Column(String(50))
    
    # Columna numérica para la edad
    age = Column(Integer)
    
    # Fecha de creación: Se genera automáticamente en el servidor MySQL al insertar el registro
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Fecha de actualización: Se actualiza automáticamente cada vez que se modifica cualquier dato del usuario
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
