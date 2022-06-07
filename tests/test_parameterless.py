# pylint: disable=no-member,import-error

import unittest

from src.option_parser import Option, OptionParser
from src.option_parser.exceptions import InvalidOptionException, InvalidParameterException

from decorators import auto_parse, with_argv


class TestRequiredOption(unittest.TestCase):
    def setUp(self):
        self.parser = OptionParser(throw_on_error=True)

        self.option = Option("required", "r")
        self.option.set_as_required()

        self.parser.add_options(self.option)

    @with_argv([])
    def test_not_providing_throws(self):
        with self.assertRaises(InvalidOptionException):
            self.parser.parse()

    @with_argv(["-r"])
    @auto_parse
    def test_providing_by_short_name_sets(self):
        self.assertTrue(self.config.is_set(self.option))

    @with_argv(["--required"])
    @auto_parse
    def test_providing_by_long_name_sets(self):
        self.assertTrue(self.config.is_set(self.option))

    @with_argv(["--required=unexpected-argument"])
    def test_providing_unexpected_argument_by_long_name_throws(self):
        with self.assertRaises(InvalidParameterException):
            self.parser.parse()


class TestOptionalOption(unittest.TestCase):
    def setUp(self):
        self.parser = OptionParser(throw_on_error=True)

        self.option = Option("optional", "o")

        self.parser.add_options(self.option)

    @with_argv([])
    @auto_parse
    def test_not_providing_does_not_set(self):
        self.assertFalse(self.config.is_set(self.option))

    @with_argv(["-o"])
    @auto_parse
    def test_providing_by_short_name_sets(self):
        self.assertTrue(self.config.is_set(self.option))

    @with_argv(["--optional"])
    @auto_parse
    def test_providing_by_long_name_sets(self):
        self.assertTrue(self.config.is_set(self.option))

    @with_argv(["--optional=unexpected-argument"])
    def test_providing_unexpected_argument_by_long_name_throws(self):
        with self.assertRaises(InvalidParameterException):
            self.parser.parse()


class TestUnknownOption(unittest.TestCase):
    def setUp(self):
        self.parser = OptionParser(throw_on_error=True)

    @with_argv(["-u"])
    def test_providing_by_short_name_throws(self):
        with self.assertRaises(InvalidOptionException):
            self.parser.parse()

    @with_argv(["--unknown"])
    def test_providing_by_long_name_throws(self):
        with self.assertRaises(InvalidOptionException):
            self.parser.parse()
