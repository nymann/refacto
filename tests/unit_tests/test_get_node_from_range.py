import libcst as cst
from libcst.metadata.parent_node_provider import ParentNodeProvider
from libcst.metadata.position_provider import PositionProvider
from libcst.metadata.scope_provider import Scope
from libcst.metadata.scope_provider import ScopeProvider
from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range


class FindNode(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (
        PositionProvider,
        ScopeProvider,
        ParentNodeProvider,
    )

    def __init__(self, selected_range: Range) -> None:
        self.selected_range = selected_range
        self.node: cst.CSTNode | None = None
        self.parent: cst.CSTNode | None = None
        self.scope: Scope | None = None

        super().__init__()

    def visit_Name(self, node: cst.Name) -> bool:
        if self._is_same_starting_position(node=node):
            self._set_things(node=node)
            return False
        return True

    def _set_things(self, node: cst.CSTNode) -> None:
        self.node = node
        self.scope = self.get_metadata(ScopeProvider, node)
        try:
            self.parent = self.get_metadata(ParentNodeProvider, node)
        except KeyError:
            # No parent
            return

    def _is_same_starting_position(self, node: cst.CSTNode) -> bool:
        libcst_range = self.get_metadata(PositionProvider, node)
        return all(
            [
                self.selected_range.start.line == libcst_range.start.line - 1,
                self.selected_range.start.character == libcst_range.start.column,
            ],
        )


def test_stuff():
    selected_range = Range(
        start=Position(line=0, character=0),
        end=Position(line=0, character=1),
    )
    with open("tests/test_cases/inline_variable/simplest/before.py", "r") as src:
        code = src.read()
    module = cst.MetadataWrapper(cst.parse_module(source=code))
    visitor = FindNode(selected_range=selected_range)
    module.visit(visitor=visitor)
    assert visitor.node is not None
