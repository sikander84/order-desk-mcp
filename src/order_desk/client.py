import time

import httpx

from order_desk.models import Order

RETRYABLE = {429, 500, 502, 503, 504}


class OrderAPIError(Exception):
    def __init__(self, status_code: int, detail: str):
        super().__init__(f"Order API error {status_code}: {detail}")
        self.status_code = status_code


class OrderClient:
    def __init__(
        self,
        http: httpx.Client,
        max_retries: int = 3,
        backoff: float = 0.5,
        sleep=time.sleep,
    ):
        self.http = http
        self.max_retries = max_retries
        self.backoff = backoff
        self.sleep = sleep

    def _request(self, method: str, path: str, **kwargs):
        for attempt in range(self.max_retries + 1):
            response = self.http.request(method, path, **kwargs)

            if response.status_code in RETRYABLE and attempt < self.max_retries:
                sleep_time = self.backoff * (2**attempt)
                self.sleep(sleep_time)
                continue
            return response

        return response

    @staticmethod
    def _check(resp) -> None:
        if resp.status_code >= 400:
            raise OrderAPIError(resp.status_code, resp.text[:200])

    def get_order(self, order_id: str) -> Order | None:
        resp = self._request("GET", f"/orders/{order_id}")
        if resp.status_code == 404:
            return None
        self._check(resp)
        return Order.model_validate(resp.json())

    def find_orders(self, email: str):
        resp = self._request("GET", "/orders", params={"email": email})
        self._check(resp)

        try:
            orders_data = resp.json()
        except ValueError as e:
            raise ValueError("Invalid JSON returned by Order API") from e
        return [Order.model_validate(order) for order in orders_data]

    def create_ticket(
        self, email: str, subject: str, description: str, order_id: str | None = None
    ):
        resp = self._request(
            "POST",
            "/tickets",
            json={
                "email": email,
                "subject": subject,
                "description": description,
                "order_id": order_id,
            },
        )

        self._check(resp)

        try:
            tickets = resp.json()
        except ValueError as e:
            raise ValueError("Invalid JSON returned by Order API") from e
        return tickets

    def create_return(self, order_id: str, sku: str, reason: str):
        resp = self._request(
            "POST",
            "/returns",
            json={"order_id": order_id, "sku": sku, "reason": reason},
        )

        self._check(resp)

        try:
            returns = resp.json()
        except ValueError as e:
            raise ValueError("Invalid JSON returned by Order API") from e
        return returns
