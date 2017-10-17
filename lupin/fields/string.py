from . import Field
from ..validators import Type


class String(Field):
    """Field used to handle string values"""

    def __init__(self, **kwargs):
        kwargs.setdefault("validators", []).append(Type(str))
        super(String, self).__init__(**kwargs)
