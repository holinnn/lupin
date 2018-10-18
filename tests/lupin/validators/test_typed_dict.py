from lupin.errors import InvalidType
from lupin.validators.typed_dict import TypedDict
import pytest


@pytest.fixture
def validator():
    return TypedDict(str, str)


class TestCall(object):
    def test_do_not_raise_error_if_none(self, validator):
        validator(None, [])

    def test_do_not_raise_error_if_valid_dict(self, validator):
        validator({"a": "a"}, [])

    def test_raise_error_if_invalid_key_type(self, validator):
        with pytest.raises(InvalidType):
            validator({1: "1"}, [])

    def test_raise_error_if_invalid_value_type(self, validator):
        with pytest.raises(InvalidType):
            validator({"1": 1}, [])
