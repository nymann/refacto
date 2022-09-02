from unittest.mock import MagicMock

import pytest
from pytest_mock.plugin import MockerFixture

from refacto.main import welcome


@pytest.fixture()
def mocked_greet(mocker: MockerFixture) -> MagicMock:
    mocked = mocker.patch("typer.echo")
    welcome(name="Joe")
    return mocked


def test_greet_positive(mocked_greet: MagicMock) -> None:
    mocked_greet.assert_called_with("Welcome Joe!")


def test_greet_negative(mocked_greet: MagicMock) -> None:
    with pytest.raises(AssertionError):
        mocked_greet.assert_called_with("Welcome Karen!")
