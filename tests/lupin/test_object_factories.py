# coding: utf-8
import pytest

from lupin import bind, constructor
from tests.fixtures import Thief


class TestBind(object):
    def test_bind_custom_attributes_on_instance(self):
        thief = bind(Thief, {"age": 28})
        assert isinstance(thief, Thief)
        assert thief.age == 28


class TestConstructor(object):
    def test_throw_error_if_invalid_argument(self):
        with pytest.raises(TypeError):
            constructor(Thief, {"age": 28})

    def test_returns_a_thief(self):
        arsene = constructor(Thief, {"first_name": "Arsène", "last_name": "Lupin"})
        assert isinstance(arsene, Thief)
        assert arsene.first_name == "Arsène"
        assert arsene.last_name == "Lupin"
