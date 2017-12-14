from lupin.errors import MissingMapping


def get_mapping(mappings, obj):
    """Get mapping for object
    If no mappings is found then it falls back to look
    for a mapping of a superclass of obj.

    Args:
        mappings (dict): index between object types and their mapping
        obj (object): object to get mapping for

    Returns:
        Mapping
    """
    mapping = mappings.get(type(obj))
    if mapping:
        return mapping
    else:
        mapping_objects = list(mappings.values())
        for mapping in mapping_objects:
            if isinstance(obj, mapping.cls):
                mappings[type(obj)] = mapping
                return mapping

    raise MissingMapping(type(obj))
