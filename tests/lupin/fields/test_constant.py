import pytest

from lupin import Constant


@pytest.fixture
def field():
    return Constant(46)


class TestLoad(object):
    def test_returns_fixed_value(self, field):
        assert field.load(None) == 46


class TestDump(object):
    def test_returns_fixed_value(self, field):
        assert field.dump(None) == 46


class TestGetValue(object):
    def test_returns_fixed_value(self, field):
        assert field.get_value(None) == 46
