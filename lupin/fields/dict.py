from . import Field
from ..validators import Type


class Dict(Field):
    """Field used to handle dictionnaries"""

    def __init__(self, **kwargs):
        kwargs.setdefault("validators", []).append(Type(dict))
        super(Dict, self).__init__(**kwargs)
