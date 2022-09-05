from collections.abc import Iterator
from difflib import unified_diff
from pathlib import Path
from typing import Callable, Iterable

from pygls.lsp.types.basic_structures import Range


def read_file(path: Path | str) -> str:
    with open(file=path, mode="r") as file_to_read:
        return file_to_read.read()


def colorize(line: str, color: int) -> str:
    return f"\033[01;{color}m{line}\033[0m"


class TestCase:
    __test__ = False

    def __init__(
        self,
        before: Path | str,
        expected: Path | str,
        selected_range: Range,
        refactoring_method: Callable[[Range, str], str],
        selected_code: str,
    ) -> None:
        self.selected_range = selected_range
        self.before = read_file(path=before)
        self.expected = read_file(path=expected)
        self.refactoring_method = refactoring_method
        self.selected_code = selected_code

    @property
    def after(self) -> str:
        return self.refactoring_method(self.selected_range, self.before)

    def diff(self) -> Iterator[str]:
        return unified_diff(
            self.expected.splitlines(keepends=True),
            self.after.splitlines(keepends=True),
        )

    def colorized_diff(self) -> Iterable[str]:
        for line in self.diff():
            if line.startswith("-"):
                yield colorize(line=line, color=31)
            elif line.startswith("+"):
                yield colorize(line=line, color=32)
            elif line.startswith("^"):
                yield colorize(line=line, color=33)
            else:
                yield line
