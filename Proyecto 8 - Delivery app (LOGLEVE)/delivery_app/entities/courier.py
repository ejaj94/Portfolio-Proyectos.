from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Courier:
    id: Optional[int]
    name: str
    nif: str
    birthdate: date
    phone: str
    whatsapp: str = ""
    email: str = ""
    vehicle: str = ""
    active: bool = True
    password_hash: str = ""
    vehicle_plate: str = ""
    id_doc: str = ""
    license_doc: str = ""
    insurance_doc: str = ""
    status: str = "pending"
    online_status: int = 0
    latitude: float = 0.0
    longitude: float = 0.0
    balance: float = 0.0
    profile_picture: str = ""

    def __post_init__(self) -> None:
        """Sanitización y control de tipos automáticos."""
        # Evitar valores None accidentales en cadenas de texto
        self.name = (self.name or "").strip()
        self.nif = (self.nif or "").strip()
        self.phone = (self.phone or "").strip()
        self.whatsapp = (self.whatsapp or "").strip()
        self.email = (self.email or "").strip()
        self.vehicle = (self.vehicle or "").strip()
        self.vehicle_plate = (self.vehicle_plate or "").strip()
        self.id_doc = (self.id_doc or "").strip()
        self.license_doc = (self.license_doc or "").strip()
        self.insurance_doc = (self.insurance_doc or "").strip()
        self.status = (self.status or "pending").strip()
        if not hasattr(self, "profile_picture") or self.profile_picture is None:
            self.profile_picture = ""
        self.profile_picture = self.profile_picture.strip()

    def disable(self) -> None:
        """Desactiva al estafeta del sistema de asignación."""
        self.active = False

    def enable(self) -> None:
        """Activa al estafeta para recibir pedidos."""
        self.active = True

    def to_dict(self) -> dict:
        """Estructura la información para respuestas de la API JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "nif": self.nif,
            "birthdate": self.birthdate.isoformat() if isinstance(self.birthdate, date) else str(self.birthdate),
            "phone": self.phone,
            "whatsapp": self.whatsapp,
            "email": self.email,
            "vehicle": self.vehicle,
            "active": self.active,
            "vehicle_plate": self.vehicle_plate,
            "id_doc": self.id_doc,
            "license_doc": self.license_doc,
            "insurance_doc": self.insurance_doc,
            "status": self.status,
            "online_status": self.online_status,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "balance": self.balance,
            "profile_picture": self.profile_picture
        }

