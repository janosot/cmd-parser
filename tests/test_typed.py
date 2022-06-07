# pylint: disable=no-member,import-error

import unittest

from src.option_parser import Option, OptionParser
from src.option_parser.exceptions import InvalidParameterException

from decorators import with_argv, auto_parse


class Reject:
    def __init__(self, value):
        raise ValueError


class Accept:
    def __init__(self, value):
        pass


class TestInvalidType(unittest.TestCase):
    def setUp(self):
        self.parser = OptionParser(throw_on_error=True)

        self.option = Option("option", "o")
        self.option.set_parameter_settings(parameter_type=Reject)

        self.parser.add_options(self.option)

    @with_argv([])
    @auto_parse
    def test_not_providing_option_does_not_set_option(self):
        self.assertFalse(self.config.is_set(self.option))

    @with_argv(["-o"])
    @auto_parse
    def test_not_providing_parameter_sets_option(self):
        self.assertTrue(self.config.is_set(self.option))

    @with_argv(["-o"])
    @auto_parse
    def test_not_providing_parameter_does_not_set_parameter(self):
        self.assertFalse(self.config.has_parameter(self.option))

    @with_argv(["-o", "parameter"])
    def test_providing_parameter_throws(self):
        with self.assertRaises(InvalidParameterException):
            self.parser.parse()


class TestValidType(unittest.TestCase):
    def setUp(self):
        self.parser = OptionParser(throw_on_error=True)

        self.option = Option("option", "o")
        self.option.set_parameter_settings(parameter_type=Accept)

        self.parser.add_options(self.option)

    @with_argv([])
    @auto_parse
    def test_not_providing_option_does_not_set_option(self):
        self.assertFalse(self.config.is_set(self.option))

    @with_argv(["-o"])
    @auto_parse
    def test_not_providing_parameter_sets_option(self):
        self.assertTrue(self.config.is_set(self.option))

    @with_argv(["-o"])
    @auto_parse
    def test_not_providing_parameter_does_not_set_parameter(self):
        self.assertFalse(self.config.has_parameter(self.option))

    @with_argv(["-o", "parameter"])
    @auto_parse
    def test_providing_parameter_sets_correct_type(self):
        self.assertIsInstance(
            self.config.get_option_parameter(self.option),
            Accept
        )


class AcceptToken:
    def __init__(self, value):
        if value != "token":
            raise ValueError


class TestMultipleTyped(unittest.TestCase):
    def setUp(self):
        self.parser = OptionParser(throw_on_error=True)

        self.option = Option("option", "o")
        self.option.set_parameter_settings(
            parameter_type=AcceptToken,
            parameter_count=5
        )

        self.parser.add_options(self.option)

    @with_argv(["-o", "token", "token", "token", "token", "token"])
    @auto_parse
    def test_all_complying_sets_correct_type(self):
        for parameter in self.config.get_option_parameter(self.option):
            self.assertIsInstance(
                parameter,
                AcceptToken
            )

    @with_argv(["-o", "token", "token", "not-token", "token", "token"])
    def test_any_not_complying_throws(self):
        with self.assertRaises(InvalidParameterException):
            self.parser.parse()
