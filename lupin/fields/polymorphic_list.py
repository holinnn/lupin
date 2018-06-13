from . import Field
from .compatibility import merge_validator
from ..validators import Type
from ..errors import MissingPolymorphicKey, InvalidPolymorphicType


class PolymorphicList(Field):
    """Field used to handle a list containing objects
    of different types, that need to be loaded, serialized
    in different ways.

    Example:
        PolymorphicList(on="type",
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
        merge_validator(kwargs, Type(list))
        super(PolymorphicList, self).__init__(**kwargs)
        self._on = on
        self._schemas_by_json_value = schemas
        self._schemas = list(schemas.values())

    def load(self, value, mapper):
        """Loads list of python objects from JSON list

        Args:
            value (list): JSON list
            mapper (Mapper): mapper used to load data

        Returns:
            list
        """
        if value is None:
            return None

        return [mapper.load(item, self._schemas_by_json_value[item[self._on]])
                for item
                in value]

    def dump(self, value, mapper):
        """Dump list of object

        Args:
            value (list): objects to dump
            mapper (Mapper): mapper used to dump data

        Returns:
            list
        """
        if value is None:
            return value

        return [mapper.get_object_mapping(item, self._schemas).dump(item, mapper)
                for item in value]

    def validate(self, value, path, mapper):
        """Validate each items of list against nested mapping.

        Args:
            value (list): value to validate
            path (list): JSON path of value
            mapper (Mapper): mapper used to validate data
        """
        super(PolymorphicList, self).validate(value, path, mapper)
        if value is not None:
            for item_index, item in enumerate(value):
                item_path = path + [str(item_index)]
                if self._on not in item:
                    raise MissingPolymorphicKey(self._on, path)

                obj_type = item[self._on]
                if obj_type not in self._schemas_by_json_value:
                    raise InvalidPolymorphicType(invalid_type=obj_type,
                                                 supported_types=list(self._schemas_by_json_value.keys()),
                                                 path=path+[self._on])

                schema = self._schemas_by_json_value[obj_type]
                mapping = mapper.get_schema_mapping(schema)
                mapping.validate(item, mapper, path=item_path)
