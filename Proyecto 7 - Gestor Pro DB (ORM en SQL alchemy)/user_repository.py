from sqlalchemy.orm import Session
from models import User

class UserRepository:
    def __init__(self, db: Session):
        # Recibimos la sesión de la base de datos (Inyección de Dependencias)
        self.db = db

    def get_all(self):
        """Retorna la lista completa de usuarios desde la base de datos"""
        return self.db.query(User).all()

    def get_by_id(self, user_id: int):
        """Busca un usuario específico por su ID. Retorna None si no existe"""
        return self.db.query(User).filter(User.id == user_id).first()

    def add(self, name: str, last_name: str, age: int):
        """
        Crea un nuevo usuario asegurando que los nombres tengan 
        formato de título (Mayúscula inicial).
        """
        # .strip() elimina espacios accidentales y .title() pone Mayúsculas iniciales
        new_user = User(
            name=name.strip().title(), 
            last_name=last_name.strip().title(), 
            age=age
        )
        self.db.add(new_user) # Prepara la inserción
        self.db.commit()      # Guarda los cambios en MySQL
        self.db.refresh(new_user) # Actualiza el objeto con datos del servidor (como el ID)
        return new_user

    def delete(self, user_id: int):
        """Elimina un usuario de la base de datos si el ID existe"""
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit() # Confirma la eliminación
            return True
        return False

    def update(self, user_id: int, name: str = None, last_name: str = None, age: int = None):
        """
        Actualiza de forma flexible. Solo modifica los campos que no sean None.
        """
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        # Lógica de actualización parcial: si el usuario no envió un dato, se queda el actual
        if name:
            user.name = name.strip().title()
        if last_name:
            user.last_name = last_name.strip().title()
        if age is not None:
            user.age = age
            
        self.db.commit()      # Guarda las modificaciones
        self.db.refresh(user) # Refresca el objeto para confirmar los cambios
        return user # IMPORTANTE: Retorna el objeto actualizado para el reporte
