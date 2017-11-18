# coding: utf-8
import pytest

from lupin import Mapper, Mapping, Schema, String
from lupin.errors import MissingMapping
from tests.fixtures import Thief


@pytest.fixture
def mapper():
    return Mapper()


@pytest.fixture(autouse=True)
def mapping(mapper, thief_schema):
    return mapper.register(Thief, thief_schema)


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
    def test_returns_thief_data(self, thief, mapper, thief_data, mapping):
        data = mapper.dump(thief, mapping)
        assert data == thief_data

    def test_uses_default_mapping(self, mapper, thief, thief_data):
        data = mapper.dump(thief)
        assert data == thief_data

    def test_dumps_list_of_objects(self, mapper, thief, thief_data):
        data = mapper.dump([thief])
        assert data == [thief_data]

    def test_raises_exception_if_no_mapping(self, mapper):
        with pytest.raises(MissingMapping):
            mapper.dump(46)


class TestLoad(object):
    def test_returns_a_thief(self, mapper, thief_data, mapping):
        thief = mapper.load(thief_data, mapping)
        assert isinstance(thief, Thief)

    def test_loads_list(self, mapper, thief_data, mapping):
        thieves = mapper.load([thief_data], mapping)
        assert isinstance(thieves, list)
        assert isinstance(thieves[0], Thief)


class TestLoadAttrs(object):
    def test_returns_a_dict(self, mapper, thief_data, mapping):
        attrs = mapper.load_attrs(thief_data, mapping)
        assert attrs == {
            "first_name": "Arsène",
            "last_name": "Lupin"
        }

    def test_loads_list(self, mapper, thief_data, mapping):
        thieves = mapper.load_attrs([thief_data], mapping)
        assert isinstance(thieves, list)
        assert isinstance(thieves[0], dict)
