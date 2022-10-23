from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class ApiResponse:
    code: int
    type: str
    message: str

    @staticmethod
    def from_dict(obj: Dict) -> ApiResponse:
        _code = obj.get("code")
        _type = obj.get("type")
        _message = obj.get("message")
        return ApiResponse(_code, _type, _message)