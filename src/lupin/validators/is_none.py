from . import Validator
from ..errors import NotNone


class IsNone(Validator):
    """Validate that a value is None"""

    def __call__(self, value, path):
        """Validate that value is None

        Args:
            value (object): value to validate
            path (list): error path
        """
        if value is not None:
            raise NotNone(value, path)
