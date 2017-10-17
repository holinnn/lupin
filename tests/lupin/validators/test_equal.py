import pytest

from lupin.validators import Equal
from lupin.errors import NotEqual


@pytest.fixture
def validator():
    return Equal(46)


class TestCall(object):
    def test_raise_error_if_invalid_value(self, validator):
        with pytest.raises(NotEqual):
            validator("46", [])

    def test_does_nothing_if_valid(self, validator):
        validator(46, [])
