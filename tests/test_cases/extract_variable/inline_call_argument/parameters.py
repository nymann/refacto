from lsprotocol.types import Position
from lsprotocol.types import Range

selected_range = Range(
    start=Position(line=16, character=42),
    end=Position(line=16, character=77),
)
selected_code = "[Order(quantity=3, item_price=2.5)]"
