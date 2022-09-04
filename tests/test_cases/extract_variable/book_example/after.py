def price(order) -> float:
    a = order.quantity * order.item_price
    return (
        a
        - max(0, order.quantity - 500) * order.item_price * 0.05
        + min(a * 0.1, 100)
    )
