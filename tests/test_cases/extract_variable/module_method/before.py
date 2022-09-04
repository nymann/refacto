from dataclasses import dataclass


@dataclass
class Order:
    item_price: float
    quantity: int


def price(order: Order) -> float:
    # price is base price - quantity discount + shipping
    return (
        order.quantity * order.item_price
        - max(0, order.quantity - 500) * order.item_price * 0.05
        + min(order.quantity * order.item_price * 0.1, 100)
    )
