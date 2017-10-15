from . import Field


class Constant(Field):
    """Field used to display a fixed value"""

    def __init__(self, value, **kwargs):
        """
        Args:
            value (object): fixed value
        """
        super(Constant, self).__init__(**kwargs)
        self._value = value

    def load(self, value):
        """Returns fixed value

        Args:
            value (object): ignored

        Returns:
            object
        """
        return self._value

    def dump(self, value):
        """Returns fixed value

        Args:
            value (object): ignored

        Returns:
            object
        """
        return self._value

    def get_value(self, obj, key=None):
        """Returns fixed value

        Args:
            obj (object): object to get value from
            key (str): attribute name

        Returns:
            object
        """
        return self._value
