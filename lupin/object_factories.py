def constructor(cls, values):
    """Use class constructor to build a new object"""
    return cls(**values)


def bind(cls, values):
    """Create a new instance of class then bind attributes to instance"""
    obj = cls.__new__(cls)
    for attr_name, value in values.items():
        setattr(obj, attr_name, value)
    return obj
