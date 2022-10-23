from requests import Request, Response

from src.api.helper import Method
from src.api.http_client import HttpClient
from src.models.order import Order


class StoreClient(HttpClient):

    def create_order(self, order: Order) -> Response:
        request_json = order.to_json()

        req = Request(
            url="/store/order",
            method=Method.POST,
            json=request_json,
        )
        return self.send_request(req)

    def get_order(self, order_id: int) -> Response:
        req = Request(
            url=f"/store/order/{order_id}",
            method=Method.GET,
        )
        return self.send_request(req)

    def delete_order(self, order_id: int) -> Response:
        req = Request(
            url=f"/store/order/{order_id}",
            method=Method.DELETE,
        )
        return self.send_request(req)