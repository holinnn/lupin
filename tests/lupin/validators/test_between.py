import pytest
from lupin.validators import Between
from lupin.errors import InvalidRange


class TestCall(object):
    def test_raise_error_if_inferior_to_min(self):
        validator = Between(min=1, include_min=False)
        with pytest.raises(InvalidRange):
            validator(0, path=[])

        with pytest.raises(InvalidRange):
            validator(1, path=[])

    def test_raise_error_if_superior_to_max(self):
        validator = Between(max=1, include_max=False)
        with pytest.raises(InvalidRange):
            validator(1, path=[])

        with pytest.raises(InvalidRange):
            validator(2, path=[])

    def test_does_not_raise_error_if_ok(self):
        validator = Between(min=1, max=2)
        validator(1.5, path=[])
        validator(2, path=[])
        validator(1, path=[])

    def test_raise_error_if_not_a_number(self):
        validator = Between(max=1, include_max=False)
        with pytest.raises(InvalidRange):
            validator("1", path=[])
