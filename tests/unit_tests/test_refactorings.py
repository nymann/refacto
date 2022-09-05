import sys

import pytest

from tests.unit_tests.collector import iterate_test_cases
from tests.unit_tests.test_case import TestCase


@pytest.mark.parametrize("test_case", iterate_test_cases())
def test_refactorings(test_case: TestCase) -> None:
    sys.stderr.writelines(test_case.colorized_diff())
    assert test_case.after == test_case.expected
