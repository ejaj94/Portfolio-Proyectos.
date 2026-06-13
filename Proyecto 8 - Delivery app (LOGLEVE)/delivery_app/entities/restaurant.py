from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Restaurant:
    id: Optional[int]
    name: str
    owner_name: str
    nif: str
    phone: str
    whatsapp: str = ""
    email: str = ""
    password_hash: str = ""
    address: str = ""
    map_link: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: str = ""
    region: str = "Porto"
    favorite_couriers: List[int] = field(default_factory=list)
    blocked_couriers: List[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Sanitización automatizada de campos de texto."""
        self.name = (self.name or "").strip()
        self.owner_name = (self.owner_name or "").strip()
        self.nif = (self.nif or "").strip()
        self.phone = (self.phone or "").strip()
        self.whatsapp = (self.whatsapp or "").strip()
        self.email = (self.email or "").strip()
        self.password_hash = (self.password_hash or "").strip()
        self.address = (self.address or "").strip()


    def add_favorite(self, courier_id: int) -> None:
        """Añade un estafeta a favoritos y lo desbloquea si estaba bloqueado."""
        if courier_id in self.blocked_couriers:
            self.blocked_couriers.remove(courier_id)
            
        if courier_id not in self.favorite_couriers:
            self.favorite_couriers.append(courier_id)

    def block_courier(self, courier_id: int) -> None:
        """Bloquea a un estafeta y lo remueve de favoritos automáticamente."""
        if courier_id in self.favorite_couriers:
            self.favorite_couriers.remove(courier_id)
            
        if courier_id not in self.blocked_couriers:
            self.blocked_couriers.append(courier_id)

    def to_dict(self) -> dict:
        """Serializa la entidad completa de forma limpia para respuestas JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "owner_name": self.owner_name,
            "nif": self.nif,
            "phone": self.phone,
            "whatsapp": self.whatsapp,
            "email": self.email,
            "address": self.address,
            "map_link": self.map_link,
            "logo_url": self.logo_url,
            "banner_url": self.banner_url,
            "region": self.region,
            "favorite_couriers": self.favorite_couriers,
            "blocked_couriers": self.blocked_couriers
        }
