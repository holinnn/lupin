from . import bind


class Mapping(object):
    """Association of a serializable class and a schema"""

    def __init__(self, cls, schema, factory=bind):
        """
        If cls is a tuple then it registers all classes for the same schema.
        But the resulting mapping will instantiate the first class from the tuple on .load()

        Args:
            cls (class): class to load and dump
            schema (Schema): a schema
            factory (callable): a factory method for instantiating objects
        """
        if not isinstance(cls, tuple):
            cls = (cls,)
        self.classes = cls
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
        return self._schema.load(self.classes[0], data, allow_partial, self._factory)

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

    def can_handle(self, obj):
        """Does this mapping can be used to load/dump obj ?

        Args:
            obj (object): an object

        Returns:
            bool
        """
        for cls in self.classes:
            if isinstance(obj, cls):
                return True

        return False
