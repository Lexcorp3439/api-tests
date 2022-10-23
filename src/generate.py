import datetime
import random
import string

from src.models.category import Category
from src.models.order import Order, OrderStatus
from src.models.pet import Pet, PetStatus
from src.models.tags import Tag
from src.models.user import User, UserStatus


def random_string(n: int) -> str:
    return ''.join(random.choice(string.ascii_lowercase) for i in range(n))


def random_number(n: int) -> int:
    return int(''.join([str(random.randint(0, 9)) for _ in range(n)]))


def random_email(prefix: str = "") -> str:
    return f"{prefix}_{random_string(5)}@test.ru"


def random_phone():
    return f"+79{str(random_number(9))}"


def random_user(status: UserStatus = UserStatus.st1) -> User:
    return User(
        id=random_number(10),
        username=random_string(10),
        firstName=random_string(5),
        lastName=random_string(9),
        email=random_email(prefix="test"),
        password=str(random_number(5)),
        phone=random_phone(),
        userStatus=status,
    )


def random_pet(status: PetStatus) -> Pet:
    return Pet(
        id=random_number(2),
        category=Category(
            id=random_number(5),
            name=random_string(5),
        ),
        name=random_string(5),
        photoUrls=[],
        tags=[Tag(id=random_number(5), name=random_string(5)) for _ in range(random.randint(1, 6))],
        status=status,
    )


def random_order(pet_id: int, status: OrderStatus = OrderStatus.placed, complete=True) -> Order:
    return Order(
        id=random.randint(1, 11),
        petId=pet_id,
        quantity=random.randint(10, 100),
        shipDate=datetime.datetime.now().astimezone().replace(microsecond=0).isoformat(),
        status=status,
        complete=complete,
    )
