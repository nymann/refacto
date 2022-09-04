from difflib import context_diff

from devtools import debug
import pytest

from tests.unit_tests.collector import TestCase
from tests.unit_tests.collector import collect_test_cases


@pytest.mark.parametrize("test_case", collect_test_cases())
def test_refactorings(test_case: TestCase) -> None:
    actual = test_case.after.splitlines()
    expected = test_case.expected.splitlines()
    debug(context_diff(expected, actual, fromfile="expected.py", tofile="actual.py"))
    assert test_case.after == test_case.expected
