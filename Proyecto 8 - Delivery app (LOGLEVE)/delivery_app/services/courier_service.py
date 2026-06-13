from typing import List

from delivery_app.entities.courier import Courier
from delivery_app.exceptions import EntityNotFoundError, ValidationError
from delivery_app.repositories.sqlite_repository import SqliteCourierRepository


class CourierService:
    def __init__(self, courier_repository: SqliteCourierRepository) -> None:
        self._courier_repository = courier_repository

    def register(self, courier: Courier) -> Courier:
        # Validación de campos obligatorios
        if not courier.name or not courier.name.strip():
            raise ValidationError("El nombre del repartidor es obligatorio y no puede estar vacío.")
            
        # Limpieza de espacios en blanco innecesarios
        courier.name = courier.name.strip()
        if hasattr(courier, 'phone') and courier.phone:
            courier.phone = courier.phone.strip()

        return self._courier_repository.add(courier)

    def list(self) -> List[Courier]:
        return self._courier_repository.list_all()

    def list_active(self) -> List[Courier]:
        return self._courier_repository.list_active()

    def get(self, courier_id: int) -> Courier:
        # Control explícito de errores de búsqueda por ID
        try:
            return self._courier_repository.get_by_id(courier_id)
        except EntityNotFoundError as error:
            raise EntityNotFoundError(
                f"No se encontró ningún repartidor registrado con el ID {courier_id}."
            ) from error
