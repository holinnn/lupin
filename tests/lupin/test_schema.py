# coding: utf-8
import pytest

from lupin import Constant
from lupin.errors import InvalidDocument, InvalidType
from tests.fixtures import Thief


class TestLoad(object):
    def test_returns_a_thief(self, thief_schema, thief_data):
        thief = thief_schema.load(Thief, thief_data)
        assert isinstance(thief, Thief)
        assert thief.last_name == "Lupin"
        assert thief.first_name == "Arsène"


class TestDump(object):
    def test_returns_a_dictionary(self, thief_schema, thief, thief_data):
        data = thief_schema.dump(thief)
        assert data == thief_data


class TestAddField(object):
    def test_add_new_field_to_schema(self, thief_schema, thief, thief_data):
        thief_schema.add_field("age", Constant(28))
        result = thief_schema.dump(thief)
        thief_data["age"] = 28
        assert result == thief_data


class TestValidate(object):
    def test_raise_exception_if_invalid_data(self, thief_schema, thief_data):
        thief_data["firstName"] = 46
        with pytest.raises(InvalidDocument) as exc:
            thief_schema.validate(thief_data)

        errors = exc.value
        assert len(errors) == 1
        error = errors[0]
        assert isinstance(error, InvalidType)
        assert error.path == ["firstName"]

    def test_does_nothing_if_valid(self, thief_schema, thief_data):
        thief_schema.validate(thief_data)
