from . import Field
from .compatibility import merge_validator
from ..validators import Type


class Float(Field):
    """Field used to handle float values"""

    def __init__(self, **kwargs):
        merge_validator(kwargs, Type(float))
        super(Float, self).__init__(**kwargs)
