from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Dict, Optional

from dateutil import parser


class OrderStatus(enum.Enum):
    placed = "placed"
    approved = "approved"
    delivered = "delivered"


@dataclass
class Order:
    id: Optional[int]
    petId: int
    quantity: int
    shipDate: str
    status: OrderStatus
    complete: bool

    @staticmethod
    def from_dict(obj: Dict) -> Order:
        _id = int(obj.get("id"))
        _petId = int(obj.get("petId"))
        _quantity = int(obj.get("quantity"))
        _shipDate = parser.parse(str(obj.get("shipDate"))).astimezone().replace(microsecond=0).isoformat()
        _status = OrderStatus(obj.get("status"))
        _complete = obj.get("complete")
        return Order(_id, _petId, _quantity, _shipDate, _status, _complete)

    def to_json(self) -> Dict:
        json = self.__dict__.copy()
        json["status"] = self.status.value
        json["shipDate"] = str(self.shipDate)
        return json
