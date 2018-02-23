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
        self.schema = schema
        self._factory = factory

    def load(self, data, mapper, allow_partial=False):
        """Load an instance of self._cls with values contained in data

        Args:
            data (dict): JSON data
            allow_partial (bool): allow partial schema, won't raise error if missing keys
            mapper (Mapper): mapper used to load data

        Returns:
            object
        """
        return self.schema.load(self.cls, data, mapper, allow_partial, self._factory)

    def load_attrs(self, data, mapper, allow_partial=False):
        """Loads attributes dictionary from `data`

        Args:
            data (dict): dictionary of data
            mapper (Mapper): mapper used to load data
            allow_partial (bool): allow partial schema, won't raise error if missing keys

        Returns:
            dict
        """
        return self.schema.load_attrs(data, mapper, allow_partial)

    def dump(self, obj, mapper):
        """Dump object into its JSON representation

        Args:
            obj (object)
            mapper (Mapper): mapper dump to load data

        Returns:
            dict
        """
        return self.schema.dump(obj, mapper)

    def validate(self, data, mapper, allow_partial=False, path=None):
        """Validate data with the schema.
        If path is provided it will be used as the base path for errors.

        Args:
            data (dict): data to validate
            mapper (Mapper): mapper used to validate data
            allow_partial (bool): allow partial schema, won't raise error if missing keys
            path (list): base path for errors
        """
        self.schema.validate(data, mapper, allow_partial, path)

    def can_handle(self, obj):
        """Does this mapping can be used to load/dump obj ?

        Args:
            obj (object): an object

        Returns:
            bool
        """
        return isinstance(obj, self.cls)
