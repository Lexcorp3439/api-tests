from requests import Request, Response

from src.models.user import User

from ..helper import Method
from ..http_client import HttpClient


class UserClient(HttpClient):

    def create_user(self, user: User) -> Response:
        request_json = user.to_json()

        req = Request(
            url="/user",
            method=Method.POST,
            json=request_json,
        )
        return self.send_request(req)

    def delete_user(self, username: str) -> Response:
        req = Request(
            url=f"/user/{username}",
            method=Method.DELETE,
        )
        return self.send_request(req)

    def get_user(self, username: str) -> Response:
        req = Request(
            url=f"/user/{username}",
            method=Method.GET,
        )
        return self.send_request(req)

    def login(self, username: str, password: str) -> Response:
        req = Request(
            url=f"/user/login",
            method=Method.GET,
            params={
                "username": username,
                "password": password,
            }
        )
        return self.send_request(req)
