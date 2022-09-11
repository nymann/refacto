from pygls.lsp.types.basic_structures import Range

from refacto.core.refactoring import Refactor
from refacto.core.refactoring_transformer import RefactoringTransformer
from refacto.refactorings.extract_variable.transformer import ExtractVariableTransformer
from refacto.refactorings.extract_variable.visitor import ExpressionFinder


class RefactorExtractVariable(Refactor):
    def __init__(self) -> None:
        self.visitor: ExpressionFinder = ExpressionFinder()

    def create_transformer(self, selected_range: Range) -> RefactoringTransformer:
        if self.visitor.expr is None:
            raise RuntimeError("Node was unexpectically None!")
        return ExtractVariableTransformer(
            expr=self.visitor.expr,
            variable_name="rename_me",
            selected_range=selected_range,
        )
