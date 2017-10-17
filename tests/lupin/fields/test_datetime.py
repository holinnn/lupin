from datetime import datetime
from lupin import fields
import pytest


@pytest.fixture
def field():
    return fields.DateTime()


@pytest.fixture
def time():
    return datetime(2017, 10, 7, 17, 35, 0)


class TestDump(object):
    def test_returns_datetime_as_string(self, field, time):
        assert field.dump(time) == "2017-10-07T17:35:00"


class TestLoad(object):
    def test_returns_a_datetime(self, field, time):
        assert field.load("2017-10-07T17:35:00") == time
