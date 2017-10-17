from . import Field
from ..validators import Type


class Int(Field):
    """Field used to handle int values"""

    def __init__(self, **kwargs):
        kwargs.setdefault("validators", []).append(Type(int))
        super(Int, self).__init__(**kwargs)
