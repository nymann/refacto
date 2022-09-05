from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range

from refacto.exceptions import InvalidRangeError


def souce_code_in_range(code_range: Range, source: str) -> str:
    start: Position = code_range.start
    end: Position = code_range.end
    if start == end:
        raise InvalidRangeError("Single character range select, is not supported")
    lines = source.splitlines()[start.line : end.line + 1]
    if start.line == end.line:
        return "".join(lines)[start.character : end.character]

    raise InvalidRangeError("Multi-line range selection is not supported")
