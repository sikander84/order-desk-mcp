import json
from pathlib import Path

from order_desk.models import Order

ORDERS = json.loads((Path(__file__).parents[1] / "data" / "orders.json").read_text())


def test_all_sample_orders_parse():
    orders = [Order.model_validate(o) for o in ORDERS]
    assert len(orders) == 6


def test_dates_become_real_dates():
    order = Order.model_validate(ORDERS[0])
    assert order.created_at.year == 2026
