# pylint: disable=no-member,import-error

import unittest

from src.option_parser import Option, OptionParser
from src.option_parser.exceptions import InvalidParameterException

from decorators import with_argv, auto_parse


class TestUpperBound(unittest.TestCase):
    def setUp(self):
        self.parser = OptionParser(throw_on_error=True)

        def validator(number):
            return number <= 100

        self.option = Option("number", "n")
        self.option.set_parameter_settings(parameter_type=int, validator=validator)

        self.parser.add_options(self.option)

    @with_argv(["-n", "50"])
    @auto_parse
    def test_positive_in_bounds_sets_correct_value(self):
        self.assertEqual(self.config.get_option_parameter(self.option), 50)

    @with_argv(["-n", "-50"])
    @auto_parse
    def test_negative_in_bounds_by_short_name_sets(self):
        self.assertTrue(self.config.is_set(self.option))

    @with_argv(["-n", "-50"])
    @auto_parse
    def test_negative_in_bounds_by_short_name_sets_parameter(self):
        self.assertTrue(self.config.has_parameter(self.option))

    @with_argv(["-n", "-50"])
    @auto_parse
    def test_negative_in_bounds_by_short_name_sets_correct_value(self):
        self.assertEqual(self.config.get_option_parameter(self.option), -50)

    @with_argv(["--number=-50"])
    @auto_parse
    def test_negative_in_bounds_by_long_name_sets(self):
        self.assertTrue(self.config.is_set(self.option))

    @with_argv(["--number=-50"])
    @auto_parse
    def test_negative_in_bounds_by_long_name_sets_parameter(self):
        self.assertTrue(self.config.has_parameter(self.option))

    @with_argv(["--number=-50"])
    @auto_parse
    def test_negative_in_bounds_by_long_name_sets_correct_value(self):
        self.assertEqual(self.config.get_option_parameter(self.option), -50)

    @with_argv(["-n", "150"])
    def test_not_in_bounds_throws(self):
        with self.assertRaises(InvalidParameterException):
            self.parser.parse()


class TestLowerBound(unittest.TestCase):
    def setUp(self):
        self.parser = OptionParser(throw_on_error=True)

        def validator(number):
            return number >= -100

        self.option = Option("number", "n")
        self.option.set_parameter_settings(parameter_type=int, validator=validator)

        self.parser.add_options(self.option)

    @with_argv(["-n", "50"])
    @auto_parse
    def test_positive_in_bounds_sets_correct_value(self):
        self.assertEqual(self.config.get_option_parameter(self.option), 50)

    @with_argv(["-n", "-50"])
    @auto_parse
    def test_negative_in_bounds_by_short_name_sets(self):
        self.assertTrue(self.config.is_set(self.option))

    @with_argv(["-n", "-50"])
    @auto_parse
    def test_negative_in_bounds_by_short_name_sets_parameter(self):
        self.assertTrue(self.config.has_parameter(self.option))

    @with_argv(["-n", "-50"])
    @auto_parse
    def test_negative_in_bounds_by_short_name_sets_correct_value(self):
        self.assertEqual(self.config.get_option_parameter(self.option), -50)

    @with_argv(["--number=-50"])
    @auto_parse
    def test_negative_in_bounds_by_long_name_sets(self):
        self.assertTrue(self.config.is_set(self.option))

    @with_argv(["--number=-50"])
    @auto_parse
    def test_negative_in_bounds_by_long_name_sets_parameter(self):
        self.assertTrue(self.config.has_parameter(self.option))

    @with_argv(["--number=-50"])
    @auto_parse
    def test_negative_in_bounds_by_long_name_sets_correct_value(self):
        self.assertEqual(self.config.get_option_parameter(self.option), -50)

    @with_argv(["-n", "-150"])
    def test_not_in_bounds_by_short_name_throws(self):
        with self.assertRaises(InvalidParameterException):
            self.parser.parse()

    @with_argv(["--number=-150"])
    def test_not_in_bounds_by_long_name_throws(self):
        with self.assertRaises(InvalidParameterException):
            self.parser.parse()

class TestMultipleBounded(unittest.TestCase):
    def setUp(self):
        self.parser = OptionParser(throw_on_error=True)

        def validator(number):
            return number >= -100 and number <= 100

        self.option = Option("numbers", "n")
        self.option.set_parameter_settings(
            parameter_type=int,
            validator=validator,
            parameter_count=5
        )

        self.parser.add_options(self.option)

    @with_argv(["-n", "-20", "-10", "0", "10", "20"])
    @auto_parse
    def test_all_in_bounds_sets_correct_value(self):
        self.assertEqual(
            self.config.get_option_parameter(self.option),
            [-20, -10, 0, 10, 20]
        )

    @with_argv(["-n", "-150", "-75", "0", "75", "150"])
    def test_any_not_in_bounds_throws(self):
        with self.assertRaises(InvalidParameterException):
            self.parser.parse()
