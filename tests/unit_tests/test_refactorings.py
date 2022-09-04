import pytest

from tests.unit_tests.collector import TestCase
from tests.unit_tests.collector import collect_test_cases


@pytest.mark.parametrize("test_case", collect_test_cases())
def test_refactorings(test_case: TestCase) -> None:
    assert test_case.expected == test_case.after
