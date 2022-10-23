from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Dict, Optional


class UserStatus(enum.Enum):
    st1 = 0
    st2 = 0
    st3 = 0


@dataclass
class User:
    id: Optional[int]
    username: str
    firstName: str
    lastName: str
    email: str
    password: str
    phone: str
    userStatus: UserStatus

    @staticmethod
    def from_dict(obj: dict) -> User:
        _id = int(obj.get("id"))
        _username = str(obj.get("username"))
        _firstName = str(obj.get("firstName"))
        _lastName = str(obj.get("lastName"))
        _email = str(obj.get("email"))
        _password = str(obj.get("password"))
        _phone = str(obj.get("phone"))
        _userStatus = UserStatus(int(obj.get("userStatus")))
        return User(_id, _username, _firstName, _lastName, _email, _password, _phone, _userStatus)

    def to_json(self) -> Dict:
        json = self.__dict__.copy()
        json["userStatus"] = self.userStatus.value
        return json
