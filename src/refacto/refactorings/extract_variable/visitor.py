import libcst as cst
from pygls.lsp.types.basic_structures import Range

from refacto.refactorings.visitor import RefactoringVisitor


class ExpressionFinder(RefactoringVisitor):
    def __init__(self, selected_range: Range) -> None:
        self.expr: cst.Expr | None = None
        super().__init__(selected_range=selected_range)

    def visit_Expr(self, node: cst.Expr) -> bool:
        self.expr = node
        return False
