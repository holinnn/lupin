from . import bind


class Schema(object):
    def __init__(self, fields):
        """
        Args:
            fields (dict): dictionary of fields
        """
        self._fields = fields

    def add_field(self, name, field):
        """Add new field to schema.

        Args:
            name (str): field name
            field (Field): a field
        """
        self._fields[name] = field

    def load(self, cls, data, factory=bind):
        """Loads an instance of cls from JSON data

        Args:
            cls (class): class to instantiate
            data (dict): JSON data

        Returns:
            object
        """
        values = {}
        for key, field in self._fields.items():
            attr_name = field.binding or key
            raw_value = data.get(key)
            value = field.load(raw_value)
            values[attr_name] = value

        return factory(cls, **values)

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
