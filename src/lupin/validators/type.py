from . import Validator
from lupin.errors import InvalidType


class Type(Validator):
    """Validates that data is of a certain type"""

    def __init__(self, expected_type):
        """
        Args:
            expected_type (type): an object type
        """
        self._expected_type = expected_type

    def __call__(self, value, path):
        """Validate that value is of expected type

        Args:
            value (object): value to validate
            path (list): error path
        """
        if not isinstance(value, self._expected_type):
            raise InvalidType(type(value),
                              self._expected_type,
                              path)
