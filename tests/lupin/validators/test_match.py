import re

import pytest

from lupin.errors import InvalidMatch
from lupin.validators import Match


@pytest.fixture
def validator():
    regexp = re.compile("hello")
    return Match(regexp)


class TestCall(object):
    def test_raise_error_if_does_not_match(self, validator):
        with pytest.raises(InvalidMatch) as exc:
            validator("bye", [])

    def test_does_nothing_if_match(self, validator):
        validator("hello", [])

    def test_raise_error_value_is_not_a_string(self, validator):
        with pytest.raises(InvalidMatch) as exc:
            validator(None, [])
