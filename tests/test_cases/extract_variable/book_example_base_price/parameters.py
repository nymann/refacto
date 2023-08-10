from lsprotocol.types import Position
from lsprotocol.types import Range

selected_range = Range(
    start=Position(line=2, character=8),
    end=Position(line=2, character=41),
)

selected_code = "order.quantity * order.item_price"
