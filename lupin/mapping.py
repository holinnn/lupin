from . import bind


class Mapping(object):
    """Association of a serializable class and a schema"""

    def __init__(self, cls, schema, factory=bind):
        """
        Args:
            cls (class): class to load and dump
            schema (Schema): a schema
            factory (callable): a factory method for instantiating objects
        """
        self.cls = cls
        self._schema = schema
        self._factory = factory

    def load(self, data):
        """Load an instance of self._cls with values contained in data

        Args:
            data (dict): JSON data

        Returns:
            object
        """
        return self._schema.load(self.cls, data, self._factory)

    def dump(self, obj):
        """Dump object into its JSON representation

        Args:
            obj (object)

        Returns:
            dict
        """
        return self._schema.dump(obj)
