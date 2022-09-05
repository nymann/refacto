from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range

selected_range = Range(
    start=Position(line=3, character=44),
    end=Position(line=3, character=79),
)

selected_code = "min(base_price * 0.1, 100)"
