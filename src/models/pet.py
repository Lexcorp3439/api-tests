from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Any, Dict, List

from src.models.category import Category
from src.models.tags import Tag


class PetStatus(enum.Enum):
    available = "available"
    pending = "pending"
    sold = "sold"


@dataclass
class Pet:
    id: int
    category: Category
    name: str
    photoUrls: List[str]
    tags: List[Tag]
    status: PetStatus

    @staticmethod
    def from_dict(obj: Any) -> Pet:
        _id = int(obj.get("id"))
        _category = Category.from_dict(obj.get("category"))
        _name = str(obj.get("name"))
        _photoUrls = obj.get("photoUrls")
        _tags = [Tag.from_dict(y) for y in obj.get("tags")]
        _status = PetStatus(str(obj.get("status")))
        return Pet(_id, _category, _name, _photoUrls, _tags, _status)

    def to_json(self) -> Dict:
        json = self.__dict__.copy()
        json["status"] = self.status.value
        json["tags"] = [t.to_json() for t in self.tags]
        json["category"] = self.category.to_json()
        return json
