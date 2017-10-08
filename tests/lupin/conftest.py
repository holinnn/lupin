import pytest

from lupin import Schema, Field, StringField

from tests.fixtures import Thief


@pytest.fixture
def thief_schema():
    return Schema({
        "firstName": StringField(binding="first_name"),
        "lastName": StringField(binding="last_name")
    })


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
