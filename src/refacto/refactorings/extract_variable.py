from typing import Optional

import libcst
from pygls.lsp.types.basic_structures import Range

from refacto.refactorings.refactoring_utilities import get_chars_in_range


class ExtractVariableTransformer(libcst.CSTTransformer):
    def __init__(self, node: libcst.BinaryOperation, variable_name: str) -> None:
        self.node: libcst.BinaryOperation = node
        self.variable_name = libcst.Name(variable_name)

    def leave_BinaryOperation(
        self,
        original_node: libcst.BinaryOperation,
        updated_node: libcst.BinaryOperation,
    ) -> libcst.BinaryOperation | libcst.Name:
        if self.node.deep_equals(original_node):
            return self.variable_name
        return updated_node

    def leave_SimpleStatementLine(
        self,
        original_node: libcst.SimpleStatementLine,
        updated_node: libcst.SimpleStatementLine,
    ) -> libcst.FlattenSentinel:
        target = libcst.AssignTarget(self.variable_name)
        assigned_variable = libcst.Assign(targets=[target], value=self.node)
        extracted_statement = libcst.SimpleStatementLine(body=[assigned_variable])
        return libcst.FlattenSentinel([extracted_statement, updated_node])


class ExpressionFinder(libcst.CSTVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.node: Optional[libcst.BinaryOperation] = None

    def visit_BinaryOperation(self, node: libcst.BinaryOperation) -> Optional[bool]:
        self.node = node
        return False


def extract_variable(selected_range: Range, source: str) -> str:
    range_tree = libcst.parse_module(get_chars_in_range(selected_range=selected_range, source=source))
    visitor = ExpressionFinder()
    range_tree.visit(visitor=visitor)
    if visitor.node is None:
        raise RuntimeError("Node was unexpectically None!")

    source_tree = libcst.parse_module(source=source)
    extract_transformer = ExtractVariableTransformer(node=visitor.node, variable_name="a")
    transformed_tree = source_tree.visit(extract_transformer)
    return transformed_tree.code
