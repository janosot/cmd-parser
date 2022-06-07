from .option import Option
from ._parsed_option import _ParsedOption
from typing import Any, List, Iterable

class ProcessedOptions:
    def __init__(self, parsed_options: Iterable[_ParsedOption], plain_arguments: Iterable[str]):
       """ 
       Represents all the parsed options and all plain arguments supplied by the user.
       """
       self._original_to_parsed_option_map = {}
       self._plain_arguments = plain_arguments
       self._count = len(parsed_options)

       for parsed_option in parsed_options:
           self._original_to_parsed_option_map[parsed_option.get_original_option()] = parsed_option

    def count(self) -> int:
        """
        Counts how many options were parsed. Does not count plain arguments.

        ## Returns
        Amount of parsed options.

        """
        return self._count

    def is_set(self, option: Option) -> bool:
        """
        Determines whether the option represented by the given `option_parser.option.Option` object was supplied by the user.

        ## Parameters
        * `option` - `Option` object added to `option_parser.option_parser.OptionParser`

        ## Returns 
        `True` if the given option was supplied, `False` otherwise. 
        """
        return option in self._original_to_parsed_option_map

    def has_parameter(self, option: Option) -> bool:
        """
        Determines whether parameters were supplied to the option represented by the given `option_parser.option.Option` object.

        ## Parameters
        * `option` - `option_parser.option.Option` object added to `option_parser.option_parser.OptionParser`

        ## Returns
        `True` if the given option received parameters, `False` otherwise.

        """
        if(not self.is_set(option)):
            return False

        return bool(self._original_to_parsed_option_map[option].get_parameters())

    def get_option_parameter(self, option: Option) -> Any:
        """
        Retrieves the given option's parameters.

        ## Parameters
        * `option` - `option_parser.option.Option` object added to `option_parser.option_parser.OptionParser`

        ## Returns
        The given option's parameter(s) if they were supplied. Return type is the type specified in `option_parser.option.Option`'s `set_parameter_settings()` if `parameter_count` is 1,
        a list of such types otherwise.
        If no parameters were supplied to the option, or the option itself was not supplied, this method returns `None`.
        """
        if(not self.is_set(option)):
            return None

        return self._original_to_parsed_option_map[option].get_parameters()

    def get_plain_args(self) -> List[str]:
        """
        Retrieves all plain arguments supplied by the user.

        ## Returns
        A list of all plain arguments.

        """
        return self._plain_arguments
