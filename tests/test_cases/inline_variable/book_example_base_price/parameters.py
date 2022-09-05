from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range

selected_range = Range(
    start=Position(line=1, character=4),
    end=Position(line=1, character=21),
)

selected_code = "inline_me_refacto"
