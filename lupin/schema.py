class Schema(object):
    def __init__(self, schema):
        """
        Args:
            schema (dict): dictionary representing the schema
        """
        self._schema = schema

    def load(self, cls, data):
        """Loads an instance of cls from JSON data

        Args:
            cls (class): class to instantiate
            data (dict): JSON data

        returns:
            object
        """
        obj = cls.__new__(cls)
        for key, field in self._schema.items():
            attr_name = field.binding or key
            raw_value = data.get(key)
            value = field.load(raw_value)
            setattr(obj, attr_name, value)
        return obj

    def dump(self, obj):
        """Dumps object into a dictionnary

        Args:
            obj (object): object to dump
        Returns:
            dict
        """
        data = {}
        for key, field in self._schema.items():
            attr_name = field.binding or key
            raw_value = getattr(obj, attr_name)
            value = field.dump(raw_value)
            data[key] = value
        return data
