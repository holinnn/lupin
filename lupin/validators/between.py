from . import Validator
from ..errors import InvalidRange


class Between(Validator):
    """Validates that a value is contained within bounds"""
    def __init__(self, min=None, max=None, include_min=True, include_max=True):
        """
        Args:
            min (int): minimum value
            max (int): maximum value
            include_min (bool): include min value
            include_max (bool): include max value
        """
        self._min = min
        self._max = max
        self._include_min = include_min
        self._include_max = include_max

    def __call__(self, value, path):
        """Validate that value is contained is the range

        Args:
            value (object): value to validate
            path (list): error path
        """
        try:
            if self._min is not None and\
                    (self._include_min and value < self._min or
                     not self._include_min and value <= self._min) or\
                    value is None:
                raise InvalidRange(value, self._min, self._max, path=path)

            if self._max is not None and\
                    (self._include_max and value > self._max or
                     not self._include_max and value >= self._max) or\
                    value is None:
                raise InvalidRange(value, self._min, self._max, path=path)
        except TypeError:
            raise InvalidRange(value, self._min, self._max, path=path)
