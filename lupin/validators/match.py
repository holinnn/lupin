from . import Validator
from ..errors import InvalidMatch


class Match(Validator):
    """Validate that a string matches a pattern"""

    def __init__(self, regex):
        """
        Args:
            regex (regex): a regexp object
        """
        self._regex = regex

    def __call__(self, value, path):
        """Validate that value matches the regex

        Args:
            value (str): string to validate
            path (list): error path
        """
        try:
            if not self._regex.match(value):
                raise InvalidMatch(value, self._regex, path)
        except TypeError:
            raise InvalidMatch(value, self._regex, path)
