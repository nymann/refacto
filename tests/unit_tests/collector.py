from collections.abc import Iterable
from pathlib import Path
from typing import Callable

from pygls.lsp.types.basic_structures import Range

from refacto.refactorings.extract_variable import extract_variable

root_test_cases_directory = Path("tests/test_cases")

refactorin_methods: dict[str, Callable[[Range, str], str]] = {
    "extract_variable": extract_variable,
}


class TestCase:
    __test__ = False

    def __init__(
        self,
        before: Path | str,
        expected: Path | str,
        range: Range,
        refactoring_method: Callable[[Range, str], str],
    ) -> None:
        self.range = range
        self.before: str = self.read_file(path=before)
        self.expected: str = self.read_file(path=expected)
        self.refactoring_method = refactoring_method

    @staticmethod
    def read_file(path: Path | str) -> str:
        with open(file=path, mode="r") as file_to_read:
            return file_to_read.read()

    @property
    def after(self) -> str:
        return self.refactoring_method(self.range, self.before)


def collect_test_cases() -> Iterable[TestCase]:
    test_cases: list[TestCase] = []
    for refactoring_method_dir in root_test_cases_directory.iterdir():
        if not refactoring_method_dir.is_dir():
            continue
        for test_case_dir in refactoring_method_dir.iterdir():
            if not test_case_dir.is_dir():
                continue
            if test_case_dir.name != "simplest":
                continue
            before = test_case_dir.joinpath("before.py")
            after = test_case_dir.joinpath("after.py")
            range: dict[str, Range] = {}
            range_path = test_case_dir.joinpath("range.py")
            with open(range_path) as range_file:
                exec(range_file.read(), range)
            refactoring_method = refactorin_methods[refactoring_method_dir.name]
            test_cases.append(
                TestCase(
                    before=before,
                    expected=after,
                    range=range["range"],
                    refactoring_method=refactoring_method,
                ),
            )
    return test_cases
