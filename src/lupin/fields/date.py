from datetime import datetime

from . import Field
from .compatibility import merge_validator
from ..validators import Type


class Date(Field):
    """Field used to handle date values"""

    def __init__(self, format="%Y-%m-%d", **kwargs):
        """
        Args:
            format (str): datetime format to use
        """
        merge_validator(kwargs, Type(str))
        super(Date, self).__init__(**kwargs)
        self._format = format

    def load(self, value, mapper):
        """Loads a date python object from a JSON string

        Args:
            value (str): a value
            mapper (Mapper): mapper used to load data

        Returns:
            date
        """
        if value is None:
            return None

        return datetime.strptime(value, self._format).date()

    def dump(self, value, mapper):
        """Dump a date to string representation

        Args:
            value (date): a date
            mapper (Mapper): mapper used to dump data

        Returns:
            str
        """
        if value is None:
            return None

        return value.strftime(self._format)
