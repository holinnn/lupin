from datetime import datetime

from . import Validator
from ..errors import InvalidDateTimeFormat


class DateTimeFormat(Validator):
    """Validates date and datetimes format"""

    def __init__(self, format):
        """
        Args:
            format (str): datetime format
        """
        self._format = format

    def __call__(self, value, path):
        """Validate that value can be parsed as a date

        Args:
            value (str): datetime string to validate
            path (list): error path
        """
        try:
            datetime.strptime(value, self._format)
        except ValueError:
            raise InvalidDateTimeFormat(value, self._format, path)
