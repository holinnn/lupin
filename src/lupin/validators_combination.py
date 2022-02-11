from .validators import Validator
from .errors import ValidationError


class ValidatorsNullCombination(object):
    """Used as a default validators combination when a field has no
    validators.
    """

    def __call__(self, *args, **kwargs):
        """Null combination does nothing"""

    def __and__(self, other):
        return ValidatorsAndCombination([other])

    def __or__(self, other):
        return ValidatorsOrCombination([other])


class ValidatorsAndCombination(object):
    """Represents an & combination of validators.
    It raise error if at least one validator is invalid.
    """
    def __init__(self, validators):
        """
        Args:
            validators list<Validator>: a list of validator
        """
        self._validators = validators

    def __call__(self, *args, **kwargs):
        for validator in self._validators:
            validator(*args, **kwargs)

    def __and__(self, other):
        if isinstance(other, ValidatorsAndCombination):
            self._validators.extend(other._validators)
            return self
        elif isinstance(other, Validator):
            self._validators.append(other)
            return self

        return ValidatorsAndCombination([self, other])

    def __or__(self, other):
        return ValidatorsOrCombination([self, other])


class ValidatorsOrCombination(object):
    """Represents an | combination of validators.
    It raise error if all validators are invalid.
    """
    def __init__(self, validators):
        """
        Args:
            validators list<Validator>: a list of validator
        """
        self._validators = validators

    def __call__(self, *args, **kwargs):
        error = None
        for validator in self._validators:
            try:
                validator(*args, **kwargs)
                return
            except ValidationError as err:
                error = err

        raise error

    def __and__(self, other):
        return ValidatorsAndCombination([self, other])

    def __or__(self, other):
        if isinstance(other, ValidatorsOrCombination):
            self._validators.extend(other._validators)
            return self
        elif isinstance(other, Validator):
            self._validators.append(other)
            return self

        return ValidatorsOrCombination([self, other])
