from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import libcst as cst


class ExtractionStrategy(ABC):
    @abstractmethod
    def extract(
        self,
        extracted_statement: cst.SimpleStatementLine,
        updated_node: cst.SimpleStatementLine,
    ) -> cst.FlattenSentinel:
        raise NotImplementedError()


class DefaultExtractionStrategy(ExtractionStrategy):
    def extract(
        self,
        extracted_statement: cst.SimpleStatementLine,
        updated_node: cst.SimpleStatementLine,
    ) -> cst.FlattenSentinel:
        return cst.FlattenSentinel([extracted_statement, updated_node])


class LeadingSpacesExtractionStrategy(ExtractionStrategy):
    def extract(
        self,
        extracted_statement: cst.SimpleStatementLine,
        updated_node: cst.SimpleStatementLine,
    ) -> cst.FlattenSentinel:
        removed_leading_lines = cst.SimpleStatementLine(body=updated_node.body)
        return cst.FlattenSentinel([extracted_statement, removed_leading_lines])


class ExtractionFactory:
    @classmethod
    def create(cls, node: object) -> ExtractionStrategy:
        if isinstance(node, cst.SimpleStatementLine):
            return LeadingSpacesExtractionStrategy()
        return DefaultExtractionStrategy()
