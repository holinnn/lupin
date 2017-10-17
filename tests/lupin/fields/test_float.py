import pytest

from lupin.fields import Float
from lupin.errors import InvalidType


@pytest.fixture
def field():
    return Float()


class TestValidate(object):
    def test_raises_error_if_not_an_float(self, field):
        with pytest.raises(InvalidType):
            field.validate("46.0", [])

    def test_does_nothing_if_float(self, field):
        field.validate(46.0, [])
