from collections.abc import Sequence

import libcst
from pygls.lsp.types.basic_structures import Range

from refacto.refactorings.refactoring_utilities import souce_code_in_range


class NameFinder(libcst.CSTVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.name: libcst.Name | None = None

    def visit_Name(self, node: libcst.Name) -> bool:
        self.name = node
        return False


class InlineVariableTransformer(libcst.CSTTransformer):
    def __init__(self, name: libcst.Name) -> None:
        self.name: libcst.Name = name
        self.inline_value: libcst.BaseExpression | None = None
        self.removed_assignment = False
        self.statent_lines_seen_since_remove = 0
        self.lines: Sequence[libcst.EmptyLine] = []

    def leave_Assign(
        self,
        original_node: libcst.Assign,
        updated_node: libcst.Assign,
    ) -> libcst.Assign | libcst.RemovalSentinel:
        for target in original_node.targets:
            if target.target.deep_equals(self.name):
                self.inline_value = original_node.value
                self.removed_assignment = True
        return updated_node

    def leave_SimpleStatementLine(
        self,
        original_node: libcst.SimpleStatementLine,
        updated_node: libcst.SimpleStatementLine,
    ) -> libcst.BaseStatement | libcst.FlattenSentinel[libcst.BaseStatement] | libcst.RemovalSentinel:
        if not self.removed_assignment or self.statent_lines_seen_since_remove > 2:
            return updated_node
        self.statent_lines_seen_since_remove += 1
        if self.statent_lines_seen_since_remove == 1:
            self.lines = updated_node.leading_lines
            return libcst.RemoveFromParent()
        return libcst.SimpleStatementLine(
            body=updated_node.body,
            leading_lines=self.lines,
            trailing_whitespace=updated_node.trailing_whitespace,
        )

    def leave_Name(self, original_node: libcst.Name, updated_node: libcst.Name) -> libcst.BaseExpression:
        if self.inline_value and self.name.deep_equals(original_node):
            return self.inline_value
        return updated_node


def inline_variable(selected_range: Range, source: str) -> str:
    range_tree = libcst.parse_module(souce_code_in_range(code_range=selected_range, source=source))
    visitor = NameFinder()
    range_tree.visit(visitor=visitor)
    if visitor.name is None:
        raise RuntimeError("Couldn't find variable to inline :-(")
    source_tree = libcst.parse_module(source=source)
    extract_transformer = InlineVariableTransformer(name=visitor.name)
    transformed_tree = source_tree.visit(extract_transformer)
    return transformed_tree.code
