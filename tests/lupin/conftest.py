# coding: utf-8
import pytest

from lupin import Schema, String, Constant, Int, Mapping, Float, processors, List

from ..fixtures import Thief, Painting, Jewel, Book


@pytest.fixture
def thief_schema():
    return Schema({
        "firstName": String(binding="first_name"),
        "lastName": String(binding="last_name")
    }, "thief")

@pytest.fixture()
def money_schema():
    return Schema({
        "currency": String(),
        "amount": Float()
    })

@pytest.fixture
def painting_schema():
    return Schema({
        "author": String(),
        "name": String(),
        "type": Constant("painting")
    }, "painting")


@pytest.fixture
def jewel_schema():
    return Schema({
        "carat": Int(),
        "name": String(),
        "type": Constant("jewel")
    }, "jewel")


@pytest.fixture
def thief_data():
    return {
        "lastName": "Lupin",
        "firstName": "Arsène"
    }


@pytest.fixture
def thief():
    return Thief(last_name="Lupin",
                 first_name="Arsène")


@pytest.fixture
def mona_lisa():
    return Painting(name="Mona Lisa",
                    author="Leonardo da Vinci")


@pytest.fixture
def painting_mapping(painting_schema):
    return Mapping(Painting, painting_schema)


@pytest.fixture
def jewel_mapping(jewel_schema):
    return Mapping(Jewel, jewel_schema)


@pytest.fixture
def mona_lisa_data():
    return {
        "name": "Mona Lisa",
        "author": "Leonardo da Vinci",
        "type": "painting"
    }

@pytest.fixture
def diamond():
    return Jewel(name="diamond", carat=20)


@pytest.fixture
def diamond_data():
    return {
        "type": "jewel",
        "name": "diamond",
        "carat": 20
    }


@pytest.fixture
def money_data():
    return {
        "currency": "Pound",
        "amount": 10000
    }


def reduce_to(n):
    """processor to reduce list"""
    def reduce(list):
        if len(list) < n:
            return n
        else:
            return list[0:n]
    return reduce


@pytest.fixture
def book_schema():
    return Schema({
        "title": String(pre_load=[processors.lower]),
        "authors": List(String(pre_load=[processors.lower]),
                        pre_load=[reduce_to(2)]),
        "type": Constant("book")
    }, "book")

@pytest.fixture
def stolen_items(mona_lisa, diamond):
    return [mona_lisa, diamond]


@pytest.fixture
def stolen_items_data(mona_lisa_data, diamond_data):
    return [mona_lisa_data, diamond_data]


@pytest.fixture
def other_stolen_items_data(mona_lisa_data, diamond_data, money_data):
    return [mona_lisa_data, diamond_data, money_data]
