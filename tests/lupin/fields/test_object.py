import pytest

from lupin import Mapper, Object
from tests.fixtures import Thief


@pytest.fixture
def mapping(thief_schema):
    mapper = Mapper()
    return mapper.register(Thief, thief_schema)


@pytest.fixture
def field(mapping):
    return Object(mapping)


class TestLoad(object):
    def test_returns_a_thief(self, field, thief_data):
        thief = field.load(thief_data)
        assert isinstance(thief, Thief)


class TestDump(object):
    def test_returns_thief_data(self, field, thief, thief_data):
        data = field.dump(thief)
        assert data == thief_data
