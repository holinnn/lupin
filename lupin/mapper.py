from collections import defaultdict

from . import Mapping, bind
from .errors import MissingMapping


class Mapper(object):
    """Mapper is used to associate the schemas with their python classes"""

    def __init__(self, default_factory=bind):
        """
        Args:
            default_factory (callable): default factory used to instantiate objects
        """
        self._default_factory = default_factory
        self._mappings = defaultdict(list)

    def register(self, cls, schema, default=False, factory=None):
        """Associate a class with a schema

        Args:
            cls (class): a python class
            schema (Schema): schema that will be used to dump & load objects of klass
            default (bool): if True, this schema will be the default one for dumping instances of `cls`
            factory (callable): factory method used to instantiate objects when loading from JSON

        Returns:
            Mapping
        """
        factory = factory or self._default_factory
        mapping = Mapping(cls, schema, factory)
        mapping_index = 0 if default else len(self._mappings[cls])
        self._mappings[cls].insert(mapping_index, mapping)
        return mapping

    def load(self, data, mapping, allow_partial=False):
        """Loads an instance of klass from JSON data

        Args:
            data (dict|list): JSON data
            mapping (Mapping): mapping used to load data
            allow_partial (bool): allow partial schema, won't raise error if missing keys

        returns:
            object
        """
        if isinstance(data, (list, set, tuple)):
            return [self.load(item, mapping, allow_partial) for item in data]

        mapping.validate(data, allow_partial=allow_partial)
        return mapping.load(data, allow_partial=allow_partial)

    def load_attrs(self, data, mapping, allow_partial=False):
        """Loads attributes dictionary from `data`

        Args:
            data (dict): dictionary of data
            allow_partial (bool): allow partial schema, won't raise error if missing keys

        Returns:
            dict
        """
        if isinstance(data, (list, set, tuple)):
            return [self.load_attrs(item, mapping, allow_partial) for item in data]

        mapping.validate(data, allow_partial=allow_partial)
        return mapping.load_attrs(data, allow_partial=allow_partial)

    def dump(self, obj, mapping=None):
        """Dump object into its JSON representation.
        If no mapping is provided, the default one will be used.

        Args:
            obj (object|list): object to dump

        Returns:
            dict
        """
        if isinstance(obj, (list, set, tuple)):
            return [self.dump(item, mapping) for item in obj]

        if not mapping:
            object_type = type(obj)
            if object_type not in self._mappings:
                raise MissingMapping(object_type)
            mapping = self._mappings[type(obj)][0]

        return mapping.dump(obj)
