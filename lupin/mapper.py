from collections import defaultdict

from . import Mapping


class Mapper(object):
    """Mapper is used to associate the schemas with their python classes"""

    def __init__(self):
        self._mappings = defaultdict(list)

    def register(self, cls, schema, default=False):
        """Associate a class with a schema

        Args:
            cls (class): a python class
            schema (Schema): schema that will be used to dump & load objects of klass
            default (bool): if True, this schema will be the default one for dumping instances of `cls`

        Returns:
            Mapping
        """
        mapping = Mapping(cls, schema)
        mapping_index = 0 if default else len(self._mappings[cls])
        self._mappings[cls].insert(mapping_index, mapping)
        return mapping

    def load(self, data, mapping):
        """Loads an instance of klass from JSON data

        Args:
            data (dict): JSON data
            klass (class): class to instantiate

        returns:
            object
        """
        return mapping.load(data)

    def dump(self, obj, mapping=None):
        """Dump object into its JSON representation.
        If no mapping is provided, the default one will be used.

        Args:
            obj (object): object to dump

        Returns:
            dict
        """
        if not mapping:
            mapping = self._mappings[type(obj)][0]

        return mapping.dump(obj)