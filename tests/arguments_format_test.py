import pytest

from src.option_parser import Option, OptionParser
from src.option_parser.exceptions import InvalidOptionException


def test_parsing_long_option_format_single_parameter(mocker):
    # Arrange
    long_option_name = "option"

    option = Option(long_option_name)
    option.set_parameter_settings(required=True)
    option.set_as_required()

    mocker.patch(
        "sys.argv",
        [
            "program",
            f"--{long_option_name}=value",
        ]
    )

    # Act
    option_parser = OptionParser(throw_on_error=True)
    option_parser.add_options(option)
    processed_options = option_parser.parse()

    # Assert
    assert processed_options.count() == 1
    assert processed_options.is_set(option)
    assert processed_options.has_parameter(option)
    assert processed_options.get_option_parameter(option) == "value"


def test_parsing_long_option_format_multiple_parameters(mocker):
    # Arrange
    long_option_name = "option"

    option = Option(long_option_name)
    option.set_parameter_settings(parameter_count=2)
    option.set_as_required()

    mocker.patch(
        "sys.argv",
        [
            "program",
            f"--{long_option_name}=firstvalue,secondvalue",
            "plainArgument"
        ]
    )

    # Act
    option_parser = OptionParser(throw_on_error=True)
    option_parser.add_options(option)
    processed_options = option_parser.parse()

    # Assert
    assert processed_options.count() == 1
    assert processed_options.is_set(option)
    assert processed_options.has_parameter(option)
    assert processed_options.get_option_parameter(option) == ["firstvalue", "secondvalue"]
    assert processed_options.get_plain_args() == ["plainArgument"]


def test_parsing_with_aliases(mocker):
    # Arrange
    short_option_name = "o"
    long_option_name = "option"

    option = Option(short_option_name, long_option_name)
    option.set_as_required()

    mocker.patch(
        "sys.argv",
        [
            "program",
            f"--{long_option_name}",
        ]
    )

    # Act
    option_parser = OptionParser(throw_on_error=True)
    option_parser.add_options(option)
    processed_options = option_parser.parse()

    # Assert
    assert processed_options.count() == 1
    assert processed_options.is_set(option)
    assert not processed_options.has_parameter(option)


def test_unknown_option(mocker):
    # Arrange
    mocker.patch(
        "sys.argv",
        [
            "program",
            "-i"
        ]
    )

    # Act
    option_parser = OptionParser(throw_on_error=True)

    # Assert
    with pytest.raises(InvalidOptionException):
        option_parser.parse()
