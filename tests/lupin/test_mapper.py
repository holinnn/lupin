# coding: utf-8
import pytest

from lupin import Mapper, Mapping, Schema, String
from lupin.errors import MissingMapping, SchemaAlreadyRegistered, InvalidDocument
from tests.fixtures import Thief


@pytest.fixture
def mapper():
    return Mapper()




class TestRegister(object):
    def test_sets_the_default_schema(self, mapper, thief_schema, thief):
        mapper.register(Thief, thief_schema)
        data = mapper.dump(thief)
        assert data == {
            "firstName": "Arsène",
            "lastName": "Lupin"
        }

    def test_raise_error_if_schema_already_registered(self, mapper, thief_schema):
        mapper.register(Thief, thief_schema)

        with pytest.raises(SchemaAlreadyRegistered):
            mapper.register(Thief, thief_schema)


class TestDump(object):
    @pytest.fixture(autouse=True)
    def mapping(self, mapper, thief_schema):
        mapper.register(Thief, thief_schema)

    def test_uses_default_mapping(self, mapper, thief, thief_data):
        data = mapper.dump(thief)
        assert data == thief_data

    def test_uses_schema(self, mapper, thief, thief_data, thief_schema):
        data = mapper.dump(thief, thief_schema)
        assert data == thief_data

    def test_dumps_list_of_objects(self, mapper, thief, thief_data):
        data = mapper.dump([thief])
        assert data == [thief_data]

    def test_raises_exception_if_no_mapping(self, mapper):
        with pytest.raises(MissingMapping):
            mapper.dump(46)


class TestLoad(object):
    @pytest.fixture(autouse=True)
    def mapping(self, mapper, thief_schema):
        mapper.register(Thief, thief_schema)

    def test_returns_a_thief(self, mapper, thief_data, thief_schema):
        thief = mapper.load(thief_data, thief_schema)
        assert isinstance(thief, Thief)

    def test_loads_list(self, mapper, thief_data, thief_schema):
        thieves = mapper.load([thief_data], thief_schema)
        assert isinstance(thieves, list)
        assert isinstance(thieves[0], Thief)


class TestValidate(object):
    @pytest.fixture(autouse=True)
    def mapping(self, mapper, thief_schema):
        mapper.register(Thief, thief_schema)

    def test_does_nothing_if_valid(self, mapper, thief_data, thief_schema):
        mapper.validate(thief_data, thief_schema)

    def test_validates_a_valid_list(self, mapper, thief_data, thief_schema):
        mapper.validate([thief_data], thief_schema)

    def test_raise_error_if_invalid(self, mapper, thief_data, thief_schema):
        with pytest.raises(InvalidDocument):
            mapper.validate({}, thief_schema)


class TestLoadAttrs(object):
    @pytest.fixture(autouse=True)
    def mapping(self, mapper, thief_schema):
        mapper.register(Thief, thief_schema)

    def test_returns_a_dict(self, mapper, thief_data, thief_schema):
        attrs = mapper.load_attrs(thief_data, thief_schema)
        assert attrs == {
            "first_name": "Arsène",
            "last_name": "Lupin"
        }

    def test_loads_list(self, mapper, thief_data, thief_schema):
        thieves = mapper.load_attrs([thief_data], thief_schema)
        assert isinstance(thieves, list)
        assert isinstance(thieves[0], dict)


class TestGetObjectMapping(object):
    @pytest.fixture(autouse=True)
    def mapping(self, mapper, thief_schema):
        mapper.register(Thief, thief_schema)

    def test_returns_mapping_of_object(self, mapper, thief):
        mapping = mapper.get_object_mapping(thief)
        assert mapping.cls == type(thief)

    def test_raises_exception_if_no_mapping(self, mapper):
        with pytest.raises(MissingMapping):
            mapper.get_object_mapping(46)

    def test_restrict_access_to_some_schemas(self, mapper, thief, thief_schema):
        schema = Schema({})
        mapper.register(Thief, schema)
        mapping = mapper.get_object_mapping(thief, schemas=[thief_schema])
        assert mapping.schema == thief_schema

    def test_raise_error_if_no_mapping_among_schemas_provided(self, mapper):
        with pytest.raises(MissingMapping):
            mapper.get_object_mapping(46, schemas=[])
