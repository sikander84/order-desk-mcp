import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from order_desk.client import OrderClient
from order_desk.mock_api import create_app
from order_desk.models import Order

ORDERS = json.loads((Path(__file__).parents[1] / "data" / "orders.json").read_text())


@pytest.fixture
def load_order():
    return lambda order_id: Order.model_validate(
        next(o for o in ORDERS if o["id"] == order_id)
    )


@pytest.fixture
def make_client():
    def _make(flaky=None, max_retries=3):
        sleeps = []
        client = OrderClient(
            TestClient(create_app(flaky=flaky)),
            max_retries=max_retries,
            sleep=sleeps.append,
        )
        client.sleeps = sleeps
        return client

    return _make
