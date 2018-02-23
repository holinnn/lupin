import pytest

from lupin.fields import Bool
from lupin.errors import InvalidType
from lupin import Mapper


@pytest.fixture
def mapper():
    return Mapper()


@pytest.fixture
def field():
    return Bool()


class TestValidate(object):
    def test_raises_error_if_not_a_boolean(self, field, mapper):
        with pytest.raises(InvalidType):
            field.validate(46, [], mapper)

    def test_does_nothing_if_boolean(self, field, mapper):
        field.validate(True, [], mapper)
