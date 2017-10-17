import pytest

from lupin.fields import Number
from lupin.errors import InvalidType


@pytest.fixture
def field():
    return Number()


class TestValidate(object):
    def test_raises_error_if_not_an_number(self, field):
        with pytest.raises(InvalidType):
            field.validate("46.0", [])

    def test_does_nothing_if_float(self, field):
        field.validate(46.0, [])

    def test_does_nothing_if_int(self, field):
        field.validate(46, [])
