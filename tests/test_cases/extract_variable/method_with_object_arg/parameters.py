from lsprotocol.types import Position
from lsprotocol.types import Range

selected_range = Range(
    start=Position(line=1, character=11),
    end=Position(line=1, character=44),
)
selected_code = "order.quantity * order.item_price"
