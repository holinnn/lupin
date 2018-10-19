import re
from lupin.errors import InvalidMatch
from lupin.validators.dict_keys_format import DictKeysFormat
import pytest


@pytest.fixture
def validator():
    return DictKeysFormat(re.compile("^\d$"))


class TestCall(object):
    def test_do_not_raise_error_if_none(self, validator):
        validator(None, [])

    def test_do_not_raise_error_if_valid_dict(self, validator):
        validator({"1": "a"}, [])

    def test_raise_error_if_invalid_format(self, validator):
        with pytest.raises(InvalidMatch):
            validator({"a": "1"}, [])
