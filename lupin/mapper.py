from collections import defaultdict

from . import Mapping, bind
from .errors import MissingMapping, SchemaAlreadyRegistered


class Mapper(object):
    """Mapper is used to associate the schemas with their python classes"""

    def __init__(self, default_factory=bind):
        """
        Args:
            default_factory (callable): default factory used to instantiate objects
        """
        self._default_factory = default_factory
        self._schemas_to_mapping = {}
        self._classes_to_mappings = defaultdict(list)

    def register(self, cls, schema, factory=None):
        """Associate a class with a schema

        Args:
            cls (class): a python class to register with schema
            schema (Schema): schema that will be used to dump & load objects of cls
            factory (callable): factory method used to instantiate objects when loading from JSON
        """
        if schema in self._schemas_to_mapping:
            raise SchemaAlreadyRegistered()

        factory = factory or self._default_factory
        mapping = Mapping(cls, schema, factory)
        self._schemas_to_mapping[schema] = mapping
        self._classes_to_mappings[cls].append(mapping)

    def validate(self, data, schema, allow_partial=False):
        """Validate data format

        Args:
            data (dict|list): JSON data
            schema (Schema): schema used to validate data
            allow_partial (bool): allow partial schema, won't raise error if missing keys
        """
        if isinstance(data, (list, set, tuple)):
            for item in data:
                self.validate(item, schema, allow_partial)
        else:
            mapping = self._schemas_to_mapping[schema]
            mapping.validate(data, self, allow_partial=allow_partial)

    def load(self, data, schema, allow_partial=False):
        """Loads an instance of klass from JSON data

        Args:
            data (dict|list): JSON data
            schema (Schema): schema used to load data
            allow_partial (bool): allow partial schema, won't raise error if missing keys

        returns:
            object
        """
        if isinstance(data, (list, set, tuple)):
            return [self.load(item, schema, allow_partial) for item in data]

        mapping = self._schemas_to_mapping[schema]
        return mapping.load(data, self, allow_partial=allow_partial)

    def load_attrs(self, data, schema, allow_partial=False):
        """Loads attributes dictionary from `data`

        Args:
            data (dict): dictionary of data
            schema (Schema): schema used to load data
            allow_partial (bool): allow partial schema, won't raise error if missing keys

        Returns:
            dict
        """
        if isinstance(data, (list, set, tuple)):
            return [self.load_attrs(item, schema, allow_partial) for item in data]

        mapping = self._schemas_to_mapping[schema]
        return mapping.load_attrs(data, self, allow_partial=allow_partial)

    def dump(self, obj, schema=None):
        """Dump object into its JSON representation.
        If no schema provided the one used on register() will be used.

        Args:
            obj (object|list): object to dump
            schema (Schema): force a schema to dump object

        Returns:
            dict
        """
        if isinstance(obj, (list, set, tuple)):
            return [self.dump(item, schema) for item in obj]

        try:
            if schema:
                mapping = self._schemas_to_mapping[schema]
            else:
                mapping = self._classes_to_mappings[type(obj)][0]
        except (KeyError, IndexError):
            raise MissingMapping(type(obj))

        return mapping.dump(obj, self)

    def get_object_mapping(self, obj, schemas=None):
        """Get mapping of obj.
        If schemas is provided it will only look for mappings associted
        to those schemas.

        Args:
            obj (object): object to get mapping for
            schemas (list<Schema>): list of Schema

        Returns:
            Mapping
        """
        try:
            if schemas is not None:
                mappings = [self._schemas_to_mapping[schema]
                            for schema in schemas]
                for mapping in mappings:
                    if mapping.can_handle(obj):
                        return mapping
            else:
                return self._classes_to_mappings[type(obj)][0]
        except (KeyError, IndexError):
            raise MissingMapping(type(obj))
        else:
            raise MissingMapping(type(obj))

    def get_schema_mapping(self, schema):
        """Returns mapping associated to schema.

        Args:
            schema (Schema): a schema

        Returns:
            Mapping
        """
        return self._schemas_to_mapping[schema]
