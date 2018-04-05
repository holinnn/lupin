from datetime import datetime

from . import Field
from .compatibility import merge_validator
from ..validators import Type


class DateTime(Field):
    """Field used to handle datetime values"""

    def __init__(self, format="%Y-%m-%dT%H:%M:%S", *args, **kwargs):
        """
        Args:
            format (str): datetime format to use
        """
        merge_validator(kwargs, Type(str))
        super(DateTime, self).__init__(*args, **kwargs)
        self._format = format

    def load(self, value, mapper):
        """Loads a datetime python object from a JSON string

        Args:
            value (str): a value
            mapper (Mapper): mapper used to load data

        Returns:
            datetime
        """
        return datetime.strptime(value, self._format)

    def dump(self, value, mapper):
        """Dump a datetime to string representation

        Args:
            value (datetime): a datetime
            mapper (Mapper): mapper used to dump data

        Returns:
            str
        """
        return value.strftime(self._format)
