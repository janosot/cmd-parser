import pytest

from src.option_parser import OptionParser, Option

def test_get_help_contains_program_description():
    description = "Test description"
    parser = OptionParser(description)

    help_page = parser.get_help()

    assert description in help_page

def test_get_help_contains_option_short_flag():
    parser = OptionParser()

    short_flag = "t"

    test_option = Option(short_flag)
    parser.add_options(test_option)
    help_page = parser.get_help()

    assert short_flag in help_page

def test_get_help_contains_option_long_flag():
    parser = OptionParser()

    long_flag = "test"

    test_option = Option(long_flag)
    parser.add_options(test_option)
    help_page = parser.get_help()

    assert long_flag in help_page

def test_get_help_contains_option_description():
    parser = OptionParser()
    option_description = "Test option description"
    test_option = Option("t", "test")
    test_option.set_description(option_description)
    parser.add_options(test_option)
    help_page = parser.get_help()

    assert option_description in help_page

def test_get_help_contains_metavar():
    parser = OptionParser()
    metavar = "TEST_METAVAR"
    test_option = Option("t", "test")
    test_option.set_parameter_settings(metavar='TEST_METAVAR')
    parser.add_options(test_option)
    help_page = parser.get_help()

    assert metavar in help_page
