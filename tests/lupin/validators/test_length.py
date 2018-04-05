import pytest

from lupin.errors import InvalidLength
from lupin.validators import Length


@pytest.fixture
def validator():
    return Length(min=2, max=3)


class TestCall(object):
    def test_raise_error_if_not_enough_values(self, validator):
        with pytest.raises(InvalidLength):
            validator([1], [])

    def test_raise_error_if_to_much_values(self, validator):
        with pytest.raises(InvalidLength):
            validator([1, 2, 3, 4], [])

    def test_does_nothing_if_enough_values(self, validator):
        validator([1, 2], [])

    def test_raise_error_if_value_has_no_length(self, validator):
        with pytest.raises(InvalidLength):
            validator(None, [])
