class Mapper(object):
    """Mapper is used to associate the schemas with their python classes"""

    def __init__(self):
        self._schemas = {}

    def register(self, klass, schema):
        """Associate a class with a schema

        Args:
            klass (class): a python class
            schema (Schema): schema that will be used to dump & load objects of klass
        """
        self._schemas[klass] = schema

    def load(self, data, klass):
        """Loads an instance of klass from JSON data

        Args:
            data (dict): JSON data
            klass (class): class to instantiate

        returns:
            object
        """
        schema = self._schemas[klass]
        schema.load(data, klass)
