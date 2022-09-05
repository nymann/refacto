from collections.abc import Sequence

import libcst as cst
from libcst.metadata.scope_provider import ScopeProvider
from pygls.lsp.types.basic_structures import Range

from refacto.core.refactoring import Refactor
from refacto.core.refactoring_transformer import RefactoringTransformer
from refacto.core.refactoring_visitor import RefactoringVisitor


class NameFinder(RefactoringVisitor):
    def __init__(self) -> None:
        self.name: cst.Name | None = None

    def visit_Name(self, node: cst.Name) -> bool:
        self.name = node
        return False


class InlineVariableTransformer(RefactoringTransformer):
    def __init__(self, name: cst.Name, selected_range: Range) -> None:
        self.name: cst.Name = name
        self.inline_value: cst.BaseExpression | None = None
        self.removed_assignment = False
        self.statent_lines_seen_since_remove = 0
        self.leading_lines: Sequence[cst.EmptyLine] = []
        super().__init__(selected_range=selected_range)

    def leave_Assign(
        self,
        original_node: cst.Assign,
        updated_node: cst.Assign,
    ) -> cst.Assign | cst.RemovalSentinel:
        for target in original_node.targets:
            if target.target.deep_equals(self.name):
                if self.is_same_position(node=target.target):
                    self.scope = self.get_metadata(ScopeProvider, target.target)
                    self.inline_value = original_node.value
                    self.removed_assignment = True
        return updated_node

    def leave_SimpleStatementLine(
        self,
        original_node: cst.SimpleStatementLine,
        updated_node: cst.SimpleStatementLine,
    ) -> cst.BaseStatement | cst.FlattenSentinel[cst.BaseStatement] | cst.RemovalSentinel:
        if not self.removed_assignment or self.statent_lines_seen_since_remove > 2:
            return updated_node
        self.statent_lines_seen_since_remove += 1
        if self.statent_lines_seen_since_remove == 1:
            self._leading_lines = updated_node.leading_lines
            return cst.RemoveFromParent()
        return cst.SimpleStatementLine(
            body=updated_node.body,
            leading_lines=self._leading_lines,
            trailing_whitespace=updated_node.trailing_whitespace,
        )

    def leave_Name(self, original_node: cst.Name, updated_node: cst.Name) -> cst.BaseExpression:
        if self.inline_value and self.name.deep_equals(original_node):
            if self.is_descendant(node=original_node):
                return self.inline_value
        return updated_node


class RefactorInlineVariable(Refactor):
    def __init__(self) -> None:
        self.visitor: NameFinder = NameFinder()

    def create_transformer(self, selected_range: Range) -> RefactoringTransformer:
        if self.visitor.name is None:
            raise RuntimeError("Couldn't find variable to inline :-(")
        return InlineVariableTransformer(
            name=self.visitor.name,
            selected_range=selected_range,
        )
