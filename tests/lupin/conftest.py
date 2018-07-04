# coding: utf-8
import pytest

from lupin import Schema, String, Constant, Int, Mapping

from ..fixtures import Thief, Painting, Jewel


@pytest.fixture
def thief_schema():
    return Schema({
        "firstName": String(binding="first_name"),
        "lastName": String(binding="last_name")
    }, "thief")


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
def stolen_items(mona_lisa, diamond):
    return [mona_lisa, diamond]


@pytest.fixture
def stolen_items_data(mona_lisa_data, diamond_data):
    return [mona_lisa_data, diamond_data]
