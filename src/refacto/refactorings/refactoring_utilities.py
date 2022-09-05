from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range

from refacto.exceptions import InvalidRangeError


def get_selected_range_source_code(selected_range: Range, source: str) -> str:
    start: Position = selected_range.start
    end: Position = selected_range.end
    if start == end:
        raise InvalidRangeError("Single character range select, is not supported")
    lines = source.splitlines()[start.line : end.line + 1]
    if start.line == end.line:
        return "".join(lines)[start.character : end.character]

    raise InvalidRangeError("Multi-line range selection is not supported")
