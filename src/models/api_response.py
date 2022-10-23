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
        code = obj.get("code")
        type = obj.get("type")
        message = obj.get("message")
        return ApiResponse(code, type, message)