import pytest

from lupin.validators import Type
from lupin.errors import InvalidType


@pytest.fixture
def validator():
    return Type(int)


class TestCall(object):
    def test_raise_error_if_invalid_type(self, validator):
        with pytest.raises(InvalidType):
            validator("not an int", [])

    def test_does_nothing_if_valid(self, validator):
        validator(1, [])
