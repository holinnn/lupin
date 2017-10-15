class Schema(object):
    def __init__(self, fields):
        """
        Args:
            fields (dict): dictionary of fields
        """
        self._fields = fields

    def load(self, cls, data):
        """Loads an instance of cls from JSON data

        Args:
            cls (class): class to instantiate
            data (dict): JSON data

        Returns:
            object
        """
        obj = cls.__new__(cls)
        for key, field in self._fields.items():
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
        return {key: field.get_value(obj, key)
                for key, field
                in self._fields.items()}
