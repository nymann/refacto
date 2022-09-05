import libcst as cst
from libcst.metadata.scope_provider import ScopeProvider
from pygls.lsp.types.basic_structures import Range

from refacto.core.refactoring import Refactor
from refacto.core.refactoring_transformer import RefactoringTransformer
from refacto.core.refactoring_visitor import RefactoringVisitor


class ExtractVariableTransformer(RefactoringTransformer):
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
        super().__init__(selected_range=selected_range)

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
            if self.is_same_position(node=original_node):
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
            if self.is_same_position(node=original_node):
                self.extract_next_statement_line = True
                self.scope = self.get_metadata(ScopeProvider, original_node)
                return self.variable_name
            if self.is_descendant(node=original_node):
                return self.variable_name
        return updated_node


class ExpressionFinder(RefactoringVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.expr: cst.Expr | None = None

    def visit_Expr(self, node: cst.Expr) -> bool:
        self.expr = node
        return False


class RefactorExtractVariable(Refactor):
    def __init__(self) -> None:
        self.visitor: ExpressionFinder = ExpressionFinder()

    def create_transformer(self, selected_range: Range) -> RefactoringTransformer:
        if self.visitor.expr is None:
            raise RuntimeError("Node was unexpectically None!")
        return ExtractVariableTransformer(
            expr=self.visitor.expr,
            variable_name="a",
            selected_range=selected_range,
        )
