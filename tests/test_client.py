import pytest

from order_desk.client import RETRYABLE, OrderAPIError
from order_desk.models import Order


def test_missing_order_returns_none(make_client):
    assert make_client().get_order("9999") is None


def test_retries_429_then_succeeds(make_client):
    client = make_client(flaky={"1001": 2})
    assert client.get_order("1001").id == "1001"
    assert client.sleeps == [0.5, 1.0]  # exponential backoff


def test_gives_up_after_max_retries(make_client):
    client = make_client(flaky={"1001": 10}, max_retries=3)
    with pytest.raises(OrderAPIError):
        client.get_order("1001")
    assert len(client.sleeps) == 3


def test_find_orders_returns_order_models(make_client):
    orders = make_client().find_orders("maya@example.com")
    assert len(orders) == 2
    assert isinstance(orders[0], Order)


def test_find_orders_unknown_email_is_empty_list(make_client):
    print(make_client().find_orders("nobody@example.com"))
    assert make_client().find_orders("nobody@example.com") == []


def test_create_return(make_client):
    r = make_client().create_return("1001", "TEE-BLK-M", "too small")
    assert r["return_id"].startswith("RMA-")


def test_create_ticket(make_client):
    t = make_client().create_ticket(
        "maya@example.com", "Damaged", "Box was crushed", "1001"
    )
    assert t["ticket_id"].startswith("TCK-")


def test_502_is_retryable():
    assert 502 in RETRYABLE
