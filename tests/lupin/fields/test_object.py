import pytest

from lupin import Mapper, Object
from lupin.errors import InvalidDocument
from tests.fixtures import Thief


@pytest.fixture
def mapper():
    return Mapper()


@pytest.fixture(autouse=True)
def mapping(mapper, thief_schema):
    mapper.register(Thief, thief_schema)


@pytest.fixture
def field(thief_schema):
    return Object(thief_schema)


class TestLoad(object):
    def test_returns_a_thief(self, field, thief_data, mapper):
        thief = field.load(thief_data, mapper)
        assert isinstance(thief, Thief)

    def test_returns_none_if_none_value(self, field, mapper):
        assert field.load(None, mapper) is None


class TestDump(object):
    def test_returns_thief_data(self, field, thief, thief_data, mapper):
        data = field.dump(thief, mapper)
        assert data == thief_data

    def test_returns_none_if_value_is_null(self, field, mapper):
        assert field.dump(None, mapper) is None


class TestValidate(object):
    def test_do_not_raise_error_if_none_and_allow_none(self, thief_schema):
        field = Object(thief_schema, allow_none=True)
        field.validate(None, [], mapper)

    def test_does_nothing_if_valid(self, field, thief_data, mapper):
        field.validate(thief_data, [], mapper)

    def test_raises_error_if_invalid_data(self, field, thief_data, mapper):
        thief_data["firstName"] = 46
        with pytest.raises(InvalidDocument):
            field.validate(thief_data, [], mapper)
