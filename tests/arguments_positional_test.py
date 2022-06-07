import pytest

from src.option_parser import Option, OptionParser
from src.option_parser.exceptions import InvalidOptionException


def test_parsing_random_arguments_combination(mocker):
    # Arrange
    first_required_option_name = "first_option"
    first_required_option_parameters = ["first_option_param1", "first_option_param2"]
    first_required_option = Option(first_required_option_name)
    first_required_option.set_as_required()
    first_required_option.set_parameter_settings(required=True, parameter_count=2)

    second_flag_option_name = "second_option"
    second_flag_option = Option(second_flag_option_name)

    plain_arguments_list = ["a", "b", "c"]

    mocker.patch(
        "sys.argv",
        [
            "program",
            f"--{first_required_option_name}={first_required_option_parameters[0]},{first_required_option_parameters[1]}",
            f"--{second_flag_option_name}",
            plain_arguments_list[0],
            plain_arguments_list[1],
            plain_arguments_list[2],
        ]
    )

    # Act
    option_parser = OptionParser(throw_on_error=True)
    option_parser.add_options(first_required_option, second_flag_option)
    processed_options = option_parser.parse()

    # Assert
    assert processed_options.count() == 2
    assert processed_options.has_parameter(first_required_option)
    assert processed_options.get_option_parameter(first_required_option) == first_required_option_parameters
    assert not processed_options.has_parameter(second_flag_option)
    assert processed_options.get_plain_args() == plain_arguments_list


def test_parsing_optional_arguments(mocker):
    # Arrange
    first_flag_option_name = "first_option"
    second_flag_option_name = "second_option"

    first_flag_option = Option(first_flag_option_name)
    second_flag_option = Option(second_flag_option_name)
    plain_arguments_list = ["first_option", "second_option", "third_option"]

    mocker.patch(
        "sys.argv",
        [
            "program",
            f"--{second_flag_option_name}",
            plain_arguments_list[0],
            plain_arguments_list[1],
            plain_arguments_list[2],
        ]
    )

    # Act
    option_parser = OptionParser(throw_on_error=True)
    option_parser.add_options(first_flag_option, second_flag_option)
    processed_options = option_parser.parse()

    # Assert
    assert processed_options.count() == 1
    assert not processed_options.is_set(first_flag_option)
    assert not processed_options.has_parameter(first_flag_option)
    assert processed_options.is_set(second_flag_option)
    assert not processed_options.has_parameter(second_flag_option)
    assert processed_options.get_plain_args() == plain_arguments_list


def test_parser_throwing_on_missing_flag(mocker):
    # Arrange
    required_flag_option_name = "required_flag"
    required_flag_option = Option(required_flag_option_name)
    required_flag_option.set_as_required()

    mocker.patch(
        "sys.argv",
        [
            "program"
        ]
    )

    # Act
    option_parser = OptionParser(throw_on_error=True)
    option_parser.add_options(required_flag_option)

    # Assert
    with pytest.raises(InvalidOptionException):
        option_parser.parse()


def test_throwing_on_missing_required_delimeter(mocker):
    # Arrange
    option = Option("o")

    mocker.patch(
        "sys.argv",
        [
            "program",
            "-o",
            "-p" # as plain argument (not delimited)
        ]
    )

    # Act
    option_parser = OptionParser(throw_on_error=True)
    option_parser.add_options(option)

    # Assert
    with pytest.raises(InvalidOptionException):
        option_parser.parse()


def test_parsing_flag_formatted_plain_argument(mocker):
    # Arrange
    option = Option("o")
    option.set_parameter_settings(required=False, parameter_count=1)

    mocker.patch(
        "sys.argv",
        [
            "program",
            "-o",
            "--", # Should not be parsed as optional parameter of -o
            "-p"  # As plain argument (delimited)
        ]
    )

    # Act
    option_parser = OptionParser(throw_on_error=True)
    option_parser.add_options(option)
    processed_options = option_parser.parse()

    # Assert
    assert processed_options.is_set(option)
    assert not processed_options.has_parameter(option)
    assert processed_options.get_plain_args() == ["-p"]

