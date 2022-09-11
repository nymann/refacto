def price(order) -> float:
    base_price = order.quantity * order.item_price
    quantity_discount = max(0, order.quantity - 500) * order.item_price * 0.05
    rename_me = min(base_price * 0.1, 100)
    return base_price - quantity_discount + rename_me
