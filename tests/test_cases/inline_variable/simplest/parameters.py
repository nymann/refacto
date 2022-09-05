from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range

selected_range = Range(
    start=Position(line=0, character=0),
    end=Position(line=0, character=9),
)
selected_code = "inline_me"
