from abc import ABC
from abc import abstractmethod

import libcst as cst
from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range

from refacto.core.refactoring_transformer import RefactoringTransformer
from refacto.core.refactoring_visitor import RefactoringVisitor
from refacto.exceptions import InvalidRangeError


class Refactor(ABC):
    def __init__(self, visitor: RefactoringVisitor) -> None:
        self.visitor = visitor

    def refactor(self, selected_range: Range, source: str) -> str:
        selected_code = self.selected_code(selected_range=selected_range, source=source)
        self.visit_visitor(selected_code=selected_code)
        transformer = self.create_transformer(selected_range=selected_range)
        return self.get_transformed_code(transformer=transformer, source=source)

    @staticmethod
    def selected_code(selected_range: Range, source: str) -> str:  # noqa: WPS602
        start: Position = selected_range.start
        end: Position = selected_range.end
        end_char = end.character
        if start == end:
            end_char += 1
        lines = source.splitlines()[start.line : end.line + 1]
        if start.line == end.line:
            return "".join(lines)[start.character : end_char]
        raise InvalidRangeError("Multi-line range selection is not supported")

    @abstractmethod
    def create_transformer(self, selected_range: Range) -> RefactoringTransformer:
        raise NotImplementedError()

    def visit_visitor(self, selected_code: str) -> None:
        range_tree = cst.parse_module(selected_code)
        range_tree.visit(visitor=self.visitor)

    def get_transformed_code(self, transformer: RefactoringTransformer, source: str) -> str:
        source_tree = cst.MetadataWrapper(cst.parse_module(source=source))
        transformed_tree = source_tree.visit(transformer)
        return transformed_tree.code
