from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range

selected_range = Range(
    start=Position(line=0, character=9),
    end=Position(line=0, character=18),
)
selected_code = "1 + 2 - 3"
