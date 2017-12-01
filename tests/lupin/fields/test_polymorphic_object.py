import pytest

from lupin import Mapper, fields as f
from lupin.errors import InvalidType, InvalidDocument, MissingPolymorphicKey

from tests.fixtures import Jewel, Painting


@pytest.fixture
def field(jewel_schema, painting_schema):
    mapper = Mapper()
    jewel_mapping = mapper.register(Jewel, jewel_schema)
    painting_mapping = mapper.register(Painting, painting_schema)
    return f.PolymorphicObject(on="type",
                               mappings={
                                   "jewel": jewel_mapping,
                                   "painting": painting_mapping
                               })


class TestLoad(object):
    def test_loads_a_diamond(self, field, diamond_data):
        diamond = field.load(diamond_data)
        assert isinstance(diamond, Jewel)

    def test_loads_a_painting(self, field, mona_lisa_data):
        painting = field.load(mona_lisa_data)
        assert isinstance(painting, Painting)


class TestDump(object):
    def test_dumps_a_painting(self, field, mona_lisa, mona_lisa_data):
        result = field.dump(mona_lisa)
        assert result == mona_lisa_data

    def test_dumps_a_diamond(self, field, diamond, diamond_data):
        result = field.dump(diamond)
        assert result == diamond_data


class TestValidate(object):
    def test_raise_exception_if_not_dict(self, field):
        with pytest.raises(InvalidType):
            field.validate("", [])

    def test_raise_exception_if_object_is_invalid(self, field, diamond_data):
        diamond_data["carat"] = "20"
        with pytest.raises(InvalidDocument) as exc:
            field.validate(diamond_data, [])

        errors = exc.value
        error = errors[0]
        assert error.path == ["carat"]

    def test_raises_exception_if_no_polymorphic_key(self, field, diamond_data):
        del diamond_data["type"]
        with pytest.raises(MissingPolymorphicKey):
            field.validate(diamond_data, [])

    def test_does_nothing_if_all_items_are_valid(self, field, diamond_data):
        field.validate(diamond_data, [])
