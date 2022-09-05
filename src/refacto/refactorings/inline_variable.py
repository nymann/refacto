from collections.abc import Sequence

import libcst as cst
from libcst.metadata import CodeRange
from libcst.metadata import MetadataWrapper
from libcst.metadata.position_provider import PositionProvider
from pygls.lsp.types.basic_structures import Range

from refacto.refactorings.refactoring_utilities import souce_code_in_range


class NameFinder(cst.CSTVisitor):
    def __init__(self) -> None:
        self.name: cst.Name | None = None

    def visit_Name(self, node: cst.Name) -> bool:
        self.name = node
        return False


class InlineVariableTransformer(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self, name: cst.Name, selected_range: Range) -> None:
        self.name: cst.Name = name
        self.inline_value: cst.BaseExpression | None = None
        self.removed_assignment = False
        self.statent_lines_seen_since_remove = 0
        self.lines: Sequence[cst.EmptyLine] = []
        self.selected_range = selected_range

    def leave_Assign(
        self,
        original_node: cst.Assign,
        updated_node: cst.Assign,
    ) -> cst.Assign | cst.RemovalSentinel:
        for target in original_node.targets:
            if target.target.deep_equals(self.name):
                pos = self.get_metadata(PositionProvider, target.target)
                if code_ranges_are_equal(selected_range=self.selected_range, libcst_range=pos):
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
            self.lines = updated_node.leading_lines
            return cst.RemoveFromParent()
        return cst.SimpleStatementLine(
            body=updated_node.body,
            leading_lines=self.lines,
            trailing_whitespace=updated_node.trailing_whitespace,
        )

    def leave_Name(self, original_node: cst.Name, updated_node: cst.Name) -> cst.BaseExpression:
        if self.inline_value and self.name.deep_equals(original_node):
            return self.inline_value
        return updated_node


def code_ranges_are_equal(libcst_range: CodeRange, selected_range: Range) -> bool:
    same_line = selected_range.start.line == libcst_range.start.line - 1
    same_col = selected_range.start.character == libcst_range.start.column
    return same_line and same_col


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
