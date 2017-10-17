from datetime import datetime
import pytest

from lupin.fields import List, DateTime
from lupin.errors import InvalidType


@pytest.fixture
def field():
    return List(DateTime(format="%Y-%m-%d"))


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


class TestValidate(object):
    def test_raise_exception_if_not_list(self, field):
        with pytest.raises(InvalidType):
            field.validate("", [])

    def test_raise_exception_if_an_item_is_invalid(self, field):
        with pytest.raises(InvalidType) as exc:
            field.validate([46], [])

        error = exc.value
        assert error.path == ["0"]

    def test_does_nothing_if_all_items_are_valid(self, field, datetime_strings):
        field.validate(datetime_strings, [])
