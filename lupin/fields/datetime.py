from datetime import datetime
from . import Field


class Datetime(Field):
    """Field used to handle datetime values"""

    def __init__(self, format="%Y-%m-%dT%H:%M:%S", *args, **kwargs):
        """
        Args:
            format (str): datetime format to use
        """
        self._format = format
        super().__init__(*args, **kwargs)

    def load(self, value):
        """Loads a datetime python object from a JSON string

        Args:
            value (str): a value

        Returns:
            datetime
        """
        return datetime.strptime(value, self._format)

    def dump(self, value):
        """Dump a datetime to string representation

        Args:
            value (datetime): a datetime

        Returns:
            str
        """
        return value.strftime(self._format)
