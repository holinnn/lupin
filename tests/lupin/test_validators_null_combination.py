from lupin import ValidatorsNullCombination, ValidatorsOrCombination, ValidatorsAndCombination
from lupin.validators import IsNone
import pytest


@pytest.fixture
def combination():
    return ValidatorsNullCombination()


class TestAnd(object):
    def test_returns_an_and_combination(self, combination):
        result = combination & IsNone()
        assert isinstance(result, ValidatorsAndCombination)


class TestOr(object):
    def test_returns_an_or_combination(self, combination):
        result = combination | IsNone()
        assert isinstance(result, ValidatorsOrCombination)
