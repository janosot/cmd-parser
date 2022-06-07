from _pytest.compat import is_generator
import pytest
import mock

from src.option_parser import OptionParser, Option
from src.option_parser.processed_options import ProcessedOptions

@mock.patch('sys.argv', ["time.py", "arg1", "arg2", "arg3"])
def test_no_option_multiple_args():
    parser = OptionParser()
    processed_options = parser.parse()
    plain_args = processed_options.get_plain_args()
    assert plain_args == ["arg1", "arg2", "arg3"]

@mock.patch('sys.argv', ["time.py", "-a", "arg1", "arg2"])
def test_single_option_multiple_plain_args():
    parser = OptionParser()
    option = Option("a")
    parser.add_options(option)
    processed_options = parser.parse()
    plain_args = processed_options.get_plain_args()
    assert plain_args == ["arg1", "arg2"]

@mock.patch('sys.argv', ["time.py", "-a", "test", "arg1", "arg2", "arg3"])
def test_single_option_single_parameter_multiple_plain_args():
    parser = OptionParser()
    option = Option("a")
    option.set_parameter_settings(parameter_type = str, required = True)
    parser.add_options(option)
    processed_options = parser.parse()
    plain_args = processed_options.get_plain_args()
    assert plain_args == ["arg1", "arg2", "arg3"]

@mock.patch('sys.argv', ["time.py", "-a", "test1", "test2", "arg1", "arg2"])
def test_single_option_multiple_parameters_multiple_plain_args():
    parser = OptionParser()
    option = Option("a")
    option.set_parameter_settings(parameter_type = str, required = True, parameter_count = 2 )
    parser.add_options(option)
    processed_options = parser.parse()
    plain_args = processed_options.get_plain_args()
    assert plain_args == ["arg1", "arg2"]
