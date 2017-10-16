from collections import defaultdict

from . import Mapping, bind


class Mapper(object):
    """Mapper is used to associate the schemas with their python classes"""

    def __init__(self):
        self._mappings = defaultdict(list)

    def register(self, cls, schema, default=False, factory=bind):
        """Associate a class with a schema

        Args:
            cls (class): a python class
            schema (Schema): schema that will be used to dump & load objects of klass
            default (bool): if True, this schema will be the default one for dumping instances of `cls`
            factory (callable): factory method used to instantiate objects when loading from JSON

        Returns:
            Mapping
        """
        mapping = Mapping(cls, schema, factory)
        mapping_index = 0 if default else len(self._mappings[cls])
        self._mappings[cls].insert(mapping_index, mapping)
        return mapping

    def load(self, data, mapping):
        """Loads an instance of klass from JSON data

        Args:
            data (dict|list): JSON data
            klass (class): class to instantiate

        returns:
            object
        """
        if isinstance(data, (list, set, tuple)):
            return [self.load(item, mapping) for item in data]

        return mapping.load(data)

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
            mapping = self._mappings[type(obj)][0]

        return mapping.dump(obj)
