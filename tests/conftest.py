import json
from pathlib import Path

import pytest

from order_desk.models import Order

ORDERS = json.loads((Path(__file__).parents[1] / "data" / "orders.json").read_text())


@pytest.fixture
def load_order():
    return lambda order_id: Order.model_validate(
        next(o for o in ORDERS if o["id"] == order_id)
    )
