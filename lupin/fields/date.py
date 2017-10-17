from datetime import datetime

from . import Field
from ..validators import Type


class Date(Field):
    """Field used to handle date values"""

    def __init__(self, format="%Y-%m-%d", **kwargs):
        """
        Args:
            format (str): datetime format to use
        """
        kwargs.setdefault("validators", []).append(Type(str))
        super(Date, self).__init__(**kwargs)
        self._format = format

    def load(self, value):
        """Loads a date python object from a JSON string

        Args:
            value (str): a value

        Returns:
            date
        """
        return datetime.strptime(value, self._format).date()

    def dump(self, value):
        """Dump a date to string representation

        Args:
            value (date): a date

        Returns:
            str
        """
        return value.strftime(self._format)
