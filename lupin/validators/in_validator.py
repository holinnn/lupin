from . import Validator
from ..errors import InvalidIn


class In(Validator):
    """Validates that a value is contained in a set of values"""

    def __init__(self, values):
        """
        Args:
            values (set|list|tuple): expected values
        """
        self._values = values

    def __call__(self, value, path):
        """Validate that value is contained in the expected ones

        Args:
            value (object): value to validate
            path (list): error path
        """
        if value not in self._values:
            raise InvalidIn(value, self._values, path)
