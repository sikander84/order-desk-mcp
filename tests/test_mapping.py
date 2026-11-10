from order_desk.mapping import to_order_summary


def test_delivered_order(load_order):
    s = to_order_summary(load_order("1001"))
    assert s.status == "delivered"
    assert s.carrier == "Canada Post"
    assert str(s.delivered_on) == "2026-10-20"
    assert s.eta is None  # no ETA once delivered
    # print(s.items[0].title)
    assert s.items[0].name == "Cotton Tee (Black / M)"


def test_in_transit_order_has_eta(load_order):
    s = to_order_summary(load_order("1002"))
    assert s.status == "shipped"
    assert str(s.eta) == "2026-11-08"


def test_unfulfilled_order_is_processing(load_order):
    s = to_order_summary(load_order("1003"))
    assert s.status == "processing"
    assert s.carrier is None and s.tracking_url is None


def test_cancelled_wins_over_everything(load_order):
    assert to_order_summary(load_order("1004")).status == "cancelled"


def test_item_without_variant_uses_title_only(load_order):
    order = load_order("1001")
    order.line_items[0].variant_title = None
    s = to_order_summary(order)
    assert s.items[0].name == "Cotton Tee"
