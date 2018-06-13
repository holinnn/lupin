import pytest

from lupin import Mapper, fields as f
from lupin.errors import InvalidType, InvalidDocument, MissingPolymorphicKey,\
    InvalidPolymorphicType, MissingMapping

from tests.fixtures import Jewel, Painting

@pytest.fixture
def mapper():
    return Mapper()


@pytest.fixture
def field(mapper, jewel_schema, painting_schema):
    mapper.register(Jewel, jewel_schema)
    mapper.register(Painting, painting_schema)
    return f.PolymorphicObject(on="type",
                               schemas={
                                   "jewel": jewel_schema,
                                   "painting": painting_schema
                               })


class TestLoad(object):
    def test_loads_a_diamond(self, field, diamond_data, mapper):
        diamond = field.load(diamond_data, mapper)
        assert isinstance(diamond, Jewel)

    def test_loads_a_painting(self, field, mona_lisa_data, mapper):
        painting = field.load(mona_lisa_data, mapper)
        assert isinstance(painting, Painting)

    def test_returs_none_if_none_value(self, field, mapper):
        assert field.load(None, mapper) is None


class TestDump(object):
    def test_dumps_a_painting(self, field, mona_lisa, mona_lisa_data, mapper):
        result = field.dump(mona_lisa, mapper)
        assert result == mona_lisa_data

    def test_dumps_a_diamond(self, field, diamond, diamond_data, mapper):
        result = field.dump(diamond, mapper)
        assert result == diamond_data

    def test_returns_none_if_value_is_null(self, field, mapper):
        assert field.dump(None, mapper) is None


class TestValidate(object):
    def test_do_not_raise_error_if_none_and_allow_none(self, mapper, jewel_schema, painting_schema):
        mapper.register(Jewel, jewel_schema)
        mapper.register(Painting, painting_schema)
        field = f.PolymorphicObject(on="type",
                                    schemas={
                                        "jewel": jewel_schema,
                                        "painting": painting_schema
                                    },
                                    allow_none=True)
        field.validate(None, [], mapper)

    def test_raise_exception_if_not_dict(self, field, mapper):
        with pytest.raises(InvalidType):
            field.validate("", [], mapper)

    def test_raise_exception_if_object_is_invalid(self, field, diamond_data, mapper):
        diamond_data["carat"] = "20"
        with pytest.raises(InvalidDocument) as exc:
            field.validate(diamond_data, [], mapper)

        errors = exc.value
        error = errors[0]
        assert error.path == ["carat"]

    def test_raises_exception_if_no_polymorphic_key(self, field, diamond_data, mapper):
        del diamond_data["type"]
        with pytest.raises(MissingPolymorphicKey):
            field.validate(diamond_data, [], mapper)

    def test_raises_exception_if_invalid_polymorphic_type(self, field, diamond_data, mapper):
        diamond_data["type"] = "car"
        with pytest.raises(InvalidPolymorphicType) as err:
            field.validate(diamond_data, [], mapper)

    def test_does_nothing_if_all_items_are_valid(self, field, diamond_data, mapper):
        field.validate(diamond_data, [], mapper)
