import libcst as cst
from libcst.metadata.position_provider import PositionProvider
from libcst.metadata.scope_provider import Scope
from libcst.metadata.scope_provider import ScopeProvider
from pygls.lsp.types.basic_structures import Range


class RefactoringTransformer(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (
        PositionProvider,
        ScopeProvider,
    )

    def __init__(self, selected_range: Range) -> None:
        self.scope: Scope | None = None
        self.selected_range = selected_range
        super().__init__()

    def is_descendant(self, node: cst.CSTNode) -> bool:
        scope = self.get_metadata(ScopeProvider, node)
        if scope is None or self.scope is None:
            return False
        return any(
            [
                scope == self.scope,
                scope.parent == self.scope,
                scope.parent.parent == self.scope,
                scope.parent.parent.parent == self.scope,
            ],
        )

    def is_same_position(self, node: cst.CSTNode) -> bool:
        libcst_range = self.get_metadata(PositionProvider, node)
        return all(
            [
                self.selected_range.start.line == libcst_range.start.line - 1,
                self.selected_range.start.character == libcst_range.start.column,
            ],
        )
