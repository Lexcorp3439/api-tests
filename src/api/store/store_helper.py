import allure
from requests import Response

from src import asserts, check
from src.api.store.store_client import StoreClient
from src.models.order import Order

store_client = StoreClient()


@allure.step("Попытка создания нового заказа")
def create_order(order: Order) -> Response:
    resp = store_client.create_order(order)
    return resp


@allure.step("Создание нового заказа")
def new_order(order: Order) -> None:
    resp = store_client.create_order(order)
    check.ok_response(resp)

    resp_order = Order.from_dict(resp.json())
    asserts.equal(order, resp_order, "Заказы совпадают")


@allure.step("Получение заказа по идентификатору {id}")
def get_order(id: int) -> Order:
    resp = store_client.get_order(id)
    check.ok_response(resp)

    ord = Order.from_dict(resp.json())
    return ord


@allure.step("Удаление заказа")
def delete_order(order_id: int):
    resp = store_client.delete_order(order_id)
    check.ok_response(resp)
