from datetime import datetime
from lupin import fields, Mapper
import pytest


@pytest.fixture
def mapper():
    return Mapper()


@pytest.fixture
def field():
    return fields.DateTime()


@pytest.fixture
def time():
    return datetime(2017, 10, 7, 17, 35, 0)


class TestDump(object):
    def test_returns_datetime_as_string(self, field, time, mapper):
        assert field.dump(time, mapper) == "2017-10-07T17:35:00"


class TestLoad(object):
    def test_returns_a_datetime(self, field, time, mapper):
        assert field.load("2017-10-07T17:35:00", mapper) == time
