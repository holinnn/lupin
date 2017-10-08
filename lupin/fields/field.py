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
