import pytest

from lupin.validators import IsNone
from lupin.errors import NotNone


@pytest.fixture
def validator():
    return IsNone()


class TestCall(object):
    def test_raise_error_if_not_none(self, validator):
        with pytest.raises(NotNone):
            validator("46", [])

    def test_does_nothing_if_none(self, validator):
        validator(None, [])
