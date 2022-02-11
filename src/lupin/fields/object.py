from . import Field
from .compatibility import merge_validator
from ..validators import Type


class Object(Field):
    """Field used for nested objects.
    It uses a mapping in order to know what class to load and the schema
    used for the JSON representation.
    """

    def __init__(self, schema, *args, **kwargs):
        """
        Args:
            schema (Schema): schema of nested object
        """
        merge_validator(kwargs, Type(dict))
        super(Object, self).__init__(*args, **kwargs)
        self._schema = schema

    def load(self, value, mapper):
        """Loads python object from JSON object

        Args:
            value (dict): nested JSON object
            mapper (Mapper): mapper used to load data

        Returns:
            object
        """
        if value is None:
            return None

        return mapper.load(value, self._schema)

    def dump(self, value, mapper):
        """Dump object into its JSON representation

        Args:
            value (object): an object
            mapper (Mapper): mapper used to dump data

        Returns:
            dict
        """
        if value is None:
            return value

        return self._schema.dump(value, mapper)

    def validate(self, value, path, mapper):
        """Validate value against mapping validators.

        Args:
            value (list): value to validate
            path (list): JSON path of value
            mapper (Mapper): mapper used to dump data
        """
        super(Object, self).validate(value, path, mapper)
        if value is not None:
            self._schema.validate(value, mapper, path=path)
