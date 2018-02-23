from . import bind
from .errors import ValidationError, InvalidDocument, MissingKey


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

    def load(self, cls, data, mapper, allow_partial=False, factory=bind):
        """Loads an instance of cls from dictionary

        Args:
            cls (class): class to instantiate
            data (dict): dictionary of data
            mapper (Mapper): mapper used to load data
            allow_partial (bool): allow partial schema, won't raise error if missing keys
            factory (callable): factory method used to instantiate objects

        Returns:
            object
        """
        attrs = self.load_attrs(data, mapper, allow_partial)
        return factory(cls, attrs)

    def load_attrs(self, data, mapper, allow_partial=False):
        """Loads attributes dictionary from `data`

        Args:
            data (dict): dictionary of data
            mapper (Mapper): mapper used to load data
            allow_partial (bool): allow partial schema, won't raise error if missing keys

        Returns:
            dict
        """
        attrs = {}
        for key, field in self._fields.items():
            if field.is_read_only:
                continue
            if key in data:
                value = field.load(data[key], mapper)
            elif allow_partial:
                continue
            else:
                value = field.default

            attr_name = field.binding or key
            attrs[attr_name] = value

        return attrs

    def dump(self, obj, mapper):
        """Dumps object into a dictionnary

        Args:
            obj (object): object to dump
            mapper (Mapper): mapper used to dump data

        Returns:
            dict
        """
        return {key: field.extract_attr(obj, mapper, key)
                for key, field
                in self._fields.items()}

    def validate(self, data, mapper, allow_partial=False, path=None):
        """Validate data with all field validators.
        If path is provided it will be used as the base path for errors.

        Args:
            data (dict): data to validate
            mapper (Mapper): mapper used to validate data
            allow_partial (bool): allow partial schema, won't raise error if missing keys
            path (list): base path for errors
        """
        path = path or []
        errors = []
        for key, field in self._fields.items():
            field_path = path + [key]
            if key in data:
                raw_value = data.get(key)
                try:
                    field.validate(raw_value, field_path, mapper)
                except ValidationError as error:
                    errors.append(error)
            elif not allow_partial and not field.is_optional:
                errors.append(MissingKey(key, field_path))

        if errors:
            raise InvalidDocument(errors)
