from pygls.lsp.types.basic_structures import Range

from refacto.refactorings.inline_variable.transformer import InlineVariableTransformer
from refacto.refactorings.inline_variable.visitor import NameFinder
from refacto.refactorings.refactor import Refactor
from refacto.refactorings.transformer import RefactoringTransformer


class RefactorInlineVariable(Refactor):
    def __init__(self) -> None:
        super().__init__(visitor=NameFinder)

    def create_transformer(self, selected_range: Range) -> RefactoringTransformer:
        if self.visitor.name is None:  # type: ignore
            raise RuntimeError("Couldn't find variable to inline :-(")
        return InlineVariableTransformer(
            name=self.visitor.name,  # type: ignore
            selected_range=selected_range,
        )
