class OptionParserException(Exception):
    """Base class for option parser exceptions."""

class InvalidConfigurationException(OptionParserException):
    """Raised when an error occurs during configuration, e.g. two options share the same flag."""

class InvalidParameterException(OptionParserException):
    """Raised when a required parameter is missing, supplied parameter type is wrong, or supplied parameter value was not validated successfully."""

class InvalidOptionException(OptionParserException):
    """Raised when a mandatory option is missing or an unknown option is encountered."""
