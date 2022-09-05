from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range

selected_range = Range(
    start=Position(line=5, character=11),
    end=Position(line=5, character=16),
)
selected_code = "4 + 1"
