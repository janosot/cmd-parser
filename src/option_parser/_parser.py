import re
from typing import Iterable, Tuple, Union
from .option import Option
from ._parsed_option import _ParsedOption
from .exceptions import InvalidOptionException

class _Parser:
    def __init__(self, options: Iterable[Option]):
        self._flag_to_option_map = {}
        self._required_options = []

        for option in options:
            for flag in option._option_flags:
                self._flag_to_option_map[flag] = option
            if(option._required):
                self._required_options.append(option)
    
    def parse(self, received_args: Iterable[str]) -> Tuple[Iterable[_ParsedOption], Iterable[str]]:
        (detected_options, plain_arguments) = self.__process_received_tokens(received_args)

        parsed_options = []
        if(len(detected_options) > 0):
            (parsed_options, plain_arguments) = self.__parse_detected_options(detected_options, plain_arguments)

        parsed_option_to_original_option_map = [parsed_option.get_original_option() for parsed_option in parsed_options]
        for required_option in self._required_options:
            if(required_option not in parsed_option_to_original_option_map):
                raise InvalidOptionException(f"Mandatory option {required_option._option_flags[0]} not supplied.")

        return(parsed_options, plain_arguments)

    def __process_received_tokens(self, received_args: Iterable[str]) -> Tuple[Tuple[str, Iterable[str]], Iterable[str]]:
        current_option_flag = ""
        current_option_parameters = []
        detected_options = []
        plain_arguments = []
        plain_delimiter_detected = False

        expanded_args = self.__expand_multiflags(received_args)

        for token in expanded_args:
            if(plain_delimiter_detected):
                plain_arguments.append(token)
            else:
                if(self.__is_option_flag(token)):
                    if(current_option_flag):
                        detected_options.append((current_option_flag, current_option_parameters))
                    if(self.__is_long_option_flag(token)):
                        current_option_flag = token.split('=')[0]
                        current_option_parameters = token.split('=')[1].split(',') if len(token.split('=')) >= 2 else []
                        detected_options.append((current_option_flag, current_option_parameters))
                        current_option_flag = ""
                        current_option_parameters = []
                    else:
                        current_option_flag = token
                        current_option_parameters = []
                elif(self.__is_plain_arg_delimiter(token)):
                    plain_delimiter_detected = True
                    if(current_option_flag):
                        detected_options.append((current_option_flag, current_option_parameters))
                        current_option_flag = ""
                        current_option_parameters = []
                elif(current_option_flag):
                    current_option_parameters.append(token)
                else:
                    plain_arguments.append(token)
        
        if(current_option_flag):
            detected_options.append((current_option_flag, current_option_parameters))

        return (detected_options, plain_arguments)

    def __parse_detected_options(self,detected_options: Iterable[Tuple[str, Iterable[str]]], current_plain_arguments: Iterable[str]) -> Tuple[Iterable[_ParsedOption], Iterable[str]]:
        parsed_options = []

        for (flag, parameters) in detected_options[:-1]:
            parsed_options.append(self.__parse_option(flag, parameters))
        
        (flag, parameters) = detected_options[-1]
        (last_parsed_option, new_plain_arguments) = self.__parse_last_option(flag, parameters)
        parsed_options.append(last_parsed_option)
        plain_arguments = current_plain_arguments + new_plain_arguments
        
        return (parsed_options, plain_arguments)

    def __expand_multiflags(self, args: Iterable[str]) -> Iterable[str]:
        result = []
        for arg in args:
            if(self.__is_multiflag(arg)):
                for flag in arg[1:]:
                    result.append(f"-{flag}")
            else:
                result.append(arg)
        return result

    def __is_option_flag(self, token: str) -> bool:
        return bool(re.search("^(-[A-Za-z])|(--[^ ]+)$", token))

    def __is_multiflag(self, token: str) -> bool:
        return bool(re.search("^-[A-Za-z]+$", token))

    def __is_long_option_flag(self, token: str) -> bool:
        return bool(re.search("^--[^ ]+$", token))

    def __is_plain_arg_delimiter(self, token: str) -> bool:
        return token == "--"

    def __get_option_from_flag(self, flag: str) -> Union[Option, None]:
        flag_without_prefix = flag[2:] if flag.startswith("--") else flag[1:]
        if(flag_without_prefix in self._flag_to_option_map):
            return self._flag_to_option_map[flag_without_prefix]
        else:
            return None

    def __parse_option(self, flag: str, parameters: Iterable[str]) -> _ParsedOption:
        option = self.__get_option_from_flag(flag)
        if(option):
            parsed_parameters = option._parse_parameters(parameters)
            return _ParsedOption(option, parsed_parameters)
        else:
            raise InvalidOptionException(f"{flag}: unrecognized")

    def __parse_last_option(self, flag:str, parameters: Iterable[str]) -> _ParsedOption:
        option = self.__get_option_from_flag(flag)
        if(option):
            if(self.__is_long_option_flag(flag)):
                parsed_parameters = option._parse_parameters(parameters)
                parsed_option = _ParsedOption(option, parsed_parameters)
                return (parsed_option, [])
            else:
                expected_parameter_count = option._get_parameter_count()
                if(option._accepts_parameter() and not option._is_parameter_required() and len(parameters) < expected_parameter_count):
                    expected_parameter_count = 0
                option_parameters = parameters[:min(len(parameters), expected_parameter_count)]
                parsed_parameters = option._parse_parameters(option_parameters)
                parsed_option = _ParsedOption(option, parsed_parameters)
                if(len(parameters) >= expected_parameter_count):
                    plain_arguments = parameters[expected_parameter_count:]
                return (parsed_option, plain_arguments)     
        else:
            raise InvalidOptionException(f"{flag}: unrecognized")
