from . import Field
from .compatibility import merge_validator
from ..validators import Type


class Dict(Field):
    """Field used to handle dictionnaries"""

    def __init__(self, **kwargs):
        merge_validator(kwargs, Type(dict))
        super(Dict, self).__init__(**kwargs)
