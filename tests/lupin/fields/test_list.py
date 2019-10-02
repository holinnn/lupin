from datetime import datetime
import pytest

from lupin.fields import List, DateTime, String
from lupin.errors import InvalidType
from lupin import Mapper, processors


@pytest.fixture
def mapper():
    return Mapper()


@pytest.fixture
def field():
    return List(DateTime(format="%Y-%m-%d"))


@pytest.fixture
def pre_load_field():
    return List(String(pre_load=[processors.lower],
                       post_load=[processors.strip],
                       post_dump=[processors.upper]),
                )


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
    def test_returns_a_list_of_datetime(self, field, datetimes, datetime_strings, mapper):
        result = field.load(datetime_strings, mapper)
        assert result == datetimes

    def test_returns_none_if_value_is_null(self, field, mapper):
        assert field.load(None, mapper) is None


class TestLoadElem(object):
    def test_returns_a_list_of_processed_element(self, pre_load_field, mapper):
        result = pre_load_field.load([" ARSENE", "LUPIN "], mapper)
        assert result == ["arsene", "lupin"]


class TestDump(object):
    def test_returns_a_list_of_datetime_strings(self, field, datetimes, datetime_strings, mapper):
        result = field.dump(datetimes, mapper)
        assert result == datetime_strings

    def test_returns_none_if_value_is_null(self, field, mapper):
        assert field.dump(None, mapper) is None


class TestDumpElem(object):
    def test_return_a_list_of_processed_element(self, pre_load_field, mapper):
        result = pre_load_field.dump(["arsene", "lupin"], mapper)
        assert result == ["ARSENE", "LUPIN"]


class TestValidate(object):
    def test_do_not_raise_error_if_none_and_allow_none(self):
        field = List(DateTime(format="%Y-%m-%d"), allow_none=True)
        field.validate(None, [], mapper)

    def test_raise_exception_if_not_list(self, field):
        with pytest.raises(InvalidType):
            field.validate("", [], mapper)

    def test_raise_exception_if_an_item_is_invalid(self, field, mapper):
        with pytest.raises(InvalidType) as exc:
            field.validate([46], [], mapper)

        error = exc.value
        assert error.path == ["0"]

    def test_does_nothing_if_all_items_are_valid(self, field, datetime_strings, mapper):
        field.validate(datetime_strings, [], mapper)
