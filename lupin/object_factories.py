def constructor(cls, **kwargs):
    """Use class constructor to build a new object"""
    return cls(**kwargs)


def bind(cls, **kwargs):
    """Create a new instance of class then bind attributes to instance"""
    obj = cls.__new__(cls)
    for attr_name, value in kwargs.items():
        setattr(obj, attr_name, value)
    return obj
