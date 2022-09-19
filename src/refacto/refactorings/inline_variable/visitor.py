from devtools import debug
import libcst as cst
from libcst.metadata import ParentNodeProvider
from libcst.metadata import WhitespaceInclusivePositionProvider
from libcst.metadata.scope_provider import Scope
from libcst.metadata.scope_provider import ScopeProvider
from pygls.lsp.types.basic_structures import Range

from refacto.refactorings.visitor import RefactoringVisitor


class NameFinder(RefactoringVisitor):
    METADATA_DEPENDENCIES = (
        WhitespaceInclusivePositionProvider,
        ScopeProvider,
        ParentNodeProvider,
    )

    def __init__(self, selected_range: Range) -> None:
        self.name: cst.Name | None = None
        self.parent: cst.CSTNode | None = None
        self.scope: Scope | None = None
        super().__init__(selected_range=selected_range)

    def visit_Name(self, node: cst.Name) -> bool:
        if self._is_same_starting_position(node=node):
            self._set_things(node=node)
            return False
        return True

    def _set_things(self, node: cst.Name) -> None:
        self.name = node
        self.scope = self.get_metadata(ScopeProvider, node)
        try:
            self.parent = self.get_metadata(ParentNodeProvider, node)
        except KeyError:
            return

    def _is_same_starting_position(self, node: cst.Name) -> bool:
        libcst_range = self.get_metadata(WhitespaceInclusivePositionProvider, node)
        if node.value == "shipping_price":
            debug(str(libcst_range), node)
        return all(
            [
                self.selected_range.start.line == libcst_range.start.line - 1,
                self.selected_range.start.character == libcst_range.start.column,
            ],
        )
