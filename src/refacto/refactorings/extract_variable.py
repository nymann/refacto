from bisect import bisect_right
import difflib
from typing import NamedTuple, Optional

from devtools import debug
import libcst
from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range
from pygls.lsp.types.basic_structures import RenameFile
from pygls.lsp.types.basic_structures import TextEdit

_OPCODES_CHANGE = {"replace", "delete", "insert"}


class ExtractVariableTransformer(libcst.CSTTransformer):
    def __init__(self, node: libcst.BinaryOperation, variable_name: str) -> None:
        self.node: libcst.BinaryOperation = node
        self.variable = libcst.Name(variable_name)

    def leave_BinaryOperation(
        self,
        original_node: libcst.BinaryOperation,
        updated_node: libcst.BinaryOperation,
    ) -> libcst.BinaryOperation | libcst.Name:
        if self.node.deep_equals(original_node):
            return self.variable
        return updated_node

    def leave_SimpleStatementLine(
        self,
        original_node: libcst.SimpleStatementLine,
        updated_node: libcst.SimpleStatementLine,
    ) -> libcst.FlattenSentinel:
        assigned_variable = libcst.Assign(targets=[libcst.AssignTarget(self.variable)], value=self.node)
        extracted_statement = libcst.SimpleStatementLine(body=[assigned_variable])
        return libcst.FlattenSentinel([extracted_statement, updated_node])


def lsp_text_edits(old_code: str, new_code: str) -> list[TextEdit]:
    position_lookup = PositionLookup(old_code)
    text_edits = []
    for opcode in get_opcodes(old_code, new_code):
        if opcode.op in _OPCODES_CHANGE:
            start = position_lookup.get(opcode.old_start)
            end = position_lookup.get(opcode.old_end)
            new_text = new_code[opcode.new_start : opcode.new_end]
            text_edits.append(
                TextEdit(
                    range=Range(start=start, end=end),
                    new_text=new_text,
                )
            )
    return text_edits


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
        """Get the position in the file that corresponds to the given
        offset."""
        line = bisect_right(self.line_starts, offset) - 1
        character = offset - self.line_starts[line]
        return Position(line=line, character=character)


class ExpressionFinder(libcst.CSTVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.node: Optional[libcst.BinaryOperation] = None

    def visit_BinaryOperation(self, node: libcst.BinaryOperation) -> Optional[bool]:
        self.node = node
        return False


def get_chars_in_range(range: Range, source: str) -> str:
    start: Position = range.start
    end: Position = range.end
    if start == end:
        raise Exception("Not a range select")
    debug(start, end)
    lines = source.splitlines()[start.line : end.line + 1]
    if start.line == end.line:
        return "".join(lines)[start.character : end.character + 1]

    raise Exception("Not supported")


def extract_variable(range: Range, source: str) -> str:
    range_tree = libcst.parse_module(get_chars_in_range(range=range, source=source))
    visitor = ExpressionFinder()
    range_tree.visit(visitor=visitor)
    if visitor.node is None:
        raise Exception()

    source_tree = libcst.parse_module(source=source)
    extract_transformer = ExtractVariableTransformer(node=visitor.node, variable_name="a")
    transformed_tree = source_tree.visit(extract_transformer)
    return transformed_tree.code


def get_opcodes(old: str, new: str) -> list[Opcode]:
    """Obtain typed opcodes from two files (old and new)"""
    diff = difflib.SequenceMatcher(a=old, b=new)
    return [Opcode(*opcode) for opcode in diff.get_opcodes()]
