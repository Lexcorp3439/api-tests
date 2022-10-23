import allure
import pytest

from src import asserts, check, generate
from src.models.order import Order, OrderStatus
from src.models.pet import PetStatus


@allure.title("Успешное выставление заказа")
@pytest.mark.parametrize("order_status", [OrderStatus.placed, OrderStatus.approved, OrderStatus.delivered])
def test_success_place_orders(user, order, store_helper, order_status):
    user(auth=True)

    with allure.step(f"Выставление заказа на питомца со статусом {order_status}"):
        by_order = order(order_status)

    with allure.step("Проверяем что заказ успешно сохранен"):
        resp_order = store_helper.get_order(by_order.id)
        asserts.equal(by_order, resp_order, "Проверка заказов на соответствие")


@allure.title("Успешное выставление заказа на питомцев c разными статусами")
@pytest.mark.parametrize("pet_status", [PetStatus.available, PetStatus.sold, PetStatus.pending])
def test_success_place_orders_with_diff_pets(user, order, store_helper, pet_status):
    user(auth=True)

    with allure.step("Выставление заказа на питомца"):
        by_order = order(OrderStatus.placed, pet_status=pet_status)

    with allure.step("Проверяем что заказ успешно сохранен"):
        resp_order = store_helper.get_order(by_order.id)
        asserts.equal(by_order, resp_order, "Проверка заказов на соответствие")
