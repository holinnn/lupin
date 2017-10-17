import pytest

from lupin.fields import Bool
from lupin.errors import InvalidType


@pytest.fixture
def field():
    return Bool()


class TestValidate(object):
    def test_raises_error_if_not_a_boolean(self, field):
        with pytest.raises(InvalidType):
            field.validate(46, [])

    def test_does_nothing_if_boolean(self, field):
        field.validate(True, [])
