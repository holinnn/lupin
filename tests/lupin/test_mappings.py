import pytest

from lupin import Mappings, Schema, StringField

from tests.fixtures import Thief


@pytest.fixture
def mappings(thief_schema):
    return Mappings(Thief, thief_schema)


@pytest.fixture
def other_schema():
    return Schema({
        "firstName": StringField(binding="first_name")
    })


class TestLoad(object):
    def test_use_default_schema(self, mappings, thief_data):
        thief = mappings.load(thief_data)
        assert isinstance(thief, Thief)
        assert thief.last_name == "Lupin"

    def test_use_other_schema(self, mappings, thief_data, other_schema):
        thief = mappings.load(thief_data, other_schema)
        assert not hasattr(thief, "last_name")


class TestDump(object):
    def test_use_default_schema(self, mappings, thief_data, thief):
        data = mappings.dump(thief)
        assert data == thief_data

    def test_use_other_schema(self, mappings, thief, other_schema):
        data = mappings.dump(thief, other_schema)
        assert data == {
            "firstName": "Arsène"
        }


class TestAdd(object):
    def test_set_default_schema(self, mappings, other_schema, thief_data):
        mappings.add(other_schema, default=True)
        thief = mappings.load(thief_data)
        assert not hasattr(thief, "last_name")
