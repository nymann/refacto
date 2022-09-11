import libcst as cst

from refacto.core.refactoring_visitor import RefactoringVisitor


class NameFinder(RefactoringVisitor):
    def __init__(self) -> None:
        self.name: cst.Name | None = None

    def visit_Name(self, node: cst.Name) -> bool:
        self.name = node
        return False
