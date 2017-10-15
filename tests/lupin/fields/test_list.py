from datetime import datetime
import pytest

from lupin import List, Datetime


@pytest.fixture
def field():
    return List(Datetime(format="%Y-%m-%d"))


@pytest.fixture
def datetimes():
    return [
        datetime(2017, 1, 1),
        datetime(2018, 1, 1)
    ]


@pytest.fixture
def datetime_strings():
    return [
        "2017-01-01",
        "2018-01-01"
    ]


class TestLoad(object):
    def test_returns_a_list_of_datetime(self, field, datetimes, datetime_strings):
        result = field.load(datetime_strings)
        assert result == datetimes


class TestDump(object):
    def test_returns_a_list_of_datetime_strings(self, field, datetimes, datetime_strings):
        result = field.dump(datetimes)
        assert result == datetime_strings
