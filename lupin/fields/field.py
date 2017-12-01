class Field(object):
    """Generic field that does not convert the values"""

    def __init__(self, binding=None, default=None, validators=None, read_only=False,
                 optional=False):
        """
        Args:
            binding (str): attribute name to map on object
            default (object): default value if data is absent
            validators (list): list of validators
            read_only (bool): if True the field will only be used to serialize data
            optional (bool): if True it won't raise an error if no value provided for this field
        """
        self.binding = binding
        self.default = default
        self._validators = validators or []
        self.is_read_only = read_only
        self.is_optional = optional

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

    def extract_attr(self, obj, key=None):
        """Get value of the `key` attribute of object.
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

    def validate(self, value, path):
        """Validate value againt field validators

        Args:
            value (object): value to validate
            path (list): JSON path of value
        """
        for validator in self._validators:
            validator(value, path)
