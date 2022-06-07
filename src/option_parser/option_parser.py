import sys

from typing import Optional

from .exceptions import InvalidConfigurationException, InvalidParameterException, InvalidOptionException
from .option import Option
from .processed_options import ProcessedOptions
from ._parser import _Parser

class OptionParser:
    def __init__(self, program_description: Optional[str] = "", throw_on_error: Optional[bool] = False):
        """Create a new `OptionParser` object. Parameters should be passed as keyword arguments. Both parameters are optional.

        ## Parameters
        * `program_description` - short string to be displayed on the first line of the help page
        * `throw_on_error` - if set to False (default), the program will handle user errors automatically by showing error info, help page and then exiting.
            if set to True, the program will handle errors by raising exceptions to be handled manually.
        """
        self._program_description = program_description
        self._throw_on_error = throw_on_error
        self._options = []

    
    def add_options(self, option: Option, *args: Optional[Option]):
        """Adds new options to support during parsing.

        ## Parameters
        * `option` - an `option_parser.option.Option` instance representing a CLI option to support.
        * `*args` - additional `option_parser.option.Option`s
        
        ## Raises
        * `option_parser.exceptions.InvalidConfigurationException` - if a duplicate flag is detected.
        """
        help_option = self.__create_help_option()
        known_flags = []
        for opt in tuple([option]) + args + tuple([help_option]):
            self._options.append(opt)
            for flag in opt._get_option_flags():
                if(flag in known_flags):
                    raise InvalidConfigurationException(f"Duplicate option flag detected : '{flag}'.")
                known_flags.append(flag)
        

    def parse(self) -> ProcessedOptions:
        """Parse the supplied CLI arguments as options.

        If a runtime error occurs during parsing (required option missing, invalid parameter type, etc.), the program
        will handle it according to the `throw_on_error` flag set in constructor.

        ## Raises
        * `option_parser.exceptions.InvalidOptionException` - if `throw_on_error` is `True` and a required option is missing, or an unrecognized option is supplied.
        * `option_parser.exceptions.InvalidParameterException` - if `throw_on_error` is `True` and an option received invalid parameters.

        ## Returns
        a `option_parser.processed_options.ProcessedOptions` instance containing all the parsed options, their parameters and plain arguments.
        """
        args = sys.argv[1:]
        if(self.__help_option_present(args)):
            print(self.get_help())
            sys.exit(0)

        parser = _Parser(self._options)
        try:
            (parsed_options, plain_arguments) = parser.parse(args)
            return ProcessedOptions(parsed_options, plain_arguments)
        except (InvalidOptionException, InvalidParameterException) as error:
            if(self._throw_on_error):
                raise error
            else:
                print(f"Error: {error}\n")
                print(self.get_help())
                sys.exit(1)

    
    def get_help(self) -> str:
        """Returns the program usage help page. The help page contains the program description
        and a list of all supported options (including help option) with their parameters and descriptions.
        
        ## Returns
        Program usage help page in a single string.
        
        """
        if(len(self._program_description) > 0):
            help_text = f"{self._program_description}\n\n"
        else:
            help_text = ""

        if(len(self._options) > 0):
            help_text += "Options:\n"
            for option in self._options:
                help_text += self.__generate_option_help_text(option)
            
        help_text += "--\n\tTerminate option list."

        return help_text

    def __generate_option_help_text(self, option: Option) -> str:
        option_text = ""

        for flag in option._get_option_flags():
            option_text += self.__generate_option_help_flag_text(option, flag) + ", "
        option_text = option_text[:-2] # removes last comma

        option_description = option._get_description()
        if(len(option_description) > 0):
            option_text += f"\n\t{option_description}\n"

        return option_text

    def __generate_option_help_flag_text(self, option: Option, flag: str) -> str:
        is_short = len(flag) == 1
        accepts_parameters = option._accepts_parameter()
        prefix = "-" if is_short else "--"
        parameter_prefix = " " if is_short else "="
        parameter_delimiter = " " if is_short else ","
        original_metavar = option._get_metavar() if accepts_parameters else None
        metavar = ""

        if(accepts_parameters):
            if(type(original_metavar) == list):
                if(len(original_metavar) != option._get_parameter_count()):
                    raise InvalidConfigurationException(f"Invalid metavar length set for option {option._get_option_flags[0]}")
                metavar = parameter_prefix + parameter_delimiter.join(original_metavar)
            else:
                metavar = parameter_prefix + original_metavar

        return f"{prefix}{flag}{metavar}"

    def __help_option_present(self, args) -> bool:
        return "-h" in args or "--help" in args

    def __create_help_option(self) -> Option:
        help_option = Option("h", "help")
        help_option.set_description("Prints this help message and exits.")
        return help_option
