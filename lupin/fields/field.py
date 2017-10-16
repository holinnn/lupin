class Field(object):
    """Generic field that does not convert the values"""

    def __init__(self, binding=None):
        """
        Args:
            binding (str): attribute name to map on object
        """
        self.binding = binding

    def load(self, value):
        """Loads python object from JSON value

        Args:
            value (object): a value

        Returns:
            object
        """
        return value

    def dump(self, value):
        """Dump value to its JSON representation

        Args:
            value (object): a value

        Returns:
            object
        """
        return value

    def extract_value(self, obj, key=None):
        """Get JSON value of `key` attribute of object.
        If field has been provided a `binding` then it will
        override `key`

        Args:
            obj (object): object to get value from
            key (str): attribute name

        Returns:
            object
        """
        key = self.binding or key
        raw_value = getattr(obj, key)
        return self.dump(raw_value)

    def inject_value(self, value, destination, key=None):
        """Load and add value to `destination` dict.
        If field has been provided a `binding` then it will
        override `key`.

        Args:
            value (object): a value to load
            destination (dict): dictionary to fill with key, value
            key (str): an attribute name
        """
        key = self.binding or key
        destination[key] = self.load(value)
