from . import Field
from ..validators import Type


class Bool(Field):
    """Field used to handle boolean values"""

    def __init__(self, **kwargs):
        kwargs.setdefault("validators", []).append(Type(bool))
        super(Bool, self).__init__(**kwargs)
