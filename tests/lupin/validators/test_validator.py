# -*- coding: utf-8 -*-
import pytest
from lupin.validators import Equal
from lupin.errors import ValidationError


@pytest.fixture
def invalid():
    return Equal("sernine")


@pytest.fixture
def valid():
    return Equal("lupin")


class TestAnd(object):
    def test_returns_an_and_combination(self, valid, invalid):
        combination = valid & invalid
        with pytest.raises(ValidationError):
            combination("andrésy", [])


class TestOr(object):
    def test_returns_an_and_combination(self, valid, invalid):
        combination = valid | invalid
        combination("lupin", [])
