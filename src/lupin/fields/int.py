from . import Field
from .compatibility import merge_validator
from ..validators import Type


class Int(Field):
    """Field used to handle int values"""

    def __init__(self, **kwargs):
        merge_validator(kwargs, Type(int))
        super(Int, self).__init__(**kwargs)
