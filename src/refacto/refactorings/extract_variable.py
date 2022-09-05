import libcst as cst
from libcst.metadata import MetadataWrapper
from libcst.metadata.position_provider import PositionProvider
from libcst.metadata.scope_provider import Scope
from libcst.metadata.scope_provider import ScopeProvider
from pygls.lsp.types.basic_structures import Range

from refacto.refactorings.refactoring_utilities import code_ranges_are_equal
from refacto.refactorings.refactoring_utilities import souce_code_in_range


class ExtractVariableTransformer(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (
        PositionProvider,
        ScopeProvider,
    )

    def __init__(
        self,
        expr: cst.Expr,
        variable_name: str,
        selected_range: Range,
    ) -> None:
        self.expr: cst.Expr = expr
        self.variable_name = cst.Name(variable_name)
        self.extract_next_statement_line = False
        self.extraced_once = False
        self.selected_range = selected_range
        self.scope: Scope | None = None

    def on_leave(  # type: ignore
        self,
        original_node: cst.CSTNodeT,
        updated_node: cst.CSTNodeT,
    ) -> cst.CSTNodeT | cst.RemovalSentinel | cst.FlattenSentinel[cst.CSTNodeT] | cst.Name:
        if isinstance(original_node, cst.Expr):
            return self.handle_extract_entire_line_edge_case(original_node=original_node, updated_node=updated_node)

        if isinstance(original_node, cst.SimpleStatementLine):
            return self.extract_variable_if_applicable(updated_node=updated_node)

        return self.replace_with_variable_if_applicable(
            original_node=original_node,
            updated_node=updated_node,
        )

    def handle_extract_entire_line_edge_case(
        self,
        original_node: cst.CSTNodeT,
        updated_node: cst.CSTNodeT,
    ) -> cst.RemovalSentinel | cst.CSTNodeT:
        if self.expr.deep_equals(original_node):
            pos = self.get_metadata(PositionProvider, original_node)
            if code_ranges_are_equal(pos, self.selected_range):
                return cst.RemovalSentinel.REMOVE
        return updated_node

    def extract_variable_if_applicable(
        self,
        updated_node: cst.SimpleStatementLine,
    ) -> cst.FlattenSentinel | cst.SimpleStatementLine:
        if not self.extract_next_statement_line or self.extraced_once:
            return updated_node
        target = cst.AssignTarget(self.variable_name)
        assigned_variable = cst.Assign(targets=[target], value=self.expr.value)
        extracted_statement = cst.SimpleStatementLine(
            body=[assigned_variable],
            leading_lines=updated_node.leading_lines,
        )
        removed_leading_lines = cst.SimpleStatementLine(body=updated_node.body)
        self.extract_next_statement_line = False
        self.extraced_once = True

        return cst.FlattenSentinel([extracted_statement, removed_leading_lines])

    def replace_with_variable_if_applicable(
        self,
        original_node: cst.CSTNodeT,
        updated_node: cst.CSTNodeT,
    ) -> cst.CSTNodeT | cst.Name:
        if self.expr.value.deep_equals(original_node):
            pos = self.get_metadata(PositionProvider, original_node)
            scope = self.get_metadata(ScopeProvider, original_node)
            if code_ranges_are_equal(pos, self.selected_range):
                self.extract_next_statement_line = True
                self.scope = scope
                return self.variable_name
            if scope is not None and scope == self.scope:
                return self.variable_name
            if self.scope is not None and scope is not None and scope.parent == self.scope:
                return self.variable_name
        return updated_node


class ExpressionFinder(cst.CSTVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.expr: cst.Expr | None = None

    def visit_Expr(self, node: cst.Expr) -> bool:
        self.expr = node
        return False


def extract_variable(selected_range: Range, source: str) -> str:
    range_tree = cst.parse_module(souce_code_in_range(code_range=selected_range, source=source))
    visitor = ExpressionFinder()
    range_tree.visit(visitor=visitor)
    if visitor.expr is None:
        raise RuntimeError("Node was unexpectically None!")

    source_tree = MetadataWrapper(cst.parse_module(source=source))
    extract_transformer = ExtractVariableTransformer(
        expr=visitor.expr,
        variable_name="a",
        selected_range=selected_range,
    )
    transformed_tree = source_tree.visit(extract_transformer)
    return transformed_tree.code
