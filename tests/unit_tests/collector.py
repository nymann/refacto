from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pygls.lsp.types.basic_structures import Range
import pytest

from refacto.core.refactoring import Refactor
from refacto.refactorings.extract_variable.refactor import RefactorExtractVariable
from refacto.refactorings.inline_variable import RefactorInlineVariable
from tests.unit_tests.test_case import TestCase

root_test_cases_directory = Path("tests/test_cases")

refactoring_methods: dict[str, Refactor] = {
    "extract_variable": RefactorExtractVariable(),
    "inline_variable": RefactorInlineVariable(),
}


@dataclass
class TestCaseBuilder:
    test_case_dir: Path
    refactor_class: Refactor

    @property
    def before(self) -> Path:
        return self.test_case_dir.joinpath("before.py")

    @property
    def after(self) -> Path:
        return self.test_case_dir.joinpath("after.py")

    @property
    def selected_range(self) -> Range:
        selected_range = self._get_params("selected_range")
        assert isinstance(selected_range, Range)
        return selected_range

    @property
    def selected_code(self) -> str:
        selected_code = self._get_params("selected_code")
        assert isinstance(selected_code, str)
        return selected_code

    def test_case(self) -> TestCase:
        return TestCase(
            before=self.before,
            expected=self.after,
            selected_range=self.selected_range,
            refactoring_method=self.refactor_class,
            selected_code=self.selected_code,
        )

    def _get_params(self, key: str) -> Range | str:
        parameters: dict[str, Range | str] = {}
        paramters_path = self.test_case_dir.joinpath("parameters.py")
        with open(paramters_path) as parameters_file:
            exec(parameters_file.read(), parameters)
        return parameters[key]


def child_directories(root_dir: Path) -> Iterable[Path]:
    for child_file in root_dir.iterdir():
        if child_file.is_dir():
            yield child_file


def iterate_test_cases() -> Iterable[Any]:
    for refactoring_method_dir in child_directories(root_test_cases_directory):
        refactoring_method_name = refactoring_method_dir.name
        refactoring_method = refactoring_methods[refactoring_method_name]
        for test_case_dir in child_directories(refactoring_method_dir):
            builder = TestCaseBuilder(test_case_dir=test_case_dir, refactor_class=refactoring_method)
            test_name = builder.test_case_dir.name
            test_id = f"{refactoring_method_name}_{test_name}"
            yield pytest.param(builder.test_case(), id=test_id)
