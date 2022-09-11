import libcst as cst
from libcst.metadata import ParentNodeProvider
from libcst.metadata.scope_provider import ScopeProvider
from pygls.lsp.types.basic_structures import Range

from refacto.core.refactoring_transformer import RefactoringTransformer
from refacto.refactorings.extract_variable.extraction_strategies import ExtractionFactory


class ExtractVariableTransformer(RefactoringTransformer):
    def __init__(
        self,
        expr: cst.Expr,
        variable_name: str,
        selected_range: Range,
    ) -> None:
        self.expr: cst.Expr = expr
        self.variable_name = cst.Name(variable_name)
        self.extract_variable: cst.If | cst.While | cst.For | cst.SimpleStatementLine | None = None
        super().__init__(selected_range=selected_range)

    def on_leave(  # type: ignore
        self,
        original_node: cst.CSTNodeT,
        updated_node: cst.CSTNodeT,
    ) -> cst.CSTNodeT | cst.RemovalSentinel | cst.FlattenSentinel[cst.CSTNodeT] | cst.Name:
        if isinstance(original_node, cst.Expr):
            return self.handle_extract_entire_line_edge_case(original_node=original_node, updated_node=updated_node)

        if self.extract_variable and original_node.deep_equals(self.extract_variable):
            return self.extract(updated_node=updated_node)

        return self.replace_with_variable_if_applicable(
            original_node=original_node,
            updated_node=updated_node,
        )

    def extract(self, updated_node: cst.SimpleStatementLine) -> cst.FlattenSentinel:
        extractor = ExtractionFactory.create(node=self.extract_variable)
        self.extract_variable = None
        target = cst.AssignTarget(self.variable_name)
        assigned_variable = cst.Assign(targets=[target], value=self.expr.value)
        extracted_statement = cst.SimpleStatementLine(
            body=[assigned_variable],
            leading_lines=updated_node.leading_lines,
        )
        return extractor.extract(extracted_statement=extracted_statement, updated_node=updated_node)

    def handle_extract_entire_line_edge_case(
        self,
        original_node: cst.CSTNodeT,
        updated_node: cst.CSTNodeT,
    ) -> cst.RemovalSentinel | cst.CSTNodeT:
        if self.expr.deep_equals(original_node):
            if self.is_same_position(node=original_node):
                return cst.RemovalSentinel.REMOVE
        return updated_node

    def replace_with_variable_if_applicable(
        self,
        original_node: cst.CSTNodeT,
        updated_node: cst.CSTNodeT,
    ) -> cst.CSTNodeT | cst.Name:
        if not self.expr.value.deep_equals(original_node):
            return updated_node
        if self.is_same_position(node=original_node):
            self.scope = self.get_metadata(ScopeProvider, original_node)
            self.extract_variable = self.find_parent(node=original_node)
            return self.variable_name
        if self.is_descendant(node=original_node):
            return self.variable_name
        return updated_node

    def find_parent(
        self,
        node: cst.CSTNode,
    ) -> cst.If | cst.SimpleStatementLine | cst.While | cst.For:
        parent: cst.CSTNode = self.get_metadata(ParentNodeProvider, node)
        if isinstance(parent, (cst.If, cst.While, cst.For, cst.SimpleStatementLine)):
            return parent
        return self.find_parent(node=parent)
