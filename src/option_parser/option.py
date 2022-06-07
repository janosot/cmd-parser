import re

from typing import Callable, Iterable, Any, Union
from ._parameter_settings import _ParameterSettings
from .exceptions import InvalidConfigurationException, InvalidParameterException

class Option:
    def __init__(self, option_key: str, *args: str):
        """Represents a single option supported by the parser. One option may have multiple keys by which it is accessed in the command-line.
        Single-letter (*short*) keys are prefixed with a single dash, longer (*long*) keys are prefixed with a double dash. That means that the keys are supplied
        to this class without any prefix, for example:

        ```python
        format_option = Option("f", "format")
        ```

        This option will then be accessed in command-line with -f and --format respectively.
        Each option must have at least one key.

        ## Parameters
        * `option_key` - an option key in `^[A-Za-z]$` or `^[^ ][^ ]+$` format
        * `*args` - alternative option keys in `^[A-Za-z]$` or `^[^ ][^ ]+$` format

        ## Raises
        * `option_parser.exceptions.InvalidConfigurationException` - if option key is not in the specified format
        """
        self._description = ""
        self._required = False
        self._parameter = None
        self._option_flags = []

        for flag in tuple([option_key]) + args:
            if(re.search("^[A-Za-z]$", flag) == None and re.search("^[^ ][^ ]+$", flag) == None):
                raise InvalidConfigurationException(f"Invalid option key format: {flag}")

            self._option_flags.append(flag)

    def set_description(self, description: str):
        """Sets option description to be displayed in the help page.

        ## Parameters
        * `description` - option description to display
        """
        self._description = description
  
    def set_as_required(self):
        """Makes the option mandatory (is optional by default)."""
        self._required = True

    def set_parameter_settings(self, parameter_type=str, required=False, metavar='', parameter_count=1, validator: Callable[[Any], bool] = None):
        """Changes option's parameter settings. Options do not accept parameters by default, meaning a call to this method will enable parameter support
        for the given option. Parameters are then configured with this method's arguments.
        Multiple calls to this method change the parameter settings, deleting the configuration set by the previous call.
        
        ## Parameters
        * `parameter_type` - expected parameter type. String by default.
        * `required` - whether the parameter is required or not. False by default.
        * `metavar` - parameter placeholder to be displayed in the help page. Empty by default.
        * `parameter_count` - how many parameters are expected to follow the option key. If the option key is a short key, then such parameters are separated by space,
        e.g. `program.py -o 1 2 3`. Long option keys are followed by an equals sign and multiple parameters are separated by commas, e.g. `program.py --option=1,2,3`
        * `validator` - callback function receiving each supplied parameter already parsed as `parameter_type`, and returning a `bool`
        representing whether the parameter has been validated successfully.
        If this callback returns `False`, then parsing stops and error handling is invoked.
        """
        self._parameter = _ParameterSettings(parameter_type, required, metavar, parameter_count, validator)
    
    def _get_option_flags(self) -> Iterable[str]:
        return self._option_flags

    def _get_description(self) -> str:
        return self._description

    def _parse_parameters(self, parameters: Iterable[str]) -> Any:
        result = []

        if(len(parameters) > 0):
            expected_parameter_count = self._get_parameter_count()

            if(expected_parameter_count != len(parameters)):
                raise InvalidParameterException(f"Option {self._option_flags[0]} received {len(parameters)} parameters, expected {expected_parameter_count}.")

            for param in parameters:
                try:
                    typed_parameter = self._parameter.get_type()(param)
                except ValueError:
                    raise InvalidParameterException(f"{self._option_flags[0]}: parameter {param} has invalid type.")

                validator = self._parameter.get_validator()
                if(validator is not None and not validator(typed_parameter)):
                    raise InvalidParameterException(f"{self._option_flags[0]}: parameter {param} is not valid.")

                result.append(typed_parameter)
        else:
            if(self._parameter is not None and self._is_parameter_required()):
                raise InvalidParameterException(f"{self._option_flags[0]} expects {self._get_parameter_count()} parameter(s), none received.")
        
        if(len(result) == 1):
            return result[0]
        else:
            return result

    def _get_metavar(self) -> Union[str, list]:
        return self._parameter.get_metavar()

    def _accepts_parameter(self) -> bool:
        return self._parameter != None

    def _is_parameter_required(self) -> bool:
        return self._parameter.is_required()

    def _get_parameter_count(self) -> int:
        return self._parameter.get_parameter_count() if self._accepts_parameter() else 0
