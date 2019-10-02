from . import Field
from .compatibility import merge_validator
from ..validators import Type


class List(Field):
    """Field handling lists containing same object types.
    It uses an inner field to handle items mapping.
    """

    def __init__(self, field, **kwargs):
        """
        Args:
            field (Field): a field handling list items
        """
        merge_validator(kwargs, Type(list))
        super(List, self).__init__(**kwargs)
        self._field = field

    def pre_load(self, value):
        value = self._pre_load_processor(value)
        if value is not None:
            value = [self._field.pre_load(item)
                     for item in value]
        return value

    def post_load(self, value):
        if value is not None:
            value = [self._field.post_load(item)
                     for item in value]
        return self._post_load_processor(value)

    def _pre_dump(self, value):
        value = self._pre_dump_processor(value)
        if value is not None:
            value = [self._field._pre_dump(item)
                     for item in value]
        return value

    def _post_dump(self, value):
        if value is not None:
            value = [self._field._post_dump(item)
                     for item in value]
        return self._post_dump_processor(value)

    def load(self, value, mapper):
        """Loads list of python objects from JSON list

        Args:
            value (list): JSON list
            mapper (Mapper): mapper used to load data

        Returns:
            list
        """
        if value is None:
            return None

        return [self._field.load(item, mapper)
                for item in value]

    def dump(self, value, mapper):
        """Dump list of object

        Args:
            value (list): list of
            mapper (Mapper): mapper used to dump data

        Returns:
            list
        """
        if value is None:
            return None

        return [self._field.dump(item, mapper)
                for item in value]

    def validate(self, value, path, mapper):
        """Validate each items of list against nested field validators.

        Args:
            value (list): value to validate
            path (list): JSON path of value
            mapper (Mapper): mapper used to validate data
        """
        super(List, self).validate(value, path, mapper)
        if value is not None:
            for item_index, item in enumerate(value):
                item_path = path + [str(item_index)]
                self._field.validate(item, item_path, mapper)
