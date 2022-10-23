import allure
from requests import Response

from src.config import consts
from src.models.api_response import ApiResponse


@allure.step("Проверяем что получили успешный ответ")
def ok_response(response: Response):
    assert response.status_code == 200, \
        f"Ответ пришел с ошибкой <{response.status_code}> \n" + \
        f"{response.text}"


@allure.step("Проверяем что ответ имеет статус код '{status_code}")
def error_response(response: Response, code: int):
    assert response.status_code == code, f"Ответ пришел с неожиданной кодом <{response.status_code}> ({code})"


@allure.step("Проверяем что внутренний код ответа - 200")
def ok_api_response(response: ApiResponse):
    assert response.code == 200, f"Ответ ApiResponse пришел с ошибкой <{response.code}>"


def response_code(response: Response, expected_code: int):
    assert response.status_code == expected_code, f"Ответ пришел с кодом <{response.status_code}>"


def login_session(response: ApiResponse) -> str:
    message_sections = response.message.split(":")
    assert len(message_sections) == 2, "Отсутствует сессия пользователя"
    session = message_sections[1]
    assert session != "", "Пустая сессия пользователя"
    return session


def api_key(response: Response):
    assert response.cookies.get(name=consts.COOKIE_HEADER), f"Куки не были установлены"
    assert response.cookies.get(name=consts.RATE_LIMIT_HEADER), f"Хедер '{consts.RATE_LIMIT_HEADER}' отсутствует"
    assert response.cookies.get(name=consts.EXPIRES_AFTER_HEADER), f"Хедер '{consts.EXPIRES_AFTER_HEADER}' отсутствует"
