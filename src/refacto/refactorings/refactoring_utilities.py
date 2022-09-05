from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range

from refacto.exceptions import InvalidRangeError


def souce_code_in_range(code_range: Range, source: str) -> str:
    start: Position = code_range.start
    end: Position = code_range.end
    end_char = end.character
    if start == end:
        end_char += 1
    lines = source.splitlines()[start.line : end.line + 1]
    if start.line == end.line:
        return "".join(lines)[start.character : end_char]

    raise InvalidRangeError("Multi-line range selection is not supported")
