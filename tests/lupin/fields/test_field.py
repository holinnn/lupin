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


class TestExtractAttr(object):
    def test_returns_attr_from_object(self, field, thief):
        value = field.extract_attr(thief, "last_name")
        assert value == thief.last_name


class TestValidate(object):
    def test_raise_error_if_invalid_data(self, field):
        with pytest.raises(e.InvalidType):
            field.validate(46, [])
