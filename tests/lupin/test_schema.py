import pytest
from lupin import Schema, StringField


@pytest.fixture
def schema():
    return Schema({
        "email": StringField()
    })
