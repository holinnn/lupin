import pytest

from lupin.fields import Constant
from lupin.errors import NotEqual


@pytest.fixture
def field():
    return Constant(46)


class TestLoad(object):
    def test_returns_fixed_value(self, field):
        assert field.load(None) == 46


class TestDump(object):
    def test_returns_fixed_value(self, field):
        assert field.dump(None) == 46


class TestExtractAttr(object):
    def test_returns_fixed_value(self, field):
        assert field.extract_attr(None) == 46


class TestValidate(object):
    def test_raises_error_if_not_constant_value(self, field):
        with pytest.raises(NotEqual):
            field.validate("arsene", [])

    def test_does_nothing_if_constant_value(self, field):
        field.validate(46, [])
