from copy import copy
from collections import defaultdict

from . import Mapping, bind
from .errors import MissingMapping, SchemaAlreadyRegistered, InvalidPolymorphicType, SchemaNotRegistered


class Mapper(object):
    """Mapper is used to associate the schemas with their python classes"""

    def __init__(self, default_factory=bind):
        """
        Args:
            default_factory (callable): default factory used to instantiate objects
        """
        self._default_factory = default_factory
        self._schemas_to_mapping = {}
        self._schemas_by_name = {}
        self._classes_to_mappings = defaultdict(list)

    def register(self, cls, schema, factory=None):
        """Associate a class with a schema

        Args:
            cls (class): a python class to register with schema
            schema (Schema): schema that will be used to dump & load objects of cls
            factory (callable): factory method used to instantiate objects when loading from JSON
        """
        if schema.name in self._schemas_by_name:
            raise SchemaAlreadyRegistered(schema.name)

        factory = factory or self._default_factory
        mapping = Mapping(cls, schema, factory)
        self._schemas_by_name[schema.name] = schema
        self._schemas_to_mapping[schema] = mapping
        self._classes_to_mappings[cls].append(mapping)

    def validate(self, data, schema, allow_partial=False):
        """Validate data format

        Args:
            data (dict|list): JSON data
            schema (Schema|str): schema (or name) used to validate data
            allow_partial (bool): allow partial schema, won't raise error if missing keys
        """
        if isinstance(data, (list, set, tuple)):
            for item in data:
                self.validate(item, schema, allow_partial)
        else:
            mapping = self.get_schema_mapping(schema)
            mapping.validate(data, self, allow_partial=allow_partial)

    def load(self, data, schema, allow_partial=False):
        """Loads an instance of klass from JSON data

        Args:
            data (dict|list): JSON data
            schema (Schema|str): schema (or name) used to load data
            allow_partial (bool): allow partial schema, won't raise error if missing keys

        returns:
            object
        """
        if isinstance(data, (list, set, tuple)):
            return [self.load(item, schema, allow_partial) for item in data]

        mapping = self.get_schema_mapping(schema)
        return mapping.load(data, self, allow_partial=allow_partial)

    def load_polymorphic(self, data, on, schemas, allow_partial=False):
        """Loads an object that can be of different type
        based on the `on` field

        Args:
            data (dict|list): JSON data
            on (str): JSON key used to get the object type
            schemas (dict): schemas used for each values used for the `on` key
            allow_partial (bool): allow partial schema, won't raise error if missing keys

        Returns:
            list|object
        """
        if isinstance(data, (list, set, tuple)):
            return [self.load_polymorphic(item, on, schemas, allow_partial) for item in data]

        obj_type = data.get(on)
        if obj_type not in schemas:
            raise InvalidPolymorphicType(invalid_type=obj_type,
                                         supported_types=list(schemas.keys()),
                                         path=[on])

        schema = schemas[obj_type]
        return self.load(data, schema, allow_partial)

    def load_attrs(self, data, schema, allow_partial=False):
        """Loads attributes dictionary from `data`

        Args:
            data (dict): dictionary of data
            schema (Schema|str): schema used to load data (or its name)
            allow_partial (bool): allow partial schema, won't raise error if missing keys

        Returns:
            dict
        """
        if isinstance(data, (list, set, tuple)):
            return [self.load_attrs(item, schema, allow_partial) for item in data]

        mapping = self.get_schema_mapping(schema)
        return mapping.load_attrs(data, self, allow_partial=allow_partial)

    def dump(self, obj, schema=None):
        """Dump object into its JSON representation.
        If no schema provided the one used on register() will be used.

        Args:
            obj (object|list): object to dump
            schema (Schema|str): force a schema to dump object (Schema object or a name)

        Returns:
            dict
        """
        if isinstance(obj, (list, set, tuple)):
            return [self.dump(item, schema) for item in obj]

        schemas = (schema,) if schema else None
        mapping = self.get_object_mapping(obj, schemas)

        return mapping.dump(obj, self)

    def get_object_mapping(self, obj, schemas=None):
        """Get mapping of obj.
        If schemas is provided it will only look for mappings associted
        to those schemas.

        Args:
            obj (object): object to get mapping for
            schemas (list<Schema|str>): list of Schema

        Returns:
            Mapping
        """
        try:
            obj_type = type(obj)
            if schemas is not None:
                mappings = [self.get_schema_mapping(schema)
                            for schema in schemas]
                for mapping in mappings:
                    if mapping.can_handle(obj):
                        return mapping

            return self._classes_to_mappings[obj_type][0]
        except KeyError as error:  # one of the schemas was not registered
            schema = error.args[0]
            raise SchemaNotRegistered(schema.name)
        except IndexError:  # No mapping in self._classes_to_mappings
            # try to find a mapping that can handle the parent class of object
            # and register it for future calls
            mappings = self._classes_to_mappings.values()
            for type_mappings in mappings:
                for mapping in type_mappings:
                    if mapping.can_handle(obj):
                        self.register(obj_type, mapping.schema.copy())
                        return self.get_object_mapping(obj)

        raise MissingMapping(obj_type)

    def get_schema_mapping(self, schema):
        """Returns mapping associated to schema.

        Args:
            schema (Schema|str): a schema or its name

        Returns:
            Mapping
        """
        if isinstance(schema, str):
            schema = self._schemas_by_name[schema]
        return self._schemas_to_mapping[schema]
