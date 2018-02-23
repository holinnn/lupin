import pytest

from lupin import fields as f, errors as e, validators as v, Mapper


@pytest.fixture
def mapper():
    return Mapper()


@pytest.fixture
def field():
    return f.Field(validators=[v.Type(str)])


class TestDump(object):
    def test_returns_the_same_value(self, field, mapper):
        assert field.dump("46", mapper) == "46"


class TestLoad(object):
    def test_returns_the_same_value(self, field, mapper):
        assert field.load("46", mapper) == "46"


class TestExtractAttr(object):
    def test_returns_attr_from_object(self, field, thief, mapper):
        value = field.extract_attr(thief, mapper, "last_name")
        assert value == thief.last_name


class TestValidate(object):
    def test_raise_error_if_invalid_data(self, field, mapper):
        with pytest.raises(e.InvalidType):
            field.validate(46, [], mapper)
