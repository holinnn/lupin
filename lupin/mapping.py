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

    def load(self, data, allow_partial=False):
        """Load an instance of self._cls with values contained in data

        Args:
            data (dict): JSON data
            allow_partial (bool): allow partial schema, won't raise error if missing keys

        Returns:
            object
        """
        return self._schema.load(self.cls, data, allow_partial, self._factory)

    def load_attrs(self, data, allow_partial=False):
        """Loads attributes dictionary from `data`

        Args:
            data (dict): dictionary of data
            allow_partial (bool): allow partial schema, won't raise error if missing keys

        Returns:
            dict
        """
        return self._schema.load_attrs(data, allow_partial)

    def dump(self, obj):
        """Dump object into its JSON representation

        Args:
            obj (object)

        Returns:
            dict
        """
        return self._schema.dump(obj)

    def validate(self, data, allow_partial=False, path=None):
        """Validate data with the schema.
        If path is provided it will be used as the base path for errors.

        Args:
            data (dict): data to validate
            allow_partial (bool): allow partial schema, won't raise error if missing keys
            path (list): base path for errors
        """
        self._schema.validate(data, allow_partial, path)
