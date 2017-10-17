import pytest

from lupin.validators import DateTimeFormat
from lupin.errors import InvalidDateTimeFormat


@pytest.fixture
def validator():
    return DateTimeFormat("%Y-%m-%d")


class TestCall(object):
    def test_raise_error_if_invalid_format(self, validator):
        with pytest.raises(InvalidDateTimeFormat):
            validator("01-01-2017", [])

    def test_does_nothing_if_valid_format(self, validator):
        validator("2017-01-01", [])
