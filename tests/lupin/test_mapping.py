# encoding: utf-8
import pytest

from lupin import Mapping, Mapper
from lupin.errors import InvalidDocument
from tests.fixtures import Thief


@pytest.fixture
def mapper():
    return Mapper()


@pytest.fixture
def mapping(thief_schema):
    return Mapping(Thief, thief_schema)


class TestLoad(object):
    def test_returns_a_thief(self, mapping, thief_data, mapper):
        thief = mapping.load(thief_data, mapper, None)
        assert isinstance(thief, Thief)
        assert thief.last_name == "Lupin"
        assert thief.first_name == "Arsène"


class TestLoadAttrs(object):
    def test_returns_a_dict(self, mapping, thief_data, mapper):
        attrs = mapping.load_attrs(thief_data, mapper, None)
        assert attrs == {
            "first_name": "Arsène",
            "last_name": "Lupin"
        }


class TestDump(object):
    def test_returns_a_dictionary(self, mapping, thief, thief_data, mapper):
        data = mapping.dump(thief, mapper)
        assert data == thief_data


class TestValidate(object):
    def test_raise_exception_if_invalid_data(self, mapping, thief_data, mapper):
        thief_data["firstName"] = 46
        with pytest.raises(InvalidDocument):
            mapping.validate(thief_data, mapper)

    def test_does_nothing_if_valid(self, mapping, thief_data, mapper):
        mapping.validate(thief_data, mapper)


class TestCanHandle(object):
    def test_returns_false_if_wrong_class(self, mapping, diamond):
        assert not mapping.can_handle(diamond)

    def test_returns_true_if_right_class(self, mapping, thief):
        assert mapping.can_handle(thief)
