from . import Field
from .compatibility import merge_validator
from ..validators import Equal


class Constant(Field):
    """Field used to display a fixed value"""

    def __init__(self, value, **kwargs):
        """
        Args:
            value (object): fixed value
        """
        merge_validator(kwargs, Equal(value))
        super(Constant, self).__init__(**kwargs)
        self._value = value

    def load(self, value, mapper):
        """Returns fixed value

        Args:
            value (object): ignored
            mapper (Mapper): mapper used to load data

        Returns:
            object
        """
        return self._value

    def dump(self, value, mapper):
        """Returns fixed value

        Args:
            value (object): ignored
            mapper (Mapper): mapper used to dump data

        Returns:
            object
        """
        return self._value

    def extract_attr(self, obj, mapper, key=None):
        """Returns fixed value

        Args:
            obj (object): object to get value from
            mapper (Mapper): mapper used to dump data
            key (str): attribute name

        Returns:
            object
        """
        return self._value
