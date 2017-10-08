class Mappings(object):
    """Link a class with its schemas.
    It's used to hold all schema associated with a class.
    """
    def __init__(self, cls, schema):
        """
        Args:
            cls (class): class to intantiate on loading data
            schema (schema): default schema to link with cls
        """
        self._cls = cls
        self._schemas = [schema]

    def load(self, data, schema=None):
        """Loads an instance of self._cls from data.
        If no schema provided it will use the default one.

        Args:
            data (dict): JSON data to transform into an object
            schema (Schema): schema to use for loading object, if None then use default schema

        Returns:
            object
        """
        if not schema:
            schema = self._schemas[0]
        return schema.load(self._cls, data)

    def dump(self, obj, schema=None):
        """Dumps obj into a dictionary.
        If no schema provided it will use the default one.

        Args:
            obj (object): object to dump
            schema (Schema): schema to use for dumping object, if None then use default schema

        Returns:
            dict
        """
        if not schema:
            schema = self._schemas[0]
        return schema.dump(obj)

    def add(self, schema, default=False):
        """Link a new schema with self._cls

        Args:
            schema (Schema): a new schema to link to cls
            default (bool): if True it will be the default schema used to dump and load objects
        """
        if default:
            self._schemas.insert(0, schema)
        else:
            self._schemas.append(schema)
