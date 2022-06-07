# pylint: disable=no-member,import-error

import unittest

from src.option_parser import Option, OptionParser
from src.option_parser.exceptions import InvalidOptionException, InvalidParameterException

from decorators import auto_parse, with_argv


class TestOptionalOptionWithOptionalParameter(unittest.TestCase):
    def setUp(self):
        self.parser = OptionParser(throw_on_error=True)

        self.option = Option("option", "o")
        self.option.set_parameter_settings()

        self.parser.add_options(self.option)

    @with_argv([])
    @auto_parse
    def test_not_providing_option_does_not_set_option(self):
        self.assertFalse(self.config.is_set(self.option))

    @with_argv(["-o"])
    @auto_parse
    def test_providing_option_sets_option(self):
        self.assertTrue(self.config.is_set(self.option))

    @with_argv(["-o"])
    @auto_parse
    def test_not_providing_parameter_does_not_set_paramater(self):
        self.assertFalse(self.config.has_parameter(self.option))

    @with_argv(["-o", "parameter"])
    @auto_parse
    def test_providing_parameter_sets_option(self):
        self.assertTrue(self.config.is_set(self.option))

    @with_argv(["-o", "parameter"])
    @auto_parse
    def test_providing_parameter_sets_parameter(self):
        self.assertTrue(self.config.has_parameter(self.option))

    @with_argv(["-o", "parameter"])
    @auto_parse
    def test_providing_parameter_sets_correct_value(self):
        self.assertEqual(
            self.config.get_option_parameter(self.option),
            "parameter"
        )


class TestRequiredOptionWithOptionalParameter(unittest.TestCase):
    def setUp(self):
        self.parser = OptionParser(throw_on_error=True)

        self.option = Option("option", "o")
        self.option.set_as_required()
        self.option.set_parameter_settings()

        self.parser.add_options(self.option)

    @with_argv([])
    def test_not_providing_option_throws(self):
        with self.assertRaises(InvalidOptionException):
            self.parser.parse()

    @with_argv(["-o"])
    @auto_parse
    def test_providing_option_sets_option(self):
        self.assertTrue(self.config.is_set(self.option))

    @with_argv(["-o"])
    @auto_parse
    def test_not_providing_parameter_does_not_set_paramater(self):
        self.assertFalse(self.config.has_parameter(self.option))

    @with_argv(["-o", "parameter"])
    @auto_parse
    def test_providing_parameter_sets_option(self):
        self.assertTrue(self.config.is_set(self.option))

    @with_argv(["-o", "parameter"])
    @auto_parse
    def test_providing_parameter_sets_parameter(self):
        self.assertTrue(self.config.has_parameter(self.option))

    @with_argv(["-o", "parameter"])
    @auto_parse
    def test_providing_parameter_sets_correct_value(self):
        self.assertEqual(
            self.config.get_option_parameter(self.option),
            "parameter"
        )


class TestOptionalOptionWithRequiredParameter(unittest.TestCase):
    def setUp(self):
        self.parser = OptionParser(throw_on_error=True)

        self.option = Option("option", "o")
        self.option.set_parameter_settings(required=True)

        self.parser.add_options(self.option)

    @with_argv([])
    @auto_parse
    def test_not_providing_option_does_not_set_option(self):
        self.assertFalse(self.config.is_set(self.option))

    @with_argv(["-o"])
    def test_not_providing_parameter_throws(self):
        with self.assertRaises(InvalidParameterException):
            self.parser.parse()

    @with_argv(["-o", "parameter"])
    @auto_parse
    def test_providing_parameter_sets_option(self):
        self.assertTrue(self.config.is_set(self.option))

    @with_argv(["-o", "parameter"])
    @auto_parse
    def test_providing_parameter_sets_parameter(self):
        self.assertTrue(self.config.has_parameter(self.option))

    @with_argv(["-o", "parameter"])
    @auto_parse
    def test_providing_parameter_sets_correct_value(self):
        self.assertEqual(
            self.config.get_option_parameter(self.option),
            "parameter"
        )


class TestRequiredOptionWithRequiredParameter(unittest.TestCase):
    def setUp(self):
        self.parser = OptionParser(throw_on_error=True)

        self.option = Option("option", "o")
        self.option.set_as_required()
        self.option.set_parameter_settings(required=True)

        self.parser.add_options(self.option)

    @with_argv([])
    def test_not_providing_option_throws(self):
        with self.assertRaises(InvalidOptionException):
            self.parser.parse()

    @with_argv(["-o"])
    def test_not_providing_parameter_throws(self):
        with self.assertRaises(InvalidParameterException):
            self.parser.parse()

    @with_argv(["-o", "parameter"])
    @auto_parse
    def test_providing_parameter_sets_option(self):
        self.assertTrue(self.config.is_set(self.option))

    @with_argv(["-o", "parameter"])
    @auto_parse
    def test_providing_parameter_sets_parameter(self):
        self.assertTrue(self.config.has_parameter(self.option))

    @with_argv(["-o", "parameter"])
    @auto_parse
    def test_providing_parameter_sets_correct_value(self):
        self.assertEqual(
            self.config.get_option_parameter(self.option),
            "parameter"
        )
