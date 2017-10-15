from . import Field


class Object(Field):
    """Field used for nested objects.
    It uses a mapping in order to know what class to load and the schema
    used for the JSON representation.
    """

    def __init__(self, mapping, *args, **kwargs):
        """
        Args:
            mapping (Mapping): mapping of nested object
        """
        super().__init__(*args, **kwargs)
        self._mapping = mapping

    def load(self, value):
        """Loads python object from JSON object

        Args:
            value (dict): nested JSON object

        Returns:
            object
        """
        return self._mapping.load(value)

    def dump(self, value):
        """Dump object into its JSON representation

        Args:
            value (object): an object

        Returns:
            dict
        """
        return self._mapping.dump(value)