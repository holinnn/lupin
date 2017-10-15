from . import Field


class PolymorphicList(Field):
    """Field used to handle a list containing objects
    of different types, that need to be loaded, serialized
    in different ways.

    Example:
        PolymorphicList(on="type",
                        mappings={
                            "diamond": diamond_mapping,
                            "painting": painting_mapping
                        })
    """
    def __init__(self, on, mappings):
        """
        Args:
            on (str): JSON key used to get the object type
            mappings (dict): mapping used for each values used for the `on` key
        """
        self._on = on
        self._mappings_by_json_value = mappings
        self._mappings_by_type = {mapping.cls: mapping for mapping in mappings.values()}

    def load(self, value):
        """Loads list of python objects from JSON list

        Args:
            value (list): JSON list

        Returns:
            list
        """
        return [self._mappings_by_json_value[item[self._on]].load(item)
                for item
                in value]

    def dump(self, value):
        """Dump list of object

        Args:
            value (list): objects to dump

        Returns:
            list
        """
        return [self._mappings_by_type[type(item)].dump(item)
                for item
                in value]
