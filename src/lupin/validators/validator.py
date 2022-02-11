import lupin


class Validator(object):
    """Validators base class"""

    def __and__(self, other):
        """Combine current validator with another one using the & operator

        Returns:
            ValidatorsAndCombination
        """
        return lupin.ValidatorsAndCombination([self, other])

    def __or__(self, other):
        """Combine current validator with another one using the | operator

        Returns:
            ValidatorsOrCombination
        """
        return lupin.ValidatorsOrCombination([self, other])
