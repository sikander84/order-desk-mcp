from fastapi.testclient import TestClient

from order_desk.mock_api import create_app

api = TestClient(create_app())


def test_get_order_returns_raw_payload():
    resp = api.get("/orders/1001")
    assert resp.status_code == 200
    assert resp.json()["email"] == "maya@example.com"


def test_unknown_order_is_404():
    assert api.get("/orders/9999").status_code == 404


def test_find_orders_returns_all_of_a_customers_orders():
    resp = api.get("/orders", params={"email": "MAYA@example.com"})
    assert resp.status_code == 200
    assert sorted(o["id"] for o in resp.json()) == ["1001", "1003"]


def test_find_orders_unknown_email_is_empty_list():
    resp = api.get("/orders", params={"email": "nobody@example.com"})
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_return():
    resp = api.post("/returns", json={"order_id": "1001", "sku": "TEE-BLK-M", "reason": "too small"})
    assert resp.status_code == 201
    assert resp.json()["return_id"].startswith("RMA-")
    assert resp.json()["sku"] == "TEE-BLK-M"


def test_create_return_missing_field_is_422():
    resp = api.post("/returns", json={"order_id": "1001"})
    assert resp.status_code == 422


def test_create_ticket_without_order():
    resp = api.post("/tickets", json={"email": "maya@example.com", "subject": "Sizing", "description": "Do tees run small?"})
    assert resp.status_code == 201
    assert resp.json()["ticket_id"].startswith("TCK-")
    assert resp.json()["status"] == "open"


def test_create_ticket_unknown_order_is_404():
    resp = api.post("/tickets", json={"email": "a@b.com", "subject": "x", "description": "y", "order_id": "9999"})
    assert resp.status_code == 404


def test_flaky_order_returns_429_first():
    flaky = {"1001": 1}
    api2 = TestClient(create_app(flaky=flaky))
    assert api2.get("/orders/1001").status_code == 429
    assert api2.get("/orders/1001").status_code == 200
    assert flaky == {"1001": 1}  # the caller's dict was not changed