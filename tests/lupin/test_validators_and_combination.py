# -*- coding: utf-8 -*-
import pytest
from lupin import ValidatorsAndCombination, ValidatorsOrCombination
from lupin.validators import Equal
from lupin.errors import ValidationError


@pytest.fixture
def invalid():
    return Equal("sernine")


@pytest.fixture
def valid():
    return Equal("lupin")


class TestCall(object):
    def test_raise_error_if_at_lease_one_validators_is_invalid(self, valid, invalid):
        combination = ValidatorsAndCombination([valid, valid, invalid])
        with pytest.raises(ValidationError):
            combination("andrésy", [])

    def test_do_not_raise_error_if_all_validators_are_valid(self, valid):
        combination = ValidatorsAndCombination([valid, valid, valid])
        combination("lupin", [])


class TestAnd(object):
    def test_returns_self_if_other_is_a_validator(self, valid):
        combination = valid & valid
        assert (combination & valid) is combination

    def test_returns_self_if_other_is_and_combination(self, valid):
        combination = valid & valid
        combination2 = valid & valid
        assert (combination & combination2) is combination

    def test_else_returns_a_new_combination(self, valid):
        combination = valid & valid
        combination2 = valid | valid
        result = combination & combination2
        assert result is not combination
        assert isinstance(result, ValidatorsAndCombination)


class TestOr(object):
    def test_returns_an_or_combination(self, valid):
        combination = valid & valid
        result = combination | valid
        assert isinstance(result, ValidatorsOrCombination)
