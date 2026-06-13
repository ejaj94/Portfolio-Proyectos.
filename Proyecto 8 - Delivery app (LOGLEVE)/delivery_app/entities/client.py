from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Client:
    id: Optional[int]
    restaurant_id: int
    name: str
    phone: str
    whatsapp: str = ""
    email: str = ""
    password_hash: str = ""
    address: str = ""
    map_link: Optional[str] = None
    is_email_verified: int = 0
    is_phone_verified: int = 0
    email_verification_token: str = ""
    phone_verification_pin: str = ""
    stripe_customer_id: str = ""
    verification_method: str = "email"

    def __post_init__(self) -> None:
        """Validaciones y sanitización automáticas tras la construcción del objeto."""
        # Asegurar que los campos de texto no queden como None si se omiten en la petición
        if self.name is None:
            self.name = ""
        if self.phone is None:
            self.phone = ""
        if self.whatsapp is None:
            self.whatsapp = ""
        if self.email is None:
            self.email = ""
        if self.password_hash is None:
            self.password_hash = ""

        if self.address is None:
            self.address = ""
        if self.email_verification_token is None:
            self.email_verification_token = ""
        if self.phone_verification_pin is None:
            self.phone_verification_pin = ""
        if self.stripe_customer_id is None:
            self.stripe_customer_id = ""

        if self.password_hash is None:
            self.password_hash = ""

        # Limpieza de espacios en blanco accidentales
        self.name = self.name.strip()
        self.phone = self.phone.strip()
        self.whatsapp = self.whatsapp.strip()
        self.email = self.email.strip()
        self.password_hash = self.password_hash.strip()
        self.address = self.address.strip()
        self.email_verification_token = self.email_verification_token.strip()
        self.phone_verification_pin = self.phone_verification_pin.strip()
        self.stripe_customer_id = self.stripe_customer_id.strip()
        if not hasattr(self, "verification_method") or self.verification_method is None:
            self.verification_method = "email"
        self.verification_method = self.verification_method.strip()


    def to_dict(self) -> dict:
        """Convierte la entidad a un diccionario serializable para la API JSON."""
        return {
            "id": self.id,
            "restaurant_id": self.restaurant_id,
            "name": self.name,
            "phone": self.phone,
            "whatsapp": self.whatsapp,
            "email": self.email,
            "address": self.address,
            "map_link": self.map_link,
            "is_email_verified": self.is_email_verified,
            "is_phone_verified": self.is_phone_verified,
            "email_verification_token": self.email_verification_token,
            "phone_verification_pin": self.phone_verification_pin,
            "stripe_customer_id": self.stripe_customer_id,
            "verification_method": self.verification_method
        }

