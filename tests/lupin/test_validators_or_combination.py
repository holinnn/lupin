# -*- coding: utf-8 -*-
from lupin import ValidatorsOrCombination, ValidatorsAndCombination
from lupin.errors import ValidationError
from lupin.validators import Equal
import pytest


@pytest.fixture
def invalid():
    return Equal("sernine")


@pytest.fixture
def valid():
    return Equal("lupin")


class TestCall(object):
    def test_raise_error_if_all_validators_are_invalid(self, invalid):
        combination = ValidatorsOrCombination([invalid, invalid, invalid])
        with pytest.raises(ValidationError):
            combination("andrésy", [])

    def test_do_not_raise_error_if_one_validator_is_valid(self, invalid, valid):
        combination = ValidatorsOrCombination([invalid, valid, invalid])
        combination("lupin", [])

    def test_do_not_raise_error_if_complex_expression_is_valid(self, invalid, valid):
        combination = (valid & valid) | invalid & valid & valid | invalid
        combination("lupin", [])

    def test_raise_error_if_complex_expression_is_invalid(self, invalid, valid):
        combination = (valid & valid) | invalid & valid & valid | invalid
        with pytest.raises(ValidationError):
            combination("andrésy", [])


class TestOr(object):
    def test_returns_self_if_other_is_a_validator(self, valid):
        combination = valid | valid
        assert (combination | valid) is combination

    def test_returns_self_if_other_is_or_combination(self, valid):
        combination = valid | valid
        combination2 = valid | valid
        assert (combination | combination2) is combination

    def test_else_returns_a_new_combination(self, valid):
        combination = valid | valid
        combination2 = valid & valid
        result = combination | combination2
        assert result is not combination
        assert isinstance(result, ValidatorsOrCombination)


class TestAnd(object):
    def test_returns_an_and_combination(self, valid):
        combination = valid | valid
        result = combination & valid
        assert isinstance(result, ValidatorsAndCombination)
