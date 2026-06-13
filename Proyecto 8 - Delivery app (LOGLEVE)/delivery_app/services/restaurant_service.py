from typing import List

from delivery_app.entities.restaurant import Restaurant
from delivery_app.exceptions import EntityNotFoundError
from delivery_app.repositories.sqlite_repository import SqliteRestaurantRepository


class RestaurantService:
    def __init__(self, restaurant_repository: SqliteRestaurantRepository) -> None:
        self._restaurant_repository = restaurant_repository

    def register(self, restaurant: Restaurant) -> Restaurant:
        return self._restaurant_repository.add(restaurant)

    def get(self, restaurant_id: int) -> Restaurant:
        try:
            return self._restaurant_repository.get_by_id(restaurant_id)
        except EntityNotFoundError as error:
            raise EntityNotFoundError(f"Restaurante {restaurant_id} no encontrado.") from error

    def list(self) -> List[Restaurant]:
        return self._restaurant_repository.list_all()
