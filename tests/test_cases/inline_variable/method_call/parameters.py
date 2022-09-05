from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range

selected_range = Range(
    start=Position(line=5, character=4),
    end=Position(line=5, character=13),
)
selected_code = "inline_me"
