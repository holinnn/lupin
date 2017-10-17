from . import Field
from ..validators import Type


class Float(Field):
    """Field used to handle float values"""

    def __init__(self, **kwargs):
        kwargs.setdefault("validators", []).append(Type(float))
        super(Float, self).__init__(**kwargs)
