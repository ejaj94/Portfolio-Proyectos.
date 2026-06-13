from typing import List, Optional

from delivery_app.entities.order import Order
from delivery_app.exceptions import BusinessRuleError, EntityNotFoundError, ValidationError
from delivery_app.repositories.sqlite_repository import (
    SqliteClientRepository,
    SqliteCourierRepository,
    SqliteOrderRepository,
    SqliteRestaurantRepository,
)


class OrderService:
    def __init__(
        self,
        order_repository: SqliteOrderRepository,
        restaurant_repository: SqliteRestaurantRepository,
        client_repository: SqliteClientRepository,
        courier_repository: SqliteCourierRepository,
    ) -> None:
        self._order_repository = order_repository
        self._restaurant_repository = restaurant_repository
        self._client_repository = client_repository
        self._courier_repository = courier_repository

    def create(self, order: Order) -> Order:
        self._ensure_restaurant_exists(order.restaurant_id)
        self._ensure_client_exists(order.client_id)
        if not order.status or order.status == "created":
            order.status = "PENDIENTE"
        return self._order_repository.add(order)

    def list(self) -> List[Order]:
        return self._order_repository.list_all()

    def get(self, order_id: int) -> Order:
        return self._order_repository.get_by_id(order_id)

    # 🌟 NUEVO MÉTODO: Procesa el pago y envía a preparación usando tus métodos
    def process_payment(self, order_id: int) -> Order:
        """Modifica el estado del pedido a PENDIENTE tras el pago del cliente."""
        order = self.get(order_id)
        
        # Invocamos la lógica de negocio que añadimos a la entidad
        order.pagar_y_preparar()
        
        # Persistimos el estado completo en la base de datos
        return self._order_repository.update(order)


    def assign_courier(self, order_id: int, courier_id: int) -> Order:
        order = self.get(order_id)
        courier = self._courier_repository.get_by_id(courier_id)
        if not courier.active:
            raise BusinessRuleError("El estafeta no está activo.")
        order.accept(courier.id)
        return self._order_repository.update(order)

    def start(self, order_id: int) -> Order:
        order = self.get(order_id)
        order.start()
        return self._order_repository.update(order)

    def complete(self, order_id: int) -> Order:
        order = self.get(order_id)
        order.complete()
        updated_order = self._order_repository.update(order)
        if order.courier_id:
            try:
                courier = self._courier_repository.get_by_id(order.courier_id)
                fare = getattr(order, "fare_amount", 3.50) or 3.50
                courier.balance = (getattr(courier, "balance", 0.0) or 0.0) + fare
                self._courier_repository.update(courier)
            except Exception as e:
                print(f"[warning] failed to credit courier: {e}")
        return updated_order


    def list_pending(self) -> List[Order]:
        return self._order_repository.list_pending()

    def _ensure_restaurant_exists(self, restaurant_id: int) -> None:
        self._restaurant_repository.get_by_id(restaurant_id)

    def _ensure_client_exists(self, client_id: int) -> None:
        self._client_repository.get_by_id(client_id)

    def select_courier(self, blocked: Optional[List[int]] = None) -> Optional[int]:
        couriers = self._courier_repository.list_active()
        blocked = blocked or []
        for courier in couriers:
            if courier.id not in blocked:
                return courier.id
        return None
