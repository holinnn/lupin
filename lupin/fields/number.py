import numbers

from . import Field
from ..validators import Type


class Number(Field):
    """Field used to handle float values"""

    def __init__(self, **kwargs):
        kwargs.setdefault("validators", []).append(Type(numbers.Number))
        super(Number, self).__init__(**kwargs)
