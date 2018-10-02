import warnings
from functools import reduce
from lupin import ValidatorsAndCombination, ValidatorsNullCombination
from ..validators import IsNone
from ..processors import null_processor


def _make_processor(processors):
    """Returns a callable for executing the processors

    Args:
        processors (list): a list of processor functions to execute
    """
    if not processors:
        return null_processor

    return lambda value: reduce(lambda new_value, proc: proc(new_value), processors, value)


class Field(object):
    """Generic field that does not convert the values"""

    def __init__(self, binding=None, default=None, validators=None, read_only=False, write_only=False,
                 optional=False, allow_none=False, pre_load=None, post_load=None,
                 pre_dump=None, post_dump=None):
        """
        Args:
            binding (str): attribute name to map on object
            default (object): default value if data is absent
            validators (list|ValidatorsCombination|Validator): list of validators or a combination a validators
            read_only (bool): if True the field will only be used to serialize data
            write_only (bool): if True the field will only be used to load data
            optional (bool): if True it won't raise an error if no value provided for this field
            allow_none (bool): if True None is a accepted has a valid value
            pre_load (list): list of processors to execute before loading the value
            post_load (list): list of processors to execute after loading the value
            pre_dump (list): list of processors to execute before dumping the value
            post_dump (list): list of processors to execute after dumping the value
        """
        if validators is None:
            validators = ValidatorsNullCombination()
        elif isinstance(validators, (list, tuple)):
            warnings.warn("List of validators is deprecated, please use combinations (&|)", DeprecationWarning)
            validators = ValidatorsAndCombination(validators)

        if allow_none:
            validators = IsNone() | validators

        self.binding = binding
        self.default = default
        self._validators = validators or []
        self.is_read_only = read_only
        self.is_write_only = write_only
        self.is_optional = optional
        self._pre_load_processor = _make_processor(pre_load)
        self._post_load_processor = _make_processor(post_load)
        self._pre_dump_processor = _make_processor(pre_dump)
        self._post_dump_processor = _make_processor(post_dump)

    def pre_load(self, value):
        return self._pre_load_processor(value)

    def post_load(self, value):
        return self._post_load_processor(value)

    def _pre_dump(self, value):
        return self._pre_dump_processor(value)

    def _post_dump(self, value):
        return self._post_dump_processor(value)

    def load(self, value, mapper):
        """Loads python object from JSON value

        Args:
            value (object): a value
            mapper (Mapper): mapper used to load data

        Returns:
            object
        """
        return value

    def dump(self, value, mapper):
        """Dump value to its JSON representation

        Args:
            value (object): a value
            mapper (Mapper): mapper used to dump data

        Returns:
            object
        """
        return value

    def extract_attr(self, obj, mapper, key=None):
        """Get value of the `key` attribute of object.
        If field has been provided a `binding` then it will
        override `key`

        Args:
            obj (object): object to get value from
            mapper (Mapper): mapper used to dump data
            key (str): attribute name

        Returns:
            object
        """
        key = self.binding or key
        raw_value = getattr(obj, key)
        value = self._pre_dump(raw_value)
        value = self.dump(value, mapper)
        return self._post_dump(value)

    def validate(self, value, path, mapper):
        """Validate value againt field validators

        Args:
            value (object): value to validate
            path (list): JSON path of value
            mapper (Mapper): mapper used to validate data
        """
        self._validators(value, path)
