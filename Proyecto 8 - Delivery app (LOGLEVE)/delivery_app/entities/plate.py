from dataclasses import dataclass
from typing import Optional

@dataclass
class Plate:
    id: Optional[int]
    restaurant_id: int
    name: str
    price: float
    image_url: str = ""
    description: str = ""
    category: str = "Pizzas"
    is_weekly: bool = False
