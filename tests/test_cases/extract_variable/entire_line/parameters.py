from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range

selected_range = Range(
    start=Position(line=0, character=0),
    end=Position(line=0, character=17),
)
selected_code = "1 - 3 + 2 * 4 - 2"
