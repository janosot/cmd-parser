from typing import overload
import pytest
import mock

from src.option_parser import OptionParser, Option
from src.option_parser.processed_options import ProcessedOptions

@mock.patch('sys.argv', ["program.py", "-o"])
def test_option_has_parameter_without_parameter():
    parser = OptionParser()
    option = Option("o")
    parser.add_options(option)
    processed_options = parser.parse()
    assert not processed_options.has_parameter("o")

@mock.patch('sys.argv', ["program.py", "-o"])
def test_get_option_parameter_without_parameter():
    parser = OptionParser()
    option = Option("o")
    parser.add_options(option)
    processed_options = parser.parse()
    assert processed_options.get_option_parameter("o") == None
