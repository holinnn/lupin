class SchemaAlreadyRegistered(Exception):
    """Error raised while trying to register a Schema that has already
    been registered
    """
    def __init__(self, name):
        """
        Args:
            name (str): schema name
        """
        super(SchemaAlreadyRegistered, self).__init__("Schema \"%s\" has already been registered in mapper" % name)


class SchemaNotRegistered(Exception):
    """Error raised while trying to use a Schema that has not
    been registered
    """
    def __init__(self, name):
        """
        Args:
            name (str): schema name
        """
        super(SchemaNotRegistered, self).__init__("Schema \"%s\" has not been registered in mapper" % name)


class MissingMapping(Exception):
    """Error raised when no mapper has been defined for a class
    while dumping an instance of that class.
    """
    def __init__(self, type):
        """
        Args:
            type (type): a type
        """
        message = "Missing mapping for object of type %s" % type
        super(MissingMapping, self).__init__(message)
        self.type = type


class InvalidDocument(Exception):
    """Error raised when validating a document.
    It's composed of all the errors detected.
    """
    def __init__(self, errors):
        super(InvalidDocument, self).__init__()
        self.errors = errors

    def __len__(self):
        """Returns errors count

        Returns:
            int
        """
        return len(self.errors)

    def __getitem__(self, index):
        """Returns error at index

        Args:
            index (int): index

        Returns:
            Exception
        """
        return self.errors[index]


class ValidationError(Exception):
    """Base class for validation errors"""

    def __init__(self, message, path):
        """
        Args:
            message (str): error message
            path (list): path of the invalid data
        """
        super(ValidationError, self).__init__(message)
        self.path = path


class InvalidType(ValidationError):
    """Error raised by `Type` validator"""

    def __init__(self, invalid, expected, path):
        """
        Args:
            invalid (type): invalid type received
            expected (type): type expected
            path (list): path of the invalid data
        """
        message = "Invalid type, got %s instead of %s" % (invalid, expected)
        super(InvalidType, self).__init__(message, path)
        self.invalid = invalid
        self.expected = expected


class NotEqual(ValidationError):
    """Error raised by `Equal` validator"""

    def __init__(self, invalid, expected, path):
        """
        Args:
            invalid (object): invalid value
            expected (object): expected value
            path (list): path of the invalid data
        """
        message = "Invalid value, got %s instead of %s" % (invalid, expected)
        super(NotEqual, self).__init__(message, path)
        self.invalid = invalid
        self.expected = expected


class InvalidMatch(ValidationError):
    """Error raised by `Match` validator"""

    def __init__(self, invalid, regexp, path):
        """
        Args:
            invalid (str): invalid value
            regexp (regexp): a regexp
            path (list): path of the invalid data
        """
        message = "Value \"%s\" does not match pattern \"%s\"" % (invalid, regexp.pattern)
        super(InvalidMatch, self).__init__(message, path)
        self.invalid = invalid
        self.regexp = regexp


class InvalidIn(ValidationError):
    """Error raised by `In` validator"""

    def __init__(self, invalid, expected, path):
        """
        Args:
            invalid (str): invalid value
            expected (list): list of expected values
            path (list): path of the invalid data
        """
        message = "Value \"%s\" is not in %s" % (invalid, expected)
        super(InvalidIn, self).__init__(message, path)
        self.invalid = invalid
        self.expected = expected


class InvalidLength(ValidationError):
    """Error raised by `Length` validator"""

    def __init__(self, length, min, max, path):
        """
        Args:
            length (int): received length
            min (int): minimum length
            max (int): maximum length
            path (list): path of the invalid data
        """
        message = "Got %s items, should have been between %s and %s" % (length, min, max)
        super(InvalidLength, self).__init__(message, path)
        self.max = max
        self.min = min
        self.length = length


class InvalidRange(ValidationError):
    """Error raised by `Between` validator"""

    def __init__(self, value, min, max, path):
        """
        Args:
            value (int): value received
            min (int): minimum value
            max (int): maximum value
            path (list): path of the invalid data
        """
        message = "%s is not between %s and %s" % (value, min, max)
        super(InvalidRange, self).__init__(message, path)
        self.max = max
        self.min = min
        self.value = value


class InvalidURL(ValidationError):
    """Error raised by `URL` validator"""

    def __init__(self, invalid, path):
        """
        Args:
            invalid (str): invalid URL
            path (list): path of the invalid data
        """
        message = "Invalid URL : %s" % (invalid)
        super(InvalidURL, self).__init__(message, path)
        self.invalid = invalid


class InvalidDateTimeFormat(ValidationError):
    """Error raised by `DateTimeFormat` validator"""

    def __init__(self, value, format, path):
        """
        Args:
            value (str): invalid datetime string
            format (str): format used to parse datetime
            path (list): path of the invalid data
        """
        message = "Date value \"%s\" can't be parsed with format \"%s\"" % (value, format)
        super(InvalidDateTimeFormat, self).__init__(message, path)
        self.value = value
        self.format = format


class NotNone(ValidationError):
    """Error raised by `IsNone` validator"""

    def __init__(self, invalid, path):
        """
        Args:
            invalid (str): invalid value
            path (list): path of the invalid data
        """
        message = "Value is not None : %s" % (invalid)
        super(NotNone, self).__init__(message, path)
        self.invalid = invalid


class MissingPolymorphicKey(ValidationError):
    """Error raised if Polymorphic object do not contain a type key"""

    def __init__(self, key, path):
        """
        Args:
            key (str): polymorphic key
            path (list): path of the invalid data
        """
        message = "Polymorphic document does not contain the \"%s\" key " % key
        super(MissingPolymorphicKey, self).__init__(message, path)
        self.key = key


class InvalidPolymorphicType(ValidationError):
    """Error raised by a polymorphic field when it does not have a
    mapping for the data it tries to validate
    """
    def __init__(self, invalid_type, supported_types, path):
        """
        Args:
            invalid_type (str): invalid type received
            supported_types (list): valid types supported
            path (list): path of the invalid data
        """
        message = "Invalid polymorphic document  \"%s\" is not supported only \"%s\" " % (invalid_type, supported_types)
        super(InvalidPolymorphicType, self).__init__(message, path)
        self.invalid_type = invalid_type
        self.supported_types = supported_types


class MissingKey(ValidationError):
    """Error raised when a key is missing from data"""

    def __init__(self, key, path):
        """
        Args:
            key (str): missing key
            path (list): path of the missing data
        """
        message = "Document does not contain the \"%s\" key" % key
        super(MissingKey, self).__init__(message, path)
        self.key = key
