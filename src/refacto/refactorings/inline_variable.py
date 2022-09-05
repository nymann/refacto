from devtools import debug
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

    def leave_Assign(
        self,
        original_node: libcst.Assign,
        updated_node: libcst.Assign,
    ) -> libcst.Assign | libcst.RemovalSentinel:
        for target in original_node.targets:
            if target.target.deep_equals(self.name):
                self.inline_value = original_node.value
                return libcst.RemovalSentinel.REMOVE
        return updated_node

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
    debug(extract_transformer.inline_value)
    return transformed_tree.code
