import pytest

from lupin.fields import Int
from lupin.errors import InvalidType


@pytest.fixture
def field():
    return Int()


class TestValidate(object):
    def test_raises_error_if_not_an_int(self, field):
        with pytest.raises(InvalidType):
            field.validate("46", [])

    def test_does_nothing_if_int(self, field):
        field.validate(46, [])
