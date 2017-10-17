from ..errors import InvalidLength


class Length(object):
    """Validates the size of value"""

    def __init__(self, min=None, max=None):
        """
        Args:
            min (int): minimum length
            max (int): maximum length
        """
        self._min = min
        self._max = max

    def __call__(self, value, path):
        """Validate that value is contained in the expected ones

        Args:
            value (object): value to validate
            path (list): error path
        """
        length = len(value)
        if self._min is not None and length < self._min or\
                self._max is not None and length > self._max:
            raise InvalidLength(length, self._min, self._max, path)
