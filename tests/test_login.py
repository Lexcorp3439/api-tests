import allure
import pytest

from src import check
from src.models.api_response import ApiResponse


@allure.title("Успешная авторизация пользователя")
@pytest.mark.xfail(reason="Куки не прилетают")
def test_success_login(user, user_helper):
    by_user = user(auth=False)

    with allure.step("Авторищация пользователя по username"):
        login_response = user_helper.login(
            username=by_user.username,
            password=by_user.password,
        )
        check.ok_response(login_response)
        check.api_key(login_response)

    with allure.step("Сессия пользователя установлена"):
        api_resp = ApiResponse.from_dict(login_response.json())
        check.login_session(api_resp)


@allure.title("Авторизация пользователя с неверным логином")
@pytest.mark.xfail(reason="Всегда 200 прилетает, хотя по спеке 401")
def test_login_with_invalid_username(user, user_helper):
    by_user = user(auth=False)

    with allure.step("Авторизация пользователя по username"):
        login_response = user_helper.login(
            username=f"{by_user.username}_wrong",
            password=by_user.password,
        )
        check.error_response(login_response, 400)


@allure.title("Авторизация пользователя с неверным паролем")
@pytest.mark.xfail(reason="Всегда 200 прилетает, хотя по спеке 401")
def test_login_with_invalid_username(user, user_helper):
    by_user = user(auth=False)

    with allure.step("Авторизация пользователя по username"):
        login_response = user_helper.login(
            username=by_user.username,
            password=f"{by_user.password}_wrong",
        )
        check.error_response(login_response, 400)
