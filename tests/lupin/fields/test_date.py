import datetime
from lupin import fields, Mapper
import pytest


@pytest.fixture
def mapper():
    return Mapper()


@pytest.fixture
def field():
    return fields.Date()


@pytest.fixture
def date():
    return datetime.date(2017, 10, 7)


class TestDump(object):
    def test_returns_date_as_string(self, field, date, mapper):
        assert field.dump(date, mapper) == "2017-10-07"


class TestLoad(object):
    def test_returns_a_date(self, field, date, mapper):
        assert field.load("2017-10-07", mapper) == date
