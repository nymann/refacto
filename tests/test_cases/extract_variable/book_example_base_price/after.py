def price(order) -> float:
    rename_me = order.quantity * order.item_price
    return (
        rename_me
        - max(0, order.quantity - 500) * order.item_price * 0.05
        + min(rename_me * 0.1, 100)
    )
