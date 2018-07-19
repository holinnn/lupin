import pytest

from lupin import fields as f, errors as e, validators as v, Mapper, processors


@pytest.fixture
def mapper():
    return Mapper()


@pytest.fixture
def field():
    return f.Field(validators=[v.Type(str)],
                   pre_dump=[processors.lower],
                   post_dump=[processors.strip],
                   pre_load=[processors.upper])


class TestDump(object):
    def test_returns_the_same_value(self, field, mapper):
        assert field.dump("46", mapper) == "46"


class TestLoad(object):
    def test_returns_the_same_value(self, field, mapper):
        assert field.load("46", mapper) == "46"


class TestPreLoad(object):
    def test_use_processor(self, field):
        assert field.pre_load("hello") == "HELLO"


class TestPostLoad(object):
    def test_use_default_processor(self, field):
        assert field.post_load("hello") == "hello"


class TestExtractAttr(object):
    def test_returns_attr_from_object(self, field, thief, mapper):
        thief.last_name = " lupin  "
        value = field.extract_attr(thief, mapper, "last_name")
        assert value == "lupin"


class TestValidate(object):
    def test_raise_error_if_invalid_data(self, field, mapper):
        with pytest.raises(e.InvalidType):
            field.validate(46, [], mapper)

    def test_do_not_raise_error_if_allow_none_is_trye(self, mapper):
        field = f.Field(validators=[v.Type(str)], allow_none=True)
        field.validate(None, [], mapper)
