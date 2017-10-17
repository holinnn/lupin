import pytest

from lupin.errors import InvalidIn
from lupin.validators import In


@pytest.fixture
def validator():
    return In({1, 2, 3})


class TestCall(object):
    def test_raise_error_if_invalid_value(self, validator):
        with pytest.raises(InvalidIn):
            validator(4, [])

    def test_does_nothing_if_valid_value(self, validator):
        validator(1, [])
