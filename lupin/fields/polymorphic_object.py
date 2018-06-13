from . import Field
from .compatibility import merge_validator
from ..validators import Type
from ..errors import MissingPolymorphicKey, InvalidPolymorphicType


class PolymorphicObject(Field):
    """Field used to handle a key that can contain multiple object types

    Example:
        PolymorphicObject(on="type",
                          schemas={
                              "diamond": diamond_schema,
                              "painting": painting_schema
                          })
    """
    def __init__(self, on, schemas, **kwargs):
        """
        Args:
            on (str): JSON key used to get the object type
            schemas (dict): schemas used for each values used for the `on` key
        """
        merge_validator(kwargs, Type(dict))
        super(PolymorphicObject, self).__init__(**kwargs)
        self._on = on
        self._schemas_by_json_value = schemas
        self._schemas = list(schemas.values())

    def load(self, value, mapper):
        """Loads python objects from JSON object

        Args:
            value (dict): JSON data
            mapper (Mapper): mapper used to load data

        Returns:
            object
        """
        if value is None:
            return None

        schema = self._schemas_by_json_value[value[self._on]]
        return mapper.load(value, schema)

    def dump(self, value, mapper):
        """Dump object

        Args:
            value (object): objects to dump
            mapper (Mapper): mapper used to dump data

        Returns:
            dict
        """
        if value is None:
            return value

        mapping = mapper.get_object_mapping(value, self._schemas)
        return mapping.dump(value, mapper)

    def validate(self, value, path, mapper):
        """Validate each items of list against nested mapping.

        Args:
            value (list): value to validate
            path (list): JSON path of value
            mapper (Mapper): mapper used to validate data
        """
        super(PolymorphicObject, self).validate(value, path, mapper)
        if value is not None:
            if self._on not in value:
                raise MissingPolymorphicKey(self._on, path)

            obj_type = value[self._on]
            if obj_type not in self._schemas_by_json_value:
                raise InvalidPolymorphicType(invalid_type=obj_type,
                                             supported_types=list(self._schemas_by_json_value.keys()),
                                             path=path+[self._on])

            schema = self._schemas_by_json_value[obj_type]
            mapping = mapper.get_schema_mapping(schema)
            mapping.validate(value, mapper, path=path)
