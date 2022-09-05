from dataclasses import dataclass


@dataclass
class Order:
    quantity: int
    item_price: float


def price(order: Order) -> float:
    base_price = order.quantity * order.item_price
    quantity_discount = max(0, order.quantity - 500) * order.item_price * 0.05
    shipping_cost = min(base_price * 0.1, 100)
    return base_price - quantity_discount + shipping_cost


a = [Order(quantity=3, item_price=2.5)]
print(sum(price(order=order) for order in a))
