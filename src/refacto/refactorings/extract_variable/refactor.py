from lsprotocol.types import Range

from refacto.refactorings.extract_variable.transformer import ExtractVariableTransformer
from refacto.refactorings.extract_variable.visitor import ExpressionFinder
from refacto.refactorings.refactor import Refactor
from refacto.refactorings.transformer import RefactoringTransformer


class RefactorExtractVariable(Refactor):
    def __init__(self) -> None:
        super().__init__(visitor=ExpressionFinder)

    def create_transformer(self, selected_range: Range) -> RefactoringTransformer:
        if self.visitor.expr is None:  # type:ignore
            raise RuntimeError("Node was unexpectically None!")
        return ExtractVariableTransformer(
            expr=self.visitor.expr,  # type: ignore
            variable_name="rename_me",
            selected_range=selected_range,
        )
