# pylint: disable=no-member,import-error
import unittest

from src.option_parser import OptionParser, Option
from src.option_parser.exceptions import InvalidParameterException

from decorators import auto_parse, with_argv


class TestAllowedValues(unittest.TestCase):
    def setUp(self):
        self.parser = OptionParser(throw_on_error=True)

        self.option = Option("option", "o")
        self.option.set_parameter_settings(
            validator=lambda parameter: parameter == "allowed"
        )

        self.parser.add_options(self.option)

    @with_argv([])
    @auto_parse
    def test_not_providing_option_does_not_set_option(self):
        self.assertFalse(self.config.is_set(self.option))

    @with_argv(["-o", "allowed"])
    @auto_parse
    def test_complying_sets_correct_value(self):
        self.assertEqual(self.config.get_option_parameter(self.option), "allowed")

    @with_argv(["-o", "not-allowed"])
    def test_not_complying_throws(self):
        with self.assertRaises(InvalidParameterException):
            self.parser.parse()


class TestMultipleAllowedValues(unittest.TestCase):
    def setUp(self):
        self.parser = OptionParser(throw_on_error=True)

        def validator(parameter):
            return parameter == "allowed1" or parameter == "allowed2"

        self.option = Option("option", "o")
        self.option.set_parameter_settings(
            validator=validator,
            parameter_count=5
        )

        self.parser.add_options(self.option)

    @with_argv(["-o", "allowed1", "allowed2", "allowed1", "allowed2", "allowed1"])
    @auto_parse
    def test_all_complying_sets_correct_value(self):
        self.assertEqual(
            self.config.get_option_parameter(self.option),
            ["allowed1", "allowed2", "allowed1", "allowed2", "allowed1"]
        )

    @with_argv(["-o", "allowed1", "allowed2", "not-allowed", "allowed2", "allowed1"])
    def test_any_not_complying_throws(self):
        with self.assertRaises(InvalidParameterException):
            self.parser.parse()
