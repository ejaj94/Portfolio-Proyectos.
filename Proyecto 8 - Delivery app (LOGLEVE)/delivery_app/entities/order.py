from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Order:
    id: Optional[int]
    restaurant_id: int
    client_id: int
    courier_id: Optional[int]
    note: Optional[str]
    delivery_note: Optional[str] = ""
    status: str = "created"
    
    # Uso correcto de la API de tiempo moderna con zona horaria UTC explícita
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    accepted_at: Optional[datetime] = None
    picked_up_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Sanitización del campo de notas obligatorias/opcionales."""
        if self.note:
            self.note = self.note.strip()
        else:
            self.note = ""

    def pagar_y_preparar(self) -> None:
        """Cambia el estado a PENDIENTE tras confirmarse el pago."""
        self.status = "PENDIENTE"

    def start_cooking(self) -> None:
        """Pasa la orden a cocina para ser cocinada."""
        self.status = "EN_PREPARACION"

    def complete_cooking(self) -> None:
        """Marca la comida como lista para recoger."""
        self.status = "LISTO_PARA_RECOGER"

    def accept(self, courier_id: int) -> None:
        """Asigna un estafeta al pedido y actualiza el estado."""
        if self.status != "LISTO_PARA_RECOGER":
            raise ValueError("El pedido debe estar listo para recoger antes de ser asignado a un repartidor.")
        self.courier_id = courier_id
        self.status = "accepted"
        self.accepted_at = datetime.now(timezone.utc)

    def start_delivery(self) -> None:
        """Cambia el estado a recogida cuando el repartidor toma los productos."""
        if self.status != "accepted":
            raise ValueError("El pedido debe ser aceptado por un repartidor antes de iniciar el reparto.")
        self.status = "picked_up"
        self.picked_up_at = datetime.now(timezone.utc)

    def complete_delivery(self) -> None:
        """Finaliza el flujo marcando el pedido como entregado al cliente."""
        if self.status != "picked_up":
            raise ValueError("El pedido debe estar en reparto antes de marcarlo como entregado.")
        self.status = "delivered"
        self.delivered_at = datetime.now(timezone.utc)

    def start(self) -> None:
        """Soporta tanto iniciar la cocina como iniciar el reparto según el estado actual."""
        if self.status in ("PENDIENTE", "created"):
            self.start_cooking()
        elif self.status == "accepted":
            self.start_delivery()
        else:
            raise ValueError(f"No se puede iniciar el pedido en el estado actual: {self.status}")

    def complete(self) -> None:
        """Soporta tanto completar la cocina como completar el reparto según el estado actual."""
        if self.status == "EN_PREPARACION":
            self.complete_cooking()
        elif self.status == "picked_up":
            self.complete_delivery()
        else:
            raise ValueError(f"No se puede completar el pedido en el estado actual: {self.status}")

    def to_dict(self) -> dict:
        """Serializa la entidad de forma segura sin romper la función jsonify de Flask."""
        return {
            "id": self.id,
            "restaurant_id": self.restaurant_id,
            "client_id": self.client_id,
            "courier_id": self.courier_id,
            "note": self.note,
            "delivery_note": self.delivery_note,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "accepted_at": self.accepted_at.isoformat() if self.accepted_at else None,
            "picked_up_at": self.picked_up_at.isoformat() if self.picked_up_at else None,
            "delivered_at": self.delivered_at.isoformat() if self.delivered_at else None
        }

