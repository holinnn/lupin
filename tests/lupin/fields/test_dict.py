import pytest

from lupin.fields import Dict
from lupin.errors import InvalidType


@pytest.fixture
def field():
    return Dict()


class TestValidate(object):
    def test_raises_error_if_not_a_dict(self, field):
        with pytest.raises(InvalidType):
            field.validate([], [])

    def test_does_nothing_if_dict(self, field):
        field.validate({}, [])
