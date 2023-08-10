from lsprotocol.types import Position
from lsprotocol.types import Range

selected_range = Range(
    start=Position(line=2, character=0),
    end=Position(line=2, character=5),
)
selected_code = "b + c"
