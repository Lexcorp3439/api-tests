from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Tag:
    id: int
    name: str

    @staticmethod
    def from_dict(obj: Any) -> Tag:
        _id = int(obj.get("id"))
        _name = str(obj.get("name"))
        return Tag(_id, _name)

    def to_json(self) -> Dict:
        return self.__dict__.copy()
