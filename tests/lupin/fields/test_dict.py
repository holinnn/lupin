import pytest

from lupin.fields import Dict
from lupin.errors import InvalidType
from lupin import Mapper


@pytest.fixture
def mapper():
    return Mapper()


@pytest.fixture
def field():
    return Dict()


class TestValidate(object):
    def test_raises_error_if_not_a_dict(self, field, mapper):
        with pytest.raises(InvalidType):
            field.validate([], [], mapper)

    def test_does_nothing_if_dict(self, field, mapper):
        field.validate({}, [], mapper)
