from datetime import date, datetime

from pydantic import BaseModel, Field


class LineItem(BaseModel):
    sku: str
    title: str
    variant_title: str | None = None  # May be null or missing
    quantity: int
    price: str
    final_sale: bool = False


class Fulfillments(BaseModel):
    shipment_status: str
    tracking_company: str | None = None
    tracking_numbers: str | None = None
    tracking_url: str | None = None
    estimated_delivery_at: date | None = None
    delivered_at: datetime | None = None


class Order(BaseModel):
    id: str
    email: str
    created_at: datetime
    cancelled_at: datetime | None = None
    line_items: list[LineItem]
    fulfillments: list[Fulfillments] = Field(default_factory=list)


class ItemSummary(BaseModel):
    sku: str
    name: str
    quantity: int


class OrderSummary(BaseModel):
    order_id: str
    status: str
    carrier: str | None = None
    tracking_url: str | None = None
    eta: date | None = None
    delivered_on: date | None = None
    items: list[ItemSummary]


class ReturnDecision(BaseModel):
    eligible: bool
    reason: str


class ReturnIn(BaseModel):
    order_id: str
    sku: str
    reason: str


class TicketIn(BaseModel):
    order_id: str | None = None
    email: str
    subject: str
    description: str
