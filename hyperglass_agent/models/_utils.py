"""Utility Functions for Pydantic Models."""

# Standard Library Imports
import re

# Third Party Imports
import pydantic


def clean_name(_name):
    """Remove unsupported characters from field names.

    Converts any "desirable" seperators to underscore, then removes all
    characters that are unsupported in Python class variable names.
    Also removes leading numbers underscores.

    Arguments:
        _name {str} -- Initial field name

    Returns:
        {str} -- Cleaned field name
    """
    _replaced = re.sub(r"[\-|\.|\@|\~|\:\/|\s]", "_", _name)
    _scrubbed = "".join(re.findall(r"([a-zA-Z]\w+|\_+)", _replaced))
    return _scrubbed.lower()


class HyperglassModel(pydantic.BaseSettings):
    """Base model for all hyperglass configuration models."""

    pass

    class Config:
        """Default Pydantic configuration.

        See https://pydantic-docs.helpmanual.io/usage/model_config
        """

        validate_all = True
        extra = "forbid"
        validate_assignment = True
