class Field(object):
    """Generic field that does not convert the values"""

    def __init__(self, binding=None, default=None, validators=None):
        """
        Args:
            binding (str): attribute name to map on object
            default (object): default value if data is absent
            validators (list): list of validators
        """
        self.binding = binding
        self._validators = validators or []
        self._default = default

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

    def inject_attr(self, data, key, attributes):
        """Load value from `data` at `key` and inject it in the attributes dictionary.
        If field has been provided a `binding` then it will override `key`.

        Args:
            data (dict): JSON data
            key (str): an attribute name
            destination (dict): dictionary to fill with key, value
        """
        if key in data:
            value = self.load(data[key])
        else:
            value = self._default

        attr_name = self.binding or key
        attributes[attr_name] = value

    def validate(self, value, path):
        """Validate value againt field validators

        Args:
            value (object): value to validate
            path (list): JSON path of value
        """
        for validator in self._validators:
            validator(value, path)
