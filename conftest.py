import pytest

from src import generate
from src.api.pet import pet_helper as _pet_helper
from src.api.store import store_helper as _store_helper
from src.api.user import user_helper as _user_helper
from src.models.order import Order, OrderStatus
from src.models.pet import Pet, PetStatus
from src.models.user import User


@pytest.fixture()
def user_helper():
    return _user_helper


@pytest.fixture()
def pet_helper():
    return _pet_helper


@pytest.fixture()
def store_helper():
    return _store_helper


@pytest.fixture()
def user(user_helper):
    users = []

    def wrapper(auth: bool = False) -> User:
        u = generate.random_user()
        user_helper.create_user(u)

        if auth:
            user_helper.authorization(
                username=u.username,
                password=u.password,
            )
        users.append(u)

        return u

    yield wrapper

    for u in users:
        user_helper.delete_user(u.username)


@pytest.fixture()
def pet(pet_helper):
    pets = []

    def wrapper(status: PetStatus) -> Pet:
        p = generate.random_pet(status)
        pet_helper.create_pet(p)

        pets.append(p)

        return p

    yield wrapper

    for p in pets:
        pet_helper.delete_pet(p.id)


@pytest.fixture()
def order(pet, store_helper):
    orders = []

    def wrapper(
            order_status: OrderStatus,
            complete: bool = False,
            pet_status: PetStatus = PetStatus.available
    ) -> Order:
        by_pet = pet(pet_status)

        o = generate.random_order(by_pet.id, order_status, complete)
        store_helper.new_order(o)

        orders.append(o)

        return o

    yield wrapper

    for o in orders:
        store_helper.delete_order(o.id)
