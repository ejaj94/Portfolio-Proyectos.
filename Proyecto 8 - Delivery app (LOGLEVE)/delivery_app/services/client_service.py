from typing import List

from delivery_app.entities.client import Client
from delivery_app.exceptions import EntityNotFoundError, ValidationError
from delivery_app.repositories.sqlite_repository import SqliteClientRepository, SqliteRestaurantRepository


class ClientService:
    def __init__(
        self,
        client_repository: SqliteClientRepository,
        restaurant_repository: SqliteRestaurantRepository,
    ) -> None:
        self._client_repository = client_repository
        self._restaurant_repository = restaurant_repository

    def register(self, client: Client) -> Client:
        # Validación de datos básicos de entrada antes de tocar la base de datos
        if not client.name or not client.name.strip():
            raise ValidationError("El nombre del cliente no puede estar vacío.")
            
        self._ensure_restaurant_exists(client.restaurant_id)
        return self._client_repository.add(client)

    def list(self) -> List[Client]:
        return self._client_repository.list_all()

    def search(self, restaurant_id: int, term: str) -> List[Client]:
        if not term or not term.strip():
            return self._client_repository.list_all() # Retorna todos si el buscador está vacío
            
        self._ensure_restaurant_exists(restaurant_id)
        return self._client_repository.find_by_name_or_phone(restaurant_id, term.strip())

    def _ensure_restaurant_exists(self, restaurant_id: int) -> None:
        try:
            self._restaurant_repository.get_by_id(restaurant_id)
        except EntityNotFoundError as error:
            # Mensaje explícito y estructurado para que el frontend pueda pintarlo fácilmente
            raise ValidationError(
                f"Operación inválida: El restaurante con ID {restaurant_id} no existe en el sistema."
            ) from error
