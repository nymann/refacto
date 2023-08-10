from lsprotocol.types import Range

from refacto.refactorings.inline_variable.transformer import InlineVariableTransformer
from refacto.refactorings.inline_variable.visitor import NameFinder
from refacto.refactorings.refactor import Refactor
from refacto.refactorings.transformer import RefactoringTransformer


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
