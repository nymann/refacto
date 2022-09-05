from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range

selected_range = Range(
    start=Position(line=3, character=4),
    end=Position(line=3, character=18),
)

selected_code = "shipping_price"
