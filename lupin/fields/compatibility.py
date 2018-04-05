import warnings
from lupin import ValidatorsAndCombination


def merge_validator(kwargs, validator):
    """Add validator to field constructor parameters
    This method will be removed from next release.

    Args:
        kwargs (dict): constructor parameters
        validator (ValidatorsCombination): a validator or a combination
    """
    validators = kwargs.get("validators")
    if not validators:
        validators = validator
    elif isinstance(validators, list):
        warnings.warn("List of validators is deprecated, please use combinations (&|)", DeprecationWarning)
        validators.append(validator)
        validators = ValidatorsAndCombination(validators)
    else:
        validators = validators & validator

    kwargs["validators"] = validators
