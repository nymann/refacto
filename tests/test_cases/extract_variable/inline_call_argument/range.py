from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range

range = Range(
    start=Position(line=16, character=42),
    end=Position(line=16, character=77),
)
