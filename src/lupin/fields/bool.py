from . import Field
from .compatibility import merge_validator
from ..validators import Type


class Bool(Field):
    """Field used to handle boolean values"""

    def __init__(self, **kwargs):
        merge_validator(kwargs, Type(bool))
        super(Bool, self).__init__(**kwargs)
