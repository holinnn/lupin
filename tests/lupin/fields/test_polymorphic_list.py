import pytest

from lupin import PolymorphicList, Mapper
from lupin.errors import InvalidType, InvalidDocument, MissingPolymorphicKey

from tests.fixtures import Jewel, Painting


@pytest.fixture
def field(jewel_schema, painting_schema):
    mapper = Mapper()
    jewel_mapping = mapper.register(Jewel, jewel_schema)
    painting_mapping = mapper.register(Painting, painting_schema)
    return PolymorphicList(on="type",
                           mappings={
                               "jewel": jewel_mapping,
                               "painting": painting_mapping
                           })


class TestLoad(object):
    def test_loads_different_object_types(self, field, stolen_items_data):
        result = field.load(stolen_items_data)
        assert len(result) == 2
        mona_lisa, diamond = result
        assert isinstance(mona_lisa, Painting)
        assert isinstance(diamond, Jewel)


class TestDump(object):
    def test_dumps_different_object_types(self, field, stolen_items, stolen_items_data):
        result = field.dump(stolen_items)
        assert result == stolen_items_data


class TestValidate(object):
    def test_raise_exception_if_not_list(self, field):
        with pytest.raises(InvalidType):
            field.validate("", [])

    def test_raise_exception_if_an_item_is_invalid(self, field, stolen_items_data):
        stolen_items_data[1]["carat"] = "20"
        with pytest.raises(InvalidDocument) as exc:
            field.validate(stolen_items_data, [])

        errors = exc.value
        error = errors[0]
        assert error.path == ["1", "carat"]

    def test_raises_exception_if_no_polymorphic_key(self, field, stolen_items_data):
        del stolen_items_data[0]["type"]
        with pytest.raises(MissingPolymorphicKey):
            field.validate(stolen_items_data, [])

    def test_does_nothing_if_all_items_are_valid(self, field, stolen_items_data):
        field.validate(stolen_items_data, [])
