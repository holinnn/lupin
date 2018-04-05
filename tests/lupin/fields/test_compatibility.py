from lupin.fields.compatibility import merge_validator
from lupin.validators import Equal
from lupin.errors import ValidationError
import pytest


@pytest.fixture
def invalid():
    return Equal("sernine")


@pytest.fixture
def valid():
    return Equal("lupin")


class TestMergeValidator(object):
    def test_add_validator_to_list(self, valid, invalid):
        kwargs = {"validators": [valid]}
        merge_validator(kwargs , invalid)
        with pytest.raises(ValidationError):
            kwargs["validators"]("lupin", [])

    def test_add_validator_to_validator(self, valid, invalid):
        kwargs = {"validators": valid}
        merge_validator(kwargs , invalid)
        with pytest.raises(ValidationError):
            kwargs["validators"]("lupin", [])

    def test_set_validator_if_no_validators(self, invalid):
        kwargs = {}
        merge_validator(kwargs , invalid)
        assert kwargs["validators"] is invalid
