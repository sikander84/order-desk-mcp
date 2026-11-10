import json
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException

from order_desk.models import ReturnIn, TicketIn

DATA_FILE = Path(__file__).parents[2] / "data" / "orders.json"


def create_app(
    data_file: Path = DATA_FILE, flaky: dict[str, int] | None = None
) -> FastAPI:
    """flaky = {order_id: n} makes the first n lookups of that order return 429."""

    # Load the orders into a dict keyed by order ID, e.g. {"1001": {...}, "1002": {...}}
    all_orders = json.loads(data_file.read_text(encoding="utf-8"))
    orders = {}
    for o in all_orders:
        orders[o["id"]] = o

    # Copy the flaky settings so we never change the caller's dict
    failures_left = {}
    if flaky is not None:
        for order_id in flaky:
            failures_left[order_id] = flaky[order_id]

    # Create the FastAPI app
    app = FastAPI(title="Mock Order API")

    @app.get("/orders/{order_id}")
    def get_order(order_id: str):
        if failures_left.get(order_id, 0) > 0:
            failures_left[order_id] = failures_left[order_id] - 1
            raise HTTPException(status_code=429, detail="rate limited")
        if order_id not in orders:
            raise HTTPException(status_code=404, detail="order not found")
        return orders[order_id]

    @app.get("/orders")
    def find_orders(email: str):
        wanted = email.strip().lower()
        matches = []
        for o in orders.values():
            if o["email"].lower() == wanted:
                matches.append(o)
        return matches

    @app.post("/returns", status_code=201)
    def create_return(body: ReturnIn):
        if body.order_id not in orders:
            raise HTTPException(status_code=404, detail="order not found")

        result = body.model_dump()
        result["return_id"] = "RMA-" + uuid.uuid4().hex[:8].upper()
        return result

    @app.post("/tickets", status_code=201)
    def create_ticket(body: TicketIn):
        if body.order_id is not None and body.order_id not in orders:
                raise HTTPException(status_code=404, detail="order not found")

        result = body.model_dump()
        result["ticket_id"] = "TCK-" + uuid.uuid4().hex[:8].upper()
        result["status"] = "open"
        return result

    return app


app = create_app()
