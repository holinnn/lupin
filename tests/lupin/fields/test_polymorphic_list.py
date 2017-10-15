import pytest

from lupin import PolymorphicList, Mapper

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
