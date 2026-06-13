import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from delivery_app.entities.client import Client
from delivery_app.entities.courier import Courier
from delivery_app.entities.order import Order
from delivery_app.entities.restaurant import Restaurant
from delivery_app.exceptions import EntityNotFoundError
from delivery_app.infrastructure.database import Database


def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
    """Convierte de forma segura una cadena ISO de SQLite a objeto datetime."""
    if not value:
        return None
    try:
        if value.endswith('Z'):
            value = value[:-1] + '+00:00'
        return datetime.fromisoformat(value)
    except Exception:
        return None



class SqliteRestaurantRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def add(self, restaurant: Restaurant) -> Restaurant:
        with self._database.connection() as conn:
            cursor = conn.execute(
                "INSERT INTO restaurants (name, owner_name, nif, phone, whatsapp, email, password_hash, address, map_link, logo_url, banner_url, region) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    restaurant.name,
                    restaurant.owner_name,
                    restaurant.nif,
                    restaurant.phone,
                    restaurant.whatsapp,
                    restaurant.email,
                    restaurant.password_hash,
                    restaurant.address,
                    restaurant.map_link or "",
                    restaurant.logo_url or "",
                    getattr(restaurant, "banner_url", "") or "",
                    getattr(restaurant, "region", "Porto") or "Porto",
                ),
            )
            restaurant.id = cursor.lastrowid
            self._update_courier_relations(conn, restaurant)
        return restaurant

    def get_by_id(self, restaurant_id: int) -> Restaurant:
        with self._database.connection() as conn:
            row = conn.execute("SELECT * FROM restaurants WHERE id = ?", (restaurant_id,)).fetchone()
            if row is None:
                raise EntityNotFoundError(f"Restaurante con ID {restaurant_id} no encontrado")
            
            keys = row.keys()
            restaurant = Restaurant(
                id=row["id"], name=row["name"], owner_name=row["owner_name"], nif=row["nif"],
                phone=row["phone"], whatsapp=row["whatsapp"], email=row["email"],
                password_hash=row["password_hash"],
                address=row["address"], map_link=row["map_link"], logo_url=row["logo_url"],
                banner_url=row["banner_url"] if "banner_url" in keys else "",
                region=row["region"] if "region" in keys else "Porto"
            )
            self._load_courier_relations(conn, restaurant)
            return restaurant

    def get_by_email(self, email: str) -> Optional[Restaurant]:
        with self._database.connection() as conn:
            row = conn.execute("SELECT * FROM restaurants WHERE email = ?", (email,)).fetchone()
            if row is None:
                return None
            keys = row.keys()
            restaurant = Restaurant(
                id=row["id"], name=row["name"], owner_name=row["owner_name"], nif=row["nif"],
                phone=row["phone"], whatsapp=row["whatsapp"], email=row["email"],
                password_hash=row["password_hash"],
                address=row["address"], map_link=row["map_link"], logo_url=row["logo_url"],
                banner_url=row["banner_url"] if "banner_url" in keys else "",
                region=row["region"] if "region" in keys else "Porto"
            )
            self._load_courier_relations(conn, restaurant)
            return restaurant

    def update(self, restaurant: Restaurant) -> Restaurant:
        with self._database.connection() as conn:
            conn.execute(
                """
                UPDATE restaurants 
                SET name = ?, owner_name = ?, nif = ?, phone = ?, whatsapp = ?, email = ?, password_hash = ?, 
                    address = ?, map_link = ?, logo_url = ?, banner_url = ?, region = ?
                WHERE id = ?
                """,
                (
                    restaurant.name,
                    restaurant.owner_name,
                    restaurant.nif,
                    restaurant.phone,
                    restaurant.whatsapp,
                    restaurant.email,
                    restaurant.password_hash,
                    restaurant.address,
                    restaurant.map_link or "",
                    restaurant.logo_url or "",
                    getattr(restaurant, "banner_url", "") or "",
                    getattr(restaurant, "region", "Porto") or "Porto",
                    restaurant.id
                )
            )
            self._update_courier_relations(conn, restaurant)
        return restaurant

    def list_all(self) -> List[Restaurant]:
        with self._database.connection() as conn:
            rows = conn.execute("SELECT * FROM restaurants").fetchall()
            restaurants = []
            for row in rows:
                keys = row.keys()
                restaurant = Restaurant(
                    id=row["id"], name=row["name"], owner_name=row["owner_name"], nif=row["nif"],
                    phone=row["phone"], whatsapp=row["whatsapp"], email=row["email"],
                    password_hash=row["password_hash"],
                    address=row["address"], map_link=row["map_link"], logo_url=row["logo_url"],
                    banner_url=row["banner_url"] if "banner_url" in keys else "",
                    region=row["region"] if "region" in keys else "Porto"
                )
                self._load_courier_relations(conn, restaurant)
                restaurants.append(restaurant)
            return restaurants

    def _load_courier_relations(self, conn, restaurant: Restaurant) -> None:
        favs = conn.execute("SELECT courier_id FROM restaurant_favorite_couriers WHERE restaurant_id = ?", (restaurant.id,)).fetchall()
        restaurant.favorite_couriers = [r["courier_id"] for r in favs]
        blocks = conn.execute("SELECT courier_id FROM restaurant_blocked_couriers WHERE restaurant_id = ?", (restaurant.id,)).fetchall()
        restaurant.blocked_couriers = [r["courier_id"] for r in blocks]

    def _update_courier_relations(self, conn, restaurant: Restaurant) -> None:
        conn.execute("DELETE FROM restaurant_favorite_couriers WHERE restaurant_id = ?", (restaurant.id,))
        for c_id in restaurant.favorite_couriers:
            conn.execute("INSERT INTO restaurant_favorite_couriers (restaurant_id, courier_id) VALUES (?, ?)", (restaurant.id, c_id))
        conn.execute("DELETE FROM restaurant_blocked_couriers WHERE restaurant_id = ?", (restaurant.id,))
        for c_id in restaurant.blocked_couriers:
            conn.execute("INSERT INTO restaurant_blocked_couriers (restaurant_id, courier_id) VALUES (?, ?)", (restaurant.id, c_id))


class SqliteClientRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def add(self, client: Client) -> Client:
        with self._database.connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO clients (
                    restaurant_id, name, phone, whatsapp, email, password_hash, address, map_link,
                    is_email_verified, is_phone_verified, email_verification_token,
                    phone_verification_pin, stripe_customer_id, verification_method
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    client.restaurant_id, client.name, client.phone, client.whatsapp,
                    client.email, client.password_hash, client.address, client.map_link or "",
                    client.is_email_verified, client.is_phone_verified,
                    client.email_verification_token, client.phone_verification_pin,
                    client.stripe_customer_id, getattr(client, "verification_method", "email") or "email"
                ),
            )
            client.id = cursor.lastrowid
        return client

    def get_by_id(self, client_id: int) -> Client:
        with self._database.connection() as conn:
            row = conn.execute("SELECT * FROM clients WHERE id = ?", (client_id,)).fetchone()
            if row is None:
                raise EntityNotFoundError(f"Cliente con ID {client_id} no encontrado")
            keys = row.keys()
            return Client(
                id=row["id"], restaurant_id=row["restaurant_id"], name=row["name"],
                phone=row["phone"], whatsapp=row["whatsapp"], email=row["email"],
                password_hash=row["password_hash"],
                address=row["address"], map_link=row["map_link"],
                is_email_verified=row["is_email_verified"],
                is_phone_verified=row["is_phone_verified"],
                email_verification_token=row["email_verification_token"],
                phone_verification_pin=row["phone_verification_pin"],
                stripe_customer_id=row["stripe_customer_id"],
                verification_method=row["verification_method"] if "verification_method" in keys else "email"
            )

    def get_by_email(self, email: str) -> Optional[Client]:
        with self._database.connection() as conn:
            row = conn.execute("SELECT * FROM clients WHERE email = ?", (email,)).fetchone()
            if row is None:
                return None
            keys = row.keys()
            return Client(
                id=row["id"], restaurant_id=row["restaurant_id"], name=row["name"],
                phone=row["phone"], whatsapp=row["whatsapp"], email=row["email"],
                password_hash=row["password_hash"],
                address=row["address"], map_link=row["map_link"],
                is_email_verified=row["is_email_verified"],
                is_phone_verified=row["is_phone_verified"],
                email_verification_token=row["email_verification_token"],
                phone_verification_pin=row["phone_verification_pin"],
                stripe_customer_id=row["stripe_customer_id"],
                verification_method=row["verification_method"] if "verification_method" in keys else "email"
            )

    def update(self, client: Client) -> Client:
        with self._database.connection() as conn:
            conn.execute(
                """
                UPDATE clients 
                SET restaurant_id = ?, name = ?, phone = ?, whatsapp = ?, email = ?, password_hash = ?, 
                    address = ?, map_link = ?, is_email_verified = ?, is_phone_verified = ?, 
                    email_verification_token = ?, phone_verification_pin = ?, stripe_customer_id = ?,
                    verification_method = ?
                WHERE id = ?
                """,
                (
                    client.restaurant_id, client.name, client.phone, client.whatsapp,
                    client.email, client.password_hash, client.address, client.map_link or "",
                    client.is_email_verified, client.is_phone_verified,
                    client.email_verification_token, client.phone_verification_pin,
                    client.stripe_customer_id, getattr(client, "verification_method", "email") or "email",
                    client.id
                )
            )
        return client

    def list_all(self) -> List[Client]:
        with self._database.connection() as conn:
            rows = conn.execute("SELECT * FROM clients").fetchall()
            return [Client(
                id=row["id"], restaurant_id=row["restaurant_id"], name=row["name"],
                phone=row["phone"], whatsapp=row["whatsapp"], email=row["email"],
                password_hash=row["password_hash"],
                address=row["address"], map_link=row["map_link"],
                is_email_verified=row["is_email_verified"],
                is_phone_verified=row["is_phone_verified"],
                email_verification_token=row["email_verification_token"],
                phone_verification_pin=row["phone_verification_pin"],
                stripe_customer_id=row["stripe_customer_id"],
                verification_method=row["verification_method"] if "verification_method" in row.keys() else "email"
            ) for row in rows]

    def find_by_name_or_phone(self, restaurant_id: int, term: str) -> List[Client]:
        """Busca clientes por coincidencia de nombre o teléfono bajo un restaurante."""
        with self._database.connection() as conn:
            query = """
                SELECT * FROM clients 
                WHERE restaurant_id = ? AND (name LIKE ? OR phone LIKE ?)
            """
            like_term = f"%{term}%"
            rows = conn.execute(query, (restaurant_id, like_term, like_term)).fetchall()
            return [Client(
                id=row["id"], restaurant_id=row["restaurant_id"], name=row["name"],
                phone=row["phone"], whatsapp=row["whatsapp"], email=row["email"],
                password_hash=row["password_hash"],
                address=row["address"], map_link=row["map_link"],
                is_email_verified=row["is_email_verified"],
                is_phone_verified=row["is_phone_verified"],
                email_verification_token=row["email_verification_token"],
                phone_verification_pin=row["phone_verification_pin"],
                stripe_customer_id=row["stripe_customer_id"],
                verification_method=row["verification_method"] if "verification_method" in row.keys() else "email"
            ) for row in rows]

    def add_favorite(self, client_id: int, restaurant_id: int) -> None:
        with self._database.connection() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO client_favorite_restaurants (client_id, restaurant_id) VALUES (?, ?)",
                (client_id, restaurant_id)
            )

    def remove_favorite(self, client_id: int, restaurant_id: int) -> None:
        with self._database.connection() as conn:
            conn.execute(
                "DELETE FROM client_favorite_restaurants WHERE client_id = ? AND restaurant_id = ?",
                (client_id, restaurant_id)
            )

    def list_favorites(self, client_id: int) -> List[int]:
        with self._database.connection() as conn:
            rows = conn.execute("SELECT restaurant_id FROM client_favorite_restaurants WHERE client_id = ?", (client_id,)).fetchall()
            return [r["restaurant_id"] for r in rows]





class SqliteCourierRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def add(self, courier: Courier) -> Courier:
        with self._database.connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO couriers (
                    name, nif, birthdate, phone, whatsapp, email, password_hash, vehicle, vehicle_plate,
                    id_doc, license_doc, insurance_doc, status, online_status, latitude, longitude, balance, active, profile_picture
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    courier.name, courier.nif, courier.birthdate.isoformat(),
                    courier.phone, courier.whatsapp, courier.email, courier.password_hash, courier.vehicle,
                    courier.vehicle_plate or "", courier.id_doc or "", courier.license_doc or "",
                    courier.insurance_doc or "", courier.status or "pending", courier.online_status or 0,
                    courier.latitude or 0.0, courier.longitude or 0.0, courier.balance or 0.0, int(courier.active),
                    getattr(courier, "profile_picture", "") or "",
                ),
            )
            courier.id = cursor.lastrowid
        return courier

    def get_by_id(self, courier_id: int) -> Courier:
        with self._database.connection() as conn:
            row = conn.execute("SELECT * FROM couriers WHERE id = ?", (courier_id,)).fetchone()
            if row is None:
                raise EntityNotFoundError(f"Estafeta con ID {courier_id} no encontrado")
            keys = row.keys()
            return Courier(
                id=row["id"], name=row["name"], nif=row["nif"],
                birthdate=datetime.fromisoformat(row["birthdate"]).date(),
                phone=row["phone"], whatsapp=row["whatsapp"], email=row["email"],
                password_hash=row["password_hash"], vehicle=row["vehicle"], active=bool(row["active"]),
                vehicle_plate=row["vehicle_plate"], id_doc=row["id_doc"], license_doc=row["license_doc"],
                insurance_doc=row["insurance_doc"], status=row["status"], online_status=row["online_status"],
                latitude=row["latitude"], longitude=row["longitude"], balance=row["balance"],
                profile_picture=row["profile_picture"] if "profile_picture" in keys else ""
            )

    def get_by_email(self, email: str) -> Optional[Courier]:
        with self._database.connection() as conn:
            row = conn.execute("SELECT * FROM couriers WHERE email = ?", (email,)).fetchone()
            if row is None:
                return None
            keys = row.keys()
            return Courier(
                id=row["id"], name=row["name"], nif=row["nif"],
                birthdate=datetime.fromisoformat(row["birthdate"]).date(),
                phone=row["phone"], whatsapp=row["whatsapp"], email=row["email"],
                password_hash=row["password_hash"], vehicle=row["vehicle"], active=bool(row["active"]),
                vehicle_plate=row["vehicle_plate"], id_doc=row["id_doc"], license_doc=row["license_doc"],
                insurance_doc=row["insurance_doc"], status=row["status"], online_status=row["online_status"],
                latitude=row["latitude"], longitude=row["longitude"], balance=row["balance"],
                profile_picture=row["profile_picture"] if "profile_picture" in keys else ""
            )

    def update(self, courier: Courier) -> Courier:
        with self._database.connection() as conn:
            conn.execute(
                """
                UPDATE couriers 
                SET name = ?, nif = ?, birthdate = ?, phone = ?, whatsapp = ?, email = ?, password_hash = ?, 
                    vehicle = ?, vehicle_plate = ?, id_doc = ?, license_doc = ?, insurance_doc = ?, 
                    status = ?, online_status = ?, latitude = ?, longitude = ?, balance = ?, active = ?, profile_picture = ?
                WHERE id = ?
                """,
                (
                    courier.name, courier.nif, courier.birthdate.isoformat(),
                    courier.phone, courier.whatsapp, courier.email, courier.password_hash,
                    courier.vehicle, courier.vehicle_plate or "", courier.id_doc or "",
                    courier.license_doc or "", courier.insurance_doc or "", courier.status or "pending",
                    courier.online_status or 0, courier.latitude or 0.0, courier.longitude or 0.0,
                    courier.balance or 0.0, int(courier.active), getattr(courier, "profile_picture", "") or "",
                    courier.id
                )
            )
        return courier

    def list_all(self) -> List[Courier]:
        with self._database.connection() as conn:
            rows = conn.execute("SELECT * FROM couriers").fetchall()
            return [Courier(
                id=row["id"], name=row["name"], nif=row["nif"],
                birthdate=datetime.fromisoformat(row["birthdate"]).date(),
                phone=row["phone"], whatsapp=row["whatsapp"], email=row["email"],
                password_hash=row["password_hash"], vehicle=row["vehicle"], active=bool(row["active"]),
                vehicle_plate=row["vehicle_plate"], id_doc=row["id_doc"], license_doc=row["license_doc"],
                insurance_doc=row["insurance_doc"], status=row["status"], online_status=row["online_status"],
                latitude=row["latitude"], longitude=row["longitude"], balance=row["balance"],
                profile_picture=row["profile_picture"] if "profile_picture" in row.keys() else ""
            ) for row in rows]

    def list_active(self) -> List[Courier]:
        """Devuelve la lista de estafetas marcados como activos."""
        with self._database.connection() as conn:
            rows = conn.execute("SELECT * FROM couriers WHERE active = 1").fetchall()
            return [Courier(
                id=row["id"], name=row["name"], nif=row["nif"],
                birthdate=datetime.fromisoformat(row["birthdate"]).date(),
                phone=row["phone"], whatsapp=row["whatsapp"], email=row["email"],
                password_hash=row["password_hash"], vehicle=row["vehicle"], active=bool(row["active"]),
                vehicle_plate=row["vehicle_plate"], id_doc=row["id_doc"], license_doc=row["license_doc"],
                insurance_doc=row["insurance_doc"], status=row["status"], online_status=row["online_status"],
                latitude=row["latitude"], longitude=row["longitude"], balance=row["balance"],
                profile_picture=row["profile_picture"] if "profile_picture" in row.keys() else ""
            ) for row in rows]




# 🌟 IMPLEMENTACIÓN COMPLETA Y CORRECTA DE LAS ÓRDENES CON PERSISTENCIA DE STATUS
class SqliteOrderRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def add(self, order: Order) -> Order:
        """Soporta guardar la columna status y created_at para evitar NOT NULL constraints"""
        with self._database.connection() as conn:
            status_actual = getattr(order, "status", "PENDIENTE") or "PENDIENTE"
            created_at_str = order.created_at.isoformat() if hasattr(order, "created_at") and order.created_at else datetime.now(timezone.utc).isoformat()
            cursor = conn.execute(
                "INSERT INTO orders (restaurant_id, client_id, courier_id, note, delivery_note, status, created_at, accepted_at, picked_up_at, delivered_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    order.restaurant_id,
                    order.client_id,
                    order.courier_id,
                    order.note,
                    order.delivery_note or "",
                    status_actual,
                    created_at_str,
                    order.accepted_at.isoformat() if order.accepted_at else None,
                    order.picked_up_at.isoformat() if order.picked_up_at else None,
                    order.delivered_at.isoformat() if order.delivered_at else None
                ),
            )
            order.id = cursor.lastrowid
            order.status = status_actual
        return order

    def get_by_id(self, order_id: int) -> Order:
        with self._database.connection() as conn:
            row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
            if row is None:
                raise EntityNotFoundError(f"Orden con ID {order_id} no encontrada")
            
            return Order(
                id=row["id"],
                restaurant_id=row["restaurant_id"],
                client_id=row["client_id"],
                courier_id=row["courier_id"],
                note=row["note"],
                delivery_note=row["delivery_note"] if "delivery_note" in row.keys() else "",
                status=row["status"],
                created_at=_parse_datetime(row["created_at"]),
                accepted_at=_parse_datetime(row["accepted_at"]),
                picked_up_at=_parse_datetime(row["picked_up_at"]),
                delivered_at=_parse_datetime(row["delivered_at"])
            )

    def find_by_restaurant(self, restaurant_id: int) -> List[Order]:
        """Trae de forma interactiva las comandas del negocio para el monitor"""
        with self._database.connection() as conn:
            rows = conn.execute(
                "SELECT * FROM orders WHERE restaurant_id = ? ORDER BY id DESC", 
                (restaurant_id,)
            ).fetchall()
            
            orders = []
            for row in rows:
                orders.append(Order(
                    id=row["id"],
                    restaurant_id=row["restaurant_id"],
                    client_id=row["client_id"],
                    courier_id=row["courier_id"],
                    note=row["note"],
                    delivery_note=row["delivery_note"] if "delivery_note" in row.keys() else "",
                    status=row["status"],
                    created_at=_parse_datetime(row["created_at"]),
                    accepted_at=_parse_datetime(row["accepted_at"]),
                    picked_up_at=_parse_datetime(row["picked_up_at"]),
                    delivered_at=_parse_datetime(row["delivered_at"])
                ))
            return orders

    def update(self, order: Order) -> Order:
        """Actualiza todos los campos de la orden, incluyendo marcas de tiempo y el courier asignado."""
        with self._database.connection() as conn:
            conn.execute(
                """
                UPDATE orders 
                SET restaurant_id = ?, client_id = ?, courier_id = ?, note = ?, delivery_note = ?, status = ?,
                    created_at = ?, accepted_at = ?, picked_up_at = ?, delivered_at = ?
                WHERE id = ?
                """,
                (
                    order.restaurant_id,
                    order.client_id,
                    order.courier_id,
                    order.note,
                    order.delivery_note or "",
                    order.status,
                    order.created_at.isoformat() if order.created_at else None,
                    order.accepted_at.isoformat() if order.accepted_at else None,
                    order.picked_up_at.isoformat() if order.picked_up_at else None,
                    order.delivered_at.isoformat() if order.delivered_at else None,
                    order.id
                ),
            )
        return order

    def update_status(self, order_id: int, new_status: str) -> None:
        """Cambia el estado en caliente (PATCH cocina / radar repartidores)"""
        with self._database.connection() as conn:
            conn.execute(
                "UPDATE orders SET status = ? WHERE id = ?", 
                (new_status, order_id)
            )

    def list_all(self) -> List[Order]:
        """Lista todas las órdenes registradas en el sistema."""
        with self._database.connection() as conn:
            rows = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
            orders = []
            for row in rows:
                orders.append(Order(
                    id=row["id"],
                    restaurant_id=row["restaurant_id"],
                    client_id=row["client_id"],
                    courier_id=row["courier_id"],
                    note=row["note"],
                    delivery_note=row["delivery_note"] if "delivery_note" in row.keys() else "",
                    status=row["status"],
                    created_at=_parse_datetime(row["created_at"]),
                    accepted_at=_parse_datetime(row["accepted_at"]),
                    picked_up_at=_parse_datetime(row["picked_up_at"]),
                    delivered_at=_parse_datetime(row["delivered_at"])
                ))
            return orders

    def list_pending(self) -> List[Order]:
        """Lista las órdenes pendientes que aún no han sido entregadas."""
        with self._database.connection() as conn:
            rows = conn.execute(
                "SELECT * FROM orders WHERE status NOT IN ('delivered', 'ENTREGADO') ORDER BY id DESC"
            ).fetchall()
            orders = []
            for row in rows:
                orders.append(Order(
                    id=row["id"],
                    restaurant_id=row["restaurant_id"],
                    client_id=row["client_id"],
                    courier_id=row["courier_id"],
                    note=row["note"],
                    delivery_note=row["delivery_note"] if "delivery_note" in row.keys() else "",
                    status=row["status"],
                    created_at=_parse_datetime(row["created_at"]),
                    accepted_at=_parse_datetime(row["accepted_at"]),
                    picked_up_at=_parse_datetime(row["picked_up_at"]),
                    delivered_at=_parse_datetime(row["delivered_at"])
                ))
            return orders


# --- NUEVO REPOSITORIO DE PLATOS (FASE 10) ---
from delivery_app.entities.plate import Plate

class SqlitePlateRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def add(self, plate: Plate) -> Plate:
        with self._database.connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO plates (restaurant_id, name, price, image_url, description, category, is_weekly)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (plate.restaurant_id, plate.name, plate.price, plate.image_url, plate.description, plate.category, int(plate.is_weekly))
            )
            plate.id = cursor.lastrowid
        return plate

    def list_by_restaurant(self, restaurant_id: int) -> List[Plate]:
        with self._database.connection() as conn:
            rows = conn.execute("SELECT * FROM plates WHERE restaurant_id = ? ORDER BY id DESC", (restaurant_id,)).fetchall()
            return [Plate(
                id=row["id"], restaurant_id=row["restaurant_id"], name=row["name"],
                price=row["price"], image_url=row["image_url"], description=row["description"],
                category=row["category"], is_weekly=bool(row["is_weekly"])
            ) for row in rows]

    def get_by_id(self, plate_id: int) -> Optional[Plate]:
        with self._database.connection() as conn:
            row = conn.execute("SELECT * FROM plates WHERE id = ?", (plate_id,)).fetchone()
            if row is None:
                return None
            return Plate(
                id=row["id"], restaurant_id=row["restaurant_id"], name=row["name"],
                price=row["price"], image_url=row["image_url"], description=row["description"],
                category=row["category"], is_weekly=bool(row["is_weekly"])
            )

    def delete(self, plate_id: int) -> None:
        with self._database.connection() as conn:
            conn.execute("DELETE FROM plates WHERE id = ?", (plate_id,))

