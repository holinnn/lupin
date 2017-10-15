import pytest

from lupin import Mapper, Mapping, Schema, String
from tests.fixtures import Thief


@pytest.fixture
def mapper():
    return Mapper()


class TestRegister(object):
    def test_returns_a_mapping(self, mapper, thief_schema):
        mapping = mapper.register(Thief, thief_schema)
        assert isinstance(mapping, Mapping)

    def test_sets_the_default_schema(self, mapper, thief_schema, thief):
        mapper.register(Thief, thief_schema)
        other_schema = Schema({
            "firstName": String(binding="first_name")
        })
        mapper.register(Thief, other_schema, default=True)
        data = mapper.dump(thief)
        assert data == {
            "firstName": "Arsène"
        }


class TestDump(object):
    @pytest.fixture(autouse=True)
    def mapping(self, mapper, thief_schema):
        return mapper.register(Thief, thief_schema)

    def test_returns_thief_data(self, thief, mapper, thief_data, mapping):
        data = mapper.dump(thief, mapping)
        assert data == thief_data

    def test_uses_default_mapping(self, mapper, thief, thief_data):
        data = mapper.dump(thief)
        assert data == thief_data


class TestLoad(object):
    @pytest.fixture
    def mapping(self, mapper, thief_schema):
        return mapper.register(Thief, thief_schema)

    def test_returns_a_thief(self, mapper, thief_data, mapping):
        thief = mapper.load(thief_data, mapping)
        assert isinstance(thief, Thief)
