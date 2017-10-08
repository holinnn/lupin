from lupin import Field
import pytest


@pytest.fixture
def field():
    return Field()


class TestDump(object):
    def test_returns_the_same_value(self, field):
        assert field.dump("46") == "46"


class TestLoad(object):
    def test_returns_the_same_value(self, field):
        assert field.load("46") == "46"
