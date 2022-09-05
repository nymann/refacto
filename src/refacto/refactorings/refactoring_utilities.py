from libcst.metadata import CodeRange
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


def code_ranges_are_equal(libcst_range: CodeRange, selected_range: Range) -> bool:
    same_line = selected_range.start.line == libcst_range.start.line - 1
    same_col = selected_range.start.character == libcst_range.start.column
    return same_line and same_col
