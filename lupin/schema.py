from . import bind
from .errors import ValidationError, InvalidDocument


class Schema(object):
    def __init__(self, fields):
        """
        Args:
            fields (dict): dictionary of fields
        """
        self._fields = fields

    def add_field(self, name, field):
        """Add new field to schema.

        Args:
            name (str): field name
            field (Field): a field
        """
        self._fields[name] = field

    def load(self, cls, data, factory=bind):
        """Loads an instance of cls from JSON data

        Args:
            cls (class): class to instantiate
            data (dict): JSON data

        Returns:
            object
        """
        values = {}
        for key, field in self._fields.items():
            field.inject_attr(data, key, values)

        return factory(cls, values)

    def dump(self, obj):
        """Dumps object into a dictionnary

        Args:
            obj (object): object to dump

        Returns:
            dict
        """
        return {key: field.extract_value(obj, key)
                for key, field
                in self._fields.items()}

    def validate(self, data, path=None):
        """Validate data with all field validators.
        If path is provided it will be used as the base path for errors.

        Args:
            data (dict): data to validate
            path (list): base path for errors
        """
        path = path or []
        errors = []
        for key, field in self._fields.items():
            raw_value = data.get(key)
            field_path = path + [key]
            try:
                field.validate(raw_value, field_path)
            except ValidationError as error:
                errors.append(error)

        if errors:
            raise InvalidDocument(errors)
