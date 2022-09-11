from collections.abc import Sequence

import libcst as cst
from libcst.metadata.scope_provider import ScopeProvider
from pygls.lsp.types.basic_structures import Range

from refacto.core.refactoring_transformer import RefactoringTransformer


class InlineVariableTransformer(RefactoringTransformer):
    def __init__(self, name: cst.Name, selected_range: Range) -> None:
        self.name: cst.Name = name
        self.inline_value: cst.BaseExpression | None = None
        self.removed_assignment = False
        self.statent_lines_seen_since_remove = 0
        self.leading_lines: Sequence[cst.EmptyLine] = []
        super().__init__(selected_range=selected_range)

    def visit_Assign(
        self,
        node: cst.Assign,
    ) -> bool:
        for target in node.targets:
            if self._is_correct_target(target=target):
                self.scope = self.get_metadata(ScopeProvider, target.target)
                self.inline_value = node.value
                self.removed_assignment = True
                return False
        return True

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

    def _is_correct_target(self, target: cst.AssignTarget) -> bool:
        if not target.target.deep_equals(self.name):
            return False
        return self.is_same_position(node=target.target)
