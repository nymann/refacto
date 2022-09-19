from abc import ABC
from abc import abstractmethod
from typing import Type

import libcst as cst
from pygls.lsp.types.basic_structures import Position
from pygls.lsp.types.basic_structures import Range

from refacto.exceptions import InvalidRangeError
from refacto.refactorings.transformer import RefactoringTransformer
from refacto.refactorings.visitor import RefactoringVisitor


class Refactor(ABC):
    def __init__(self, visitor: Type[RefactoringVisitor]) -> None:
        self.visitor_type = visitor
        self.visitor: RefactoringVisitor | None = None

    def refactor(self, selected_range: Range, source: str) -> str:
        self.visitor = self.visitor_type(selected_range=selected_range)
        selected_code = self.selected_code(selected_range=selected_range, source=source)
        self.visit_visitor(selected_code=selected_code)
        transformer = self.create_transformer(selected_range=selected_range)
        return self.get_transformed_code(transformer=transformer, source=source)

    @classmethod
    def selected_code(cls, selected_range: Range, source: str) -> str:  # noqa: WPS602
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
        range_tree = cst.MetadataWrapper(cst.parse_module(selected_code))
        range_tree.visit(visitor=self.visitor)  # type: ignore

    def get_transformed_code(self, transformer: RefactoringTransformer, source: str) -> str:
        source_tree = cst.MetadataWrapper(cst.parse_module(source=source))
        transformed_tree = source_tree.visit(transformer)
        return transformed_tree.code
