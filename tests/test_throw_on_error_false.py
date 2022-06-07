from _pytest.compat import is_generator
import pytest
import mock

from src.option_parser import OptionParser, Option
from src.option_parser.exceptions import InvalidConfigurationException

# parser.add_options(opt1, opt2, ...) throws InvalidConfigurationException when options with the same key were detected
@mock.patch('sys.argv', ["program.py", "-f"])
def test_throw_exception_when_same_key_detected():
    parser = OptionParser(throw_on_error = False)
    option1 = Option('f')
    option2 = Option('f')

    with pytest.raises(InvalidConfigurationException):
        parser.add_options(option1, option2)

# parser.parse() throws SystemExit when an unrecognized option is supplied 
@mock.patch('sys.argv', ["program.py", "-o", "value"])
def test_system_exit_is_raised_on_unrecognized_option():
    parser = OptionParser(throw_on_error = False)

    with pytest.raises(SystemExit):
        parser.parse()

# parser.parse() throws SystemExit when a required option is missing
@mock.patch('sys.argv', ["program.py", "-o", "value"])
def test_system_exit_is_raised_on_missing_required_option():
    parser = OptionParser(throw_on_error = False)
    option = Option('r')
    option.set_as_required()
    parser.add_options(option)

    with pytest.raises(SystemExit):
        parser.parse()

# parser.parse() throws SystemExit when required parameters were not present
@mock.patch('sys.argv', ["program.py", "-o"])
def test_system_exit_is_raised_on_missing_required_parameters():
    parser = OptionParser(throw_on_error=False)
    option = Option('o')
    option.set_parameter_settings(required=True)
    parser.add_options(option)

    with pytest.raises(SystemExit):
        parser.parse()

# parser.parse() throws SystemExit when int parameter receives non-int value
@mock.patch('sys.argv', ["program.py", "-o", "thisisstring"])
def test_system_exit_is_raised_on_retrival_of_nonint_value():
    parser = OptionParser(throw_on_error = False)
    option = Option('o')
    option.set_parameter_settings(parameter_type=int)
    parser.add_options(option)

    with pytest.raises(SystemExit):
        parser.parse()

# parser.parse() throws SystemExit when validator returns False
@mock.patch('sys.argv', ["program.py", "-o", "value"])
def test_system_exit_is_raised_on_validator_returns_false():
    parser = OptionParser(throw_on_error = False)
    option = Option('o')

    def validator(parameter):
        return False

    option.set_parameter_settings(validator = validator)
    parser.add_options(option)

    with pytest.raises(SystemExit):
        parser.parse()
