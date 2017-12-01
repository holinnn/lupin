from . import Field
from ..validators import Type


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
        kwargs.setdefault("validators", []).append(Type(dict))
        super(Object, self).__init__(*args, **kwargs)
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

    def validate(self, value, path):
        """Validate value against mapping validators.

        Args:
            value (list): value to validate
            path (list): JSON path of value
        """
        super(Object, self).validate(value, path)
        self._mapping.validate(value, path)
