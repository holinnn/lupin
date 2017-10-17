import pytest

from lupin import fields as f, errors as e, validators as v


@pytest.fixture
def field():
    return f.Field(validators=[v.Type(str)])


class TestDump(object):
    def test_returns_the_same_value(self, field):
        assert field.dump("46") == "46"


class TestLoad(object):
    def test_returns_the_same_value(self, field):
        assert field.load("46") == "46"


class TestInjectAttr(object):
    def test_add_loaded_value_to_dict(self, field):
        attrs = {}
        data = {"id": "46"}
        field.inject_attr(data, "id", attrs)
        assert attrs == {
            "id": "46"
        }

    def test_uses_default_if_no_value(self):
        field = f.Field(default="46")
        attrs = {}
        data = {}
        field.inject_attr(data, "id", attrs)
        assert attrs == {
            "id": "46"
        }


class TestValidate(object):
    def test_raise_error_if_invalid_data(self, field):
        with pytest.raises(e.InvalidType):
            field.validate(46, [])
