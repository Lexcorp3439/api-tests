from typing import Any, Optional

import allure

from src.config import config, consts


def __assert_wrapper(value: Any, err_msg: str, limit_msg: int = config.MAX_ERROR_LENGTH) -> None:
    if not value:
        raise AssertionError(err_msg[:limit_msg])


@allure.step("(equal) {message}")
def equal(
        actual: Any,
        expected: Any,
        message: str,
        error_message: Optional[str] = None,
):
    if error_message is None:
        error_message = f"(equal) {message}\nactual: '{actual}'\nexpected: '{expected}'"
    __assert_wrapper(actual == expected, err_msg=error_message)


@allure.step("(not_equal) {message}")
def not_equal(actual: Any, expected: Any, message: str) -> None:
    __assert_wrapper(
        actual != expected, f"(not_equal) {message}\nactual: '{actual}'\nexpected: '{expected}'"
    )

@allure.step("(is_none) {message}")
def is_none(value: Any, message: str) -> None:
    try:
        __assert_wrapper(value is None, f"(is_none) {message}\nvalue: <in attachment>")
    except AssertionError:
        allure.attach(str(value), "value", attachment_type=consts.TEXT)
        raise


@allure.step("(is_not_none) {message}")
def is_not_none(value: Any, message: str) -> None:
    try:
        __assert_wrapper(value is not None, f"(is_not_none) {message}\nvalue: <in attachment>")
    except AssertionError:
        allure.attach(str(value), "value", attachment_type=consts.TEXT)
        raise
