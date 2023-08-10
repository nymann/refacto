from lsprotocol.types import Position
from lsprotocol.types import Range

selected_range = Range(
    start=Position(line=1, character=4),
    end=Position(line=1, character=9),
)
selected_code = "1 + 2"
