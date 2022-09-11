import libcst as cst

from refacto.core.refactoring_visitor import RefactoringVisitor


class ExpressionFinder(RefactoringVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.expr: cst.Expr | None = None

    def visit_Expr(self, node: cst.Expr) -> bool:
        self.expr = node
        return False
