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

    def test_returns_none_if_none_value(self, field):
        assert field.load(None) is None


class TestDump(object):
    def test_returns_thief_data(self, field, thief, thief_data):
        data = field.dump(thief)
        assert data == thief_data

    def test_returns_none_if_value_is_null(self, field):
        assert field.dump(None) is None


class TestValidate(object):
    def test_does_nothing_if_valid(self, field, thief_data):
        field.validate(thief_data, [])

    def test_raises_error_if_invalid_data(self, field, thief_data):
        thief_data["firstName"] = 46
        with pytest.raises(InvalidDocument):
            field.validate(thief_data, [])
