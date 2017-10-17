import pytest

from lupin.fields import String
from lupin.errors import InvalidType


@pytest.fixture
def field():
    return String()


class TestValidate(object):
    def test_raises_error_if_not_a_string(self, field):
        with pytest.raises(InvalidType):
            field.validate(46, [])

    def test_does_nothing_if_string(self, field):
        field.validate("46", [])
