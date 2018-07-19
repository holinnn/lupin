def null_processor(value):
    """Processor that does nothing, just returns the value"""
    return value


def strip(value):
    """Removes whitespaces from value on both side"""
    return value.strip() if value else value


def lower(value):
    """Lowercase the string passed as argument"""
    return value.lower() if value else value


def upper(value):
    """Uppercase the string passed as argument"""
    return value.upper() if value else value
