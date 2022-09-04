from typing import Optional

import libcst
from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range


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
    lines = source.splitlines()[start.line - 1 : end.line]
    if start.line == end.line:
        return "".join(lines)[start.character - 1 : end.character]

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
