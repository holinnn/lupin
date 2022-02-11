from .validator import Validator
from ..errors import InvalidType


class TypedDict(Validator):
    """Validates that keys and values are well typed"""
    def __init__(self, key_type, value_type):
        """
        Args:
            key_type (str): expected type for all keys
            value_type (str): expected type for all values
        """
        self._key_type = key_type
        self._value_type = value_type

    def __call__(self, value, path):
        """Validate items of dict are well typed

        Args:
            value (dict): a dictionnary
            path (list): error path
        """
        if value is None:
            return

        for key, val in value.items():
            if not isinstance(key, self._key_type):
                raise InvalidType(invalid=type(key),
                                  expected=self._key_type,
                                  path=path + [key])

            if not isinstance(val, self._value_type):
                raise InvalidType(invalid=type(key),
                                  expected=self._value_type,
                                  path=path + [key])
