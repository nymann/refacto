import libcst
from pygls.lsp.types.basic_structures import Range


class RefactoringVisitor(libcst.CSTVisitor):
    def __init__(self, selected_range: Range) -> None:
        self.selected_range = selected_range
