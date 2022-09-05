import sys

import pytest

from refacto.refactorings.refactoring_utilities import souce_code_in_range
from tests.unit_tests.collector import iterate_test_cases
from tests.unit_tests.test_case import TestCase


@pytest.mark.parametrize("test_case", iterate_test_cases())
def test_refactorings(test_case: TestCase) -> None:
    sys.stderr.writelines(test_case.colorized_diff())
    assert test_case.after == test_case.expected


@pytest.mark.parametrize("test_case", iterate_test_cases())
def test_selected_code(test_case: TestCase) -> None:
    actual: str = souce_code_in_range(code_range=test_case.selected_range, source=test_case.before)
    assert actual == test_case.selected_code
