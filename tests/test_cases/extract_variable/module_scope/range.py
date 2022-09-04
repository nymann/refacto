from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range

range = Range(
    start=Position(line=2, character=0),
    end=Position(line=2, character=4),
)
