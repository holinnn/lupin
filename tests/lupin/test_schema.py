# coding: utf-8
import pytest

from lupin import Constant, fields as f, Mapper
from lupin.errors import InvalidDocument, InvalidType, MissingKey
from tests.fixtures import Thief


@pytest.fixture
def mapper():
    return Mapper()


class TestLoad(object):
    def test_returns_a_thief(self, thief_schema, thief_data, mapper):
        thief = thief_schema.load(Thief, thief_data, mapper)
        assert isinstance(thief, Thief)
        assert thief.last_name == "Lupin"
        assert thief.first_name == "Arsène"


class TestLoadAttrs(object):
    def test_returns_a_dict_with_all_attrs(self, thief_schema, thief_data, mapper):
        attrs = thief_schema.load_attrs(thief_data, mapper)
        assert attrs == {
            "first_name": "Arsène",
            "last_name": "Lupin"
        }

    def test_returns_default_value_if_missing_key(self, thief_schema, thief_data, mapper):
        del thief_data["firstName"]
        attrs = thief_schema.load_attrs(thief_data, mapper)
        assert attrs == {
            "first_name": None,
            "last_name": "Lupin"
        }

    def test_returns_no_attr_if_allow_partial_and_missing_key(self, thief_schema, thief_data, mapper):
        del thief_data["firstName"]
        attrs = thief_schema.load_attrs(thief_data, mapper, allow_partial=True)
        assert attrs == {
            "last_name": "Lupin"
        }

    def test_do_not_load_read_only_attribute(self, thief_schema, thief_data, mapper):
        thief_schema.add_field("lastName", f.String(read_only=True))
        attrs = thief_schema.load_attrs(thief_data, mapper, allow_partial=True)
        assert attrs == {
            "first_name": "Arsène"
        }


class TestDump(object):
    def test_returns_a_dictionary(self, thief_schema, thief, thief_data, mapper):
        data = thief_schema.dump(thief, mapper)
        assert data == thief_data


class TestAddField(object):
    def test_add_new_field_to_schema(self, thief_schema, thief, thief_data, mapper):
        thief_schema.add_field("age", Constant(28))
        result = thief_schema.dump(thief, mapper)
        thief_data["age"] = 28
        assert result == thief_data


class TestValidate(object):
    def test_raise_exception_if_invalid_data(self, thief_schema, thief_data, mapper):
        thief_data["firstName"] = 46
        with pytest.raises(InvalidDocument) as exc:
            thief_schema.validate(thief_data, mapper)

        errors = exc.value
        assert len(errors) == 1
        error = errors[0]
        assert isinstance(error, InvalidType)
        assert error.path == ["firstName"]

    def test_does_nothing_if_valid(self, thief_schema, thief_data, mapper):
        thief_schema.validate(thief_data, mapper)

    def test_raise_error_if_missing_key(self, thief_schema, thief_data, mapper):
        del thief_data["firstName"]
        with pytest.raises(InvalidDocument) as exc:
            thief_schema.validate(thief_data, mapper)

        errors = exc.value
        assert len(errors) == 1
        error = errors[0]
        assert isinstance(error, MissingKey)
        assert error.path == ["firstName"]

    def test_do_not_raise_exception_if_allow_partial_and_missing_key(self, thief_schema, thief_data, mapper):
        del thief_data["firstName"]
        thief_schema.validate(thief_data, mapper, allow_partial=True)

    def test_do_not_raise_exception_if_optional_field(self, thief_schema, thief_data, mapper):
        thief_schema.add_field("age", f.String(optional=True))
        assert "age" not in thief_data
        thief_schema.validate(thief_data, mapper)
