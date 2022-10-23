import allure

from src import asserts, check
from src.models.api_response import ApiResponse
from src.models.pet import Pet

from .pet_client import PetClient

pet_client = PetClient()


@allure.step("Создание нового питомца")
def create_pet(pet: Pet) -> None:
    resp = pet_client.create_pet(pet)
    check.ok_response(resp)

    resp_pet = Pet.from_dict(resp.json())
    asserts.equal(pet, resp_pet, "Питомцы совпадают", "Не совпадает идентификатор питомца")

    # Такое приходится добавлять, тк код 200 внезапно не означает, что питомец создался...
    resp = pet_client.get_pet_by_id(pet.id)
    resp_pet = Pet.from_dict(resp.json())
    asserts.equal(pet, resp_pet, "Питомцы совпадают", "Не совпадает идентификатор питомца")


@allure.step("Удаление питомца")
def delete_pet(pet_id: int):
    resp = pet_client.delete_pet(pet_id)
    check.ok_response(resp)

    api_resp = ApiResponse.from_dict(resp.json())
    check.ok_api_response(api_resp)
    asserts.equal(pet_id, int(api_resp.message), "Идентификатор удаленного питомца совпадает")
