import allure
from requests import Response

from src import asserts, check
from src.models.api_response import ApiResponse
from src.models.user import User

from .user_client import UserClient

user_client = UserClient()


@allure.step("Создание нового пользователя")
def create_user(user: User) -> None:
    resp = user_client.create_user(user)
    check.ok_response(resp)

    api_resp = ApiResponse.from_dict(resp.json())
    check.ok_api_response(api_resp)
    asserts.is_not_none(api_resp.message, "Проверяем что идентификатор не пустой")
    asserts.equal(user.id, int(api_resp.message), "Проверяем идентификатор пользователя в ответе")


@allure.step("Удаление пользователя по username {username}")
def delete_user(username: str) -> None:
    resp = user_client.delete_user(username)
    check.ok_response(resp)

    api_resp = ApiResponse.from_dict(resp.json())
    check.ok_api_response(api_resp)

    asserts.equal(username, api_resp.message, "Проверяем имя пользователя в ответе")

@allure.step("Получение пользователя по username {username}")
def get_user(username: str) -> User:
    resp = user_client.get_user(username)
    check.ok_response(resp)

    user = User.from_dict(resp.json())
    return user


@allure.step("Авторизация пользователя {username}")
def authorization(username: str, password: str) -> str:
    resp = user_client.login(username, password)
    check.ok_response(resp)

    api_resp = ApiResponse.from_dict(resp.json())
    check.ok_api_response(api_resp)
    check.login_session(api_resp)
    session = api_resp.message.split(":")[1]
    return session


@allure.step("Попытка авторизации пользователя по {username}")
def login(username: str, password: str) -> Response:
    resp = user_client.login(username, password)
    check.ok_response(resp)
    return resp
