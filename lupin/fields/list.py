from . import Field


class List(Field):
    """Field handling lists containing same object types.
    It uses an inner field to handle items mapping.
    """

    def __init__(self, field, **kwargs):
        """
        Args:
            field (Field): a field handling list items
        """
        super().__init__(**kwargs)
        self._field = field

    def load(self, value):
        """Loads list of python objects from JSON list

        Args:
            value (list): JSON list

        Returns:
            list
        """
        return [self._field.load(item) for item in value]

    def dump(self, value):
        """Dump list of object

        Args:
            value (list): list of

        Returns:
            list
        """
        return [self._field.dump(item) for item in value]
