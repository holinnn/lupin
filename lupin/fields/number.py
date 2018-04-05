import numbers

from . import Field
from .compatibility import merge_validator
from ..validators import Type


class Number(Field):
    """Field used to handle float values"""

    def __init__(self, **kwargs):
        merge_validator(kwargs, Type(numbers.Number))
        super(Number, self).__init__(**kwargs)
