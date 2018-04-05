import pytest
from lupin.validators import URL
from lupin.errors import InvalidURL


VALID_URLS = [
    "http://www.example.com",
    "http://www.example.com/logo.png",
    "http://www.example.com/logo.png?var1=1",
    "http://1.1.1.1:80/logo.png?var1=1"
]

INVALID_URLS = [
    "www.example.com",
    "http://",
    None
]


@pytest.fixture
def validator():
    return URL(schemes={"http"})


class TestCall(object):
    @pytest.mark.parametrize("url", VALID_URLS)
    def test_does_not_raise_error_if_ok(self, validator, url):
        validator(url, path=[])

    def test_raise_error_if_invalid_scheme(self, validator):
        with pytest.raises(InvalidURL):
            validator("ftp://1.1.1.1/", path=[])

    @pytest.mark.parametrize("url", INVALID_URLS)
    def test_raise_error_if_invalid_url(self, validator, url):
        with pytest.raises(InvalidURL):
            validator(url, path=[])
