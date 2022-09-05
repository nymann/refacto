def price(order) -> float:
    inline_me_refacto = order.quantity * order.item_price
    return (
        inline_me_refacto
        - max(0, order.quantity - 500) * order.item_price * 0.05
        + min(inline_me_refacto * 0.1, 100)
    )
