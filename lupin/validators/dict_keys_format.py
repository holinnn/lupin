from .validator import Validator
from lupin.errors import InvalidMatch


class DictKeysFormat(Validator):
    """Validates that keys of dict matches a pattern"""
    def __init__(self, pattern):
        """
        Args:
            pattern (SRE_Pattern): expected pattern for dict keys
        """
        self._pattern = pattern

    def __call__(self, value, path):
        """Validate dict keys match the pattern

        Args:
            value (dict): a dictionnary
            path (list): error path
        """
        if value is None:
            return

        for key in value.keys():
            if not self._pattern.match(key):
                raise InvalidMatch(
                    invalid=key,
                    regexp=self._pattern,
                    path=path + [key]
                )
