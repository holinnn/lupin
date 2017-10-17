import pytest

from lupin import Mapper, Object
from lupin.errors import InvalidDocument
from tests.fixtures import Thief


@pytest.fixture
def mapping(thief_schema):
    mapper = Mapper()
    return mapper.register(Thief, thief_schema)


@pytest.fixture
def field(mapping):
    return Object(mapping)


class TestLoad(object):
    def test_returns_a_thief(self, field, thief_data):
        thief = field.load(thief_data)
        assert isinstance(thief, Thief)


class TestDump(object):
    def test_returns_thief_data(self, field, thief, thief_data):
        data = field.dump(thief)
        assert data == thief_data


class TestValidate(object):
    def test_does_nothing_if_valid(self, field, thief_data):
        field.validate(thief_data, [])

    def test_raises_error_if_invalid_data(self, field, thief_data):
        thief_data["firstName"] = 46
        with pytest.raises(InvalidDocument):
            field.validate(thief_data, [])
