from . import Field
from .compatibility import merge_validator
from ..validators import Type


class String(Field):
    """Field used to handle string values"""

    def __init__(self, **kwargs):
        merge_validator(kwargs, Type(str))
        super(String, self).__init__(**kwargs)
