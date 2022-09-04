from bisect import bisect_right
import difflib
from typing import NamedTuple

from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range
from pygls.lsp.types.basic_structures import TextEdit


class Opcode(NamedTuple):
    op: str
    old_start: int
    old_end: int
    new_start: int
    new_end: int


class PositionLookup:
    def __init__(self, code: str) -> None:
        self.line_starts = []
        offset = 0
        for line in code.splitlines(keepends=True):
            self.line_starts.append(offset)
            offset += len(line)

    def get(self, offset: int) -> Position:
        line = bisect_right(self.line_starts, offset) - 1
        character = offset - self.line_starts[line]
        return Position(line=line, character=character)


def lsp_text_edits(old_code: str, new_code: str) -> list[TextEdit]:
    position_lookup = PositionLookup(old_code)
    text_edits = []
    for opcode in get_opcodes(old_code, new_code):
        if opcode.op not in {"replace", "delete", "insert"}:
            continue
        text_edits.append(
            TextEdit(
                range=Range(
                    start=position_lookup.get(opcode.old_start),
                    end=position_lookup.get(opcode.old_end),
                ),
                new_text=new_code[opcode.new_start : opcode.new_end],
            ),
        )
    return text_edits


def get_opcodes(old: str, new: str) -> list[Opcode]:
    diff = difflib.SequenceMatcher(a=old, b=new)
    return [Opcode(*opcode) for opcode in diff.get_opcodes()]
