from copy import copy
from . import bind
from .validators_combination import ValidatorsNullCombination
from .errors import ValidationError, InvalidDocument, MissingKey


# compatibility : used to generate schema names if not provided (2018-07-04)
_globals = {
    "schemas_count": 0
}


def _generate_name():
    """Generate schema name if not provided"""
    _globals["schemas_count"] += 1
    return "schema%i" % _globals["schemas_count"]


class Schema(object):
    def __init__(self, fields, name=None, validators=None):
        """
        Args:
            fields (dict): dictionary of fields
            name (str): schema name
            validators (ValidatorsCombination|Validator): list of validators or a combination a validators
        """
        self._fields = fields

        if not name:
            name = _generate_name()
        self.name = name

        if validators is None:
            validators = ValidatorsNullCombination()
        self._validators = validators

    def add_field(self, name, field):
        """Add new field to schema.

        Args:
            name (str): field name
            field (Field): a field
        """
        self._fields[name] = field

    def copy(self, new_name=None):
        """Returns a new schema based on current schema

        Args:
            new_names (str): name of new schema

        Returns:
            Schema
        """
        return type(self)(copy(self._fields), new_name)

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
                raw_value = data[key]
                value = field.pre_load(raw_value)
                value = field.load(value, mapper)
                value = field.post_load(value)
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
                in self._fields.items() if not field.is_write_only}

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

        # Validate the fields
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

        # Validate data with global validators
        try:
            self._validators(data, path)
        except ValidationError as error:
            errors.append(error)

        if errors:
            raise InvalidDocument(errors)
            raise InvalidDocument(errors)
