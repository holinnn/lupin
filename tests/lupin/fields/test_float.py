import pytest

from lupin.fields import Float
from lupin.errors import InvalidType
from lupin import Mapper


@pytest.fixture
def mapper():
    return Mapper()


@pytest.fixture
def field():
    return Float()


class TestValidate(object):
    def test_raises_error_if_not_an_float(self, field, mapper):
        with pytest.raises(InvalidType):
            field.validate("46.0", [], mapper)

    def test_does_nothing_if_float(self, field, mapper):
        field.validate(46.0, [], mapper)
