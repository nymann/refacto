from collections.abc import Sequence

import libcst as cst
from libcst.metadata import MetadataWrapper
from libcst.metadata.position_provider import PositionProvider
from libcst.metadata.scope_provider import Scope
from libcst.metadata.scope_provider import ScopeProvider
from pygls.lsp.types.basic_structures import Range

from refacto.refactorings.refactoring_utilities import code_ranges_are_equal
from refacto.refactorings.refactoring_utilities import souce_code_in_range


class NameFinder(cst.CSTVisitor):
    def __init__(self) -> None:
        self.name: cst.Name | None = None

    def visit_Name(self, node: cst.Name) -> bool:
        self.name = node
        return False


class InlineVariableTransformer(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (
        PositionProvider,
        ScopeProvider,
    )

    def __init__(self, name: cst.Name, selected_range: Range) -> None:
        self._name: cst.Name = name
        self._inline_value: cst.BaseExpression | None = None
        self._removed_assignment = False
        self._statent_lines_seen_since_remove = 0
        self._leading_lines: Sequence[cst.EmptyLine] = []
        self._selected_range = selected_range
        self._scope: Scope | None = None

    def leave_Assign(
        self,
        original_node: cst.Assign,
        updated_node: cst.Assign,
    ) -> cst.Assign | cst.RemovalSentinel:
        for target in original_node.targets:
            if target.target.deep_equals(self._name):
                pos = self.get_metadata(PositionProvider, target.target)
                if code_ranges_are_equal(selected_range=self._selected_range, libcst_range=pos):
                    self.scope = self.get_metadata(ScopeProvider, target.target)
                    self._inline_value = original_node.value
                    self._removed_assignment = True
        return updated_node

    def leave_SimpleStatementLine(
        self,
        original_node: cst.SimpleStatementLine,
        updated_node: cst.SimpleStatementLine,
    ) -> cst.BaseStatement | cst.FlattenSentinel[cst.BaseStatement] | cst.RemovalSentinel:
        if not self._removed_assignment or self._statent_lines_seen_since_remove > 2:
            return updated_node
        self._statent_lines_seen_since_remove += 1
        if self._statent_lines_seen_since_remove == 1:
            self._leading_lines = updated_node.leading_lines
            return cst.RemoveFromParent()
        return cst.SimpleStatementLine(
            body=updated_node.body,
            leading_lines=self._leading_lines,
            trailing_whitespace=updated_node.trailing_whitespace,
        )

    def leave_Name(self, original_node: cst.Name, updated_node: cst.Name) -> cst.BaseExpression:
        if self._inline_value and self._name.deep_equals(original_node):
            if self.scope and self.scope == self.get_metadata(ScopeProvider, original_node):
                return self._inline_value
        return updated_node


def inline_variable(selected_range: Range, source: str) -> str:
    range_tree = cst.parse_module(souce_code_in_range(code_range=selected_range, source=source))
    visitor = NameFinder()
    range_tree.visit(visitor=visitor)
    if visitor.name is None:
        raise RuntimeError("Couldn't find variable to inline :-(")
    source_tree = MetadataWrapper(cst.parse_module(source=source))
    extract_transformer = InlineVariableTransformer(name=visitor.name, selected_range=selected_range)
    transformed_tree = source_tree.visit(extract_transformer)
    return transformed_tree.code
