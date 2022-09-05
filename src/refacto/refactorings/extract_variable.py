from typing import Optional

import libcst
from pygls.lsp.types.basic_structures import Range

from refacto.refactorings.refactoring_utilities import get_chars_in_range


class ExtractVariableTransformer(libcst.CSTTransformer):
    def __init__(self, expr: libcst.Expr, variable_name: str) -> None:
        self.expr: libcst.Expr = expr
        self.variable_name = libcst.Name(variable_name)
        self.extract_next_statement_line = False
        self.extraced_once: bool = False

    def leave_Expr(self, original_node: libcst.Expr, updated_node: libcst.Expr) -> libcst.Expr | libcst.RemovalSentinel:
        if self.expr.deep_equals(original_node):
            return libcst.RemovalSentinel.REMOVE
        return updated_node

    def leave_Call(self, original_node: libcst.Call, updated_node: libcst.Call) -> libcst.Call | libcst.Name:
        if self.expr.value.deep_equals(original_node):
            self.extract_next_statement_line = True
            return self.variable_name
        return updated_node

    def visit_Call(self, node: libcst.Call) -> bool:
        return not self.expr.value.deep_equals(node)

    def leave_BinaryOperation(
        self,
        original_node: libcst.BinaryOperation,
        updated_node: libcst.BinaryOperation,
    ) -> libcst.BinaryOperation | libcst.Name:
        if self.expr.value.deep_equals(original_node):
            self.extract_next_statement_line = True
            return self.variable_name
        return updated_node

    def leave_SimpleStatementLine(
        self,
        original_node: libcst.SimpleStatementLine,
        updated_node: libcst.SimpleStatementLine,
    ) -> libcst.FlattenSentinel | libcst.SimpleStatementLine:
        if not self.extract_next_statement_line or self.extraced_once:
            return updated_node
        target = libcst.AssignTarget(self.variable_name)
        assigned_variable = libcst.Assign(targets=[target], value=self.expr.value)
        extracted_statement = libcst.SimpleStatementLine(body=[assigned_variable])
        self.extract_next_statement_line = False
        self.extraced_once = True
        return libcst.FlattenSentinel([extracted_statement, updated_node])


class ExpressionFinder(libcst.CSTVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.expr: libcst.Expr | None = None

    def visit_Expr(self, node: libcst.Expr) -> Optional[bool]:
        self.expr = node
        return True


def extract_variable(selected_range: Range, source: str) -> str:
    range_tree = libcst.parse_module(get_chars_in_range(selected_range=selected_range, source=source))
    visitor = ExpressionFinder()
    range_tree.visit(visitor=visitor)
    if visitor.expr is None:
        raise RuntimeError("Node was unexpectically None!")

    source_tree = libcst.parse_module(source=source)
    extract_transformer = ExtractVariableTransformer(expr=visitor.expr, variable_name="a")
    transformed_tree = source_tree.visit(extract_transformer)
    return transformed_tree.code
