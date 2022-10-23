from requests import Request, Response

from src.models.pet import Pet, PetStatus

from ..helper import Method
from ..http_client import HttpClient


class PetClient(HttpClient):

    def create_pet(self, pet: Pet) -> Response:
        request_json = pet.to_json()

        req = Request(
            url="/pet",
            method=Method.POST,
            json=request_json,
        )
        return self.send_request(req)

    def get_pet_by_id(self, pet_id: int) -> Response:
        req = Request(
            url=f"/pet/{pet_id}",
            method=Method.GET,
        )
        return self.send_request(req)

    def get_pet_by_status(self, status: PetStatus) -> Response:
        req = Request(
            url="/pet/findByStatus",
            method=Method.GET,
            params={
                "status": status.value
            }
        )
        return self.send_request(req)

    def update_pet_in_store(self, pet_id: int, name: str = None, status: PetStatus = None) -> Response:
        request_json = {}
        if name:
            request_json["name"] = name
        if status:
            request_json["status"] = status.value
        req = Request(
            url=f"/pet/{pet_id}",
            method=Method.POST,
            json=request_json,
        )
        return self.send_request(req)

    def delete_pet(self, pet_id: int) -> Response:
        req = Request(
            url=f"/pet/{pet_id}",
            method=Method.DELETE,
        )
        return self.send_request(req)