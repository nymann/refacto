from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range

from refacto.exceptions import InvalidRangeError


def get_chars_in_range(selected_range: Range, source: str) -> str:
    start: Position = selected_range.start
    end: Position = selected_range.end
    if start == end:
        raise InvalidRangeError("Single character range select, is not supported")
    lines = source.splitlines()[start.line : end.line + 1]
    if start.line == end.line:
        return "".join(lines)[start.character : end.character + 1]

    raise InvalidRangeError("Multi-line range selection is not supported")
