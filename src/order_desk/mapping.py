from order_desk.models import ItemSummary, Order, OrderSummary


def order_status(orderData: Order) -> str:

    if orderData.cancelled_at is not None:
        orderStatus = "cancelled"
    elif not orderData.fulfillments:
        orderStatus = "processing"
    elif orderData.fulfillments[-1].shipment_status == "delivered":
        orderStatus = "delivered"
    else:
        orderStatus = "shipped"

    return orderStatus


def to_order_summary(orderData: Order) -> OrderSummary:
    order_id = orderData.id
    status = order_status(orderData)
    items = [
        ItemSummary(
            sku=i.sku,
            quantity=i.quantity,
            name=i.title if not i.variant_title else f"{i.title} ({i.variant_title})",
        )
        for i in orderData.line_items
    ]

    if orderData.fulfillments:
        f = orderData.fulfillments[-1]
        carrier = f.tracking_company
        tracking_url = f.tracking_url
        delivered_on = f.delivered_at.date() if f.delivered_at else None
        if not delivered_on:
            eta = orderData.fulfillments[-1].estimated_delivery_at
        else:
            eta = None
    else:
        carrier = None
        tracking_url = None
        eta = None
        delivered_on = None

    return OrderSummary(
        order_id=order_id,
        status=status,
        carrier=carrier,
        tracking_url=tracking_url,
        eta=eta,
        delivered_on=delivered_on,
        items=items,
    )
