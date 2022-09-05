from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range

selected_range = Range(
    start=Position(line=5, character=11),
    end=Position(line=5, character=32),
)
selected_code = "add(1, 2) + add(3, 4)"
