from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range

range = Range(
    start=Position(line=2, character=8),
    end=Position(line=2, character=41),
)
