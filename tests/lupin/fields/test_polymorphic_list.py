import pytest

from lupin import PolymorphicList, Mapper
from lupin.errors import InvalidType, InvalidDocument, MissingPolymorphicKey,\
    InvalidPolymorphicType

from tests.fixtures import Jewel, Painting


@pytest.fixture
def mapper():
    return Mapper()

@pytest.fixture
def field(mapper, jewel_schema, painting_schema):
    mapper.register(Jewel, jewel_schema)
    mapper.register(Painting, painting_schema)
    return PolymorphicList(on="type",
                           schemas={
                               "jewel": jewel_schema,
                               "painting": painting_schema
                           })


class TestLoad(object):
    def test_loads_different_object_types(self, field, stolen_items_data, mapper):
        result = field.load(stolen_items_data, mapper)
        assert len(result) == 2
        mona_lisa, diamond = result
        assert isinstance(mona_lisa, Painting)
        assert isinstance(diamond, Jewel)

    def test_returns_none_if_value_is_null(self, field, mapper):
        assert field.load(None, mapper) is None


class TestDump(object):
    def test_dumps_different_object_types(self, field, stolen_items, stolen_items_data, mapper):
        result = field.dump(stolen_items, mapper)
        assert result == stolen_items_data

    def test_returns_none_if_value_is_null(self, field, mapper):
        assert field.dump(None, mapper) is None


class TestValidate(object):
    def test_do_not_raise_error_if_none_and_allow_none(self, mapper, jewel_schema, painting_schema):
        mapper.register(Jewel, jewel_schema)
        mapper.register(Painting, painting_schema)
        field = PolymorphicList(on="type",
                                schemas={
                                    "jewel": jewel_schema,
                                    "painting": painting_schema
                                },
                                allow_none=True)
        field.validate(None, [], mapper)

    def test_raise_exception_if_not_list(self, field, mapper):
        with pytest.raises(InvalidType):
            field.validate("", [], mapper)

    def test_raise_exception_if_an_item_is_invalid(self, field, stolen_items_data, mapper):
        stolen_items_data[1]["carat"] = "20"
        with pytest.raises(InvalidDocument) as exc:
            field.validate(stolen_items_data, [], mapper)

        errors = exc.value
        error = errors[0]
        assert error.path == ["1", "carat"]

    def test_raises_exception_if_no_polymorphic_key(self, field, stolen_items_data, mapper):
        del stolen_items_data[0]["type"]
        with pytest.raises(MissingPolymorphicKey):
            field.validate(stolen_items_data, [], mapper)

    def test_raises_exception_if_invalid_polymorphic_type(self, field, stolen_items_data, mapper):
        stolen_items_data[0]["type"] = "car"
        with pytest.raises(InvalidPolymorphicType):
            field.validate(stolen_items_data, [], mapper)

    def test_does_nothing_if_all_items_are_valid(self, field, stolen_items_data, mapper):
        field.validate(stolen_items_data, [], mapper)
