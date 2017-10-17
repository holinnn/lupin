from ..errors import NotEqual


class Equal(object):
    """Validate that a value equals an expected one"""

    def __init__(self, expected):
        """
        Args:
            expected (object): expected value
        """
        self._expected = expected

    def __call__(self, value, path):
        """Validate that value equals expected one

        Args:
            value (object): value to validate
            path (list): error path
        """
        if value != self._expected:
            raise NotEqual(value, self._expected, path)
