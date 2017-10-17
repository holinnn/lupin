# encoding: utf-8
import pytest

from lupin import Mapper
from lupin.errors import InvalidDocument
from tests.fixtures import Thief


@pytest.fixture
def mapping(thief_schema):
    mapper = Mapper()
    return mapper.register(Thief, thief_schema)


class TestLoad(object):
    def test_returns_a_thief(self, mapping, thief_data):
        thief = mapping.load(thief_data)
        assert isinstance(thief, Thief)
        assert thief.last_name == "Lupin"
        assert thief.first_name == "Arsène"


class TestDump(object):
    def test_returns_a_dictionary(self, mapping, thief, thief_data):
        data = mapping.dump(thief)
        assert data == thief_data


class TestValidate(object):
    def test_raise_exception_if_invalid_data(self, mapping, thief_data):
        thief_data["firstName"] = 46
        with pytest.raises(InvalidDocument):
            mapping.validate(thief_data)

    def test_does_nothing_if_valid(self, mapping, thief_data):
        mapping.validate(thief_data)
