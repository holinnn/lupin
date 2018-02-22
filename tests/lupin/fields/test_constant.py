import pytest

from lupin.fields import Constant
from lupin.errors import NotEqual
from lupin import Mapper


@pytest.fixture
def mapper():
    return Mapper()


@pytest.fixture
def field():
    return Constant(46)


class TestLoad(object):
    def test_returns_fixed_value(self, field, mapper):
        assert field.load(None, mapper) == 46


class TestDump(object):
    def test_returns_fixed_value(self, field, mapper):
        assert field.dump(None, mapper) == 46


class TestExtractAttr(object):
    def test_returns_fixed_value(self, field, mapper):
        assert field.extract_attr(None, mapper) == 46


class TestValidate(object):
    def test_raises_error_if_not_constant_value(self, field, mapper):
        with pytest.raises(NotEqual):
            field.validate("arsene", [], mapper)

    def test_does_nothing_if_constant_value(self, field, mapper):
        field.validate(46, [], mapper)
