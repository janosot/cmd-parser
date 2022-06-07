import pytest

from src.option_parser import Option, OptionParser
from src.option_parser.exceptions import InvalidParameterException


def test_parsing_integer_parameter_value(mocker):
    # Arrange
    option = Option("o")
    option.set_parameter_settings(parameter_type=int, required=True)

    mocker.patch(
        "sys.argv",
        [
            "program",
            "-o",
            "4"
        ]
    )

    # Act
    option_parser = OptionParser(throw_on_error=True)
    option_parser.add_options(option)
    processed_options = option_parser.parse()

    # Assert
    assert processed_options.is_set(option)
    assert processed_options.has_parameter(option)
    assert processed_options.get_option_parameter(option) == 4


def test_parsing_constrained_integer_parameter_value(mocker):
    # Arrange
    option = Option("o")

    def validator(number):
        return number >= 3 and number <= 7

    option.set_parameter_settings(parameter_type=int, required=True, validator=validator)

    mocker.patch(
        "sys.argv",
        [
            "program",
            "-o",
            "4"
        ]
    )

    # Act
    option_parser = OptionParser(throw_on_error=True)
    option_parser.add_options(option)
    processed_options = option_parser.parse()

    # Assert
    assert processed_options.is_set(option)
    assert processed_options.has_parameter(option)
    assert processed_options.get_option_parameter(option) == 4


def test_limited_string_parameter_values(mocker):
    # Arrange
    option = Option("o")

    def validator(parameter):
        return parameter == "a" or parameter == "b" or parameter == "c"

    option.set_parameter_settings(required=True, parameter_count=2, validator=validator)

    mocker.patch(
        "sys.argv",
        [
            "program",
            "-o",
            "a",
            "b",
        ]
    )

    # Act
    option_parser = OptionParser(throw_on_error=True)
    option_parser.add_options(option)
    processed_options = option_parser.parse()

    # Assert
    assert processed_options.is_set(option)
    assert processed_options.has_parameter(option)
    assert processed_options.get_option_parameter(option) == ["a", "b"]


def test_throwing_on_not_allowed_parameter_value(mocker):
    # Arrange
    option = Option("o")

    def validator(parameter):
        return parameter == "a" or parameter == "b" or parameter == "c"

    option.set_parameter_settings(required=True, parameter_count=2, validator=validator)

    mocker.patch(
        "sys.argv",
        [
            "program",
            "-o",
            "a",
            "d",  # Not allowed parameter value
        ]
    )

    # Act
    option_parser = OptionParser(throw_on_error=True)
    option_parser.add_options(option)

    # Assert
    with pytest.raises(InvalidParameterException):
        option_parser.parse()


def test_throwing_on_violated_integer_constraint(mocker):
    # Arrange
    option = Option("o")

    def validator(parameter):
        return parameter >= -5 and parameter <= 5

    option.set_parameter_settings(parameter_type=int, required=True, parameter_count=2, validator=validator)

    mocker.patch(
        "sys.argv",
        [
            "program",
            "-o",
            "5",
            "6",
        ]
    )

    # Act
    option_parser = OptionParser(throw_on_error=True)
    option_parser.add_options(option)

    # Assert
    with pytest.raises(InvalidParameterException):
        option_parser.parse()


def test_required_invalid_parameter_count(mocker):
    # Arrange
    option = Option("o")
    option.set_parameter_settings(required=True, parameter_count=2)

    mocker.patch(
        "sys.argv",
        [
            "program",
            "-o",
        ]
    )

    # Act
    option_parser = OptionParser(throw_on_error=True)
    option_parser.add_options(option)

    # Assert
    with pytest.raises(InvalidParameterException):
        option_parser.parse()


def test_optional_invalid_parameter_count(mocker):
    # Arrange
    option = Option("o")
    option.set_parameter_settings(parameter_count=2)

    mocker.patch(
        "sys.argv",
        [
            "program",
            "-o",
            "a", # As parameter_count is not fulfilled, this is expected to be parsed as a plain argument
        ]
    )

    # Act
    option_parser = OptionParser(throw_on_error=True)
    option_parser.add_options(option)
    processed_options = option_parser.parse()

    # Assert
    assert processed_options.is_set(option)
    assert not processed_options.has_parameter(option)
    assert processed_options.get_plain_args() == ["a"]
