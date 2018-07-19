# coding: utf-8
import pytest

from lupin import Mapper, Schema
from lupin.errors import MissingMapping, SchemaAlreadyRegistered, InvalidDocument, \
    InvalidPolymorphicType, SchemaNotRegistered
from tests.fixtures import Thief, Painting, Jewel


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

    def test_works_with_schema_name(self, mapper, thief, thief_data):
        data = mapper.dump(thief, "thief")
        assert data == thief_data


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

    def test_load_with_schema_name(self, mapper, thief_data):
        thieves = mapper.load([thief_data], "thief")
        assert isinstance(thieves, list)
        assert isinstance(thieves[0], Thief)


class TestLoadPolymorphic(object):
    @pytest.fixture(autouse=True)
    def setup(self, mapper, painting_schema, jewel_schema):
        mapper.register(Jewel, jewel_schema)
        mapper.register(Painting, painting_schema)

    def test_returns_a_painting(self, mapper, painting_schema, jewel_schema, mona_lisa_data):
        result = mapper.load_polymorphic(mona_lisa_data,
                                         on="type",
                                         schemas={
                                             "painting": painting_schema,
                                             "jewel": jewel_schema
                                         })

        assert isinstance(result, Painting)

    def test_loads_list(self, mapper, painting_schema, jewel_schema, stolen_items_data):
        result = mapper.load_polymorphic(stolen_items_data,
                                         on="type",
                                         schemas={
                                             "painting": painting_schema,
                                             "jewel": jewel_schema
                                         })

        assert len(result) == 2
        assert isinstance(result[0], Painting)
        assert isinstance(result[1], Jewel)

    def test_raise_error_if_invalid_type(self, mapper, painting_schema):
        with pytest.raises(InvalidPolymorphicType):
            mapper.load_polymorphic({}, on="type", schemas={"painting_schema": painting_schema})

    def test_works_with_schema_names(self, mapper, painting_schema, jewel_schema, mona_lisa_data):
        result = mapper.load_polymorphic(mona_lisa_data,
                                         on="type",
                                         schemas={
                                             "painting": "painting",
                                             "jewel": "jewel"
                                         })
        assert isinstance(result, Painting)


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

    def test_validate_with_schema_name(self, mapper, thief_data):
        mapper.validate(thief_data, "thief")


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

    def test_works_with_schema_name(self, mapper, thief_data):
        attrs = mapper.load_attrs(thief_data, "thief")
        assert attrs == {
            "first_name": "Arsène",
            "last_name": "Lupin"
        }


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

    def test_returns_a_mapping_from_the_super_class(self, mapper, thief_schema):
        class JuniorThief(Thief):
            pass

        thief = JuniorThief("John", "Doe")
        mapping = mapper.get_object_mapping(thief)
        data = mapping.dump(thief, mapper)
        assert data == {
            "firstName": "John",
            "lastName": "Doe"
        }

    def test_raise_error_if_schema_not_registered(self, mapper, jewel_schema):
        with pytest.raises(SchemaNotRegistered):
            mapper.get_object_mapping(object(), [jewel_schema])
